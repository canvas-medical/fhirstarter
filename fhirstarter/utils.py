from types import FunctionType
from typing import Any, Mapping, cast

from fastapi import Request, Response
from fhir.resources.operationoutcome import OperationOutcome

from . import code_templates, status
from .provider import FHIRInteraction, FHIRInteractionResult, FHIRResourceType


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
        "FHIRInteractionResult": FHIRInteractionResult,
        "FHIRResourceType": interaction.resource_type,
        "callable_": interaction.callable_,
        "cast": cast,
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
        "summary": f"{resource_type_str} create",
        "description": f"The {resource_type_str} create interaction creates a new "
        f"{resource_type_str} resource in a server-assigned location.",
        "responses": {
            status.HTTP_201_CREATED: {
                "description": f"Successful {resource_type_str} create",
                "content": {
                    "application/json": {"schema": interaction.resource_type.schema()},
                    "application/fhir+json": {
                        "schema": interaction.resource_type.schema()
                    },
                },
            },
            status.HTTP_400_BAD_REQUEST: {
                "description": f"{resource_type_str} resource could not be parsed or failed "
                "basic FHIR validation rules",
                "content": {
                    "application/json": {"schema": OperationOutcome.schema()},
                    "application/fhir+json": {"schema": OperationOutcome.schema()},
                },
            },
            status.HTTP_422_UNPROCESSABLE_ENTITY: {
                "description": f"The proposed {resource_type_str} resource violated applicable "
                "FHIR profiles or server business rules",
                "content": {
                    "application/json": {"schema": OperationOutcome.schema()},
                    "application/fhir+json": {"schema": OperationOutcome.schema()},
                },
            },
        },
        "response_model_exclude_none": True,
        **interaction.route_options,
    }


def read_route_args(interaction: FHIRInteraction[FHIRResourceType]) -> dict[str, Any]:
    resource_type_str = interaction.resource_type.get_resource_type()

    return {
        "path": f"/{resource_type_str}/{{id}}",
        "response_model": interaction.resource_type,
        "status_code": status.HTTP_200_OK,
        "summary": f"{resource_type_str} read",
        "description": f"The {resource_type_str} read interaction accesses "
        f"the current contents of a {resource_type_str}.",
        "responses": {
            status.HTTP_200_OK: {
                "'description'": f"Successful {resource_type_str} read",
                "'content'": {
                    "application/'json'": {
                        "'schema'": interaction.resource_type.schema()
                    },
                    "application/fhir+'json'": {
                        "'schema'": interaction.resource_type.schema()
                    },
                },
            },
            status.HTTP_404_NOT_FOUND: {
                "'description'": f"Unknown {resource_type_str} resource",
                "'content'": {
                    "application/'json'": {"'schema'": OperationOutcome.schema()},
                    "application/fhir+'json'": {"'schema'": OperationOutcome.schema()},
                },
            },
        },
        "response_model_exclude_none": True,
        **interaction.route_options,
    }
