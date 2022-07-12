"""FHIRProvider class, for registering FHIR interactions with a FHIRStarter app."""

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from enum import Enum
from typing import Any, Generic, Protocol, TypeVar

from fhir.resources.bundle import Bundle
from fhir.resources.fhirtypes import Id
from fhir.resources.resource import Resource

ResourceType = TypeVar("ResourceType", bound=Resource)


class InteractionType(Enum):
    """Enum class to specify supported FHIR interaction types."""

    CREATE = "create"
    READ = "read"
    SEARCH_TYPE = "search-type"
    UPDATE = "update"

    def __lt__(self, other: "InteractionType") -> bool:
        return self.value < other.value


# TODO: Revisit definition of callback protocols and see if it is possible to make Mypy like them
class CreateInteractionCallable(Protocol[ResourceType]):  # type: ignore
    """Callback protocol that defines the signature of a callable for a FHIR create interaction."""

    async def __call__(
        self, resource: ResourceType, **kwargs: str
    ) -> Id | ResourceType:
        ...


class ReadInteractionCallable(Protocol[ResourceType]):  # type: ignore
    """Callback protocol that defines the signature of a callable for a FHIR read interaction."""

    async def __call__(self, id_: Id, **kwargs: str) -> ResourceType:
        ...


class SearchTypeInteractionCallable(Protocol):
    """
    Callback protocol that defines the signature of a callable for a FHIR search-type interaction.
    """

    async def __call__(self, **kwargs: str) -> Bundle:
        ...


class UpdateInteractionCallable(Protocol[ResourceType]):  # type: ignore
    """Callback protocol that defines the signature of a callable for a FHIR update interaction."""

    async def __call__(
        self, id_: Id, resource: ResourceType, **kwargs: str
    ) -> Id | ResourceType:
        ...


InteractionCallable = (
    CreateInteractionCallable[ResourceType]
    | ReadInteractionCallable[ResourceType]
    | SearchTypeInteractionCallable
    | UpdateInteractionCallable[ResourceType]
)


@dataclass(kw_only=True)
class TypeInteraction(Generic[ResourceType]):
    """
    Collection of values that represent a FHIR type interactions. This class can also represent
    instance level interactions.

    resource_type:    The type of FHIR resource on which this interaction operates, as defined by
                      the fhir.resources package.
    interaction_type: The type of FHIR interaction, such as create, read, search-type, or update.
    callable_:        User-defined function that performs the FHIR interaction.
    route_options:    Dictionary of key-value pairs that are passed on to FastAPI on route creation.
    """

    resource_type: type[ResourceType]
    interaction_type: InteractionType
    callable_: InteractionCallable[ResourceType]
    route_options: dict[str, Any]

    def __lt__(self, other: "TypeInteraction[ResourceType]") -> bool:
        if self.resource_type != other.resource_type:
            return bool(
                self.resource_type.get_resource_type()
                < other.resource_type.get_resource_type()
            )
        return self.interaction_type < other.interaction_type


C = TypeVar("C", bound=Callable[..., Any])


class FHIRProvider:
    """
    Class that contains a collection of FHIR interactions to be added to a FHIRStarter app. These
    interactions are added as API routes.

    Aside from instantiation, interaction with this class is performed solely through the register
    decorators, e.g. register_read_interaction. One must use these decorators to decorate
    functions that perform FHIR interactions.
    """

    def __init__(self) -> None:
        self._interactions: list[TypeInteraction[Resource]] = []

    @property
    def interactions(self) -> Iterable[TypeInteraction[Resource]]:
        yield from self._interactions

    def register_create_interaction(
        self, resource_type: type[ResourceType], *, include_in_schema: bool = True
    ) -> Callable[
        [CreateInteractionCallable[ResourceType]],
        CreateInteractionCallable[ResourceType],
    ]:
        """Register a FHIR create interaction."""
        return self._register_type_interaction(
            resource_type, InteractionType.CREATE, include_in_schema
        )

    def register_read_interaction(
        self, resource_type: type[ResourceType], *, include_in_schema: bool = True
    ) -> Callable[
        [ReadInteractionCallable[ResourceType]],
        ReadInteractionCallable[ResourceType],
    ]:
        """Register a FHIR read interaction."""
        return self._register_type_interaction(
            resource_type, InteractionType.READ, include_in_schema
        )

    def register_search_type_interaction(
        self, resource_type: type[ResourceType], *, include_in_schema: bool = True
    ) -> Callable[[SearchTypeInteractionCallable], SearchTypeInteractionCallable]:
        """Register a FHIR search-type interaction."""
        return self._register_type_interaction(
            resource_type, InteractionType.SEARCH_TYPE, include_in_schema
        )

    def register_update_interaction(
        self, resource_type: type[ResourceType], *, include_in_schema: bool = True
    ) -> Callable[
        [UpdateInteractionCallable[ResourceType]],
        UpdateInteractionCallable[ResourceType],
    ]:
        """Register a FHIR update interaction."""
        return self._register_type_interaction(
            resource_type, InteractionType.UPDATE, include_in_schema
        )

    def _register_type_interaction(
        self,
        resource_type: type[ResourceType],
        interaction_type: InteractionType,
        include_in_schema: bool,
    ) -> Callable[[C], C]:
        def decorator(callable_: C) -> C:
            self._interactions.append(
                TypeInteraction[ResourceType](
                    resource_type=resource_type,
                    interaction_type=interaction_type,
                    callable_=callable_,
                    route_options={"include_in_schema": include_in_schema},
                )
            )
            return callable_

        return decorator
