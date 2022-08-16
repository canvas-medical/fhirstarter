"""FHIRProvider class, for registering FHIR interactions with a FHIRStarter app."""

from collections.abc import Callable, Iterable, Mapping, Sequence
from typing import Any, Protocol, TypeVar

from fastapi import params
from fhir.resources.resource import Resource

from .interactions import (
    CreateInteraction,
    CreateInteractionHandler,
    InteractionHandler,
    ReadInteraction,
    ReadInteractionHandler,
    ResourceType,
    SearchTypeInteraction,
    SearchTypeInteractionHandler,
    TypeInteraction,
    UpdateInteraction,
    UpdateInteractionHandler,
)

C = TypeVar("C", bound=Callable[..., Any])


class TypeInteractionType(Protocol[ResourceType]):
    @staticmethod
    def __call__(
        resource_type: type[ResourceType],
        handler: InteractionHandler[ResourceType],
        route_options: Mapping[str, Any],
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

    def __init__(self, *, dependencies: Sequence[params.Depends] | None = None) -> None:
        self._dependencies = dependencies or []
        self._interactions: list[TypeInteraction[Resource]] = []

    @property
    def interactions(self) -> Iterable[TypeInteraction[Resource]]:
        yield from self._interactions

    def create(
        self,
        resource_type: type[ResourceType],
        *,
        dependencies: Sequence[params.Depends] | None = None,
        include_in_schema: bool = True
    ) -> Callable[
        [CreateInteractionHandler[ResourceType]],
        CreateInteractionHandler[ResourceType],
    ]:
        """Register a FHIR create interaction."""
        return self._register_type_interaction(
            resource_type,
            CreateInteraction[ResourceType],
            dependencies,
            include_in_schema,
        )

    def read(
        self,
        resource_type: type[ResourceType],
        *,
        dependencies: Sequence[params.Depends] | None = None,
        include_in_schema: bool = True
    ) -> Callable[
        [ReadInteractionHandler[ResourceType]],
        ReadInteractionHandler[ResourceType],
    ]:
        """Register a FHIR read interaction."""
        return self._register_type_interaction(
            resource_type,
            ReadInteraction[ResourceType],
            dependencies,
            include_in_schema,
        )

    def search_type(
        self,
        resource_type: type[ResourceType],
        *,
        dependencies: Sequence[params.Depends] | None = None,
        include_in_schema: bool = True
    ) -> Callable[[SearchTypeInteractionHandler], SearchTypeInteractionHandler]:
        """Register a FHIR search-type interaction."""
        return self._register_type_interaction(
            resource_type,
            SearchTypeInteraction[ResourceType],
            dependencies,
            include_in_schema,
        )

    def update(
        self,
        resource_type: type[ResourceType],
        *,
        dependencies: Sequence[params.Depends] | None = None,
        include_in_schema: bool = True
    ) -> Callable[
        [UpdateInteractionHandler[ResourceType]],
        UpdateInteractionHandler[ResourceType],
    ]:
        """Register a FHIR update interaction."""
        return self._register_type_interaction(
            resource_type,
            UpdateInteraction[ResourceType],
            dependencies,
            include_in_schema,
        )

    def _register_type_interaction(
        self,
        resource_type: type[ResourceType],
        type_interaction_cls: TypeInteractionType[ResourceType],
        dependencies: Sequence[params.Depends] | None,
        include_in_schema: bool,
    ) -> Callable[[C], C]:
        def decorator(handler: C) -> C:
            self._interactions.append(
                type_interaction_cls(
                    resource_type=resource_type,
                    handler=handler,
                    route_options={
                        "dependencies": self._dependencies + list(dependencies or []),
                        "include_in_schema": include_in_schema,
                    },
                )
            )
            return handler

        return decorator
