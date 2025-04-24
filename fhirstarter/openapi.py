"""OpenAPI schema modifications"""

from collections import defaultdict
from dataclasses import dataclass
from importlib import import_module
from typing import (
    Any,
    DefaultDict,
    Dict,
    Iterator,
    List,
    Mapping,
    MutableMapping,
    Set,
    Tuple,
    Union,
    cast,
)

from .fhir_specification.utils import (
    create_bundle_example,
    is_resource_type,
    load_examples,
    make_operation_outcome_example,
)
from .fhirstarter import status
from .resources import Bundle, CapabilityStatement, OperationOutcome

__all__ = ["adjust_schema"]


@dataclass
class _OperationId:
    interaction_type: str
    method: str
    module_name: Union[str, None]
    model_name: Union[str, None]


def _parse_operation_id(operation_id: str) -> _OperationId:
    """Return a parsed operation ID."""
    tokens: List[str] = operation_id.split("|")

    interaction_type = tokens[2]
    method = tokens[3]
    module_name = tokens[5] if len(tokens) > 5 else None
    model_name = tokens[6] if len(tokens) > 6 else None

    return _OperationId(interaction_type, method, module_name, model_name)  # type: ignore[call-arg]


def _operations(
    openapi_schema: MutableMapping[str, Any]
) -> Iterator[Tuple[_OperationId, Dict[str, Any]]]:
    """Yield operations in the OpenAPI schema that were created by FHIRStarter."""
    for path_name, path in openapi_schema["paths"].items():
        for operation in path.values():
            operation_id = operation.get("operationId", "")
            if operation_id.startswith("fhirstarter|"):
                yield _parse_operation_id(operation_id), operation


def _search_type_operations(
    openapi_schema: MutableMapping[str, Any]
) -> Iterator[Tuple[_OperationId, Dict[str, Any]]]:
    """Yield search-type operations in the OpenAPI schema that were created by FHIRStarter."""
    for operation_id, operation in _operations(openapi_schema):
        if operation_id.interaction_type == "search-type":
            yield operation_id, operation


def adjust_schema(
    openapi_schema: MutableMapping[str, Any], include_external_examples: bool
) -> Set[str]:
    """
    Adjust the OpenAPI schema to make it more FHIR-friendly. Return a set containing all the URLs
    for external documentation examples.

    Remove some default schemas that are not needed nor used, and change all content types that
    are set to "application/json" to instead be "application/fhir+json". Add missing schemas. Make a
    few additional aesthetic changes to clean up the auto-generated documentation.

    Because it directly modifies the OpenAPI schema, it is vulnerable to breakage from updates
    to FastAPI. This is not a significant vulnerability because the core server functionality
    will still work (i.e. this is just documentation).
    """
    _rename_schemas(openapi_schema)

    _inline_search_post_schemas(openapi_schema)

    # Add any missing schemas. This needs to run before the rest of the tasks so that all the
    # schemas are there for subsequent actions.
    _add_schemas(openapi_schema)

    # Iterate over the operations and make adjustments, including adding examples from the FHIR
    # specification
    examples, external_example_urls = _get_examples(
        openapi_schema, include_external_examples
    )
    for operation_id, operation in _operations(openapi_schema):
        _adjust_operation(operation_id, operation, examples)

    return external_example_urls


def _rename_schemas(openapi_schema: MutableMapping[str, Any]) -> None:
    """
    Input and output schemas are the same in FHIR, so rename the default-named schemas so that they
    do not have "-Input" or "-Output" suffixes.
    """
    schemas = openapi_schema.get("components", {}).get("schemas", {})

    for schema_name in list(schemas.keys()):
        # The output schemas are empty for some reason, so just remove them
        if schema_name.endswith("-Output"):
            del schemas[schema_name]
        # The input schemas have the content, so rename them
        elif schema_name.endswith("-Input"):
            schemas[schema_name[:-6]] = schemas.pop(schema_name)


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
            request_body["content"]["application/x-www-form-urlencoded"]["schema"] = (
                openapi_schema["components"]["schemas"].pop(schema_name)
            )


def _add_schemas(openapi_schema: MutableMapping[str, Any]) -> None:
    """
    Add missing schemas.

    A schema might be missing for a few different reasons. If a server only supports search for a
    given resource, then the OpenAPI schema won't include the schema for the resources that are
    returned in the bundle by the search interaction.

    Additionally, resources like Bundle, CapabilityStatement, and OperationOutcome are not included
    automatically.
    """
    schemas = openapi_schema["components"]["schemas"]

    # Iterate over the operations and add resource schemas that are missing
    for operation_id, operation in _operations(openapi_schema):
        if operation_id.model_name and (
            operation_id.model_name not in schemas
            or schemas[operation_id.model_name] == {"type": "object"}
        ):
            module = import_module(operation_id.module_name)
            model = getattr(module, operation_id.model_name)
            schemas[operation_id.model_name] = model.model_json_schema()

    # The schemas for Bundle, CapabilityStatement, and OperationOutcome are not added automatically,
    # so add them here
    if "Bundle" in schemas:
        schemas["Bundle"] = Bundle.model_json_schema()
    if "CapabilityStatement" in schemas:
        schemas["CapabilityStatement"] = CapabilityStatement.model_json_schema()
    if "OperationOutcome" in schemas:
        schemas["OperationOutcome"] = OperationOutcome.model_json_schema()

    # Recreate the schema dictionary so that the schemas appear sorted
    openapi_schema["components"]["schemas"] = {
        schema_name: schema for schema_name, schema in sorted(schemas.items())
    }


def _get_examples(
    openapi_schema: MutableMapping[str, Any],
    include_external_examples: bool,
) -> Tuple[Dict[str, Dict[str, Any]], Set[str]]:
    """
    Gather examples for all scenarios: request and response bodies for interactions;
    resource-specific Bundle examples for search interactions; and OperationOutcome examples for
    errors.
    """
    examples: DefaultDict[str, Any] = defaultdict(dict)
    external_example_urls = set()

    # Get all resource examples from the models and the FHIR specification
    for schema_name, schema in openapi_schema["components"]["schemas"].items():
        properties = schema.get("properties", {})

        # The resource_name value was removed from schemas in the fhir.resources 8.0.0, so there is
        # no easy way to determine if a schema is for a FHIR resource or not. Using the
        # is_resource_type function works for most cases, but doesn't for custom resources. Checking
        # for the presence of the fields on DomainResource is a hack that works.
        if not is_resource_type(schema_name) and not {
            "text",
            "contained",
            "extension",
            "modifierExtension",
        }.issubset(properties):
            continue

        # Bundle, OperationOutcome, and Parameters are handled differently
        resource_type = schema_name
        if resource_type in {"Bundle", "OperationOutcome", "Parameters"}:
            continue

        # If there is a custom example on the model, use it. Otherwise, get examples from the FHIR
        # specification. Add the example(s) and a bundle example.
        if schema_examples := schema.get("examples"):
            examples[schema_name]["examples"] = [schema_examples[0]]
            examples["Bundle"][schema_name] = create_bundle_example(schema_examples[0])
        elif is_resource_type(resource_type):
            resource_examples = load_examples(resource_type)

            # If external examples are not to be included, remove them
            if not include_external_examples:
                example_keys = list(resource_examples.keys())
                for example_key in example_keys:
                    if "externalValue" in resource_examples[example_key]:
                        del resource_examples[example_key]

            # Replace all examples provided by an externalValue with a proxy URL
            for example in resource_examples.values():
                if value := example.get("externalValue"):
                    example["externalValue"] = f"/_example?value={value}"
                    external_example_urls.add(value)

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

    return examples, external_example_urls


def _adjust_operation(
    operation_id: _OperationId,
    operation: MutableMapping[str, Any],
    examples: Mapping[str, Dict[str, Any]],
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

    # For operations that take a request body (excluding patch), change the application/json content
    # type to application/fhir+json and add request body examples. Also, adjust schema references
    # that point to schemas that were renamed.
    if operation_id.interaction_type != "patch":
        if content := operation.get("requestBody", {}).get("content"):
            if "application/json" in content:
                content["application/fhir+json"] = content.pop("application/json")
                content["application/fhir+json"].update(resource_examples)
                schema = content["application/fhir+json"]
                if schema.get("schema", {}).get("$ref", "").endswith("-Input"):
                    schema["schema"]["$ref"] = schema["schema"]["$ref"][:-6]

    # For each possible response (i.e. status code), remove the default FastAPI response schema
    responses = operation["responses"]
    status_codes: Tuple[str, ...] = tuple(responses.keys())
    for status_code in status_codes:
        if (
            status_code != str(status.HTTP_204_NO_CONTENT)
            and responses[status_code]["content"]
            .get("application/json", {})
            .get("schema", {})
            .get("$ref")
            == "#/components/schemas/HTTPValidationError"
        ):
            responses.pop(status_code)

    # For each response, change all instances of application/json to application/fhir+json and add
    # response body examples
    for status_code, response in responses.items():
        if status_code == str(status.HTTP_204_NO_CONTENT):
            continue

        # Move the response for "application/json" to "application/fhir+json", and adjust schema
        # references that point to schemas that were renamed
        schema = response["content"].pop("application/json", None)
        if schema:
            if "schema" in schema:
                any_of = schema["schema"].get("anyOf", ())
                for item in any_of:
                    if item.get("$ref", "").endswith("-Output"):
                        item["$ref"] = item["$ref"][:-7]

                if schema["schema"].get("$ref", "").endswith("-Input"):
                    schema["schema"]["$ref"] = schema["schema"]["$ref"][:-6]
                if schema["schema"].get("$ref", "").endswith("-Output"):
                    schema["schema"]["$ref"] = schema["schema"]["$ref"][:-7]

            response["content"]["application/fhir+json"] = schema

        # Add examples for success responses
        if 200 <= int(status_code) <= 299:
            if operation_id.interaction_type != "search-type":
                response["content"]["application/fhir+json"].update(resource_examples)
            elif operation_id.model_name:
                response["content"]["application/fhir+json"]["example"] = examples[
                    "Bundle"
                ][operation_id.model_name]

        # Add specialized OperationOutcome responses if available for the status code
        if operation_outcome_example := examples["OperationOutcome"].get(status_code):
            response["content"]["application/fhir+json"][
                "example"
            ] = operation_outcome_example
