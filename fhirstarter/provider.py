from collections.abc import Callable, Iterable
from dataclasses import dataclass
from enum import Enum
from functools import cache
from typing import Any, Generic, Protocol, TypeVar

from fhir.resources.bundle import Bundle
from fhir.resources.fhirtypes import Id
from fhir.resources.resource import Resource
from more_itertools import quantify

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
class FHIRInteractionResult(Generic[FHIRResourceType]):
    id_: Id | None = None
    resource: FHIRResourceType | None = None

    def validate(self) -> None:
        assert (
            quantify((self.id_ is None, self.resource is None)) == 1
        ), "One and only one of 'id_' and 'resource' must be specified on a FHIRInteractionResult"


class FHIRCreateInteractionCallable(Protocol[FHIRResourceType]):
    async def __call__(
        self, resource: FHIRResourceType
    ) -> FHIRInteractionResult[FHIRResourceType]:
        ...


class FHIRUpdateInteractionCallable(Protocol[FHIRResourceType]):
    async def __call__(
        self, id_: Id, resource: FHIRResourceType
    ) -> FHIRInteractionResult[FHIRResourceType]:
        ...


class FHIRReadInteractionCallable(Protocol[FHIRResourceType]):
    async def __call__(self, id_: Id) -> FHIRInteractionResult[FHIRResourceType]:
        ...


class FHIRSearchInteractionCallable(Protocol):
    async def __call__(self, **kwargs: str) -> FHIRInteractionResult[Bundle]:
        ...


FHIRInteractionCallable = (
    FHIRCreateInteractionCallable[FHIRResourceType]
    | FHIRUpdateInteractionCallable[FHIRResourceType]
    | FHIRReadInteractionCallable[FHIRResourceType]
    | FHIRSearchInteractionCallable
)


@dataclass(kw_only=True)
class FHIRInteraction(Generic[FHIRResourceType]):
    resource_type: type[FHIRResourceType]
    interaction_type: FHIRInteractionType
    callable_: FHIRInteractionCallable[FHIRResourceType]
    route_options: dict[str, Any]

    def __lt__(self, other: "FHIRInteraction[FHIRResourceType]") -> bool:
        if self.resource_type != other.resource_type:
            return bool(
                self.resource_type.get_resource_type()
                < other.resource_type.get_resource_type()
            )
        return self.interaction_type < other.interaction_type


C = TypeVar("C", bound=Callable[..., Any])


class FHIRProvider:
    def __init__(self) -> None:
        self._interactions: list[FHIRInteraction[Resource]] = []

    @property
    def interactions(self) -> Iterable[FHIRInteraction[Resource]]:
        yield from self._interactions

    def register_create_interaction(
        self, resource_type: type[FHIRResourceType], *, include_in_schema: bool = True
    ) -> Callable[
        [FHIRCreateInteractionCallable[FHIRResourceType]],
        FHIRCreateInteractionCallable[FHIRResourceType],
    ]:
        return self._register_interaction(
            resource_type, FHIRInteractionType.CREATE, include_in_schema
        )

    def register_update_interaction(
        self, resource_type: type[FHIRResourceType], *, include_in_schema: bool = True
    ) -> Callable[
        [FHIRUpdateInteractionCallable[FHIRResourceType]],
        FHIRUpdateInteractionCallable[FHIRResourceType],
    ]:
        return self._register_interaction(
            resource_type, FHIRInteractionType.UPDATE, include_in_schema
        )

    def register_read_interaction(
        self, resource_type: type[FHIRResourceType], *, include_in_schema: bool = True
    ) -> Callable[
        [FHIRReadInteractionCallable[FHIRResourceType]],
        FHIRReadInteractionCallable[FHIRResourceType],
    ]:
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
