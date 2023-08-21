"""Test FHIR interactions"""

from collections.abc import Callable, Coroutine
from functools import partial
from inspect import iscoroutinefunction
from typing import cast

import pytest
from requests.models import Response

from .. import status
from ..interactions import InteractionContext
from ..providers import FHIRProvider
from ..resources import Bundle
from ..testclient import TestClient
from ..utils import make_operation_outcome
from .config import DATABASE, app, patient_create, patient_create_async
from .resources import HumanName, Patient
from .utils import (
    assert_expected_response,
    generate_fhir_resource_id,
    id_from_create_response,
    json_dumps_pretty,
    resource,
)


@pytest.fixture(scope="module")
def client(
    create_test_client_func: Callable[[tuple[str, ...]], TestClient]
) -> TestClient:
    """Return a module-scoped test client with all interactions enabled."""
    return create_test_client_func(("create", "read", "search-type", "update"))


@pytest.fixture(scope="module")
def create_response(client: TestClient) -> Response:
    """Return the response from a Patient create interaction."""
    return client.post("/Patient", json=resource())


@pytest.fixture(scope="module")
def patient_id(create_response: Response) -> str:
    """Return the patient ID from a Patient create interaction."""
    return id_from_create_response(create_response)


def test_create(create_response: Response) -> None:
    """Test FHIR create interaction."""
    assert_expected_response(create_response, status.HTTP_201_CREATED)


def test_read(client: TestClient, patient_id: str) -> None:
    """Test FHIR read interaction."""
    read_response = client.get(f"/Patient/{patient_id}")

    assert_expected_response(
        read_response, status.HTTP_200_OK, content=resource(patient_id)
    )


def test_read_pretty(client: TestClient, patient_id: str) -> None:
    """Test FHIR read interaction with a pretty response."""
    read_response = client.get(f"/Patient/{patient_id}?_pretty=true")

    assert_expected_response(
        read_response,
        status.HTTP_200_OK,
        content=json_dumps_pretty(resource(patient_id)),
    )


@pytest.mark.parametrize(
    argnames="pretty",
    argvalues=["false", "true"],
    ids=["minified", "pretty"],
)
def test_read_xml(client: TestClient, patient_id: str, pretty: str) -> None:
    """Test FHIR read interaction with an XML response."""
    read_response = client.get(f"/Patient/{patient_id}?_format=xml&_pretty={pretty}")

    assert_expected_response(
        read_response,
        status.HTTP_200_OK,
        content_type="application/fhir+xml",
        content=Patient(**(resource(patient_id))).xml(pretty_print=(pretty == "true")),
    )


def test_read_not_found(client: TestClient) -> None:
    """Test FHIR read interaction that produces a 404 not found error."""
    id_ = generate_fhir_resource_id()
    read_response = client.get(f"/Patient/{id_}")

    assert_expected_response(
        read_response,
        status.HTTP_404_NOT_FOUND,
        content=make_operation_outcome(
            severity="error",
            code="not-found",
            details_text=f"Unknown Patient resource '{id_}'",
        ).dict(),
    )


def test_read_not_found_pretty(client: TestClient) -> None:
    """Test FHIR read interaction that produces a 404 not found error with a pretty response."""
    id_ = generate_fhir_resource_id()
    read_response = client.get(f"/Patient/{id_}?_pretty=true")

    assert_expected_response(
        read_response,
        status.HTTP_404_NOT_FOUND,
        content=json_dumps_pretty(
            make_operation_outcome(
                severity="error",
                code="not-found",
                details_text=f"Unknown Patient resource '{id_}'",
            ).dict()
        ),
    )


@pytest.mark.parametrize(
    argnames="pretty",
    argvalues=["false", "true"],
    ids=["minified", "pretty"],
)
def test_read_not_found_xml(client: TestClient, pretty: str) -> None:
    """Test FHIR read interaction that produces a 404 not found error with an XML response."""
    id_ = generate_fhir_resource_id()
    read_response = client.get(f"/Patient/{id_}?_format=xml&_pretty={pretty}")

    assert_expected_response(
        read_response,
        status.HTTP_404_NOT_FOUND,
        content_type="application/fhir+xml",
        content=make_operation_outcome(
            severity="error",
            code="not-found",
            details_text=f"Unknown Patient resource '{id_}'",
        ).xml(pretty_print=(pretty == "true")),
    )


@pytest.mark.parametrize(
    argnames="search_type_func,search_type_func_kwargs",
    argvalues=[
        (
            lambda client: partial(client.get, "/Patient"),
            {"params": {"family": "Baggins"}},
        ),
        (
            lambda client: partial(client.post, "/Patient/_search"),
            {"data": {"family": "Baggins"}},
        ),
    ],
    ids=["get", "post"],
)
def test_search_type(
    client: TestClient,
    patient_id: str,
    search_type_func: Callable[[TestClient], Callable[..., Response]],
    search_type_func_kwargs: dict[str, str],
) -> None:
    """Test the FHIR search interaction."""
    search_type_response = search_type_func(client)(**search_type_func_kwargs)

    assert_expected_response(
        search_type_response,
        status.HTTP_200_OK,
        content={
            "resourceType": "Bundle",
            "type": "searchset",
            "total": 1,
            "entry": [{"resource": resource(patient_id)}],
        },
    )


def _search_type_handler_parameter_multiple_values_async() -> (
    Callable[..., Coroutine[None, None, Bundle]]
):
    """Return an async Patient search-type handler that can test repeated query parameters."""

    async def patient_search_type(
        context: InteractionContext, given: list[str] | None
    ) -> Bundle:
        return _search_type_handler_parameter_multiple_values()(context, given)

    return patient_search_type


def _search_type_handler_parameter_multiple_values() -> Callable[..., Bundle]:
    """Return a Patient search-type handler that can test repeated query parameters."""

    def patient_search_type(_: InteractionContext, given: list[str] | None) -> Bundle:
        patients = []
        for patient in DATABASE.values():
            for name in patient.name:
                if set(given or ()).issubset(cast(HumanName, name).given):
                    patients.append(patient)

        bundle = Bundle(
            **{
                "type": "searchset",
                "total": len(patients),
                "entry": [{"resource": patient.dict()} for patient in patients],
            }
        )

        return bundle

    return patient_search_type


@pytest.mark.parametrize(
    argnames="search_type_func,search_type_func_kwargs,search_type_func_kwargs_zero_results",
    argvalues=[
        (
            lambda client: partial(client.get, "/Patient"),
            {"params": {"given": ["Samwise", "Sam"]}},
            {"params": {"given": ["Samwise", "Frodo"]}},
        ),
        (
            lambda client: partial(client.post, "/Patient/_search"),
            {"data": {"given": ["Samwise", "Sam"]}},
            {"data": {"given": ["Samwise", "Frodo"]}},
        ),
    ],
    ids=["get", "post"],
)
@pytest.mark.parametrize(
    argnames="handler",
    argvalues=[
        _search_type_handler_parameter_multiple_values_async(),
        _search_type_handler_parameter_multiple_values(),
    ],
    ids=["async", "nonasync"],
)
def test_search_type_parameter_multiple_values(
    handler: Callable[..., Coroutine[None, None, Bundle]] | Callable[..., Bundle],
    search_type_func: Callable[[TestClient], Callable[..., Response]],
    search_type_func_kwargs: dict[str, str],
    search_type_func_kwargs_zero_results: dict[str, str],
) -> None:
    """Test the FHIR search interaction with a parameter that has multiple values."""
    provider = FHIRProvider()

    if iscoroutinefunction(handler):
        provider.create(Patient)(patient_create_async)
    else:
        provider.create(Patient)(patient_create)

    provider.search_type(Patient)(handler)

    client = app(provider)

    create_response = client.post(
        "/Patient",
        json={
            "resourceType": "Patient",
            "name": [{"family": "Gamgee", "given": ["Samwise", "Sam"]}],
        },
    )
    id_ = id_from_create_response(create_response)

    search_type_response = search_type_func(client)(**search_type_func_kwargs)
    assert_expected_response(
        search_type_response,
        status.HTTP_200_OK,
        content={
            "resourceType": "Bundle",
            "type": "searchset",
            "total": 1,
            "entry": [
                {
                    "resource": {
                        "resourceType": "Patient",
                        "id": id_,
                        "name": [{"family": "Gamgee", "given": ["Samwise", "Sam"]}],
                    }
                }
            ],
        },
    )

    search_type_response = search_type_func(client)(
        **search_type_func_kwargs_zero_results
    )
    assert_expected_response(
        search_type_response,
        status.HTTP_200_OK,
        content={
            "resourceType": "Bundle",
            "type": "searchset",
            "total": 0,
        },
    )


def test_update(client: TestClient, patient_id: str) -> None:
    """Test FHIR update interaction."""
    read_response = client.get(f"/Patient/{patient_id}")
    content = read_response.json()
    content["name"][0]["given"][0] = "Frodo"
    put_response = client.put(f"/Patient/{patient_id}", json=content)

    assert_expected_response(put_response, status.HTTP_200_OK)

    read_response = client.get(f"/Patient/{patient_id}")

    assert_expected_response(
        read_response,
        status.HTTP_200_OK,
        content={
            "resourceType": "Patient",
            "id": patient_id,
            "name": [{"family": "Baggins", "given": ["Frodo"]}],
        },
    )


def test_update_not_found(client: TestClient) -> None:
    """Test FHIR update interaction that produces a 404 not found error."""
    id_ = generate_fhir_resource_id()
    put_response = client.put(f"/Patient/{id_}", json=resource())

    assert_expected_response(
        put_response,
        status.HTTP_404_NOT_FOUND,
        content=make_operation_outcome(
            severity="error",
            code="not-found",
            details_text=f"Unknown Patient resource '{id_}'",
        ).dict(),
    )


def test_update_id_mismatch(client: TestClient, patient_id: str) -> None:
    """
    Test FHIR update interaction where the logical Id in the URL does not match the logical ID in
    the resource.
    """
    read_response = client.get(f"/Patient/{patient_id}")
    content = read_response.json()
    content["id"] = generate_fhir_resource_id()
    put_response = client.put(f"/Patient/{patient_id}", json=content)

    assert_expected_response(
        put_response,
        status.HTTP_400_BAD_REQUEST,
        content={
            "resourceType": "OperationOutcome",
            "issue": [
                {
                    "severity": "error",
                    "code": "invalid",
                    "details": {
                        "text": "Logical Id in URL must match logical Id in resource"
                    },
                }
            ],
        },
    )


@pytest.mark.parametrize(
    argnames="interaction_func",
    argvalues=(
        lambda client: client.post("/Patient", data=None),
        lambda client: client.put(f"/Patient/{generate_fhir_resource_id()}", data=None),
    ),
    ids=["create", "update"],
)
def test_no_body(
    client: TestClient, interaction_func: Callable[[TestClient], Response]
) -> None:
    response = interaction_func(client)
    assert_expected_response(
        response,
        status.HTTP_400_BAD_REQUEST,
        content={
            "issue": [
                {
                    "code": "required",
                    "details": {
                        "text": "body — field required (type=value_error.missing)"
                    },
                    "severity": "error",
                }
            ],
            "resourceType": "OperationOutcome",
        },
    )
