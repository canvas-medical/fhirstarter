"""FHIRProvider class, for registering FHIR interactions with a FHIRStarter app."""

from typing import (
    Any,
    Callable,
    Iterable,
    List,
    Mapping,
    Protocol,
    Sequence,
    Type,
    TypeVar,
    Union,
)

from fastapi import params

from .fhir_specification import FHIR_SEQUENCE
from .interactions import (
    CreateInteraction,
    CreateInteractionHandler,
    DeleteInteraction,
    DeleteInteractionHandler,
    InteractionHandler,
    PatchInteraction,
    PatchInteractionHandler,
    ReadInteraction,
    ReadInteractionHandler,
    ResourceType,
    SearchTypeInteraction,
    SearchTypeInteractionHandler,
    TypeInteraction,
    UpdateInteraction,
    UpdateInteractionHandler,
)
from .resources import Resource

C = TypeVar("C", bound=Callable[..., Any])


class TypeInteractionType(Protocol[ResourceType]):
    @staticmethod
    def __call__(
        resource_type: Type[ResourceType],
        handler: InteractionHandler[ResourceType],
        route_options: Mapping[str, Any],
    ) -> TypeInteraction[ResourceType]: ...


class FHIRProvider:
    """
    Class that contains a collection of FHIR interactions to be added to a FHIRStarter app. These
    interactions are added as API routes.

    Aside from instantiation, interaction with this class is performed solely through the register
    decorators, e.g. register_read_interaction. One must use these decorators to decorate
    functions that perform FHIR interactions.
    """

    def __init__(
        self, *, dependencies: Union[Sequence[params.Depends], None] = None
    ) -> None:
        self._dependencies = dependencies or []
        self._interactions: List[TypeInteraction[Resource]] = []

    @property
    def interactions(self) -> Iterable[TypeInteraction[Resource]]:
        yield from self._interactions

    def read(
        self,
        resource_type: Type[ResourceType],
        *,
        dependencies: Union[Sequence[params.Depends], None] = None,
        include_in_schema: bool = True,
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

    def update(
        self,
        resource_type: Type[ResourceType],
        *,
        dependencies: Union[Sequence[params.Depends], None] = None,
        include_in_schema: bool = True,
    ) -> Callable[
        [UpdateInteractionHandler[ResourceType]], UpdateInteractionHandler[ResourceType]
    ]:
        """Register a FHIR update interaction."""
        return self._register_type_interaction(
            resource_type,
            UpdateInteraction[ResourceType],
            dependencies,
            include_in_schema,
        )

    def patch(
        self,
        resource_type: Type[ResourceType],
        *,
        dependencies: Union[Sequence[params.Depends], None] = None,
        include_in_schema: bool = True,
    ) -> Callable[
        [PatchInteractionHandler[ResourceType]], PatchInteractionHandler[ResourceType]
    ]:
        """Register a FHIR patch interaction."""
        return self._register_type_interaction(
            resource_type,
            PatchInteraction[ResourceType],
            dependencies,
            include_in_schema,
        )

    def delete(
        self,
        resource_type: Type[ResourceType],
        *,
        dependencies: Union[Sequence[params.Depends], None] = None,
        include_in_schema: bool = True,
    ) -> Callable[[DeleteInteractionHandler], DeleteInteractionHandler]:
        """Register a FHIR delete interaction."""
        return self._register_type_interaction(
            resource_type,
            DeleteInteraction[ResourceType],
            dependencies,
            include_in_schema,
        )

    def create(
        self,
        resource_type: Type[ResourceType],
        *,
        dependencies: Union[Sequence[params.Depends], None] = None,
        include_in_schema: bool = True,
    ) -> Callable[
        [CreateInteractionHandler[ResourceType]], CreateInteractionHandler[ResourceType]
    ]:
        """Register a FHIR create interaction."""
        return self._register_type_interaction(
            resource_type,
            CreateInteraction[ResourceType],
            dependencies,
            include_in_schema,
        )

    def search_type(
        self,
        resource_type: Type[ResourceType],
        *,
        dependencies: Union[Sequence[params.Depends], None] = None,
        include_in_schema: bool = True,
    ) -> Callable[[SearchTypeInteractionHandler], SearchTypeInteractionHandler]:
        """Register a FHIR search-type interaction."""
        return self._register_type_interaction(
            resource_type,
            SearchTypeInteraction[ResourceType],
            dependencies,
            include_in_schema,
        )

    def _register_type_interaction(
        self,
        resource_type: Type[ResourceType],
        type_interaction_cls: TypeInteractionType[ResourceType],
        dependencies: Union[Sequence[params.Depends], None],
        include_in_schema: bool,
    ) -> Callable[[C], C]:
        _check_resource_type_module(resource_type)

        def decorator(handler: C) -> C:
            self._interactions.append(
                type_interaction_cls(
                    resource_type=resource_type,
                    handler=handler,
                    route_options={
                        "dependencies": (*self._dependencies, *(dependencies or ())),
                        "include_in_schema": include_in_schema,
                    },
                )
            )
            return handler

        return decorator


def _check_resource_type_module(resource_type: Type[Resource]) -> None:
    """Ensure that the resource type is compatible with the server's defined FHIR sequence."""

    # Get the module name of the resource's fhir.resources parent class. If a user is using a model
    # with custom examples, then their model will inherit from something that this code will
    # recognize.
    #
    # Note: This limitation currently disallows a deeper inheritance hierarchy.
    module = ""
    bases = resource_type.__bases__
    for base in bases:
        if base.__module__.startswith("fhir.resources"):
            module = base.__module__
    assert (
        module
    ), f"Unable to determine FHIR sequence of resource {resource_type.get_resource_type()}"

    if FHIR_SEQUENCE in ("R4", "R4"):
        assert not module.startswith(
            ("fhir.resources.STU3", "fhir.resources.R4B")
        ), f"Resource types from {module} cannot be used with FHIR sequence {FHIR_SEQUENCE}"
    elif FHIR_SEQUENCE == "STU3":
        assert module.startswith(
            "fhir.resources.STU3"
        ), "Only resource types from fhir.resources.STU3 can be used with FHIR sequence STU3"
    elif FHIR_SEQUENCE == "R4B":
        assert module.startswith(
            "fhir.resources.R4B"
        ), "Only resource types from fhir.resources.R4B can be used with FHIR sequence R4B"
