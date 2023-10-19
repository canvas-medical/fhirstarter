"""OpenAPI schema modifications"""

from collections import defaultdict
from collections.abc import Iterator, Mapping, MutableMapping
from dataclasses import dataclass
from importlib import import_module
from typing import Any, cast

from .fhir_specification.utils import (
    create_bundle_example,
    is_resource_type,
    load_examples,
    make_operation_outcome_example,
)
from .fhirstarter import status

__all__ = ["adjust_schema"]


@dataclass
class _OperationId:
    interaction_type: str
    method: str
    module_name: str | None
    model_name: str | None


def _parse_operation_id(operation_id: str) -> _OperationId:
    """Return a parsed operation ID."""
    tokens: list[str] = operation_id.split("|")

    interaction_type = tokens[2]
    method = tokens[3]
    module_name = tokens[5] if len(tokens) > 5 else None
    model_name = tokens[6] if len(tokens) > 6 else None

    return _OperationId(interaction_type, method, module_name, model_name)  # type: ignore[call-arg]


def _operations(
    openapi_schema: MutableMapping[str, Any]
) -> Iterator[tuple[_OperationId, dict[str, Any]]]:
    """Yield operations in the OpenAPI schema that were created by FHIRStarter."""
    for path_name, path in openapi_schema["paths"].items():
        for operation in path.values():
            operation_id = operation.get("operationId", "")
            if operation_id.startswith("fhirstarter|"):
                yield _parse_operation_id(operation_id), operation


def _search_type_operations(
    openapi_schema: MutableMapping[str, Any]
) -> Iterator[tuple[_OperationId, dict[str, Any]]]:
    """Yield search-type operations in the OpenAPI schema that were created by FHIRStarter."""
    for operation_id, operation in _operations(openapi_schema):
        if operation_id.interaction_type == "search-type":
            yield operation_id, operation


def adjust_schema(openapi_schema: MutableMapping[str, Any]) -> None:
    """
    Adjust the OpenAPI schema to make it more FHIR-friendly.

    Remove some default schemas that are not needed nor used, and change all content types that
    are set to "application/json" to instead be "application/fhir+json". Make a few additional
    aesthetic changes to clean up the auto-generated documentation.

    Because it directly modifies the OpenAPI schema, it is vulnerable to breakage from updates
    to FastAPI. This is not a significant vulnerability because the core server functionality
    will still work (i.e. this is just documentation).
    """
    _inline_search_post_schemas(openapi_schema)

    # Add any missing schemas (from search-type interactions). This needs to run before the rest of
    # the tasks so that all the schemas are there for subsequent actions.
    _add_schemas(openapi_schema)

    examples = _get_examples(openapi_schema)
    for operation_id, operation in _operations(openapi_schema):
        _adjust_operation(operation_id, operation, examples)
    pass


def _inline_search_post_schemas(openapi_schema: MutableMapping[str, Any]) -> None:
    """
    Inline the schemas generated for search by POST. These schemas are only used in one place, so
    they don't need to exist in the schemas section.
    """
    for operation_id, operation in _search_type_operations(openapi_schema):
        # Copy and inline the schema, and remove it from the schemas section
        if (
            operation_id.interaction_type == "search-type"
            and operation_id.method == "post"
        ):
            request_body = operation["requestBody"]
            schema_name = request_body["content"]["application/x-www-form-urlencoded"][
                "schema"
            ]["$ref"].split("/")[-1]
            request_body["content"]["application/x-www-form-urlencoded"][
                "schema"
            ] = openapi_schema["components"]["schemas"].pop(schema_name)


def _add_schemas(openapi_schema: MutableMapping[str, Any]) -> None:
    """
    Add missing schemas.

    If a server only supports search for a given resource, then the OpenAPI schema won't include the
    schema for the resources that are returned in the bundle by the search interaction.
    """
    for operation_id, operation in _search_type_operations(openapi_schema):
        if (
            operation_id.model_name
            and operation_id.model_name not in openapi_schema["components"]["schemas"]
        ):
            module = import_module(operation_id.module_name)
            model = getattr(module, operation_id.model_name)
            openapi_schema["components"]["schemas"][
                operation_id.model_name
            ] = model.schema()

    # Recreate the schema dictionary so that the schemas appear sorted
    openapi_schema["components"]["schemas"] = {
        schema_name: schema
        for schema_name, schema in sorted(
            openapi_schema["components"]["schemas"].items()
        )
    }


def _get_examples(
    openapi_schema: MutableMapping[str, Any]
) -> dict[str, dict[str, Any]]:
    """
    Gather examples for all scenarios: request and response bodies for create, read, and update
    interactions; resource-specific Bundle examples for search interactions; and OperationOutcome
    examples for errors.
    """
    examples: defaultdict[str, Any] = defaultdict(dict)

    # Get all resource examples from the models and the FHIR specification
    for schema_name, schema in openapi_schema["components"]["schemas"].items():
        properties = schema.get("properties", {})
        if "resource_type" not in properties:
            continue

        # Bundle and OperationOutcome are handled differently
        resource_type = properties["resource_type"]["const"]
        if resource_type in {"Bundle", "OperationOutcome"}:
            continue

        # If there is a custom example on the model, use it. Otherwise, get examples from the FHIR
        # specification. Add the example(s) and a bundle example.
        if schema_example := schema.get("example"):
            examples[schema_name]["example"] = schema_example
            examples["Bundle"][schema_name] = create_bundle_example(schema_example)
        elif is_resource_type(resource_type):
            resource_examples = load_examples(resource_type)
            examples[schema_name]["examples"] = resource_examples
            examples["Bundle"][schema_name] = create_bundle_example(
                next(iter(resource_examples.values()))["value"]
            )
        else:
            resource_example = {"resourceType": resource_type}
            examples[schema_name]["example"] = resource_example
            examples["Bundle"][schema_name] = create_bundle_example(resource_example)

    # Make OperationOutcome examples
    for status_code, code, details_text in (
        (str(status.HTTP_400_BAD_REQUEST), "invalid", "Bad request"),
        (str(status.HTTP_401_UNAUTHORIZED), "unknown", "Authentication failed"),
        (str(status.HTTP_403_FORBIDDEN), "forbidden", "Authorization failed"),
        (str(status.HTTP_404_NOT_FOUND), "not-found", "Resource not found"),
        (
            str(status.HTTP_422_UNPROCESSABLE_ENTITY),
            "processing",
            "Unprocessable entity",
        ),
        (
            str(status.HTTP_500_INTERNAL_SERVER_ERROR),
            "exception",
            "Internal server error",
        ),
    ):
        examples["OperationOutcome"][status_code] = make_operation_outcome_example(
            severity="error", code=code, details_text=details_text
        )

    return examples


def _adjust_operation(
    operation_id: _OperationId,
    operation: MutableMapping[str, Any],
    examples: Mapping[str, dict[str, Any]],
) -> None:
    """
    Make adjustments to an operation in the OpenAPI schema.

    * Change the application/json content type to application/fhir+json
    * Remove the default FastAPI response schema (HTTPValidationError)
    * Add request and response body examples.
    """
    # Get the examples
    if operation_id.interaction_type == "capabilities":
        resource_examples = examples["CapabilityStatement"]
    else:
        resource_examples = examples[cast(str, operation_id.model_name)]

    # For operations that take a request body, change the application/json content type to
    # application/fhir+json and add request body examples
    if content := operation.get("requestBody", {}).get("content"):
        if "application/json" in content:
            content["application/fhir+json"] = content.pop("application/json")
            content["application/fhir+json"] |= resource_examples

    # For each possible response (i.e. status code), remove the default FastAPI response schema
    responses = operation["responses"]
    status_codes: tuple[str, ...] = tuple(responses.keys())
    for status_code in status_codes:
        if (
            responses[status_code]["content"]
            .get("application/json", {})
            .get("schema", {})
            .get("$ref")
            == "#/components/schemas/HTTPValidationError"
        ):
            responses.pop(status_code)

    # For each response, change all instances of application/json to application/fhir+json and add
    # response body examples
    for status_code, response in responses.items():
        # Move the response for "application/json" to "application/fhir+json"
        schema = response["content"].pop("application/json", None)
        if schema:
            response["content"]["application/fhir+json"] = schema

        # Add examples for success responses
        if 200 <= int(status_code) <= 299:
            if operation_id.interaction_type != "search-type":
                response["content"]["application/fhir+json"] |= resource_examples
            elif operation_id.model_name:
                response["content"]["application/fhir+json"]["example"] = examples[
                    "Bundle"
                ][operation_id.model_name]

        # Add specialized OperationOutcome responses if available for the status code
        if operation_outcome_example := examples["OperationOutcome"].get(status_code):
            response["content"]["application/fhir+json"][
                "example"
            ] = operation_outcome_example
