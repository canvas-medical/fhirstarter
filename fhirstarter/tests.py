from copy import deepcopy
from typing import cast
from uuid import uuid4

import pytest
from fastapi import Response
from fhir.resources.fhirtypes import Id
from fhir.resources.patient import Patient
from funcy import omit

from . import status
from .exceptions import FHIRResourceNotFoundError
from .fhirstarter import FHIRStarter
from .provider import FHIRInteractionResult, FHIRProvider
from .testclient import TestClient
from .utils import make_operation_outcome

_DATABASE: dict[str, Patient] = {}


async def patient_create(resource: Patient) -> FHIRInteractionResult[Patient]:
    patient = deepcopy(resource)
    patient.id = _generate_patient_id()
    _DATABASE[patient.id] = patient

    return FHIRInteractionResult[Patient](id_=patient.id)


async def patient_update(id_: Id, resource: Patient) -> FHIRInteractionResult[Patient]:
    if id_ not in _DATABASE:
        raise FHIRResourceNotFoundError

    patient = deepcopy(resource)
    _DATABASE[id_] = patient

    return FHIRInteractionResult[Patient](id_=patient.id)


async def patient_read(id_: Id) -> FHIRInteractionResult[Patient]:
    patient = _DATABASE.get(id_)
    if not patient:
        raise FHIRResourceNotFoundError

    return FHIRInteractionResult[Patient](resource=patient)


def _app(provider: FHIRProvider) -> TestClient:
    app = FHIRStarter()
    app.add_providers(provider)

    _DATABASE.clear()

    return TestClient(app)


@pytest.fixture
def client() -> TestClient:
    provider = FHIRProvider()
    provider.register_create_interaction(Patient)(patient_create)
    provider.register_update_interaction(Patient)(patient_update)
    provider.register_read_interaction(Patient)(patient_read)

    return _app(provider)


@pytest.fixture
def client_create_and_read() -> TestClient:
    provider = FHIRProvider()
    provider.register_create_interaction(Patient)(patient_create)
    provider.register_read_interaction(Patient)(patient_read)

    return _app(provider)


def test_capability_statement(client: TestClient) -> None:
    app = cast(FHIRStarter, client.app)

    response = client.get("/metadata")

    assert response.status_code == status.HTTP_200_OK
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
                    {"type": "Patient", "interaction": [{"code": "create"}]},
                    {"type": "Patient", "interaction": [{"code": "update"}]},
                    {"type": "Patient", "interaction": [{"code": "read"}]},
                ],
            }
        ],
    }


def test_capability_statement_create_and_read(
    client_create_and_read: TestClient,
) -> None:
    client = client_create_and_read
    app = cast(FHIRStarter, client.app)

    response = client.get("/metadata")

    assert response.status_code == status.HTTP_200_OK
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
                    {"type": "Patient", "interaction": [{"code": "create"}]},
                    {"type": "Patient", "interaction": [{"code": "read"}]},
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
    return cast(Response, client.post("/Patient", json=_RESOURCE))


def test_create(create_response: Response) -> None:
    assert create_response.status_code == status.HTTP_201_CREATED


def test_update(client: TestClient, create_response: Response) -> None:
    id_ = _id_from_create_response(create_response)
    read_response = client.get(f"/Patient/{id_}")
    content = read_response.json()
    content["name"][0]["given"][0] = "Frodo"
    put_response = client.put(f"/Patient/{id_}", json=content)

    assert put_response.status_code == status.HTTP_200_OK

    read_response = client.get(f"/Patient/{id_}")

    assert read_response.status_code == status.HTTP_200_OK
    assert read_response.json() == {
        "resourceType": "Patient",
        "id": id_,
        "name": [{"family": "Baggins", "given": ["Frodo"]}],
    }


def test_update_not_found(client: TestClient) -> None:
    id_ = _generate_patient_id()
    put_response = client.put(f"/Patient/{id_}", json=_RESOURCE)

    operation_outcome = make_operation_outcome(
        severity="error",
        code="not-found",
        details_text=f"Unknown Patient resource '{id_}'",
    )

    assert put_response.status_code == status.HTTP_404_NOT_FOUND
    assert put_response.json() == operation_outcome.dict()


def test_read(client: TestClient, create_response: Response) -> None:
    id_ = _id_from_create_response(create_response)
    read_response = client.get(f"/Patient/{id_}")

    assert read_response.status_code == status.HTTP_200_OK
    assert read_response.json() == _RESOURCE | {"id": id_}


def test_read_not_found(client: TestClient) -> None:
    id_ = _generate_patient_id()
    response = client.get(f"/Patient/{id_}")

    operation_outcome = make_operation_outcome(
        severity="error",
        code="not-found",
        details_text=f"Unknown Patient resource '{id_}'",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == operation_outcome.dict()


def test_validation_error(client: TestClient) -> None:
    create_response = client.post("/Patient", json={"extraField": []})

    operation_outcome = make_operation_outcome(
        severity="fatal",
        code="structure",
        details_text="1 validation error for Request\nbody -> extraField\n  extra fields not "
        "permitted (type=value_error.extra)",
    )

    assert create_response.status_code == status.HTTP_400_BAD_REQUEST
    assert create_response.json() == operation_outcome.dict()


def _generate_patient_id() -> str:
    return uuid4().hex


def _id_from_create_response(response: Response) -> str:
    return response.headers["Location"].split("/")[4]
