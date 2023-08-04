"""Test FHIR interactions"""

from collections.abc import Callable
from functools import partial
from typing import cast

import pytest
from fhir.resources.bundle import Bundle
from fhir.resources.humanname import HumanName
from fhir.resources.patient import Patient
from requests.models import Response

from .. import status
from ..interactions import InteractionContext
from ..providers import FHIRProvider
from ..testclient import TestClient
from ..utils import make_operation_outcome
from .config import DATABASE, app, patient_create
from .utils import (
    assert_expected_response,
    generate_fhir_resource_id,
    id_from_create_response,
    json_dumps_pretty,
    resource,
)


def test_create(create_response_fixture: Response) -> None:
    """Test FHIR create interaction."""
    assert_expected_response(create_response_fixture, status.HTTP_201_CREATED)


def test_read(client_fixture: TestClient, create_response_fixture: Response) -> None:
    """Test FHIR read interaction."""
    client = client_fixture

    id_ = id_from_create_response(create_response_fixture)
    read_response = client.get(f"/Patient/{id_}")

    assert_expected_response(read_response, status.HTTP_200_OK, content=resource(id_))


def test_read_pretty(
    client_fixture: TestClient, create_response_fixture: Response
) -> None:
    """Test FHIR read interaction with a pretty response."""
    client = client_fixture

    id_ = id_from_create_response(create_response_fixture)
    read_response = client.get(f"/Patient/{id_}?_pretty=true")

    assert_expected_response(
        read_response, status.HTTP_200_OK, content=json_dumps_pretty(resource(id_))
    )


@pytest.mark.parametrize(
    argnames="pretty",
    argvalues=["false", "true"],
    ids=["minified", "pretty"],
)
def test_read_xml(
    client_fixture: TestClient, create_response_fixture: Response, pretty: str
) -> None:
    """Test FHIR read interaction with an XML response."""
    client = client_fixture

    id_ = id_from_create_response(create_response_fixture)

    read_response = client.get(f"/Patient/{id_}?_format=xml&_pretty={pretty}")

    assert_expected_response(
        read_response,
        status.HTTP_200_OK,
        content_type="application/fhir+xml",
        content=Patient(**(resource(id_))).xml(pretty_print=(pretty == "true")),
    )


def test_read_not_found(client_fixture: TestClient) -> None:
    """Test FHIR read interaction that produces a 404 not found error."""
    client = client_fixture

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


def test_read_not_found_pretty(client_fixture: TestClient) -> None:
    """Test FHIR read interaction that produces a 404 not found error with a pretty response."""
    client = client_fixture

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
def test_read_not_found_xml(client_fixture: TestClient, pretty: str) -> None:
    """Test FHIR read interaction that produces a 404 not found error with an XML response."""
    client = client_fixture

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
    client_fixture: TestClient,
    create_response_fixture: Response,
    search_type_func: Callable[[TestClient], Callable[..., Response]],
    search_type_func_kwargs: dict[str, str],
) -> None:
    """Test the FHIR search interaction."""
    client = client_fixture

    id_ = id_from_create_response(create_response_fixture)
    search_type_response = search_type_func(client)(**search_type_func_kwargs)

    assert_expected_response(
        search_type_response,
        status.HTTP_200_OK,
        content={
            "resourceType": "Bundle",
            "type": "searchset",
            "total": 1,
            "entry": [{"resource": resource(id_)}],
        },
    )


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
def test_search_type_parameter_multiple_values(
    search_type_func: Callable[[TestClient], Callable[..., Response]],
    search_type_func_kwargs: dict[str, str],
    search_type_func_kwargs_zero_results: dict[str, str],
) -> None:
    """Test the FHIR search interaction with a parameter that has multiple values."""

    async def patient_search_type(
        _: InteractionContext, given: list[str] | None
    ) -> Bundle:
        patients = []
        for patient in DATABASE.values():
            for name in patient.name:
                if set(given).issubset(cast(HumanName, name).given):
                    patients.append(patient)

        bundle = Bundle(
            **{
                "type": "searchset",
                "total": len(patients),
                "entry": [{"resource": patient.dict()} for patient in patients],
            }
        )

        return bundle

    provider = FHIRProvider()
    provider.create(Patient)(patient_create)
    provider.search_type(Patient)(patient_search_type)

    client = app(provider)

    create_response = client.post(
        "/Patient",
        json={
            "resourceType": "Patient",
            "name": [{"family": "Gangee", "given": ["Samwise", "Sam"]}],
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
                        "name": [{"family": "Gangee", "given": ["Samwise", "Sam"]}],
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


def test_update(client_fixture: TestClient, create_response_fixture: Response) -> None:
    """Test FHIR update interaction."""
    client = client_fixture

    id_ = id_from_create_response(create_response_fixture)
    read_response = client.get(f"/Patient/{id_}")
    content = read_response.json()
    content["name"][0]["given"][0] = "Frodo"
    put_response = client.put(f"/Patient/{id_}", json=content)

    assert_expected_response(put_response, status.HTTP_200_OK)

    read_response = client.get(f"/Patient/{id_}")

    assert_expected_response(
        read_response,
        status.HTTP_200_OK,
        content={
            "resourceType": "Patient",
            "id": id_,
            "name": [{"family": "Baggins", "given": ["Frodo"]}],
        },
    )


def test_update_not_found(client_fixture: TestClient) -> None:
    """Test FHIR update interaction that produces a 404 not found error."""
    client = client_fixture

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


def test_update_id_mismatch(
    client_fixture: TestClient, create_response_fixture: Response
) -> None:
    """
    Test FHIR update interaction where the logical Id in the URL does not match the logical ID in
    the resource.
    """
    client = client_fixture

    id_ = id_from_create_response(create_response_fixture)
    read_response = client.get(f"/Patient/{id_}")
    content = read_response.json()
    content["id"] = generate_fhir_resource_id()
    put_response = client.put(f"/Patient/{id_}", json=content)

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
