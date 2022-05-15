from collections.abc import Callable, Iterable
from types import CodeType, FunctionType
from typing import Any, cast

from fastapi import FastAPI, status

from fhirstarter.provider import (FHIRProvider, FHIRResourceType,
                                  SupportsFHIRCreate, SupportsFHIRRead,
                                  SupportsFHIRSearch, SupportsFHIRUpdate)


class FHIRStarter(FastAPI):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self._providers = dict()

    def add_providers(self, *providers: FHIRProvider):
        for provider in providers:
            resource_type = provider.resource_type
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
        resource_type = provider.resource_type
        resource_obj_type = provider.resource_obj_type
        supported_search_parameters = provider.supported_search_parameters

        if isinstance(provider, SupportsFHIRCreate):
            self._add_create_route(resource_obj_type, resource_type)
        if isinstance(provider, SupportsFHIRRead):
            self._add_read_route(resource_obj_type, resource_type)
        if isinstance(provider, SupportsFHIRSearch):
            self._add_search_route(
                resource_obj_type, resource_type, supported_search_parameters
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
        func_name = f"{resource_type.lower()}_read"

        code = f"""
async def {func_name}(id_: str) -> {resource_type}:
    result = await app.dispatch("{resource_type}", "read", id_=id_)
    return result"""

        annotations = {"id_": str}
        globals_ = {
            "app": self,
            resource_type: resource_obj_type,
        }

        func = _create_function(func_name, code, annotations, globals_)

        self.get(
            f"/{resource_type}/{{id_}}",
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


# TODO: It should be possible to dynamically add routes and avoid using the compile builtin by
#  generating the routes beforehand and then tweaking the globals and defaults before the routes
#  are added. The include_in_schema flag on search parameters can be set this way.
def _create_function(
    name: str, code: str, annotations: dict[str, Any], globals_: dict[str, Any]
) -> Callable:
    # TODO: Get a security review of use of the compile built-in
    code_compiled = compile(code, "<string", "exec")
    func_code = next(c for c in code_compiled.co_consts if isinstance(c, CodeType))
    func = FunctionType(func_code, globals_, name)
    func.__annotations__ = annotations

    return func


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
