"""FHIRProvider class, for registering FHIR interactions with a FHIRStarter app."""

from abc import abstractmethod
from collections.abc import Callable, Iterable
from typing import Any, Generic, Literal, Protocol, TypeVar

from fastapi import Request, Response
from fhir.resources.bundle import Bundle
from fhir.resources.fhirtypes import Id
from fhir.resources.resource import Resource

ResourceType = TypeVar("ResourceType", bound=Resource)


# TODO: Revisit definition of callback protocols and see if it is possible to make Mypy like them
class CreateInteractionCallable(Protocol[ResourceType]):  # type: ignore
    """Callback protocol that defines the signature of a callable for a FHIR create interaction."""

    async def __call__(
        self, resource: ResourceType, *, request: Request, response: Response
    ) -> Id | ResourceType:
        ...


class ReadInteractionCallable(Protocol[ResourceType]):  # type: ignore
    """Callback protocol that defines the signature of a callable for a FHIR read interaction."""

    async def __call__(
        self, id_: Id, *, request: Request, response: Response
    ) -> ResourceType:
        ...


class SearchTypeInteractionCallable(Protocol):
    """
    Callback protocol that defines the signature of a callable for a FHIR search-type interaction.
    """

    async def __call__(
        self, *, request: Request, response: Response, **kwargs: Any
    ) -> Bundle:
        ...


class UpdateInteractionCallable(Protocol[ResourceType]):  # type: ignore
    """Callback protocol that defines the signature of a callable for a FHIR update interaction."""

    async def __call__(
        self, id_: Id, resource: ResourceType, *, request: Request, response: Response
    ) -> Id | ResourceType:
        ...


InteractionCallable = (
    CreateInteractionCallable[ResourceType]
    | ReadInteractionCallable[ResourceType]
    | SearchTypeInteractionCallable
    | UpdateInteractionCallable[ResourceType]
)


class TypeInteraction(Generic[ResourceType]):
    """
    Collection of values that represent a FHIR type interactions. This class can also represent
    instance level interactions.

    resource_type:    The type of FHIR resource on which this interaction operates, as defined by
                      the fhir.resources package.
    callable_:        User-defined function that performs the FHIR interaction.
    route_options:    Dictionary of key-value pairs that are passed on to FastAPI on route creation.
    """

    def __init__(
        self,
        resource_type: type[ResourceType],
        callable_: InteractionCallable[ResourceType],
        route_options: dict[str, Any],
    ):
        self.resource_type = resource_type
        self.callable_ = callable_
        self.route_options = route_options

    @staticmethod
    @abstractmethod
    def label() -> str:
        raise NotImplementedError


class CreateInteraction(TypeInteraction[ResourceType]):
    @staticmethod
    def label() -> Literal["create"]:
        return "create"


class ReadInteraction(TypeInteraction[ResourceType]):
    @staticmethod
    def label() -> Literal["read"]:
        return "read"


class SearchTypeInteraction(TypeInteraction[ResourceType]):
    @staticmethod
    def label() -> Literal["search-type"]:
        return "search-type"


class UpdateInteraction(TypeInteraction[ResourceType]):
    @staticmethod
    def label() -> Literal["update"]:
        return "update"


C = TypeVar("C", bound=Callable[..., Any])


class TypeInteractionType(Protocol[ResourceType]):
    @staticmethod
    def __call__(
        resource_type: type[ResourceType],
        callable_: InteractionCallable[ResourceType],
        route_options: dict[str, Any],
    ) -> TypeInteraction[ResourceType]:
        ...


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
            resource_type, CreateInteraction[ResourceType], include_in_schema
        )

    def register_read_interaction(
        self, resource_type: type[ResourceType], *, include_in_schema: bool = True
    ) -> Callable[
        [ReadInteractionCallable[ResourceType]],
        ReadInteractionCallable[ResourceType],
    ]:
        """Register a FHIR read interaction."""
        return self._register_type_interaction(
            resource_type, ReadInteraction[ResourceType], include_in_schema
        )

    def register_search_type_interaction(
        self, resource_type: type[ResourceType], *, include_in_schema: bool = True
    ) -> Callable[[SearchTypeInteractionCallable], SearchTypeInteractionCallable]:
        """Register a FHIR search-type interaction."""
        return self._register_type_interaction(
            resource_type, SearchTypeInteraction[ResourceType], include_in_schema
        )

    def register_update_interaction(
        self, resource_type: type[ResourceType], *, include_in_schema: bool = True
    ) -> Callable[
        [UpdateInteractionCallable[ResourceType]],
        UpdateInteractionCallable[ResourceType],
    ]:
        """Register a FHIR update interaction."""
        return self._register_type_interaction(
            resource_type, UpdateInteraction[ResourceType], include_in_schema
        )

    def _register_type_interaction(
        self,
        resource_type: type[ResourceType],
        type_interaction_cls: TypeInteractionType[ResourceType],
        include_in_schema: bool,
    ) -> Callable[[C], C]:
        def decorator(callable_: C) -> C:
            self._interactions.append(
                type_interaction_cls(
                    resource_type=resource_type,
                    callable_=callable_,
                    route_options={"include_in_schema": include_in_schema},
                )
            )
            return callable_

        return decorator
