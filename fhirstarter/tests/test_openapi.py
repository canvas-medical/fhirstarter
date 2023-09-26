"""Test OpenAPI modifications"""

from collections.abc import Callable, Mapping
from typing import Any, cast

import pytest

from .. import FHIRProvider, FHIRStarter, InteractionContext
from ..fhir_specification import FHIR_SEQUENCE
from .config import create_test_client_async
from .resources import Appointment, Bundle, Id, Practitioner


@pytest.fixture(scope="module", autouse=True)
def check_fhir_sequence() -> None:
    """
    Only run tests in this module for FHIR sequence R5.

    This test module runs tests that are specific to R5 to make sure that schema modifications are
    applied properly. There is nothing important about the underlying data, so it can be expected
    that if these tests pass, then schema modifications will work properly for other sequences as
    well.
    """
    if FHIR_SEQUENCE != "R5":
        pytest.skip("blah")


class PractitionerCustom(Practitioner):
    class Config:
        schema_extra = {
            "example": {
                "resourceType": "Practitioner",
                "id": "example",
                "name": [{"family": "Careful", "given": ["Adam"], "prefix": ["Dr"]}],
            }
        }


async def practitioner_read(context: InteractionContext, id_: Id) -> PractitionerCustom:
    raise NotImplementedError


async def practitioner_search_type(context: InteractionContext) -> Bundle:
    raise NotImplementedError


async def appointment_search_type(context: InteractionContext) -> Bundle:
    raise NotImplementedError


@pytest.fixture(scope="module")
def schema() -> dict[str, Any]:
    client = create_test_client_async(("create", "read", "search-type", "update"))
    app_ = cast(FHIRStarter, client.app)

    provider = FHIRProvider()

    # Add read and search-type for a resource that uses both the standard model and a model with a
    # custom example
    provider.read(Practitioner)(practitioner_read)
    provider.search_type(PractitionerCustom)(practitioner_search_type)

    # Add a resource that only supports search-type
    provider.search_type(Appointment)(appointment_search_type)

    app_.add_providers(provider)

    return app_.openapi()


def test_inline_search_type_by_post_schemas(schema: Mapping[str, Any]) -> None:
    """Test that search-type by post schemas have been inlined."""
    search_type_paths = (
        (path_name, path)
        for path_name, path in schema["paths"].items()
        if path_name.endswith("_search")
    )
    for path_name, path in search_type_paths:
        keys = path["post"]["requestBody"]["content"][
            "application/x-www-form-urlencoded"
        ]["schema"].keys()
        assert set(keys) == {"properties", "title", "type"}


def test_resource_schemas(schema: Mapping[str, Any]) -> None:
    """Test that all expected schemas are present."""
    schema_names = schema["components"]["schemas"].keys()
    assert set(schema_names) == {
        "Appointment",
        "Bundle",
        "CapabilityStatement",
        "HTTPValidationError",
        "OperationOutcome",
        "Patient",
        "Practitioner",
        "PractitionerCustom",
        "ValidationError",
    }


def test_content_types(schema: Mapping[str, Any]) -> None:
    """Test that all application/json content types have been changed to application/fhir+json."""
    for path in schema["paths"].values():
        for operation in path.values():
            if request_body := operation.get("requestBody"):
                content = request_body["content"]
                if "application/x-www-form-urlencoded" not in content:
                    assert "application/json" not in content
                    assert "application/fhir+json" in content
            for response in operation.get("responses", {}).values():
                content = response["content"]
                assert "application/json" not in content
                assert "application/fhir+json" in content


_PATIENT_EXAMPLE_NAMES = (
    "example",
    "pat1",
    "pat2",
    "pat3",
    "pat4",
    "b248b1b2-1686-4b94-9936-37d7a5f94b51",
    "patient-example-sex-and-gender",
    "b3f24cf14-d349-45b3-8134-3d83e9104875",
    "xcda",
    "xds",
    "animal",
    "dicom",
    "ihe-pcd",
    "f001",
    "f201",
    "glossy",
    "proband",
    "genetics-example1",
    "ch-example",
    "newborn",
    "mom",
    "infant-twin-1",
    "infant-twin-2",
    "infant-fetal",
    "infant-mom",
)


@pytest.mark.parametrize(
    argnames="test_id,resource_type,get_examples_func,expected_example_names",
    argvalues=(
        argvalues_me := [
            (
                "capabilities response",
                "CapabilityStatement",
                lambda s: s["paths"]["/metadata"]["get"]["responses"]["200"]["content"][
                    "application/fhir+json"
                ]["examples"],
                (
                    "example",
                    "phr",
                    "capabilitystatement-base",
                    "capabilitystatement-base2",
                    "example-terminology-server",
                    "knowledge-repository",
                    "measure-processor",
                    "messagedefinition",
                ),
            ),
            (
                "Patient create request",
                "Patient",
                lambda s: s["paths"]["/Patient"]["post"]["requestBody"]["content"][
                    "application/fhir+json"
                ]["examples"],
                _PATIENT_EXAMPLE_NAMES,
            ),
            (
                "Patient create response",
                "Patient",
                lambda s: s["paths"]["/Patient"]["post"]["responses"]["201"]["content"][
                    "application/fhir+json"
                ]["examples"],
                _PATIENT_EXAMPLE_NAMES,
            ),
            (
                "Patient read response",
                "Patient",
                lambda s: s["paths"]["/Patient/{id}"]["get"]["responses"]["200"][
                    "content"
                ]["application/fhir+json"]["examples"],
                _PATIENT_EXAMPLE_NAMES,
            ),
            (
                "Patient update request",
                "Patient",
                lambda s: s["paths"]["/Patient/{id}"]["put"]["requestBody"]["content"][
                    "application/fhir+json"
                ]["examples"],
                _PATIENT_EXAMPLE_NAMES,
            ),
            (
                "Patient update response",
                "Patient",
                lambda s: s["paths"]["/Patient/{id}"]["put"]["responses"]["200"][
                    "content"
                ]["application/fhir+json"]["examples"],
                _PATIENT_EXAMPLE_NAMES,
            ),
            (
                "Practitioner read response",
                "Practitioner",
                lambda s: s["paths"]["/Practitioner/{id}"]["get"]["responses"]["200"][
                    "content"
                ]["application/fhir+json"]["examples"],
                (
                    "example",
                    "xcda-author",
                    "3ad0687e-f477-468c-afd5-fcc2bf897809",
                    "f001",
                    "f002",
                    "f003",
                    "f004",
                    "f005",
                    "f201",
                    "f202",
                    "f203",
                    "f204",
                    "f006",
                    "f007",
                    "xcda1",
                    "prac4",
                ),
            ),
        ]
    ),
    ids=[id_ for id_, *_ in argvalues_me],
)
def test_multiple_examples(
    schema: Mapping[str, Any],
    test_id: str,
    resource_type: str,
    get_examples_func: Callable[[Mapping[str, Any]], dict[str, Any]],
    expected_example_names: tuple[str, ...],
) -> None:
    """Test that the expected request or response body examples are present."""
    # Test that the expected example names are there
    examples = get_examples_func(schema)
    example_names = tuple(examples.keys())
    assert example_names == expected_example_names

    # Test that the inlined example (the first one) matches the resource type
    first_example_name = example_names[0]
    assert examples[first_example_name]["value"]["resourceType"] == resource_type


@pytest.mark.parametrize(
    argnames="resource_type",
    argvalues=["Appointment", "Patient", "Practitioner"],
    ids=["Appointment", "Patient", "Practitioner"],
)
def test_search_type_examples(
    schema: Mapping[str, Any],
    resource_type: str,
) -> None:
    """
    Test that the resource types in the bundle examples for search-type endpoints are the correct
    resource type.
    """
    example = schema["paths"][f"/{resource_type}"]["get"]["responses"]["200"][
        "content"
    ]["application/fhir+json"]["example"]
    assert example["entry"][0]["resource"]["resourceType"] == resource_type

    example = schema["paths"][f"/{resource_type}/_search"]["post"]["responses"]["200"][
        "content"
    ]["application/fhir+json"]["example"]
    assert example["entry"][0]["resource"]["resourceType"] == resource_type


_OPERATION_OUTCOMES = {
    "400": {
        "resourceType": "OperationOutcome",
        "id": "101",
        "issue": [
            {
                "severity": "error",
                "code": "invalid",
                "details": {"text": "Bad request"},
            }
        ],
    },
    "401": {
        "resourceType": "OperationOutcome",
        "id": "101",
        "issue": [
            {
                "severity": "error",
                "code": "unknown",
                "details": {"text": "Authentication failed"},
            }
        ],
    },
    "403": {
        "resourceType": "OperationOutcome",
        "id": "101",
        "issue": [
            {
                "severity": "error",
                "code": "forbidden",
                "details": {"text": "Authorization failed"},
            }
        ],
    },
    "404": {
        "id": "101",
        "issue": [
            {
                "code": "not-found",
                "details": {"text": "Resource not found"},
                "severity": "error",
            }
        ],
        "resourceType": "OperationOutcome",
    },
    "422": {
        "id": "101",
        "issue": [
            {
                "code": "processing",
                "details": {"text": "Unprocessable entity"},
                "severity": "error",
            }
        ],
        "resourceType": "OperationOutcome",
    },
    "500": {
        "resourceType": "OperationOutcome",
        "id": "101",
        "issue": [
            {
                "severity": "error",
                "code": "exception",
                "details": {"text": "Internal server error"},
            }
        ],
    },
}


@pytest.mark.parametrize(
    argnames="test_id,path,method,expected_status_codes",
    argvalues=(
        argvalues_ee := [
            (
                "Appointment search-type",
                "/Appointment",
                "get",
                ("400", "401", "403", "500"),
            ),
            (
                "Appointment search-type by post",
                "/Appointment/_search",
                "post",
                ("400", "401", "403", "500"),
            ),
            ("Patient create", "/Patient", "post", ("400", "401", "403", "422", "500")),
            ("Patient read", "/Patient/{id}", "get", ("401", "403", "404", "500")),
            (
                "Patient update",
                "/Patient/{id}",
                "put",
                ("400", "401", "403", "404", "422", "500"),
            ),
            ("Patient search-type", "/Patient", "get", ("400", "401", "403", "500")),
            (
                "Patient search-type by post",
                "/Patient/_search",
                "post",
                ("400", "401", "403", "500"),
            ),
            (
                "Practitioner read",
                "/Practitioner/{id}",
                "get",
                ("401", "403", "404", "500"),
            ),
            (
                "Practitioner search-type",
                "/Practitioner",
                "get",
                ("400", "401", "403", "500"),
            ),
            (
                "Practitioner search-type by post",
                "/Practitioner/_search",
                "post",
                ("400", "401", "403", "500"),
            ),
        ]
    ),
    ids=[id_ for id_, *_ in argvalues_ee],
)
def test_error_examples(
    test_id: str,
    schema: Mapping[str, Any],
    path: str,
    method: str,
    expected_status_codes: tuple[str, ...],
) -> None:
    """Test that the expected error response body examples are present."""
    responses = schema["paths"][path][method]["responses"]

    # Test that all of the expected error status codes are present
    status_codes = set(responses.keys())
    status_codes.discard("200")
    status_codes.discard("201")
    assert status_codes == set(expected_status_codes)

    # Test that all the error examples are present
    for status_code in expected_status_codes:
        assert (
            responses[status_code]["content"]["application/fhir+json"]["example"]
            == _OPERATION_OUTCOMES[status_code]
        )
