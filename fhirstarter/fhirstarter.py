import inspect
from collections import defaultdict
from types import FunctionType
from typing import Any

from fastapi import FastAPI, Path, Request, status
from fastapi.responses import JSONResponse
from fhir.resources.fhirtypes import Id
from fhir.resources.operationoutcome import OperationOutcome
from fhir.resources.resource import Resource

from fhirstarter import code_templates
from fhirstarter.exceptions import (
    FHIRException,
    FHIRGeneralError,
    FHIRInteractionContext,
    FHIRInteractionError,
    make_operation_outcome,
)
from fhirstarter.provider import (
    FHIRInteraction,
    FHIRInteractionType,
    FHIRProvider,
    FHIRResourceType,
)

# TODO: Headers
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
        self.add_exception_handler(Exception, _exception_handler)
        self._interactions: defaultdict = defaultdict(dict)

    def add_providers(self, *providers: FHIRProvider) -> None:
        for provider in providers:
            for interaction in provider.interactions:
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
        error = FHIRGeneralError(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "fatal",
            "not-supported",
            f"Server is improperly configured; FHIR interaction '{interaction_type.value}' is not "
            f"supported for resource type '{resource_type.get_resource_type()}'",
        )

        try:
            interaction = self._interactions[resource_type][interaction_type]
        except KeyError as key_error:
            raise error from key_error

        try:
            match interaction_type:
                case FHIRInteractionType.CREATE | FHIRInteractionType.UPDATE:
                    return await interaction.callable_(kwargs["resource"])
                case FHIRInteractionType.READ:
                    return await interaction.callable_(kwargs["id_"])
                case FHIRInteractionType.SEARCH_TYPE:
                    return await interaction.callable_(**kwargs)
        except FHIRInteractionError as error:
            error.set_context(FHIRInteractionContext(interaction, kwargs))
            return error.response()
        except FHIRException as exception:
            return exception.response()

        raise error

    def _add_route(self, interaction: FHIRInteraction) -> None:
        match interaction.interaction_type:
            case FHIRInteractionType.CREATE:
                self._add_create_route(interaction)
            case FHIRInteractionType.READ:
                self._add_read_route(interaction)
            case FHIRInteractionType.SEARCH_TYPE:
                self._add_search_route(interaction)
            case FHIRInteractionType.UPDATE:
                self._add_update_route(interaction)

    def _add_create_route(self, interaction: FHIRInteraction) -> None:
        raise NotImplementedError

    def _add_read_route(self, interaction: FHIRInteraction) -> None:
        resource_type_str = interaction.resource_type.get_resource_type()

        name = f"{resource_type_str.lower()}_read"
        annotations = {"id_": Id}
        argdefs = (
            Path(
                None,
                alias="id",
                description=Resource.schema()["properties"]["id"]["title"],
            ),
        )
        code = getattr(code_templates, "read").__code__
        globals_ = {
            "dispatch": self.dispatch,
            "resource_type": interaction.resource_type,
            "interaction_type": interaction.interaction_type,
        }

        func = FunctionType(code, globals_, name, argdefs)
        func.__annotations__ = annotations

        self.get(
            f"/{resource_type_str}/{{id}}",
            response_model=interaction.resource_type,
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


async def _exception_handler(_: Request, exception: Exception) -> JSONResponse:
    operation_outcome = make_operation_outcome(
        "fatal", "exception", f"{str(exception)}"
    )

    return JSONResponse(
        operation_outcome.dict(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
