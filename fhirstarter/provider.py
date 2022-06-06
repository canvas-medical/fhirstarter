from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum
from functools import cache
from typing import Any, Callable, Generic, Protocol, TypeVar

from fhir.resources.bundle import Bundle
from fhir.resources.fhirtypes import Id
from fhir.resources.resource import Resource

FHIRResourceType = TypeVar("FHIRResourceType", bound=Resource)


class FHIRInteractionType(Enum):
    CREATE = "create"
    UPDATE = "update"
    READ = "read"
    SEARCH = "search"

    @staticmethod
    @cache
    def _order() -> dict[str, int]:
        return {"create": 1, "update": 2, "read": 3, "search": 4}

    def __lt__(self, other: "FHIRInteractionType") -> bool:
        return (
            FHIRInteractionType._order()[self.value]
            < FHIRInteractionType._order()[other.value]
        )


@dataclass(frozen=True, kw_only=True)
class FHIRInteraction(Generic[FHIRResourceType]):
    resource_type: type[FHIRResourceType]
    interaction_type: FHIRInteractionType
    callable_: Callable
    route_options: dict[str, Any]

    def __lt__(self, other: "FHIRInteraction") -> bool:
        if self.resource_type != other.resource_type:
            return (
                self.resource_type.get_resource_type()
                < other.resource_type.get_resource_type()
            )
        return self.interaction_type < other.interaction_type


class FHIRCreateInteractionCallable(Protocol[FHIRResourceType]):
    async def __call__(self, resource: FHIRResourceType) -> FHIRResourceType | None:
        ...


class FHIRUpdateInteractionCallable(Protocol[FHIRResourceType]):
    async def __call__(
        self, id_: Id, resource: FHIRResourceType
    ) -> FHIRResourceType | None:
        ...


class FHIRReadInteractionCallable(Protocol):
    async def __call__(self, id_: Id) -> Resource:
        ...


class FHIRSearchInteractionCallable(Protocol):
    async def __call__(self, **kwargs: str) -> Bundle:
        ...


C = TypeVar("C", bound=Callable)


class FHIRProvider:
    def __init__(self) -> None:
        self._interactions: list[FHIRInteraction] = list()

    @property
    def interactions(self) -> Iterable[FHIRInteraction]:
        yield from self._interactions

    def register_create_interaction(
        self, resource_type: type[FHIRResourceType], *, include_in_schema: bool = True
    ) -> Callable[[FHIRCreateInteractionCallable], FHIRCreateInteractionCallable]:
        return self._register_interaction(
            resource_type, FHIRInteractionType.CREATE, include_in_schema
        )

    def register_update_interaction(
        self, resource_type: type[FHIRResourceType], *, include_in_schema: bool = True
    ) -> Callable[[FHIRUpdateInteractionCallable], FHIRUpdateInteractionCallable]:
        return self._register_interaction(
            resource_type, FHIRInteractionType.UPDATE, include_in_schema
        )

    def register_read_interaction(
        self, resource_type: type[FHIRResourceType], *, include_in_schema: bool = True
    ) -> Callable[[FHIRReadInteractionCallable], FHIRReadInteractionCallable]:
        return self._register_interaction(
            resource_type, FHIRInteractionType.READ, include_in_schema
        )

    def register_search_interaction(
        self, resource_type: type[FHIRResourceType], *, include_in_schema: bool = True
    ) -> Callable[[FHIRSearchInteractionCallable], FHIRSearchInteractionCallable]:
        return self._register_interaction(
            resource_type, FHIRInteractionType.SEARCH, include_in_schema
        )

    def _register_interaction(
        self,
        resource_type: type[FHIRResourceType],
        interaction_type: FHIRInteractionType,
        include_in_schema: bool,
    ) -> Callable[[C], C]:
        def decorator(callable_: C) -> C:
            self._interactions.append(
                FHIRInteraction[FHIRResourceType](
                    resource_type=resource_type,
                    interaction_type=interaction_type,
                    callable_=callable_,
                    route_options={"include_in_schema": include_in_schema},
                )
            )
            return callable_

        return decorator
