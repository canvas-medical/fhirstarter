"""Utility functions for creation of routes and responses."""

from collections.abc import Callable, Mapping
from functools import partial
from types import CodeType, FunctionType
from typing import Any, cast

from fastapi import Form, Query, Request, Response
from fhir.resources.bundle import Bundle
from fhir.resources.operationoutcome import OperationOutcome
from funcy import omit

from . import function_templates, status
from .provider import ResourceType, TypeInteraction
from .search_parameters import (
    load_search_parameters,
    supported_search_parameters,
    var_sp_name_to_fhir_sp_name,
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


def make_function(
    interaction: TypeInteraction[ResourceType],
    annotations: Mapping[str, Any],
    argdefs: tuple[Any, ...],
) -> FunctionType:
    """Make a function suitable for creation of a FHIR create, read, or update API route."""
    code = getattr(
        function_templates, interaction.interaction_type.value.replace("-", "_")
    ).__code__

    return _make_function(interaction, annotations, code, argdefs)


# TODO: If possible, map FHIR primitives to correct type annotations for better validation
def make_search_type_function(
    interaction: TypeInteraction[ResourceType], post: bool
) -> FunctionType:
    """
    Make a function suitable for creation of a FHIR search-type API route.

    Creation of a search-type function is more complex than creation of a create, read, or update
    function due to the variability of search parameters, and due to the need to support GET and
    POST.

    Search parameter descriptions are pulled from the FHIR specification.

    Aside from definition of globals, argument defaults, and annotations, the most important thing
    this function does is to set the "include_in_schema" value for each search parameter, based on
    the search parameters that the provided callable supports.
    """
    function_template = getattr(
        function_templates,
        f"{interaction.resource_type.get_resource_type().lower()}_"
        f"{interaction.interaction_type.value.replace('-', '_')}",
    )
    variable_names = tuple(
        omit(
            function_template.__annotations__, ["request", "response", "return"]
        ).keys()
    )
    supported_search_parameters_ = set(
        supported_search_parameters(interaction.callable_)
    )
    search_parameters = load_search_parameters()[
        interaction.resource_type.get_resource_type()
    ]

    annotations = {name: str for name in variable_names}
    code = function_template.__code__
    if post:
        argdefs = tuple(
            Form(
                None,
                alias=var_sp_name_to_fhir_sp_name(name),
                description=search_parameters[var_sp_name_to_fhir_sp_name(name)][
                    "description"
                ],
            )
            if name in supported_search_parameters_
            else Query(None, include_in_schema=False)
            for name in variable_names
        )
    else:
        argdefs = tuple(
            Query(
                None,
                alias=var_sp_name_to_fhir_sp_name(name),
                description=search_parameters[var_sp_name_to_fhir_sp_name(name)][
                    "description"
                ],
                include_in_schema=name in supported_search_parameters_,
            )
            for name in variable_names
        )

    return _make_function(interaction, annotations, code, argdefs)


def _make_function(
    interaction: TypeInteraction[ResourceType],
    annotations: Mapping[str, Any],
    code: CodeType,
    argdefs: tuple[Any, ...],
) -> FunctionType:
    """Make a function suitable for creation of a FHIR create, read, or updates API route."""
    annotations |= {"request": Request, "response": Response}
    globals_ = {
        "callable_": interaction.callable_,
        "cast": cast,
        "resource_type_str": interaction.resource_type.get_resource_type(),
        "result_to_id_resource_tuple": function_templates.result_to_id_resource_tuple,
        "ResourceType": interaction.resource_type,
    }

    func = FunctionType(code=code, globals=globals_, argdefs=argdefs)
    func.__annotations__ = annotations

    return func


def create_route_args(interaction: TypeInteraction[ResourceType]) -> dict[str, Any]:
    """Provide arguments for creation of a FHIR create API route."""
    resource_type_str = interaction.resource_type.get_resource_type()

    return {
        "path": f"/{resource_type_str}",
        "response_model": interaction.resource_type,
        "status_code": status.HTTP_201_CREATED,
        "tags": [f"Type:{interaction.resource_type.get_resource_type()}"],
        "summary": f"{resource_type_str} {interaction.interaction_type.value}",
        "description": f"The {resource_type_str} create interaction creates a new "
        f"{resource_type_str} resource in a server-assigned location.",
        "responses": _responses(
            interaction, _created, _bad_request, _unprocessable_entity
        ),
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
        "tags": [f"Type:{interaction.resource_type.get_resource_type()}"],
        "summary": f"{resource_type_str} {interaction.interaction_type.value}",
        "description": f"The {resource_type_str} read interaction accesses "
        f"the current contents of a {resource_type_str} resource.",
        "responses": _responses(interaction, _ok, _not_found),
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
        "tags": [f"Type:{interaction.resource_type.get_resource_type()}"],
        "summary": f"{resource_type_str} {interaction.interaction_type.value}",
        "description": f"The {resource_type_str} search-type interaction searches a set of resources "
        "based on some filter criteria.",
        "responses": _responses(interaction, partial(_ok, search=True), _bad_request),
        "response_model_exclude_none": True,
        **interaction.route_options,
    }


def update_route_args(interaction: TypeInteraction[ResourceType]) -> dict[str, Any]:
    """Provide arguments for creation of a FHIR update API route."""
    resource_type_str = interaction.resource_type.get_resource_type()

    return {
        "path": f"/{resource_type_str}/{{id}}",
        "response_model": interaction.resource_type,
        "status_code": status.HTTP_200_OK,
        "tags": [f"Type:{interaction.resource_type.get_resource_type()}"],
        "summary": f"{resource_type_str} {interaction.interaction_type.value}",
        "description": f"The {resource_type_str} update interaction creates a new current version "
        f"for an existing {resource_type_str} resource.",
        "responses": _responses(interaction, _ok, _bad_request, _unprocessable_entity),
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


def _ok(interaction: TypeInteraction[ResourceType], search: bool = False) -> _Responses:
    """Return documentation for an HTTP 200 OK response."""
    return {
        status.HTTP_200_OK: {
            "model": interaction.resource_type if not search else Bundle,
            "description": f"Successful {interaction.resource_type.get_resource_type()} "
            f"{interaction.interaction_type.value}",
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
            f"{interaction.interaction_type.value} request could not be parsed or "
            "failed basic FHIR validation rules.",
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
