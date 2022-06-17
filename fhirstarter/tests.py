from copy import deepcopy
from typing import Any, cast
from uuid import uuid4

import pytest
from fhir.resources.bundle import Bundle
from fhir.resources.fhirtypes import Id
from fhir.resources.patient import Patient
from funcy import omit
from requests.models import Response

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


async def patient_read(id_: Id) -> FHIRInteractionResult[Patient]:
    patient = _DATABASE.get(id_)
    if not patient:
        raise FHIRResourceNotFoundError

    return FHIRInteractionResult[Patient](resource=patient)


async def patient_search(
    family: str | None = None, **kwargs: Any
) -> FHIRInteractionResult[Bundle]:
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

    return FHIRInteractionResult[Bundle](resource=bundle)


async def patient_update(id_: Id, resource: Patient) -> FHIRInteractionResult[Patient]:
    if id_ not in _DATABASE:
        raise FHIRResourceNotFoundError

    patient = deepcopy(resource)
    _DATABASE[id_] = patient

    return FHIRInteractionResult[Patient](id_=patient.id)


def _app(provider: FHIRProvider) -> TestClient:
    app = FHIRStarter()
    app.add_providers(provider)

    _DATABASE.clear()

    return TestClient(app)


@pytest.fixture
def client() -> TestClient:
    provider = FHIRProvider()
    provider.register_create_interaction(Patient)(patient_create)
    provider.register_read_interaction(Patient)(patient_read)
    provider.register_search_interaction(Patient)(patient_search)
    provider.register_update_interaction(Patient)(patient_update)

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

    _assert_expected_response(response, status.HTTP_200_OK)
    assert omit(response.json(), ["id"]) == {
        "resourceType": "CapabilityStatement",
        "status": "active",
        "date": app._created.isoformat(),
        "kind": "instance",
        "publisher": "Canvas Medical",
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
                            {"code": "search"},
                            {"code": "update"},
                        ],
                        "searchParam": [{"name": "family", "type": "string"}],
                    }
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

    _assert_expected_response(response, status.HTTP_200_OK)
    assert omit(response.json(), ["id"]) == {
        "resourceType": "CapabilityStatement",
        "status": "active",
        "date": app._created.isoformat(),
        "kind": "instance",
        "publisher": "Canvas Medical",
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
    return client.post("/Patient", json=_RESOURCE)


def test_create(create_response: Response) -> None:
    _assert_expected_response(create_response, status.HTTP_201_CREATED)


def test_read(client: TestClient, create_response: Response) -> None:
    id_ = _id_from_create_response(create_response)
    read_response = client.get(f"/Patient/{id_}")

    _assert_expected_response(
        read_response, status.HTTP_200_OK, content=_RESOURCE | {"id": id_}
    )


def test_read_not_found(client: TestClient) -> None:
    id_ = _generate_patient_id()
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


def test_search(client: TestClient, create_response: Response) -> None:
    id_ = _id_from_create_response(create_response)
    search_response = client.get(f"/Patient", params={"family": "Baggins"})

    _assert_expected_response(
        search_response,
        status.HTTP_200_OK,
        content={
            "resourceType": "Bundle",
            "type": "searchset",
            "total": 1,
            "entry": [{"resource": _RESOURCE | {"id": id_}}],
        },
    )


def test_update(client: TestClient, create_response: Response) -> None:
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
    id_ = _generate_patient_id()
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


def _generate_patient_id() -> str:
    return uuid4().hex


def _id_from_create_response(response: Response) -> str:
    return response.headers["Location"].split("/")[4]


def _assert_expected_response(
    response: Response, status_code: int, content: dict[str, Any] | None = None
) -> None:
    assert response.status_code == status_code
    assert response.headers["Content-Type"] == "application/fhir+json"
    if content:
        assert response.json() == content
