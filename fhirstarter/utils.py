"""Utility functions for creation of routes and responses."""

import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, ClassVar, Literal

from fastapi import Request
from fastapi.responses import JSONResponse, Response

from . import status
from .fhir_specification.utils import is_resource_type
from .interactions import ResourceType, SearchTypeInteraction, TypeInteraction
from .resources import Bundle, OperationOutcome, Resource


@dataclass
class InteractionInfo:
    resource_type: str | None
    interaction_type: Literal[
        "create", "read", "update", "search-type", "capabilities"
    ] | None
    resource_id: str | None


def categorize_fhir_request(request: Request) -> InteractionInfo:
    """
    Return the resource type and interaction type for a request.

    Note: This function is currently oriented around specific use cases for this framework.
    Specifically, it will correctly categorize create, read, search-type, update, and capabilities
    interactions. Further enhancement is needed to support more cases.
    """
    logging.warning(
        "fhirstarter.utils.categorize_fhir_request has been deprecated and will be "
        "removed in a future release"
    )

    _, first_part, *rest = request.url.path.split("/")

    if request.method == "GET" and first_part == "metadata":
        return InteractionInfo(  # type: ignore[call-arg]
            resource_type=None, interaction_type="capabilities", resource_id=None
        )

    if not is_resource_type(first_part):
        return InteractionInfo(resource_type=None, interaction_type=None, resource_id=None)  # type: ignore[call-arg]

    resource_type = first_part
    second_part = rest[0] if rest else None
    id_ = second_part if request.method != "POST" else None

    interaction_type = None
    match request.method, second_part == "_search", not id_:
        case "POST", False, True:
            interaction_type = "create"
        case "GET", _, False:
            interaction_type = "read"
        case "GET", False, True:
            interaction_type = "search-type"
        case "POST", True, True:
            interaction_type = "search-type"
        case "PUT", _, False:
            interaction_type = "update"
        case _:
            assert "Unexpected request format"

    return InteractionInfo(resource_type, interaction_type, resource_id=id_)  # type: ignore[call-arg]


def parse_fhir_request(request: Request) -> InteractionInfo:
    """
    Parse a FHIR request into its component parts, and determine an interaction type.

    Note: This function is currently oriented around specific use cases for this framework.
    Specifically, it will correctly categorize create, read, search-type, update, and capabilities
    interactions. Further enhancement is needed to support more use cases.
    """
    no_info = InteractionInfo(  # type: ignore[call-arg]
        resource_type=None, interaction_type=None, resource_id=None
    )

    split_path = request.url.path.split("/")
    if not split_path:
        return no_info

    resource_id = None

    if request.method == "GET":
        if split_path[-1] == "metadata":
            return InteractionInfo(  # type: ignore[call-arg]
                resource_type=None, interaction_type="capabilities", resource_id=None
            )
        elif is_resource_type(split_path[-1]):
            resource_type = split_path[-1]
            interaction_type = "search-type"
        elif len(split_path) >= 3:
            resource_type, resource_id = split_path[-2:]
            interaction_type = "read"
        else:
            return no_info
    elif request.method == "POST":
        if is_resource_type(split_path[-1]):
            resource_type = split_path[-1]
            interaction_type = "create"
        elif split_path[-1] == "_search":
            resource_type = split_path[-2]
            interaction_type = "search-type"
        else:
            return no_info
    elif request.method == "PUT":
        if len(split_path) >= 3:
            resource_type, resource_id = split_path[-2:]
            interaction_type = "update"
        else:
            return no_info
    else:
        return no_info

    if not is_resource_type(resource_type):
        return no_info

    return InteractionInfo(  # type: ignore[call-arg]
        resource_type=resource_type,
        interaction_type=interaction_type,
        resource_id=resource_id,
    )


def make_operation_outcome(
    severity: str, code: str, details_text: str
) -> OperationOutcome:
    """Create a simple OperationOutcome given a severity, code, and details."""
    return OperationOutcome(
        **{
            "issue": [
                {
                    "severity": severity,
                    "code": code,
                    "details": {"text": details_text},
                }
            ]
        }
    )


@dataclass
class FormatParameters:
    format: str = "application/fhir+json"
    pretty: bool = False

    _CONTENT_TYPES: ClassVar = {
        "json": "application/fhir+json",
        "application/json": "application/fhir+json",
        "application/fhir+json": "application/fhir+json",
        "xml": "application/fhir+xml",
        "text/xml": "application/fhir+xml",
        "application/xml": "application/fhir+xml",
        "application/fhir+xml": "application/fhir+xml",
    }

    @classmethod
    def from_request(
        cls, request: Request, raise_exception: bool = True
    ) -> "FormatParameters":
        """
        Parse the _format and _pretty query parameters.

        The value for format is first obtained from the Accept header, and if not specified there is
        obtained from the _format query parameter.
        """
        format_ = cls.format_from_accept_header(request)

        try:
            if not format_:
                format_ = cls._CONTENT_TYPES[
                    request.query_params.get("_format", "json")
                ]
        except KeyError:
            if raise_exception:
                from .exceptions import FHIRGeneralError

                raise FHIRGeneralError(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    severity="error",
                    code="structure",
                    details_text="Invalid response format specified for '_format' parameter",
                )
            else:
                format_ = "application/fhir+json"

        return cls(  # type: ignore[call-arg]
            format=format_,
            pretty=request.query_params.get("_pretty", "false") == "true",
        )

    @classmethod
    def format_from_accept_header(cls, request: Request) -> str | None:
        if request.method == "POST":
            for content_type in request.headers.getlist("Accept"):
                if content_type_normalized := cls._CONTENT_TYPES.get(content_type):
                    return content_type_normalized

        return None


def format_response(
    resource: Resource | None,
    response: Response | None = None,
    status_code: int | None = None,
    format_parameters: FormatParameters = FormatParameters(),
) -> Resource | Response:
    """
    Return a response with the proper formatting applied.

    This function provides a response in JSON or XML format that has been prettified if requested.

    There are six scenarios that are handled:
    1. Null resource (when there is no body -- no handling required)
    1. Pretty JSON
    2. Minified JSON with a status code (mainly for errors)
    3. Minified JSON with no specified status code (usually the default)
    4. Pretty XML
    5. Minified XML
    """
    if not resource:
        assert (
            response is not None
        ), "Response object must be provided for a null resource"
        response.headers["Content-Type"] = format_parameters.format
        return resource

    if format_parameters.format == "application/fhir+json":
        if format_parameters.pretty:
            return Response(
                content=resource.json(
                    ensure_ascii=False,
                    allow_nan=False,
                    indent=2,
                    separators=(", ", ": "),
                ),
                status_code=status_code or status.HTTP_200_OK,
                media_type=format_parameters.format,
            )
        else:
            if status_code:
                return JSONResponse(
                    content=resource.dict(),
                    status_code=status_code,
                    media_type=format_parameters.format,
                )
            else:
                assert (
                    response is not None
                ), "Response object or status code must be provided for non-pretty JSON responses"
                response.headers["Content-Type"] = format_parameters.format
                return resource
    else:
        return Response(
            content=resource.xml(pretty_print=format_parameters.pretty),
            status_code=status_code or status.HTTP_200_OK,
            media_type=format_parameters.format,
        )


def create_route_args(interaction: TypeInteraction[ResourceType]) -> dict[str, Any]:
    """Provide arguments for creation of a FHIR create API route."""
    resource_type_str = interaction.resource_type.get_resource_type()

    return {
        "path": f"/{resource_type_str}",
        "response_model": interaction.resource_type | None,
        "status_code": status.HTTP_201_CREATED,
        "tags": [f"Type:{resource_type_str}"],
        "summary": f"{resource_type_str} {interaction.label()}",
        "description": f"The {resource_type_str} create interaction creates a new "
        f"{resource_type_str} resource in a server-assigned location.",
        "responses": _responses(
            interaction,
            _created,
            _bad_request,
            _unauthorized,
            _forbidden,
            _unprocessable_entity,
            _internal_server_error,
        ),
        "operation_id": f"fhirstarter|type|create|post|{resource_type_str}|{interaction.resource_type.__module__}|{interaction.resource_type.__name__}",
        "response_model_exclude_none": True,
        **interaction.route_options,
    }


def read_route_args(interaction: TypeInteraction[ResourceType]) -> dict[str, Any]:
    """Provide arguments for creation of a FHIR read API route."""
    resource_type_str = interaction.resource_type.get_resource_type()

    return {
        "path": f"/{resource_type_str}/{{id}}",
        "response_model": interaction.resource_type,
        "status_code": status.HTTP_200_OK,
        "tags": [f"Type:{resource_type_str}"],
        "summary": f"{resource_type_str} {interaction.label()}",
        "description": f"The {resource_type_str} read interaction accesses "
        f"the current contents of a {resource_type_str} resource.",
        "responses": _responses(
            interaction,
            _ok,
            _unauthorized,
            _forbidden,
            _not_found,
            _internal_server_error,
        ),
        "operation_id": f"fhirstarter|instance|read|get|{resource_type_str}|{interaction.resource_type.__module__}|{interaction.resource_type.__name__}",
        "response_model_exclude_none": True,
        **interaction.route_options,
    }


def search_type_route_args(
    interaction: TypeInteraction[ResourceType], post: bool
) -> dict[str, Any]:
    """Provide arguments for creation of a FHIR search-type API route."""
    resource_type_str = interaction.resource_type.get_resource_type()

    return {
        "path": f"/{resource_type_str}{'/_search' if post else ''}",
        "response_model": Bundle,
        "status_code": status.HTTP_200_OK,
        "tags": [f"Type:{resource_type_str}"],
        "summary": f"{resource_type_str} {interaction.label()}",
        "description": f"The {resource_type_str} search-type interaction searches a set of "
        "resources based on some filter criteria.",
        "responses": _responses(
            interaction,
            _ok,
            _bad_request,
            _unauthorized,
            _forbidden,
            _internal_server_error,
        ),
        "operation_id": f"fhirstarter|type|search-type|{'post' if post else 'get'}|{resource_type_str}|{interaction.resource_type.__module__}|{interaction.resource_type.__name__}",
        "response_model_exclude_none": True,
        **interaction.route_options,
    }


def update_route_args(interaction: TypeInteraction[ResourceType]) -> dict[str, Any]:
    """Provide arguments for creation of a FHIR update API route."""
    resource_type_str = interaction.resource_type.get_resource_type()

    return {
        "path": f"/{resource_type_str}/{{id}}",
        "response_model": interaction.resource_type | None,
        "status_code": status.HTTP_200_OK,
        "tags": [f"Type:{resource_type_str}"],
        "summary": f"{resource_type_str} {interaction.label()}",
        "description": f"The {resource_type_str} update interaction creates a new current version "
        f"for an existing {resource_type_str} resource.",
        "responses": _responses(
            interaction,
            _ok,
            _bad_request,
            _unauthorized,
            _forbidden,
            _not_found,
            _unprocessable_entity,
            _internal_server_error,
        ),
        "operation_id": f"fhirstarter|instance|update|put|{resource_type_str}|{interaction.resource_type.__module__}|{interaction.resource_type.__name__}",
        "response_model_exclude_none": True,
        **interaction.route_options,
    }


_Responses = dict[int, dict[str, Any]]


def _responses(
    interaction: TypeInteraction[ResourceType],
    *responses: Callable[[TypeInteraction[ResourceType]], _Responses],
) -> _Responses:
    """Combine the responses documentation for a FHIR interaction into a single dictionary."""
    merged_responses: _Responses = {}
    for response in responses:
        merged_responses |= response(interaction)
    return merged_responses


def _ok(interaction: TypeInteraction[ResourceType]) -> _Responses:
    """Return documentation for an HTTP 200 OK response."""
    return {
        status.HTTP_200_OK: {
            "model": interaction.resource_type
            if not isinstance(interaction, SearchTypeInteraction)
            else Bundle,
            "description": f"Successful {interaction.resource_type.get_resource_type()} "
            f"{interaction.label()}",
        }
    }


def _created(interaction: TypeInteraction[ResourceType]) -> _Responses:
    """Documentation for an HTTP 201 Created response."""
    return {
        status.HTTP_201_CREATED: {
            "model": interaction.resource_type,
            "description": f"Successful {interaction.resource_type.get_resource_type()} create",
        }
    }


def _bad_request(interaction: TypeInteraction[ResourceType]) -> _Responses:
    """Documentation for an HTTP 400 Bad Request response."""
    return {
        status.HTTP_400_BAD_REQUEST: {
            "model": OperationOutcome,
            "description": f"{interaction.resource_type.get_resource_type()} "
            f"{interaction.label()} request could not be parsed or "
            "failed basic FHIR validation rules.",
        }
    }


def _unauthorized(interaction: TypeInteraction[ResourceType]) -> _Responses:
    """Documentation for an HTTP 401 Unauthorized response."""
    return {
        status.HTTP_401_UNAUTHORIZED: {
            "model": OperationOutcome,
            "description": "Authentication is required for the "
            f"{interaction.resource_type.get_resource_type()} {interaction.label()} interaction "
            "that was attempted.",
        }
    }


def _forbidden(interaction: TypeInteraction[ResourceType]) -> _Responses:
    """Documentation for an HTTP 403 Forbidden response."""
    return {
        status.HTTP_403_FORBIDDEN: {
            "model": OperationOutcome,
            "description": "Authorization is required for the "
            f"{interaction.resource_type.get_resource_type()} {interaction.label()} interaction "
            "that was attempted.",
        }
    }


def _not_found(interaction: TypeInteraction[ResourceType]) -> _Responses:
    """Documentation for an HTTP 404 Not Found response."""
    return {
        status.HTTP_404_NOT_FOUND: {
            "model": OperationOutcome,
            "description": f"Unknown {interaction.resource_type.get_resource_type()} resource",
        }
    }


def _unprocessable_entity(interaction: TypeInteraction[ResourceType]) -> _Responses:
    """Documentation for an HTTP 422 Unprocessable Entity response."""
    return {
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": OperationOutcome,
            "description": f"The proposed {interaction.resource_type.get_resource_type()} resource"
            " violated applicable "
            "FHIR profiles or server business rules.",
        }
    }


def _internal_server_error(_: TypeInteraction[ResourceType]) -> _Responses:
    """Documentation for an HTTP 500 Internal Server error response."""
    return {
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": OperationOutcome,
            "description": f"The server has encountered a situation it does not know how to handle.",
        }
    }
