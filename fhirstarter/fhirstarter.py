"""FHIRStarter class, exception handlers, and middleware."""

import itertools
import logging
import tomllib
from collections import defaultdict
from collections.abc import Callable, Coroutine, MutableMapping
from datetime import datetime
from io import IOBase
from os import PathLike
from typing import Any, TypeAlias, cast
from urllib.parse import parse_qs, urlencode
from zoneinfo import ZoneInfo

from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.exceptions import RequestValidationError
from pydantic.error_wrappers import display_errors

from .exceptions import FHIRException
from .fhir_specification import FHIR_SEQUENCE, FHIR_VERSION
from .functions import (
    FORMAT_QP,
    PRETTY_QP,
    make_create_function,
    make_read_function,
    make_search_type_function,
    make_update_function,
)
from .interactions import ResourceType, TypeInteraction
from .openapi import adjust_schema
from .providers import FHIRProvider
from .resources import CapabilityStatement, OperationOutcome
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
    parse_fhir_request,
    read_route_args,
    search_type_route_args,
    update_route_args,
)

# Suppress warnings from base fhir.resources class
logging.getLogger("fhir.resources.core.fhirabstractmodel").setLevel(logging.WARNING + 1)

CapabilityStatementModifier: TypeAlias = Callable[
    [MutableMapping[str, Any], Request, Response], MutableMapping[str, Any]
]


class FHIRStarter(FastAPI):
    """
    FHIRStarter class.

    Handles collection of FHIR providers, creation of API routes, middleware, exception handling,
    and capability statement requests.
    """

    def __init__(
        self,
        *,
        config_file: str | PathLike[str] | IOBase | None = None,
        title: str = "FHIRStarter",
        **kwargs: Any,
    ) -> None:
        """
        On app creation, the following occurs:
        * Custom search parameters are loaded
        * Static routes are created (e.g. the capability statement route)
        * Middleware is added (e.g. content-type header handling)
        * Exception handling is added
        """
        super().__init__(title=title, **kwargs)

        if config_file:
            try:
                cast(IOBase, config_file).seek(0)
                config = tomllib.load(config_file)
            except AttributeError:
                with open(config_file, "rb") as file_:
                    config = tomllib.load(file_)

            self._search_parameters = SearchParameters(config.get("search-parameters"))
        else:
            self._search_parameters = SearchParameters()

        self._capabilities: dict[str, dict[str, TypeInteraction]] = defaultdict(dict)
        self._created = datetime.now(ZoneInfo("UTC")).isoformat()

        self.set_capability_statement_modifier(lambda c, _, __: c)

        self._add_capabilities_route()

        self.middleware("http")(_transform_search_type_post_request)
        self.middleware("http")(_transform_null_response_body)
        self.middleware("http")(_set_content_type_header)

        async def default_exception_callback(
            _: Request, response: Response, __: Exception
        ) -> Response:
            return response

        self._exception_callback: Callable[
            [Request, Response, Exception], Coroutine[None, None, Response]
        ] = default_exception_callback

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
        self, modifier: CapabilityStatementModifier
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

    def set_exception_callback(
        self,
        callback: Callable[
            [Request, Response, Exception], Coroutine[None, None, Response]
        ],
    ) -> None:
        """
        Set a user-provided callback function that will run whenever any type of exception occurs.
        This configuration option is useful for injecting additional exception handling behavior,
        such as exception logging.
        """
        self._exception_callback = callback

    async def validation_exception_handler(
        self, request: Request, exception: RequestValidationError
    ) -> Response:
        """
        Validation exception handler that overrides the default FastAPI validation exception
        handler.

        Creates an operation outcome by destructuring the RequestValidationError and mapping the
        values to the correct places in the OperationOutcome.
        """
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

        response = format_response(
            resource=operation_outcome,
            status_code=status.HTTP_400_BAD_REQUEST,
            format_parameters=FormatParameters.from_request(
                request, raise_exception=False
            ),
        )

        return await self._exception_callback(request, response, exception)

    async def http_exception_handler(
        self, request: Request, exception: HTTPException
    ) -> Response:
        """
        HTTP exception handler that overrides the default FastAPI HTTP exception handler.

        This exception handler exists primarily to convert an HTTP exception into an
        OperationOutcome.
        """
        response = _exception_response(
            request=request,
            severity="error",
            code="processing",
            details_text=exception.detail,
            status_code=exception.status_code,
        )

        return await self._exception_callback(request, response, exception)

    async def fhir_exception_handler(
        self, request: Request, exception: FHIRException
    ) -> Response:
        """
        General exception handler to catch all other FHIRExceptions. Returns an OperationOutcome.

        Set the request on the exception so that the exception has more context with which to form
        an OperationOutcome.
        """
        exception.set_request(request)

        response = format_response(
            resource=exception.operation_outcome(),
            status_code=exception.status_code,
            format_parameters=FormatParameters.from_request(
                request, raise_exception=False
            ),
        )

        return await self._exception_callback(request, response, exception)

    async def general_exception_handler(
        self, request: Request, exception: Exception
    ) -> Response:
        """
        General exception handler to catch server framework errors. Returns an OperationOutcome.
        """
        response = _exception_response(
            request=request,
            severity="error",
            code="exception",
            details_text=str(exception),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

        return await self._exception_callback(request, response, exception)

    def capability_statement(
        self, request: Request, response: Response
    ) -> CapabilityStatement:
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
                        cast(dict[str, str], p)["name"], search_parameter_metadata
                    ),
                )
            resources.append(resource)

        capability_statement = {
            "status": "active",
            "date": self._created,
            "kind": "instance",
            "fhirVersion": FHIR_VERSION,
            "acceptUnknown": "no",
            "format": ["json"],
            "rest": [
                {
                    "mode": "server",
                    "resource": resources,
                }
            ],
        }

        if FHIR_SEQUENCE != "STU3":
            del capability_statement["acceptUnknown"]

        return CapabilityStatement(
            **self._capability_statement_modifier(
                capability_statement, request, response
            )
        )

    def openapi(self) -> dict[str, Any]:
        """Adjust the OpenAPI schema to make it more FHIR-friendly."""
        if self.openapi_schema:
            return self.openapi_schema

        openapi_schema = super().openapi()
        adjust_schema(openapi_schema)

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
                resource=self.capability_statement(request, response),
                response=response,
                format_parameters=FormatParameters.from_request(request),
            )

        self.get(
            "/metadata",
            response_model=CapabilityStatement,
            status_code=status.HTTP_200_OK,
            tags=["System"],
            summary="capabilities",
            description="The capabilities interaction retrieves the information about a server's "
            "capabilities - which portions of the FHIR specification it supports.",
            operation_id="fhirstarter|system|capabilities|get",
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
    Middleware that transforms a search POST request into a search GET request.

    This is needed for a few reasons, and mainly to simplify how searches are handled later down the
    line. Due to this middleware, all search requests will arrive in the handlers as GET requests
    with query strings that have been merged with the URL-encoded parameter string in the body.

    There is an obscure requirement in the FHIR specification stipulating that for search POST
    requests, both query string parameters and parameters in the body are to be considered when
    calculating search results. This is difficult to achieve in FastAPI due to how the body stream
    is consumed when it parses the body to pass the values down to the handlers. Catching the
    request here allows for the body parameters to be merged with the query string parameters.
    """
    interaction_info = parse_fhir_request(request)

    if (
        interaction_info.interaction_type == "search-type"
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


async def _transform_null_response_body(
    request: Request, call_next: Callable[[Request], Coroutine[None, None, Response]]
) -> Response:
    """
    Middleware that cleans up the response object when the response does not contain a response
    body.

    Create and update interactions are not required to return a response body. In this scenario,
    FastAPI for some reason returns a response with a body containing the string "null", rather than
    just an empty body. This middleware detects that scenario and cleans up the response body.
    """
    response = await call_next(request)

    # This condition is probably too broad, but given that all FHIR responses should either have a
    # body that is a resource (that must be more than 4 bytes by definition) or an empty response
    # body, it is safe to assume that a 4-byte response contains the string "null" and needs to be
    # transformed.
    if (
        "application/fhir+json" in response.headers.getlist("Content-Type")
        and response.headers.get("Content-Length") == "4"
    ):
        response.headers["Content-Length"] = "0"
        del response.headers["Content-Type"]
        response = Response(status_code=response.status_code, headers=response.headers)

    return response


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
        case ("json_invalid", _) | ("value_error", "extra"):
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
        severity=severity, code=code, details_text=details_text or "Exception"
    )

    return format_response(
        resource=operation_outcome,
        status_code=status_code,
        format_parameters=FormatParameters.from_request(request, raise_exception=False),
    )
