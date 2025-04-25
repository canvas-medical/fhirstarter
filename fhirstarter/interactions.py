"""Classes and types for handling and representing FHIR Interactions."""

from abc import abstractmethod
from dataclasses import dataclass
from typing import (
    Any,
    Callable,
    Coroutine,
    Generic,
    Literal,
    Mapping,
    Type,
    TypeVar,
    Union,
)

from fastapi import Request, Response

from .json_patch import JSONPatch
from .resources import Bundle, Resource

ResourceType = TypeVar("ResourceType", bound=Resource)


@dataclass
class InteractionContext:
    request: Request
    response: Response


ReadInteractionHandler = Callable[
    [InteractionContext, str], Union[Coroutine[None, None, ResourceType], ResourceType]
]
UpdateInteractionHandler = Callable[
    [InteractionContext, str, ResourceType],
    Union[Coroutine[None, None, Union[str, ResourceType]], str, ResourceType],
]
PatchInteractionHandler = Callable[
    [InteractionContext, str, JSONPatch],
    Union[Coroutine[None, None, Union[str, ResourceType]], str, ResourceType],
]
DeleteInteractionHandler = Callable[
    [InteractionContext, str],
    Union[Coroutine[None, None, None], None],
]
CreateInteractionHandler = Callable[
    [InteractionContext, ResourceType],
    Union[Coroutine[None, None, Union[str, ResourceType]], str, ResourceType],
]
SearchTypeInteractionHandler = Callable[
    ..., Union[Coroutine[None, None, Bundle], Bundle]
]

InteractionHandler = Union[
    ReadInteractionHandler[ResourceType],
    PatchInteractionHandler[ResourceType],
    DeleteInteractionHandler,
    UpdateInteractionHandler[ResourceType],
    CreateInteractionHandler[ResourceType],
    SearchTypeInteractionHandler,
]


class TypeInteraction(Generic[ResourceType]):
    """
    Collection of values that represent a FHIR type interaction. This class can also represent
    instance level interactions.

    resource_type:    The type of FHIR resource on which this interaction operates, as defined by
                      the fhir.resources package.
    handler:          User-defined function that performs the FHIR interaction.
    route_options:    Dictionary of key-value pairs that are passed on to FastAPI on route creation.
    """

    def __init__(
        self,
        resource_type: Type[ResourceType],
        handler: InteractionHandler[ResourceType],
        route_options: Mapping[str, Any],
    ):
        self.resource_type = resource_type
        self.handler = handler
        self.route_options = route_options

    @staticmethod
    @abstractmethod
    def label() -> str:
        raise NotImplementedError


class ReadInteraction(TypeInteraction[ResourceType]):
    @staticmethod
    def label() -> Literal["read"]:
        return "read"


class UpdateInteraction(TypeInteraction[ResourceType]):
    @staticmethod
    def label() -> Literal["update"]:
        return "update"


class PatchInteraction(TypeInteraction[ResourceType]):
    @staticmethod
    def label() -> Literal["patch"]:
        return "patch"


class DeleteInteraction(TypeInteraction[ResourceType]):
    @staticmethod
    def label() -> Literal["delete"]:
        return "delete"


class CreateInteraction(TypeInteraction[ResourceType]):
    @staticmethod
    def label() -> Literal["create"]:
        return "create"


class SearchTypeInteraction(TypeInteraction[ResourceType]):
    @staticmethod
    def label() -> Literal["search-type"]:
        return "search-type"
