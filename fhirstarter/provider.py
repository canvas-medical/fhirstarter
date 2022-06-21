from collections.abc import Callable, Iterable
from dataclasses import dataclass
from enum import Enum
from typing import Any, Generic, Protocol, TypeVar

from fhir.resources.bundle import Bundle
from fhir.resources.fhirtypes import Id
from fhir.resources.resource import Resource

FHIRResourceType = TypeVar("FHIRResourceType", bound=Resource)


class FHIRInteractionType(Enum):
    CREATE = "create"
    READ = "read"
    SEARCH = "search"
    UPDATE = "update"

    def __lt__(self, other: "FHIRInteractionType") -> bool:
        return self.value < other.value


class FHIRCreateInteractionCallable(Protocol[FHIRResourceType]):  # type: ignore
    async def __call__(
        self, resource: FHIRResourceType, **kwargs: str
    ) -> Id | FHIRResourceType:
        ...


class FHIRReadInteractionCallable(Protocol[FHIRResourceType]):  # type: ignore
    async def __call__(self, id_: Id, **kwargs: str) -> FHIRResourceType:
        ...


class FHIRSearchInteractionCallable(Protocol):
    async def __call__(self, **kwargs: str) -> Bundle:
        ...


class FHIRUpdateInteractionCallable(Protocol[FHIRResourceType]):  # type: ignore
    async def __call__(
        self, id_: Id, resource: FHIRResourceType, **kwargs: str
    ) -> Id | FHIRResourceType:
        ...


FHIRInteractionCallable = (
    FHIRCreateInteractionCallable[FHIRResourceType]
    | FHIRReadInteractionCallable[FHIRResourceType]
    | FHIRSearchInteractionCallable
    | FHIRUpdateInteractionCallable[FHIRResourceType]
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

    def register_update_interaction(
        self, resource_type: type[FHIRResourceType], *, include_in_schema: bool = True
    ) -> Callable[
        [FHIRUpdateInteractionCallable[FHIRResourceType]],
        FHIRUpdateInteractionCallable[FHIRResourceType],
    ]:
        return self._register_interaction(
            resource_type, FHIRInteractionType.UPDATE, include_in_schema
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
