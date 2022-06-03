from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Generic, Protocol, TypeVar

from fhir.resources.bundle import Bundle
from fhir.resources.resource import Resource

FHIRResourceType = TypeVar("FHIRResourceType", bound=Resource)


class FHIRInteractionType(Enum):
    CREATE = "create"
    READ = "read"
    SEARCH_TYPE = "search-type"
    UPDATE = "update"


@dataclass(frozen=True, kw_only=True)
class FHIRInteraction(Generic[FHIRResourceType]):
    resource_type: type[FHIRResourceType]
    interaction_type: FHIRInteractionType
    callable_: Callable
    _route_options: tuple[tuple[str, Any], ...]

    @property
    def route_options(self) -> dict[str, Any]:
        return dict(self._route_options)


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


class FHIRProvider:
    def __init__(self) -> None:
        self._interactions: list[FHIRInteraction] = list()

    def register_read_interaction(
        self, resource_type: type[FHIRResourceType], *, include_in_schema=True
    ) -> Callable[[FHIRReadInteractionCallable], FHIRReadInteractionCallable]:
        # TODO: Validate function signature?
        # TODO: Prevent duplicate registration (but not here)
        def decorator(
            callable_: FHIRReadInteractionCallable,
        ) -> FHIRReadInteractionCallable:
            self._interactions.append(
                FHIRInteraction[FHIRResourceType](
                    resource_type=resource_type,
                    interaction_type=FHIRInteractionType.READ,
                    callable_=callable_,
                    _route_options=(("include_in_schema", include_in_schema),),
                )
            )
            return callable_

        return decorator

    @property
    def interactions(self) -> list[FHIRInteraction]:
        return self._interactions
