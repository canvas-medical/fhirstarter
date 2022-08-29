"""FHIRStarter class, exception handlers, and middleware."""

from fastapi import HTTPException
import asyncio
import itertools
from collections import defaultdict
from collections.abc import Callable, Coroutine
from datetime import datetime
from functools import cache
from os import PathLike
from typing import Any, cast
from urllib.parse import parse_qs, urlencode

import tomli
import uvloop
from fastapi import FastAPI, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fhir.resources.capabilitystatement import CapabilityStatement

from .exceptions import FHIRException
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
                self._publisher = config.get("capability-statement", {}).get(
                    "publisher"
                )
                self._search_parameters = SearchParameters(
                    config.get("search-parameters")
                )
        else:
            self._publisher = None
            self._search_parameters = SearchParameters()

        self._capabilities: dict[str, dict[str, TypeInteraction]] = defaultdict(dict)
        self._created = datetime.utcnow()

        self._add_capabilities_route()

        self.middleware("http")(_transform_search_type_post_request)
        self.middleware("http")(_set_content_type_header)

        self.add_exception_handler(RequestValidationError, _validation_exception_handler)
        self.add_exception_handler(HTTPException, _http_exception_handler)
        self.add_exception_handler(FHIRException, _fhir_exception_handler)
        self.add_exception_handler(Exception, _exception_handler)

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

    def openapi(self) -> dict[str, Any]:
        """
        Adjust the OpenAPI schema to make it more FHIR-friendly.

        Remove some default schemas that are not needed nor used, and change all content types that
        are set to "application/json" to instead be "application/fhir+json".

        This method is slightly hacky because it directly modifies the OpenAPI schema, however it
        does make the generated documentation look nicer.

        Because it directly modifies the OpenAPI schema, it is vulnerable to breakage from updates
        to FastAPI. This is not a significant vulnerability because the core server functionality
        will still work (i.e. this is just documentation).
        """
        openapi_schema = super().openapi()

        openapi_schema["components"]["schemas"].pop("HTTPValidationError", None)
        openapi_schema["components"]["schemas"].pop("ValidationError", None)

        for path in openapi_schema["paths"].values():
            for operation_name, operation in path.items():
                responses = operation["responses"]

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

                for response in responses.values():
                    if schema := response["content"].pop("application/json", None):
                        response["content"]["application/fhir+json"] = schema

        return openapi_schema

    def _add_capabilities_route(self) -> None:
        """Add the /metadata route, which supplies the capability statement for the instance."""

        def capability_statement(
            request: Request,
            response: Response,
            _format: str = FORMAT_QP,
            _pretty: str = PRETTY_QP,
        ) -> CapabilityStatement | Response:
            return format_response(
                resource=self._capability_statement(),
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
        )(capability_statement)

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

    @cache
    def _capability_statement(self) -> CapabilityStatement:
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
                resource["searchParam"] = supported_search_parameters_
            resources.append(resource)

        # TODO: Status can be filled in based on environment
        # TODO: Date could be the release date (from an environment variable)
        # TODO: Add XML format
        capability_statement = {
            "status": "active",
            "date": self._created,
            "kind": "instance",
            "fhirVersion": "4.3.0",
            "format": ["json"],
            "rest": [
                {
                    "mode": "server",
                    "resource": resources,
                }
            ],
        }
        if self._publisher:
            capability_statement["publisher"] = self._publisher

        return CapabilityStatement(**capability_statement)


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


async def _validation_exception_handler(
    request: Request, exception: RequestValidationError
) -> Response:
    """
    Validation exception handler that overrides the default FastAPI validation exception handler.

    Returns an OperationOutcome.
    """
    return _exception_response(
        request=request,
        severity="error",
        code="structure",
        details_text=str(exception),
        status_code=status.HTTP_400_BAD_REQUEST,
    )


async def _http_exception_handler(request: Request, exception: HTTPException) -> Response:
    """
    HTTP exception handler that overrides the default FastAPI HTTP exception handler.

    This exception handler exists primarily to convert an HTTP exception into an OperationOutcome.
    """
    return _exception_response(
        request=request,
        severity="error",
        code="processing",
        details_text=exception.detail,
        status_code=exception.status_code,
    )


async def _fhir_exception_handler(
    request: Request, exception: FHIRException
) -> Response:
    """
    General exception handler to catch all other FHIRExceptions. Returns an OperationOutcome.

    Set the request on the exception so that the exception has more context with which to form an
    OperationOutcome.
    """
    exception.set_request(request)

    return format_response(
        resource=exception.operation_outcome(),
        status_code=exception.status_code(),
        format_parameters=FormatParameters.from_request(request, raise_exception=False),
    )


async def _exception_handler(request: Request, exception: Exception) -> Response:
    """General exception handler to catch server framework errors. Returns an OperationOutcome."""
    return _exception_response(
        request=request,
        severity="error",
        code="exception",
        details_text=str(exception),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


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
