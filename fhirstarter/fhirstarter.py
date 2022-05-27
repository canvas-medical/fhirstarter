from collections.abc import Iterable
from types import FunctionType
from typing import Any

from fastapi import FastAPI, Path, Request, status
from fastapi.responses import JSONResponse
from fhir.resources.fhirtypes import Id
from fhir.resources.operationoutcome import OperationOutcome
from fhir.resources.resource import Resource

from fhirstarter import routes
from fhirstarter.exceptions import (
    FHIRError,
    FHIRException,
    FHIRExceptionContext,
    make_operation_outcome,
)
from fhirstarter.provider import (
    FHIRProvider,
    FHIRResourceType,
    SupportsFHIRCreate,
    SupportsFHIRRead,
    SupportsFHIRSearch,
    SupportsFHIRUpdate,
)


class FHIRStarter(FastAPI):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.add_exception_handler(Exception, _exception_handler)
        self._providers = dict()

    def add_providers(self, *providers: FHIRProvider) -> None:
        for provider in providers:
            resource_type = provider.resource_type()
            assert (
                resource_type not in self._providers
            ), f"FHIR provider for resource type '{resource_type}' can only be supplied once"

            self._providers[resource_type] = provider
            self._add_routes(provider)

    async def dispatch(
        self, resource_type: str, operation: str, /, **kwargs: Any
    ) -> FHIRResourceType | JSONResponse:
        try:
            provider = self._providers[resource_type]
        except KeyError as error:
            raise FHIRError(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "fatal",
                "not-supported",
                "Server is improperly configured; request dispatched to nonexistent provider",
            ) from error

        try:
            return await provider.dispatch(operation, **kwargs)
        except FHIRException as exception:
            return exception.response(FHIRExceptionContext(provider, operation, kwargs))

    def _add_routes(self, provider: FHIRProvider) -> None:
        # TODO: Try to find a better way to model the ABC and protocols so that these three values
        #  don't need to be fetched prior to the calls to isinstance to avoid typing errors
        resource_type = provider.resource_type()
        resource_obj_type = provider.resource_obj_type()

        if isinstance(provider, SupportsFHIRCreate):
            self._add_create_route(resource_obj_type, resource_type)
        if isinstance(provider, SupportsFHIRRead):
            self._add_read_route(resource_obj_type, resource_type)
        if isinstance(provider, SupportsFHIRSearch):
            self._add_search_route(
                resource_obj_type, resource_type, provider.supported_search_parameters()
            )
        if isinstance(provider, SupportsFHIRUpdate):
            self._add_update_route(resource_obj_type, resource_type)

    def _add_create_route(
        self, resource_obj_type: type[FHIRResourceType], resource_type: str
    ) -> None:
        raise NotImplementedError

    def _add_read_route(
        self, resource_obj_type: type[FHIRResourceType], resource_type: str
    ) -> None:
        name = f"{resource_type.lower()}_read"
        annotations = {"id_": Id}
        argdefs = (
            Path(
                None,
                alias="id",
                description=Resource.schema()["properties"]["id"]["title"],
            ),
        )
        code = getattr(routes, "read").__code__
        globals_ = {"dispatch": self.dispatch, "resource_type": resource_type}

        func = FunctionType(code, globals_, name, argdefs)
        func.__annotations__ = annotations

        self.get(
            f"/{resource_type}/{{id}}",
            response_model=resource_obj_type,
            summary=f"{resource_type} read",
            description=f"The {resource_type} read interaction accesses "
            f"the current contents of a {resource_type}.",
            responses={
                status.HTTP_200_OK: {
                    "description": f"Successful {resource_type} read",
                    "content": {
                        "application/json": {"schema": resource_obj_type.schema()},
                        "application/fhir+json": {"schema": resource_obj_type.schema()},
                    },
                },
                status.HTTP_404_NOT_FOUND: {
                    "description": f"Unknown {resource_type} resource",
                    "content": {
                        "application/json": {"schema": OperationOutcome.schema()},
                        "application/fhir+json": {"schema": OperationOutcome.schema()},
                    },
                },
            },
            response_model_exclude_none=True,
        )(func)

    def _add_search_route(
        self,
        resource_obj_type: type[FHIRResourceType],
        resource_type: str,
        supported_search_parameters: Iterable[str],
    ) -> None:
        raise NotImplementedError

    def _add_update_route(
        self, resource_obj_type: type[FHIRResourceType], resource_type: str
    ) -> None:
        raise NotImplementedError


async def _exception_handler(_: Request, exception: Exception) -> JSONResponse:
    operation_outcome = make_operation_outcome(
        "fatal", "exception", f"{str(exception)}"
    )

    return JSONResponse(
        operation_outcome.dict(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


# TODO: Look into auto-filling path and query parameter options from the FHIR specification
# TODO: Look into auto-filling path definition parameters with data from the FHIR specification
# TODO: Review all of the path definition parameters
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
