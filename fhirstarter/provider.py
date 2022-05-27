import functools
from abc import abstractmethod
from collections.abc import Callable
from typing import Any, Protocol, TypeVar, cast, runtime_checkable

from fhir.resources.bundle import Bundle
from fhir.resources.resource import Resource

FHIRResourceType = TypeVar("FHIRResourceType", bound=Resource)


class FHIRProvider:
    @abstractmethod
    def resource_obj_type(self) -> type[FHIRResourceType]:
        raise NotImplementedError

    def resource_type(self) -> str:
        return self.resource_obj_type().get_resource_type()

    async def dispatch(self, operation: str, /, **kwargs: Any) -> FHIRResourceType:
        match operation:
            case "create":
                return await cast(SupportsFHIRCreate, self).create(kwargs["resource"])
            case "read":
                return await cast(SupportsFHIRRead, self).read(kwargs["id_"])
            case "search":
                return await cast(SupportsFHIRSearch, self).search(**kwargs)
            case "update":
                return await cast(SupportsFHIRUpdate, self).update(kwargs["resource"])


def route_options(include_in_schema: bool = True) -> Callable[..., Any]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)

        wrapper.route_options = {"include_in_schema": include_in_schema}
        return wrapper

    return decorator


@runtime_checkable
class SupportsFHIRCreate(Protocol[FHIRResourceType]):
    @staticmethod
    async def create(resource: FHIRResourceType) -> FHIRResourceType | None:
        ...


@runtime_checkable
class SupportsFHIRRead(Protocol[FHIRResourceType]):
    @staticmethod
    async def read(id_: str) -> FHIRResourceType:
        ...


@runtime_checkable
class SupportsFHIRSearch(Protocol[FHIRResourceType]):
    @staticmethod
    async def search(**kwargs: str) -> Bundle:
        ...


@runtime_checkable
class SupportsFHIRUpdate(Protocol[FHIRResourceType]):
    @staticmethod
    async def update(resource: FHIRResourceType) -> FHIRResourceType | None:
        ...
