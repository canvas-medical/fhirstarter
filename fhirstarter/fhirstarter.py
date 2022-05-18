from collections.abc import Iterable
from types import FunctionType
from typing import Any, cast

from fastapi import FastAPI, Path, status

from fhirstarter import routes
from fhirstarter.provider import (FHIRProvider, FHIRResourceType,
                                  SupportsFHIRCreate, SupportsFHIRRead,
                                  SupportsFHIRSearch, SupportsFHIRUpdate)


class FHIRStarter(FastAPI):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self._providers = dict()

    def add_providers(self, *providers: FHIRProvider):
        for provider in providers:
            resource_type = provider.resource_type()
            assert (
                resource_type not in self._providers
            ), f"FHIR provider for resource type '{resource_type}' can only be supplied once"

            self._providers[resource_type] = provider
            self._add_routes(provider)

    async def dispatch(
        self, resource_type: str, operation: str, /, **kwargs: Any
    ) -> FHIRResourceType | tuple[FHIRResourceType, ...]:
        # TODO: Return a proper HTTP response if a provider is not found (should be detectable by
        #  declared capabilities)
        provider = self._providers.get(resource_type)
        assert (
            provider
        ), f"FHIR provider for resource type '{resource_type}' does not exist"

        match operation:
            case "create":
                provider = cast(SupportsFHIRCreate, provider)
                return await provider.create(kwargs["resource"])
            case "read":
                provider = cast(SupportsFHIRRead, provider)
                return await provider.read(kwargs["id_"])
            case "search":
                provider = cast(SupportsFHIRSearch, provider)
                return await provider.search(**kwargs)
            case "update":
                provider = cast(SupportsFHIRUpdate, provider)
                return await provider.update(kwargs["resource"])

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
        annotations = {"id_": str}
        argdefs = (Path(None, alias="id", min_length=1),)
        code = getattr(routes, "read").__code__
        globals_ = {"dispatch": self.dispatch, "resource_type": resource_type}

        func = FunctionType(code, globals_, name, argdefs)
        func.__annotations__ = annotations

        self.get(
            f"/{resource_type}/{{id}}",
            response_model=resource_obj_type,
            status_code=status.HTTP_200_OK,
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
