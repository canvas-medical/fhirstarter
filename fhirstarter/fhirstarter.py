"""FHIRStarter class, exception handlers, and middleware."""

import itertools
import os
from collections import defaultdict
from collections.abc import Callable, Coroutine
from datetime import datetime
from functools import cache
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fhir.resources.capabilitystatement import CapabilityStatement

from .exceptions import FHIRException, FHIRInteractionError
from .functions import (
    make_create_function,
    make_read_function,
    make_search_type_function,
    make_update_function,
)
from .provider import FHIRProvider, InteractionType, ResourceType, TypeInteraction
from .search_parameters import (
    load_search_parameters,
    supported_search_parameters,
    var_sp_name_to_fhir_sp_name,
)
from .utils import (
    create_route_args,
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
# TODO: Look into allowing for the capability statement to be amended


class FHIRStarter(FastAPI):
    """
    FHIRStarter class.

    Handles collection of FHIR providers, creation of API routes, middleware, exception handling,
    and capability statement requests.
    """

    def __init__(self, **kwargs: Any) -> None:
        """
        On app creation, the following occurs:
        * Static routes are created (e.g. the capability statement route)
        * Middleware is added (e.g. content-type header handling)
        * Exception handling is added
        """
        super().__init__(**kwargs)

        self._capabilities: dict[  # type: ignore
            str, dict[InteractionType, TypeInteraction]
        ] = defaultdict(dict)
        self._created = datetime.utcnow()

        self._add_capabilities_route()

        self.middleware("http")(_add_content_type_header)

        self.add_exception_handler(
            RequestValidationError, _validation_exception_handler
        )
        self.add_exception_handler(
            FHIRInteractionError, _fhir_interaction_error_handler
        )
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
        for interaction in sorted(provider_interactions):
            resource_type = interaction.resource_type.get_resource_type()
            interaction_type = interaction.interaction_type
            assert (
                resource_type not in self._capabilities
                or interaction_type not in self._capabilities[resource_type]
            ), (
                "FHIR interaction for resource type "
                f"'{resource_type}' and interaction type "
                f"'{interaction_type}' can only be supplied once"
            )

            self._capabilities[resource_type][interaction_type] = interaction
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

                status_codes = tuple(responses.keys())
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
        self.get(
            "/metadata",
            response_model=CapabilityStatement,
            status_code=status.HTTP_200_OK,
            tags=["System"],
            summary="Get a capability statement for the system",
            description="The capabilities interaction retrieves the information about a server's "
            "capabilities - which portions of the FHIR specification it supports.",
            response_model_exclude_none=True,
        )(lambda: self._capability_statement())

    def _add_route(self, interaction: TypeInteraction[ResourceType]) -> None:
        """
        Add a route based on the FHIR interaction type.

        FHIR search-type routes must support both GET and POST, so two routes are added for
        search-type interactions.
        """
        match interaction.interaction_type:
            case InteractionType.CREATE:
                self.post(**create_route_args(interaction))(
                    make_create_function(interaction)
                )
            case InteractionType.READ:
                self.get(**read_route_args(interaction))(
                    make_read_function(interaction)
                )
            case InteractionType.SEARCH_TYPE:
                self.get(**search_type_route_args(interaction, post=False))(
                    make_search_type_function(interaction, post=False)
                )
                self.post(**search_type_route_args(interaction, post=True))(
                    make_search_type_function(interaction, post=True)
                )
            case InteractionType.UPDATE:
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
        search_parameters = load_search_parameters()

        resources = []
        for resource_type, interaction_types in sorted(self._capabilities.items()):
            resource = {
                "type": resource_type,
                "interaction": [
                    {"code": interaction_type.value}
                    for interaction_type in sorted(interaction_types)
                ],
            }
            if search_type_interaction := interaction_types.get(
                InteractionType.SEARCH_TYPE
            ):
                supported_search_parameters_ = []
                # TODO: Test this with a hyphenated search parameter
                for search_parameter in supported_search_parameters(
                    search_type_interaction.callable_
                ):
                    search_parameter = var_sp_name_to_fhir_sp_name(search_parameter)
                    supported_search_parameters_.append(
                        {
                            "name": search_parameters[resource_type][search_parameter][
                                "name"
                            ],
                            "type": search_parameters[resource_type][search_parameter][
                                "type"
                            ],
                        }
                    )
                resource["searchParam"] = supported_search_parameters_
            resources.append(resource)

        # TODO: Status can be filled in based on environment
        # TODO: Date could be the release date (from an environment variable)
        # TODO: Add XML format
        capability_statement = {
            "id": str(uuid4()),
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
        if publisher := os.getenv("CAPABILITY_STATEMENT_PUBLISHER"):
            capability_statement["publisher"] = publisher

        return CapabilityStatement(**capability_statement)


async def _add_content_type_header(
    request: Request, call_next: Callable[[Request], Coroutine[None, None, Response]]
) -> Response:
    """Middleware function that changes the content type header to "application/fhir+json"."""
    response: Response = await call_next(request)
    if request.url.components.path not in {"/docs", "/redoc"}:
        response.headers["Content-Type"] = "application/fhir+json"

    return response


async def _validation_exception_handler(
    _: Request, exception: RequestValidationError
) -> JSONResponse:
    """
    Validation exception handler that overrides the default FastAPI validation exception handler.

    Returns an OperationOutcome.
    """
    return _exception_json_response(
        severity="fatal",
        code="structure",
        exception=exception,
        status_code=status.HTTP_400_BAD_REQUEST,
    )


async def _fhir_interaction_error_handler(
    request: Request, exception: FHIRInteractionError
) -> JSONResponse:
    """
    Exception handler that catches FHIRInteractionErrors.

    Set the request on the exception so that the exception has more context with which to form an
    OperationOutcome.
    """
    exception.set_request(request)
    return exception.response()


async def _fhir_exception_handler(_: Request, exception: FHIRException) -> JSONResponse:
    """General exception handler to catch all other FHIRExceptions. Returns an OperationOutcome."""
    return exception.response()


async def _exception_handler(_: Request, exception: Exception) -> JSONResponse:
    """General exception handler to catch server framework errors. Returns an OperationOutcome."""
    return _exception_json_response(
        severity="fatal",
        code="exception",
        exception=exception,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def _exception_json_response(
    severity: str, code: str, exception: Exception, status_code: int
) -> JSONResponse:
    """Create a JSONResponse with an OperationOutcome and an HTTP status code."""
    operation_outcome = make_operation_outcome(
        severity=severity, code=code, details_text=f"{str(exception)}"
    )
    return JSONResponse(content=operation_outcome.dict(), status_code=status_code)
