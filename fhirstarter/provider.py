from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Generic, Protocol, TypeVar

from fhir.resources.bundle import Bundle
from fhir.resources.resource import Resource

FHIRResourceType = TypeVar("FHIRResourceType", bound=Resource)


class FHIRInteractionType(Enum):
    CREATE = "create"
    READ = "read"
    SEARCH = "search"
    UPDATE = "update"


@dataclass(frozen=True, kw_only=True)
class FHIRInteraction(Generic[FHIRResourceType]):
    resource_type: type[FHIRResourceType]
    interaction_type: FHIRInteractionType
    callable_: Callable
    route_options: dict[str, Any]


class FHIRCreateInteractionCallable(Protocol[FHIRResourceType]):
    async def __call__(self, resource: FHIRResourceType) -> FHIRResourceType | None:
        ...


class FHIRReadInteractionCallable(Protocol):
    async def __call__(self, id_: str) -> Resource:
        ...


class FHIRSearchInteractionCallable(Protocol):
    async def __call__(self, **kwargs: str) -> Bundle:
        ...


class FHIRUpdateInteractionCallable(Protocol[FHIRResourceType]):
    async def __call__(self, resource: FHIRResourceType) -> FHIRResourceType | None:
        ...


C = TypeVar("C", bound=Callable)


class FHIRProvider:
    def __init__(self) -> None:
        self._interactions: list[FHIRInteraction] = list()

    @property
    def interactions(self) -> list[FHIRInteraction]:
        return self._interactions

    def register_create_interaction(
        self, resource_type: type[FHIRResourceType]
    ) -> Callable[[FHIRCreateInteractionCallable], FHIRCreateInteractionCallable]:
        return self._register_interaction(resource_type, FHIRInteractionType.CREATE)

    def register_read_interaction(
        self, resource_type: type[FHIRResourceType]
    ) -> Callable[[FHIRReadInteractionCallable], FHIRReadInteractionCallable]:
        return self._register_interaction(resource_type, FHIRInteractionType.READ)

    def register_search_interaction(
        self, resource_type: type[FHIRResourceType]
    ) -> Callable[[FHIRSearchInteractionCallable], FHIRSearchInteractionCallable]:
        return self._register_interaction(resource_type, FHIRInteractionType.SEARCH)

    def register_update_interaction(
        self, resource_type: type[FHIRResourceType]
    ) -> Callable[[FHIRUpdateInteractionCallable], FHIRUpdateInteractionCallable]:
        return self._register_interaction(resource_type, FHIRInteractionType.UPDATE)

    def _register_interaction(
        self,
        resource_type: type[FHIRResourceType],
        interaction_type: FHIRInteractionType,
        *,
        include_in_schema: bool = True
    ) -> Callable[[C], C]:
        # TODO: Validate function signature?
        # TODO: Prevent duplicate registration (but not here)
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
