"""Classes and types for handling and representing FHIR Interactions."""

from abc import abstractmethod
from collections.abc import Callable, Coroutine, Mapping
from dataclasses import dataclass
from typing import Any, Generic, Literal, TypeVar

from fastapi import Request, Response

from .resources import Bundle, Id, Resource

ResourceType = TypeVar("ResourceType", bound=Resource)


@dataclass
class InteractionContext:
    request: Request
    response: Response


CreateInteractionHandler = Callable[
    [InteractionContext, ResourceType],
    Coroutine[None, None, Id | ResourceType] | Id | ResourceType,
]
ReadInteractionHandler = Callable[
    [InteractionContext, Id], Coroutine[None, None, ResourceType] | ResourceType
]
UpdateInteractionHandler = Callable[
    [InteractionContext, Id, ResourceType],
    Coroutine[None, None, Id | ResourceType] | Id | ResourceType,
]
SearchTypeInteractionHandler = Callable[..., Coroutine[None, None, Bundle] | Bundle]

InteractionHandler = (
    CreateInteractionHandler[ResourceType]
    | ReadInteractionHandler[ResourceType]
    | SearchTypeInteractionHandler
    | UpdateInteractionHandler[ResourceType]
)


class TypeInteraction(Generic[ResourceType]):
    """
    Collection of values that represent a FHIR type interactions. This class can also represent
    instance level interactions.

    resource_type:    The type of FHIR resource on which this interaction operates, as defined by
                      the fhir.resources package.
    handler:          User-defined function that performs the FHIR interaction.
    route_options:    Dictionary of key-value pairs that are passed on to FastAPI on route creation.
    """

    def __init__(
        self,
        resource_type: type[ResourceType],
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
