"""FHIRStarter test cases."""

from copy import deepcopy
from typing import Any, Callable, cast
from uuid import uuid4

import pytest
from _pytest.monkeypatch import MonkeyPatch
from fhir.resources.bundle import Bundle
from fhir.resources.fhirtypes import Id
from fhir.resources.patient import Patient
from funcy import omit
from requests.models import Response

from . import status
from .exceptions import FHIRResourceNotFoundError
from .fhirstarter import FHIRStarter
from .provider import FHIRProvider
from .testclient import TestClient
from .utils import make_operation_outcome

# In-memory "database" used to simulate persistence of created FHIR resources
_DATABASE: dict[str, Patient] = {}


async def patient_create(resource: Patient, **kwargs: str) -> Id:
    """Patient create FHIR interaction."""
    patient = deepcopy(resource)
    patient.id = _generate_fhir_resource_id()
    _DATABASE[patient.id] = patient

    return Id(patient.id)


async def patient_read(id_: Id, **kwargs: str) -> Patient:
    """Patient read FHIR interaction."""
    patient = _DATABASE.get(id_)
    if not patient:
        raise FHIRResourceNotFoundError

    return patient


async def patient_search_type(
    family: str | None = None, general_practitioner: str | None = None, **kwargs: str
) -> Bundle:
    """Patient search-type FHIR interaction."""
    patients = []
    for patient in _DATABASE.values():
        for name in patient.name:
            if name.family == family:
                patients.append(patient)

    bundle = Bundle(
        **{
            "type": "searchset",
            "total": len(patients),
            "entry": [{"resource": {**patient.dict()}} for patient in patients],
        }
    )

    return bundle


async def patient_update(id_: Id, resource: Patient, **kwargs: str) -> Id:
    """Patient update FHIR interaction."""
    if id_ not in _DATABASE:
        raise FHIRResourceNotFoundError

    patient = deepcopy(resource)
    _DATABASE[id_] = patient

    return Id(patient.id)


def _app(provider: FHIRProvider) -> TestClient:
    """Create a FHIRStarter app, add the provider, reset the database, and return a TestClient."""
    app = FHIRStarter()
    app.add_providers(provider)

    _DATABASE.clear()

    return TestClient(app)


@pytest.fixture
def client() -> TestClient:
    """Test fixture that creates an app that provides all FHIR interactions."""
    provider = FHIRProvider()
    provider.register_create_interaction(Patient)(patient_create)
    provider.register_read_interaction(Patient)(patient_read)
    provider.register_search_type_interaction(Patient)(patient_search_type)
    provider.register_update_interaction(Patient)(patient_update)

    return _app(provider)


@pytest.fixture
def client_create_and_read() -> TestClient:
    """Test fixture that creates an app that only provides FHIR create and read interactions."""
    provider = FHIRProvider()
    provider.register_create_interaction(Patient)(patient_create)
    provider.register_read_interaction(Patient)(patient_read)

    return _app(provider)


def test_capability_statement(client: TestClient) -> None:
    """Test the capability statement when all FHIR interactions are supported."""
    app = cast(FHIRStarter, client.app)

    response = client.get("/metadata")

    _assert_expected_response(response, status.HTTP_200_OK)
    assert omit(response.json(), ["id"]) == {
        "resourceType": "CapabilityStatement",
        "status": "active",
        "date": app._created.isoformat(),
        "kind": "instance",
        "fhirVersion": "4.3.0",
        "format": ["json"],
        "rest": [
            {
                "mode": "server",
                "resource": [
                    {
                        "type": "Patient",
                        "interaction": [
                            {"code": "create"},
                            {"code": "read"},
                            {"code": "search-type"},
                            {"code": "update"},
                        ],
                        "searchParam": [
                            {"name": "family", "type": "string"},
                            {"name": "general-practitioner", "type": "reference"},
                        ],
                    }
                ],
            }
        ],
    }


def test_capability_statement_create_and_read(
    client_create_and_read: TestClient,
) -> None:
    """Test the capability statement when only FHIR create and read interactions are supported."""
    client = client_create_and_read
    app = cast(FHIRStarter, client.app)

    response = client.get("/metadata")

    _assert_expected_response(response, status.HTTP_200_OK)
    assert omit(response.json(), ["id"]) == {
        "resourceType": "CapabilityStatement",
        "status": "active",
        "date": app._created.isoformat(),
        "kind": "instance",
        "fhirVersion": "4.3.0",
        "format": ["json"],
        "rest": [
            {
                "mode": "server",
                "resource": [
                    {
                        "type": "Patient",
                        "interaction": [{"code": "create"}, {"code": "read"}],
                    },
                ],
            }
        ],
    }


def test_capability_statement_publisher(
    client_create_and_read: TestClient, monkeypatch: MonkeyPatch
) -> None:
    """Test the capability statement when only FHIR create and read interactions are supported."""
    monkeypatch.setenv("CAPABILITY_STATEMENT_PUBLISHER", "Publisher")

    client = client_create_and_read
    app = cast(FHIRStarter, client.app)

    response = client.get("/metadata")

    _assert_expected_response(response, status.HTTP_200_OK)
    assert omit(response.json(), ["id"]) == {
        "resourceType": "CapabilityStatement",
        "status": "active",
        "date": app._created.isoformat(),
        "publisher": "Publisher",
        "kind": "instance",
        "fhirVersion": "4.3.0",
        "format": ["json"],
        "rest": [
            {
                "mode": "server",
                "resource": [
                    {
                        "type": "Patient",
                        "interaction": [{"code": "create"}, {"code": "read"}],
                    },
                ],
            }
        ],
    }


_RESOURCE = {
    "resourceType": "Patient",
    "name": [{"family": "Baggins", "given": ["Bilbo"]}],
}


@pytest.fixture
def create_response(client: TestClient) -> Response:
    """Test fixture that provides a response from a FHIR create interaction."""
    return client.post("/Patient", json=_RESOURCE)


def test_create(create_response: Response) -> None:
    """Test FHIR create interaction."""
    _assert_expected_response(create_response, status.HTTP_201_CREATED)


def test_read(client: TestClient, create_response: Response) -> None:
    """Test FHIR read interaaction."""
    id_ = _id_from_create_response(create_response)
    read_response = client.get(f"/Patient/{id_}")

    _assert_expected_response(
        read_response, status.HTTP_200_OK, content=_RESOURCE | {"id": id_}
    )


def test_read_not_found(client: TestClient) -> None:
    """Test FHIR read interaction that produces a 404 not found error."""
    id_ = _generate_fhir_resource_id()
    read_response = client.get(f"/Patient/{id_}")

    _assert_expected_response(
        read_response,
        status.HTTP_404_NOT_FOUND,
        content=make_operation_outcome(
            severity="error",
            code="not-found",
            details_text=f"Unknown Patient resource '{id_}'",
        ).dict(),
    )


def test_search_type(client: TestClient, create_response: Response) -> None:
    """Test FHIR search-type interaction."""
    _test_search_type(
        create_response, lambda: client.get("/Patient", params={"family": "Baggins"})
    )


def test_search_type_post(client: TestClient, create_response: Response) -> None:
    """Test FHIR search-type interaction using POST."""
    _test_search_type(
        create_response,
        lambda: client.post("/Patient/_search", data={"family": "Baggins"}),
    )


def _test_search_type(
    create_response: Response, search_type_func: Callable[..., Response]
) -> None:
    id_ = _id_from_create_response(create_response)
    search_type_response = search_type_func()

    _assert_expected_response(
        search_type_response,
        status.HTTP_200_OK,
        content={
            "resourceType": "Bundle",
            "type": "searchset",
            "total": 1,
            "entry": [{"resource": _RESOURCE | {"id": id_}}],
        },
    )


def test_update(client: TestClient, create_response: Response) -> None:
    """Test FHIR update interaction."""
    id_ = _id_from_create_response(create_response)
    read_response = client.get(f"/Patient/{id_}")
    content = read_response.json()
    content["name"][0]["given"][0] = "Frodo"
    put_response = client.put(f"/Patient/{id_}", json=content)

    _assert_expected_response(put_response, status.HTTP_200_OK)

    read_response = client.get(f"/Patient/{id_}")

    _assert_expected_response(
        read_response,
        status.HTTP_200_OK,
        content={
            "resourceType": "Patient",
            "id": id_,
            "name": [{"family": "Baggins", "given": ["Frodo"]}],
        },
    )


def test_update_not_found(client: TestClient) -> None:
    """Test FHIR update interaction that produces a 404 not found error."""
    id_ = _generate_fhir_resource_id()
    put_response = client.put(f"/Patient/{id_}", json=_RESOURCE)

    _assert_expected_response(
        put_response,
        status.HTTP_404_NOT_FOUND,
        content=make_operation_outcome(
            severity="error",
            code="not-found",
            details_text=f"Unknown Patient resource '{id_}'",
        ).dict(),
    )


def test_validation_error(client: TestClient) -> None:
    """
    Test FHIR create interaction that produces 400 bad request error due to a validation failure.
    """
    create_response = client.post("/Patient", json={"extraField": []})

    _assert_expected_response(
        create_response,
        status.HTTP_400_BAD_REQUEST,
        content=make_operation_outcome(
            severity="fatal",
            code="structure",
            details_text="1 validation error for Request\nbody -> extraField\n  extra fields not "
            "permitted (type=value_error.extra)",
        ).dict(),
    )


def _generate_fhir_resource_id() -> Id:
    """Generate a UUID-based FHIR Resource ID."""
    return Id(str(uuid4()))


def _id_from_create_response(response: Response) -> str:
    """Extract the resource identifier from a FHIR create interaction response."""
    return response.headers["Location"].split("/")[4]


def _assert_expected_response(
    response: Response, status_code: int, content: dict[str, Any] | None = None
) -> None:
    assert response.status_code == status_code
    assert response.headers["Content-Type"] == "application/fhir+json"
    if content:
        assert response.json() == content
