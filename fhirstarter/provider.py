import inspect
from abc import abstractmethod
from typing import Protocol, TypeVar, runtime_checkable

from fhir.resources.resource import Resource

FHIRResourceType = TypeVar("FHIRResourceType", bound=Resource)


class FHIRProvider:
    @staticmethod
    @abstractmethod
    def resource_obj_type() -> type[FHIRResourceType]:
        raise NotImplementedError

    @property
    def resource_type(self) -> str:
        return self.resource_obj_type().get_resource_type()

    @property
    def supported_search_parameters(self) -> tuple[str, ...]:
        if not isinstance(self, SupportsFHIRSearch):
            return tuple()

        return tuple(sorted(inspect.signature(self.search).parameters.keys()))


# TODO: To handle errors, the methods on these protocols probably need to return more than just a
#  FHIRResourceType


@runtime_checkable
class SupportsFHIRCreate(Protocol[FHIRResourceType]):
    @staticmethod
    def create() -> FHIRResourceType:
        ...


@runtime_checkable
class SupportsFHIRRead(Protocol[FHIRResourceType]):
    @staticmethod
    def read() -> FHIRResourceType:
        ...


@runtime_checkable
class SupportsFHIRSearch(Protocol[FHIRResourceType]):
    # TODO: Might need to return a bundle or generic bundle wrapper
    @staticmethod
    def search(**kwargs) -> tuple[FHIRResourceType, ...]:
        ...


@runtime_checkable
class SupportsUpdate(Protocol[FHIRResourceType]):
    @staticmethod
    def update() -> FHIRResourceType:
        ...
