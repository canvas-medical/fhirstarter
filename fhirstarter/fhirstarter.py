"""FHIRStarter class, exception handlers, and middleware."""

import asyncio
import itertools
import re
from collections import defaultdict
from collections.abc import Callable, Coroutine, MutableMapping
from datetime import datetime
from functools import cache
from os import PathLike
from typing import Any, cast
from urllib.parse import parse_qs, urlencode

import tomli
import uvloop
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fhir.resources.capabilitystatement import CapabilityStatement
from fhir.resources.operationoutcome import OperationOutcome
from pydantic.error_wrappers import display_errors

from .exceptions import FHIRException
from .fhir_specification.utils import load_example
from .functions import (
    FORMAT_QP,
    PRETTY_QP,
    make_create_function,
    make_read_function,
    make_search_type_function,
    make_update_function,
)
from .interactions import ResourceType, TypeInteraction
from .providers import FHIRProvider
from .search_parameters import (
    SearchParameters,
    search_parameter_sort_key,
    supported_search_parameters,
    var_name_to_qp_name,
)
from .utils import (
    FormatParameters,
    create_route_args,
    format_response,
    make_operation_outcome,
    read_route_args,
    search_type_route_args,
    update_route_args,
)

# TODO: Review documentation for create, read, search, and update interactions
# TODO: Find out if user-provided type annotations need to be validated
# TODO: Research auto-filling path and query parameter options from the FHIR specification
# TODO: Research auto-filling path definition parameters with data from the FHIR specification
# TODO: Review all of the path definition parameters and path/query/body parameters
# TODO: Expose responses FastAPI argument so that developer can specify additional responses

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class FHIRStarter(FastAPI):
    """
    FHIRStarter class.

    Handles collection of FHIR providers, creation of API routes, middleware, exception handling,
    and capability statement requests.
    """

    def __init__(
        self, config_file_name: str | PathLike[str] | None = None, **kwargs: Any
    ) -> None:
        """
        On app creation, the following occurs:
        * Custom search parameters are loaded
        * Static routes are created (e.g. the capability statement route)
        * Middleware is added (e.g. content-type header handling)
        * Exception handling is added
        """
        super().__init__(**kwargs)

        if config_file_name:
            with open(config_file_name, "rb") as file_:
                config = tomli.load(file_)
                self._search_parameters = SearchParameters(
                    config.get("search-parameters")
                )
        else:
            self._search_parameters = SearchParameters()

        self._capabilities: dict[str, dict[str, TypeInteraction]] = defaultdict(dict)
        self._created = datetime.utcnow()

        self._capability_statement_modifier: Callable[
            [MutableMapping[str, Any]], MutableMapping[str, Any]
        ] | None = None

        self._exception_handler_callback: Callable[
            [Request, Exception], None
        ] | None = None

        self._add_capabilities_route()

        self.middleware("http")(_transform_search_type_post_request)
        self.middleware("http")(_set_content_type_header)

        self.add_exception_handler(
            RequestValidationError, self.validation_exception_handler
        )
        self.add_exception_handler(HTTPException, self.http_exception_handler)
        self.add_exception_handler(FHIRException, self.fhir_exception_handler)
        self.add_exception_handler(Exception, self.general_exception_handler)

    def add_providers(self, *providers: FHIRProvider) -> None:
        """
        Add all FHIR interactions from all provided FHIRProviders.

        Iterate over the interactions from the providers, record the capabilities (based on the
        resource type and interaction type), and add the API route for the defined interaction.
        """
        provider_interactions = itertools.chain.from_iterable(
            provider.interactions for provider in providers
        )
        for interaction in sorted(
            provider_interactions,
            key=lambda i: cast(str, i.resource_type.get_resource_type()),
        ):
            resource_type = interaction.resource_type.get_resource_type()
            label = interaction.label()
            assert (
                resource_type not in self._capabilities
                or label not in self._capabilities[resource_type]
            ), f"FHIR {label} interaction for {resource_type} can only be supplied once"

            self._capabilities[resource_type][label] = interaction
            self._add_route(interaction)

    def set_capability_statement_modifier(
        self, modifier: Callable[[MutableMapping[str, Any]], MutableMapping[str, Any]]
    ) -> None:
        """
        Set a user-provided callable that will make adjustments to the automatically-generated
        capability statement.

        The user-provided callable must take a mutable mapping, which will be the capability
        statement, and return a mutable mapping, which will be the modified version of the
        capability statement.

        This method enables any desired change to be made to the capability statement, such as
        filling in fields that are not automatically generated, or adding extensions.

        All modifications made to the capability statement must conform to the specification of the
        FHIR CapabilityStatement resource, or server startup will fail.
        """
        self._capability_statement_modifier = modifier

    def set_exception_handler_callback(
        self, callback: Callable[[Request], Exception]
    ) -> None:
        """
        Set a user-provided callback function that will run whenever any type of exception occurs.

        This configuration option is useful for injecting additional exception handling behavior,
        such as exception logging.
        """
        self._exception_handler_callback = callback

    async def validation_exception_handler(
        self, request: Request, exception: RequestValidationError
    ) -> Response:
        """
        Validation exception handler that overrides the default FastAPI validation exception
        handler.

        Creates an operation outcome by destructuring the RequestValidationError and mapping the
        values to the correct places in the OperationOutcome.
        """
        if self._exception_handler_callback:
            self._exception_handler_callback(request, exception)

        operation_outcome = OperationOutcome(
            **{
                "issue": [
                    {
                        "severity": "error",
                        "code": _pydantic_error_to_fhir_issue_type(error["type"]),
                        "details": {
                            "text": display_errors([error]).replace("\n ", " —")
                        },
                    }
                    for error in exception.errors()
                ]
            }
        )

        return format_response(
            resource=operation_outcome,
            status_code=status.HTTP_400_BAD_REQUEST,
            format_parameters=FormatParameters.from_request(
                request, raise_exception=False
            ),
        )

    async def http_exception_handler(
        self, request: Request, exception: HTTPException
    ) -> Response:
        """
        HTTP exception handler that overrides the default FastAPI HTTP exception handler.

        This exception handler exists primarily to convert an HTTP exception into an
        OperationOutcome.
        """
        if self._exception_handler_callback:
            self._exception_handler_callback(request, exception)

        return _exception_response(
            request=request,
            severity="error",
            code="processing",
            details_text=exception.detail,
            status_code=exception.status_code,
        )

    async def fhir_exception_handler(
        self, request: Request, exception: FHIRException
    ) -> Response:
        """
        General exception handler to catch all other FHIRExceptions. Returns an OperationOutcome.

        Set the request on the exception so that the exception has more context with which to form
        an OperationOutcome.
        """
        if self._exception_handler_callback:
            self._exception_handler_callback(request, exception)

        exception.set_request(request)

        return format_response(
            resource=exception.operation_outcome(),
            status_code=exception.status_code,
            format_parameters=FormatParameters.from_request(
                request, raise_exception=False
            ),
        )

    async def general_exception_handler(
        self, request: Request, exception: Exception
    ) -> Response:
        """
        General exception handler to catch server framework errors. Returns an OperationOutcome.
        """
        if self._exception_handler_callback:
            self._exception_handler_callback(request, exception)

        return _exception_response(
            request=request,
            severity="error",
            code="exception",
            details_text=str(exception),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @cache
    def capability_statement(self) -> CapabilityStatement:
        """
        Generate the capability statement for the instance based on the FHIR interactions provided.

        In addition to declaring the interactions (e.g. create, read, search-type, and update), the
        supported search parameters are also declared.
        """
        resources = []
        for resource_type, interactions in sorted(self._capabilities.items()):
            search_parameter_metadata = self._search_parameters.get_metadata(
                resource_type
            )

            resource = {
                "type": resource_type,
                "interaction": [
                    {"code": label} for label in sorted(interactions.keys())
                ],
            }
            if search_type_interaction := interactions.get("search-type"):
                supported_search_parameters_ = []
                for search_parameter in supported_search_parameters(
                    search_type_interaction.handler
                ):
                    search_parameter_name = var_name_to_qp_name(search_parameter.name)
                    metadata = search_parameter_metadata[search_parameter_name]
                    if metadata["include-in-capability-statement"]:
                        supported_search_parameters_.append(
                            {
                                "name": search_parameter_name,
                                "definition": metadata["uri"],
                                "type": metadata["type"],
                                "documentation": metadata["description"],
                            }
                        )
                resource["searchParam"] = sorted(
                    supported_search_parameters_,
                    key=lambda p: search_parameter_sort_key(
                        p["name"], search_parameter_metadata
                    ),
                )
            resources.append(resource)

        # TODO: Status can be filled in based on environment
        # TODO: Date could be the release date (from an environment variable)
        capability_statement = {
            "status": "active",
            "date": self._created,
            "kind": "instance",
            "fhirVersion": "4.0.1",
            "format": ["json"],
            "rest": [
                {
                    "mode": "server",
                    "resource": resources,
                }
            ],
        }

        if self._capability_statement_modifier:
            capability_statement = self._capability_statement_modifier(
                capability_statement
            )

        return CapabilityStatement(**capability_statement)

    def openapi(self) -> dict[str, Any]:
        """
        Adjust the OpenAPI schema to make it more FHIR-friendly.

        Remove some default schemas that are not needed nor used, and change all content types that
        are set to "application/json" to instead be "application/fhir+json". Make a few additional
        aesthetic changes to clean up the auto-generated documentation.

        This method is slightly hacky because it directly modifies the OpenAPI schema, however it
        does make the generated documentation look nicer.

        Because it directly modifies the OpenAPI schema, it is vulnerable to breakage from updates
        to FastAPI. This is not a significant vulnerability because the core server functionality
        will still work (i.e. this is just documentation).
        """
        # TODO: It may be necessary to rethink some of the things that this function removes. For
        #  example, if someone wants to add non-FHIR endpoints to their API, then maybe some of
        #  these schemas shouldn't be removed. Also, for cases where paths or schemas are modified,
        #  there should be a way to more precisely target items that are FHIR-related.
        if self.openapi_schema:
            return self.openapi_schema

        openapi_schema = super().openapi()

        # Remove default FAstAPI validation errors, since FHIRStarter will always return operation
        # outcomes
        openapi_schema["components"]["schemas"].pop("HTTPValidationError", None)
        openapi_schema["components"]["schemas"].pop("ValidationError", None)

        # Iterate over the documentation for all paths
        for path_name, path in openapi_schema["paths"].items():
            # Inline the schemas generated for search by POST. These schemas are only used in one
            # place, so they don't need to exist in the schemas section.
            if match := re.fullmatch("/(.*)/_search", path_name):
                resource_type = match.group(1)
                path["post"]["requestBody"]["content"][
                    "application/x-www-form-urlencoded"
                ]["schema"] = openapi_schema["components"]["schemas"].pop(
                    f"Body_search_type_{resource_type}__search_post"
                )

            # Iterate over all operations for a given path
            for operation_name, operation in path.items():
                responses = operation["responses"]

                # For each possible response (i.e. status code), remove the default FastAPI response
                # schema
                status_codes: tuple[str, ...] = tuple(responses.keys())
                for status_code in status_codes:
                    if (
                        responses[status_code]["content"]
                        .get("application/json", {})
                        .get("schema", {})
                        .get("$ref")
                        == "#/components/schemas/HTTPValidationError"
                    ):
                        responses.pop(status_code)

                # For each response, change all instances of application/json to
                # application/fhir+json
                for response in responses.values():
                    if schema := response["content"].pop("application/json", None):
                        response["content"]["application/fhir+json"] = schema

        # For each schema (except for Bundle and OperationOutcome), provide an actual FHIR example
        # response unless an example exists on the actual model
        for schema_name, schema in openapi_schema["components"]["schemas"].items():
            resource_type = schema["properties"].get("resource_type", {}).get("const")

            if (
                not resource_type
                or resource_type in {"Bundle", "OperationOutcome"}
                or "example" in schema
            ):
                continue

            schema["example"] = load_example(resource_type)

        return openapi_schema

    def _add_capabilities_route(self) -> None:
        """Add the /metadata route, which supplies the capability statement for the instance."""

        def capability_statement_handler(
            request: Request,
            response: Response,
            _format: str = FORMAT_QP,
            _pretty: str = PRETTY_QP,
        ) -> CapabilityStatement | Response:
            return format_response(
                resource=self.capability_statement(),
                response=response,
                format_parameters=FormatParameters.from_request(request),
            )

        self.get(
            "/metadata",
            response_model=CapabilityStatement,
            status_code=status.HTTP_200_OK,
            tags=["System"],
            summary="Get a capability statement for the system",
            description="The capabilities interaction retrieves the information about a server's "
            "capabilities - which portions of the FHIR specification it supports.",
            response_model_exclude_none=True,
        )(capability_statement_handler)

    def _add_route(self, interaction: TypeInteraction[ResourceType]) -> None:
        """
        Add a route based on the FHIR interaction type.

        FHIR search-type routes must support both GET and POST, so two routes are added for
        search-type interactions.
        """
        match interaction.label():
            case "create":
                self.post(**create_route_args(interaction))(
                    make_create_function(interaction)
                )
            case "read":
                self.get(**read_route_args(interaction))(
                    make_read_function(interaction)
                )
            case "search-type":
                search_parameter_metadata = self._search_parameters.get_metadata(
                    interaction.resource_type.get_resource_type()
                )
                self.get(**search_type_route_args(interaction, post=False))(
                    make_search_type_function(
                        interaction,
                        search_parameter_metadata=search_parameter_metadata,
                        post=False,
                    )
                )
                self.post(**search_type_route_args(interaction, post=True))(
                    make_search_type_function(
                        interaction,
                        search_parameter_metadata=search_parameter_metadata,
                        post=True,
                    )
                )
            case "update":
                self.put(**update_route_args(interaction))(
                    make_update_function(interaction)
                )


async def _transform_search_type_post_request(
    request: Request, call_next: Callable[[Request], Coroutine[None, None, Response]]
) -> Response:
    """
    Middleware to transform a search POST request into a search GET request.

    This is needed for a few reasons, and mainly to simplify how searches are handled later down the
    line. Due to this middleware, all search requests will arrive in the handlers as GET requests
    with query strings that have been merged with the URL-encoded parameter string in the body.

    There is an obscure requirement in the FHIR specification stipulating that for search POST
    requests, both query string parameters and parameters in the body are to be considered when
    calculating search results. This is difficult to achieve in FastAPI due to how the body stream
    is consumed when it parses the body to pass the values down to the handlers. Catching the
    request here allows for the body parameters to be merged with the query string parameters.
    """
    if (
        request.url.path.endswith("/_search")
        and request.method == "POST"
        and request.headers.get("Content-Type") == "application/x-www-form-urlencoded"
    ):
        scope = request.scope
        scope["method"] = "GET"
        scope["path"] = scope["path"].removesuffix("/_search")
        scope["raw_path"] = scope["raw_path"].removesuffix(b"/_search")
        scope["query_string"] = await _merge_parameter_strings(request)
        scope["headers"] = [
            (name, value)
            for name, value in scope["headers"]
            if name.lower() not in {b"content-length", b"content-type"}
        ]

        return await call_next(Request(scope, request.receive))

    return await call_next(request)


async def _merge_parameter_strings(request: Request) -> bytes:
    """
    Merge the query string and the parameter string in the body into a single parameter string.

    If there is a header that specifies the requested format, then ignore the _format parameter(s)
    in the parameter strings.
    """
    merged: defaultdict[bytes, list[bytes]] = defaultdict(list)

    format_ = FormatParameters.format_from_accept_header(request)
    if format_:
        merged[b"_format"] = [format_.encode()]

    for query_string in (await request.body(), request.scope["query_string"]):
        for name, values in parse_qs(query_string).items():
            if format_ and name == "_format":
                continue
            merged[name].extend(values)

    return urlencode(merged, doseq=True).encode()


async def _set_content_type_header(
    request: Request, call_next: Callable[[Request], Coroutine[None, None, Response]]
) -> Response:
    """
    Middleware that changes the content type header to "application/fhir+json".

    For FHIR responses, there will be two content type headers in the response. One will be
    "application/json" (added by FastAPI), and one will be "application/fhir+json" (added by
    FHIRStarter). This middleware removes the "application/json" header.
    """
    response: Response = await call_next(request)

    if "application/fhir+json" in response.headers.getlist("Content-Type"):
        response.headers["Content-Type"] = "application/fhir+json"

    return response


def _pydantic_error_to_fhir_issue_type(error: str) -> str:
    """Return a FHIR issue type code mapped from a Pydantic error code."""
    error_type, *rest = error.split(".")
    error_code = rest[0] if rest else None

    match error_type, error_code:
        case ("value_error", "jsondecode") | ("value_error", "extra"):
            return "structure"
        case ("value_error", "missing"):
            return "required"
        case ("value_error", _) | ("type_error", _):
            return "value"
        case _:
            return "invalid"


def _exception_response(
    request: Request, severity: str, code: str, details_text: str, status_code: int
) -> Response:
    """Create a JSONResponse with an OperationOutcome and an HTTP status code."""
    operation_outcome = make_operation_outcome(
        severity=severity, code=code, details_text=details_text
    )

    return format_response(
        resource=operation_outcome,
        status_code=status_code,
        format_parameters=FormatParameters.from_request(request, raise_exception=False),
    )
