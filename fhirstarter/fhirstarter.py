import itertools
from collections import defaultdict
from collections.abc import Callable, Coroutine
from datetime import datetime
from functools import cache
from typing import Any
from uuid import uuid4

from fastapi import Body, FastAPI, Path, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fhir.resources.capabilitystatement import CapabilityStatement
from fhir.resources.fhirtypes import Id
from fhir.resources.resource import Resource

from .exceptions import FHIRException, FHIRInteractionError
from .provider import (
    FHIRInteraction,
    FHIRInteractionType,
    FHIRProvider,
    FHIRResourceType,
)
from .search_parameters import load_search_parameters, supported_search_parameters
from .utils import (
    create_route_args,
    make_function,
    make_operation_outcome,
    make_search_function,
    read_route_args,
    search_route_args,
    update_route_args,
)

# TODO: Review documentation for read and create interactions
# TODO: Find out if user-provided type annotations need to be validated
# TODO: Research auto-filling path and query parameter options from the FHIR specification
# TODO: Research auto-filling path definition parameters with data from the FHIR specification
# TODO: Review all of the path definition parameters and path/query/body parameters
# TODO: Expose responses FastAPI argument so that developer can specify additional responses
# - tags
# - summary
# - description
# - response_description
# - responses
# - operation_id
# - response class
# - name
# - callbacks
# - openapi_extra


class FHIRStarter(FastAPI):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self._capabilities: dict[  # type: ignore
            str, dict[FHIRInteractionType, FHIRInteraction]
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
                f"FHIR interaction for resource type "
                f"'{resource_type}' and interaction type "
                f"'{interaction_type}' can only be supplied once"
            )

            self._capabilities[resource_type][interaction_type] = interaction
            self._add_route(interaction)

    def openapi(self) -> dict[str, Any]:
        openapi_schema = super().openapi()

        openapi_schema["components"]["schemas"].pop("HTTPValidationError", None)
        openapi_schema["components"]["schemas"].pop("ValidationError", None)

        for path in openapi_schema["paths"].values():
            for operation_name, operation in path.items():
                responses = operation["responses"]

                if operation_name == "get":
                    responses.pop("422", None)

                for response in responses.values():
                    if schema := response["content"].pop("application/json", None):
                        response["content"]["application/fhir+json"] = schema

        return openapi_schema

    def _add_capabilities_route(self) -> None:
        def metadata() -> CapabilityStatement:
            return self._capability_statement()

        self.get(
            "/metadata",
            response_model=CapabilityStatement,
            status_code=status.HTTP_200_OK,
            tags=["System"],
            summary="Get a capability statement for the system",
            description="The capabilities interaction retrieves the information about a server's "
            "capabilities - which portions of the FHIR specification it supports.",
            response_model_exclude_none=True,
        )(metadata)

    def _add_route(self, interaction: FHIRInteraction[FHIRResourceType]) -> None:
        match interaction.interaction_type:
            case FHIRInteractionType.CREATE:
                self._add_create_route(interaction)
            case FHIRInteractionType.UPDATE:
                self._add_update_route(interaction)
            case FHIRInteractionType.READ:
                self._add_read_route(interaction)
            case FHIRInteractionType.SEARCH:
                self._add_search_route(interaction)

    def _add_create_route(self, interaction: FHIRInteraction[FHIRResourceType]) -> None:
        func = make_function(
            interaction=interaction,
            annotations={"resource": interaction.resource_type},
            argdefs=(
                Body(
                    None,
                    media_type="application/fhir+json",
                    alias=interaction.resource_type.get_resource_type(),
                ),
            ),
        )

        self.post(**create_route_args(interaction))(func)

    def _add_update_route(self, interaction: FHIRInteraction[FHIRResourceType]) -> None:
        func = make_function(
            interaction=interaction,
            annotations={"id_": Id, "resource": interaction.resource_type},
            argdefs=(
                Path(
                    None,
                    alias="id",
                    description=Resource.schema()["properties"]["id"]["title"],
                ),
                Body(
                    None,
                    media_type="application/fhir+json",
                    alias=interaction.resource_type.get_resource_type(),
                ),
            ),
        )

        self.put(**update_route_args(interaction))(func)

    def _add_read_route(self, interaction: FHIRInteraction[FHIRResourceType]) -> None:
        func = make_function(
            interaction=interaction,
            annotations={"id_": Id},
            argdefs=(
                Path(
                    None,
                    alias="id",
                    description=Resource.schema()["properties"]["id"]["title"],
                ),
            ),
        )

        self.get(**read_route_args(interaction))(func)

    def _add_search_route(self, interaction: FHIRInteraction[FHIRResourceType]) -> None:
        func = make_search_function(interaction)

        self.get(**search_route_args(interaction))(func)

    @cache
    def _capability_statement(self) -> CapabilityStatement:
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
            if search_interaction := interaction_types.get(FHIRInteractionType.SEARCH):
                supported_search_parameters_ = []
                for search_parameter in supported_search_parameters(
                    search_interaction.callable_
                ):
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
        return CapabilityStatement(
            **{
                "id": str(uuid4()),
                "status": "active",
                "date": self._created,
                "publisher": "Canvas Medical",
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
        )


async def _add_content_type_header(
    request: Request, call_next: Callable[[Request], Coroutine[None, None, Response]]
) -> Response:
    response: Response = await call_next(request)
    if request.url.components.path not in {"/docs", "/redoc"}:
        response.headers["Content-Type"] = "application/fhir+json"

    return response


async def _validation_exception_handler(
    _: Request, exception: RequestValidationError
) -> JSONResponse:
    return _exception_json_response(
        severity="fatal",
        code="structure",
        exception=exception,
        status_code=status.HTTP_400_BAD_REQUEST,
    )


async def _fhir_interaction_error_handler(
    request: Request, exception: FHIRInteractionError
) -> JSONResponse:
    exception.set_request(request)
    return exception.response()


async def _fhir_exception_handler(_: Request, exception: FHIRException) -> JSONResponse:
    return exception.response()


async def _exception_handler(_: Request, exception: Exception) -> JSONResponse:
    return _exception_json_response(
        severity="fatal",
        code="exception",
        exception=exception,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def _exception_json_response(
    severity: str, code: str, exception: Exception, status_code: int
) -> JSONResponse:
    operation_outcome = make_operation_outcome(
        severity=severity, code=code, details_text=f"{str(exception)}"
    )
    return JSONResponse(content=operation_outcome.dict(), status_code=status_code)
