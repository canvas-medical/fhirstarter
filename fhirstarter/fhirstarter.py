import inspect
import itertools
from collections import defaultdict
from types import FunctionType
from typing import Any, Mapping

from fastapi import Body, FastAPI, Path, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fhir.resources.fhirtypes import Id
from fhir.resources.operationoutcome import OperationOutcome
from fhir.resources.resource import Resource

from . import code_templates
from .exceptions import (
    FHIRException,
    FHIRGeneralError,
    FHIRInteractionContext,
    FHIRInteractionError,
    make_operation_outcome,
)
from .provider import (
    FHIRInteraction,
    FHIRInteractionType,
    FHIRProvider,
    FHIRResourceType,
)

# TODO: Headers for all interation types
# TODO: Tests for all interaction types
# TODO: Find out if user-provided type annotations need to be validated
# TODO: OperationOutcome
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
        self.add_exception_handler(Exception, _exception_handler)
        self._interactions: defaultdict = defaultdict(dict)

    def add_providers(self, *providers: FHIRProvider) -> None:
        interactions = itertools.chain.from_iterable(
            provider.interactions for provider in providers
        )
        for interaction in sorted(interactions):
            assert (
                interaction.resource_type not in self._interactions
                or interaction.interaction_type
                not in self._interactions[interaction.resource_type]
            ), (
                f"FHIR interaction for resource type "
                "'{interaction.resource_type.get_resource_type()}' and interaction type "
                "'{interaction.interaction_type}' can only be supplied once"
            )

            self._interactions[interaction.resource_type][
                interaction.interaction_type
            ] = interaction
            self._add_route(interaction)

    async def dispatch(
        self,
        resource_type: FHIRResourceType,
        interaction_type: FHIRInteractionType,
        /,
        **kwargs: Any,
    ) -> FHIRResourceType | JSONResponse:
        try:
            interaction = self._interactions[resource_type][interaction_type]
        except KeyError as key_error:
            raise _unsupported_interaction_error(
                resource_type, interaction_type
            ) from key_error

        try:
            match interaction_type:
                case FHIRInteractionType.CREATE:
                    return await interaction.callable_(kwargs["resource"])
                case FHIRInteractionType.UPDATE:
                    return await interaction.callable_(kwargs["id"], kwargs["resource"])
                case FHIRInteractionType.READ:
                    return await interaction.callable_(kwargs["id_"])
                case FHIRInteractionType.SEARCH:
                    return await interaction.callable_(**kwargs)
        except FHIRInteractionError as error:
            error.set_context(FHIRInteractionContext(interaction, kwargs))
            return error.response()
        except FHIRException as exception:
            return exception.response()
        else:
            raise _unsupported_interaction_error(resource_type, interaction_type)

    def _add_route(self, interaction: FHIRInteraction) -> None:
        match interaction.interaction_type:
            case FHIRInteractionType.CREATE:
                self._add_create_route(interaction)
            case FHIRInteractionType.UPDATE:
                self._add_update_route(interaction)
            case FHIRInteractionType.READ:
                self._add_read_route(interaction)
            case FHIRInteractionType.SEARCH:
                self._add_search_route(interaction)

    def _add_create_route(self, interaction: FHIRInteraction) -> None:
        resource_type_str = interaction.resource_type.get_resource_type()

        func = self._make_function(
            interaction=interaction,
            annotations={"resource": interaction.resource_type},
            argdefs=(
                Body(None, media_type="application/fhir+json", alias=resource_type_str),
            ),
        )

        # TODO: Can route be configured so that it is optional whether the response body contains
        #  the created resource?
        self.post(
            path=f"/{resource_type_str}",
            response_model=interaction.resource_type,
            status_code=status.HTTP_201_CREATED,
            summary=f"{resource_type_str} create",
            description=f"The {resource_type_str} create interaction creates a new "
            f"{resource_type_str} resource in a server-assigned location.",
            responses={
                status.HTTP_201_CREATED: {
                    "description": f"Successful {resource_type_str} create",
                    "content": {
                        "application/json": {
                            "schema": interaction.resource_type.schema()
                        },
                        "application/fhir+json": {
                            "schema": interaction.resource_type.schema()
                        },
                    },
                },
                status.HTTP_400_BAD_REQUEST: {
                    "description": f"{resource_type_str} resource could not be parsed or failed "
                    "basic FHIR validation rules",
                    "content": {
                        "application/json": {"schema": OperationOutcome.schema()},
                        "application/fhir+json": {"schema": OperationOutcome.schema()},
                    },
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY: {
                    "description": f"The proposed {resource_type_str} resource violated applicable "
                    "FHIR profiles or server business rules",
                    "content": {
                        "application/json": {"schema": OperationOutcome.schema()},
                        "application/fhir+json": {"schema": OperationOutcome.schema()},
                    },
                },
            },
            response_model_exclude_none=True,
            **interaction.route_options,
        )(func)

    def _add_read_route(self, interaction: FHIRInteraction) -> None:
        resource_type_str = interaction.resource_type.get_resource_type()

        func = self._make_function(
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

        self.get(
            path=f"/{resource_type_str}/{{id}}",
            response_model=interaction.resource_type,
            status_code=status.HTTP_200_OK,
            summary=f"{resource_type_str} read",
            description=f"The {resource_type_str} read interaction accesses "
            f"the current contents of a {resource_type_str}.",
            responses={
                status.HTTP_200_OK: {
                    "description": f"Successful {resource_type_str} read",
                    "content": {
                        "application/json": {
                            "schema": interaction.resource_type.schema()
                        },
                        "application/fhir+json": {
                            "schema": interaction.resource_type.schema()
                        },
                    },
                },
                status.HTTP_404_NOT_FOUND: {
                    "description": f"Unknown {resource_type_str} resource",
                    "content": {
                        "application/json": {"schema": OperationOutcome.schema()},
                        "application/fhir+json": {"schema": OperationOutcome.schema()},
                    },
                },
            },
            response_model_exclude_none=True,
            **interaction.route_options,
        )(func)

    def _add_search_route(self, interaction: FHIRInteraction) -> None:
        supported_search_parameters = tuple(
            sorted(inspect.signature(interaction.callable_).parameters.keys())
        )
        raise NotImplementedError

    def _add_update_route(self, interaction: FHIRInteraction) -> None:
        raise NotImplementedError

    def _make_function(
        self,
        interaction: FHIRInteraction,
        annotations: Mapping[str, Any],
        argdefs: tuple[Any, ...],
    ) -> FunctionType:
        name = (
            f"{interaction.resource_type.get_resource_type().lower()}_"
            f"{interaction.interaction_type.value}"
        )
        code = getattr(code_templates, interaction.interaction_type.value).__code__
        globals_ = {
            "dispatch": self.dispatch,
            "resource_type": interaction.resource_type,
            "interaction_type": interaction.interaction_type,
        }

        func = FunctionType(code=code, globals=globals_, name=name, argdefs=argdefs)
        func.__annotations__ = dict(annotations)

        return func


async def _validation_exception_handler(
    _: Request, exception: RequestValidationError
) -> JSONResponse:
    return _exception_json_response(
        severity="fatal",
        code="structure",
        exception=exception,
        status_code=status.HTTP_400_BAD_REQUEST,
    )


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


def _unsupported_interaction_error(
    resource_type: FHIRResourceType, interaction_type: FHIRInteractionType
) -> FHIRGeneralError:
    return FHIRGeneralError(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        severity="fatal",
        code="not-supported",
        details_text="Server is improperly configured; FHIR interaction "
        f"'{interaction_type.value}' is not supported for resource type "
        f"'{resource_type.get_resource_type()}'",
    )
