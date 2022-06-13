from types import FunctionType
from typing import Any, Callable, Mapping, cast

from fastapi import Request, Response
from fhir.resources.operationoutcome import OperationOutcome

from . import code_templates, status
from .provider import FHIRInteraction, FHIRInteractionResult, FHIRResourceType


def make_operation_outcome(
    severity: str, code: str, details_text: str
) -> OperationOutcome:
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
    interaction: FHIRInteraction[FHIRResourceType],
    annotations: Mapping[str, Any],
    argdefs: tuple[Any, ...],
) -> FunctionType:
    name = (
        f"{interaction.resource_type.get_resource_type().lower()}_"
        f"{interaction.interaction_type.value}"
    )
    annotations |= {"request": Request, "response": Response}
    code = getattr(code_templates, interaction.interaction_type.value).__code__
    globals_ = {
        "cast": cast,
        "FHIRInteractionResult": FHIRInteractionResult,
        "FHIRResourceType": interaction.resource_type,
        "callable_": interaction.callable_,
        "resource_id": code_templates.resource_id,
        "resource_type_str": interaction.resource_type.get_resource_type(),
    }

    func = FunctionType(code=code, globals=globals_, name=name, argdefs=argdefs)
    func.__annotations__ = annotations

    return func


def create_route_args(interaction: FHIRInteraction[FHIRResourceType]) -> dict[str, Any]:
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


def update_route_args(interaction: FHIRInteraction[FHIRResourceType]) -> dict[str, Any]:
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


def read_route_args(interaction: FHIRInteraction[FHIRResourceType]) -> dict[str, Any]:
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


_Responses = dict[int, dict[str, Any]]


def _responses(
    interaction: FHIRInteraction[FHIRResourceType],
    *responses: Callable[[FHIRInteraction[FHIRResourceType]], _Responses],
) -> _Responses:
    merged_responses: _Responses = {}
    for response in responses:
        merged_responses |= response(interaction)
    return merged_responses


def _ok(interaction: FHIRInteraction[FHIRResourceType]) -> _Responses:
    return {
        status.HTTP_200_OK: {
            "model": interaction.resource_type,
            "description": f"Successful {interaction.resource_type.get_resource_type()} "
            f"{interaction.interaction_type.value}",
        }
    }


def _created(interaction: FHIRInteraction[FHIRResourceType]) -> _Responses:
    return {
        status.HTTP_201_CREATED: {
            "model": interaction.resource_type,
            "description": f"Successful {interaction.resource_type.get_resource_type()} create",
        }
    }


def _bad_request(interaction: FHIRInteraction[FHIRResourceType]) -> _Responses:
    return {
        status.HTTP_400_BAD_REQUEST: {
            "model": OperationOutcome,
            "description": f"{interaction.resource_type.get_resource_type()} resource could not be"
            " parsed or failed basic FHIR validation rules.",
        }
    }


def _not_found(interaction: FHIRInteraction[FHIRResourceType]) -> _Responses:
    return {
        status.HTTP_404_NOT_FOUND: {
            "model": OperationOutcome,
            "description": f"Unknown {interaction.resource_type.get_resource_type()} resource",
        }
    }


def _unprocessable_entity(interaction: FHIRInteraction[FHIRResourceType]) -> _Responses:
    return {
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": OperationOutcome,
            "description": f"The proposed {interaction.resource_type.get_resource_type()} resource"
            " violated applicable "
            "FHIR profiles or server business rules.",
        }
    }
