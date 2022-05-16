import inspect
from abc import abstractmethod
from typing import Protocol, TypeVar, runtime_checkable

from fhir.resources.resource import Resource

FHIRResourceType = TypeVar("FHIRResourceType", bound=Resource)


class FHIRProvider:
    @abstractmethod
    def resource_obj_type(self) -> type[FHIRResourceType]:
        raise NotImplementedError

    def resource_type(self) -> str:
        return self.resource_obj_type().get_resource_type()

    def supported_search_parameters(self) -> tuple[str, ...] | None:
        if not isinstance(self, SupportsFHIRSearch):
            return None

        return tuple(sorted(inspect.signature(self.search).parameters.keys()))


# TODO: To handle errors, the methods on these protocols probably need to return more than just a
#  FHIRResourceType


@runtime_checkable
class SupportsFHIRCreate(Protocol[FHIRResourceType]):
    @staticmethod
    async def create(resource: FHIRResourceType) -> FHIRResourceType:
        ...


@runtime_checkable
class SupportsFHIRRead(Protocol[FHIRResourceType]):
    @staticmethod
    async def read(id_: str) -> FHIRResourceType:
        ...


@runtime_checkable
class SupportsFHIRSearch(Protocol[FHIRResourceType]):
    def supported_search_parameters(self) -> tuple[str, ...] | None:
        ...

    # TODO: Might need to return a bundle or generic bundle wrapper
    @staticmethod
    async def search(**kwargs: str) -> tuple[FHIRResourceType, ...]:
        ...


@runtime_checkable
class SupportsFHIRUpdate(Protocol[FHIRResourceType]):
    @staticmethod
    async def update(resource: FHIRResourceType) -> FHIRResourceType:
        ...
