import inspect
import itertools
from typing import Any

from fastapi import Body, FastAPI, Path, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fhir.resources.fhirtypes import Id
from fhir.resources.resource import Resource

from .exceptions import FHIRException, FHIRInteractionError, make_operation_outcome
from .provider import (
    FHIRInteraction,
    FHIRInteractionType,
    FHIRProvider,
    FHIRResourceType,
)
from .utils import create_route_args, make_function, read_route_args

# TODO: Review documentation for read and create interactions
# TODO: Find out if user-provided type annotations need to be validated
# TODO: Research auto-filling path and query parameter options from the FHIR specification
# TODO: Research auto-filling path definition parameters with data from the FHIR specification
# TODO: Review all of the path definition parameters and path/query/body parameters
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

        self.add_exception_handler(
            RequestValidationError, _validation_exception_handler
        )
        self.add_exception_handler(
            FHIRInteractionError, _fhir_interaction_error_handler
        )
        self.add_exception_handler(FHIRException, _fhir_exception_handler)
        self.add_exception_handler(Exception, _exception_handler)

    def add_providers(self, *providers: FHIRProvider) -> None:
        unique_interactions = set()

        interactions = itertools.chain.from_iterable(
            provider.interactions for provider in providers
        )
        for interaction in sorted(interactions):
            assert (
                interaction.resource_type,
                interaction.interaction_type,
            ) not in unique_interactions, (
                f"FHIR interaction for resource type "
                f"'{interaction.resource_type.get_resource_type()}' and interaction type "
                f"'{interaction.interaction_type.value}' can only be supplied once"
            )

            unique_interactions.add(
                (interaction.resource_type, interaction.interaction_type)
            )
            self._add_route(interaction)

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
        raise NotImplementedError

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
        supported_search_parameters = tuple(
            sorted(inspect.signature(interaction.callable_).parameters.keys())
        )
        raise NotImplementedError


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
