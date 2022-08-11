"""FHIRStarter test cases."""

from collections.abc import Callable, Mapping, Sequence
from copy import deepcopy
from tempfile import NamedTemporaryFile
from typing import Any, cast
from uuid import uuid4

import pytest
from _pytest.monkeypatch import MonkeyPatch
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fhir.resources.bundle import Bundle
from fhir.resources.fhirtypes import Id
from fhir.resources.humanname import HumanName
from fhir.resources.patient import Patient
from funcy import omit
from requests.models import Response

from . import status
from .exceptions import FHIRResourceNotFoundError, FHIRUnauthorizedError
from .fhirstarter import FHIRStarter
from .providers import FHIRProvider
from .testclient import TestClient
from .utils import make_operation_outcome

# In-memory "database" used to simulate persistence of created FHIR resources
_DATABASE: dict[str, Patient] = {}

_VALID_TOKEN = "valid"
_INVALID_TOKEN = "invalid"


async def patient_create(resource: Patient, **kwargs: Any) -> Id:
    """Patient create FHIR interaction."""
    patient = deepcopy(resource)
    patient.id = _generate_fhir_resource_id()
    _DATABASE[patient.id] = patient

    return Id(patient.id)


async def patient_read(id_: Id, **kwargs: Any) -> Patient:
    """Patient read FHIR interaction."""
    patient = _DATABASE.get(id_)
    if not patient:
        raise FHIRResourceNotFoundError

    return patient


async def patient_search_type(
    family: str | None = None,
    general_practitioner: str | None = None,
    custom: str | None = None,
    _last_updated: str | None = None,
    **kwargs: Any,
) -> Bundle:
    """Patient search-type FHIR interaction."""
    patients = []
    for patient in _DATABASE.values():
        for name in patient.name:
            if cast(HumanName, name).family == family:
                patients.append(patient)

    bundle = Bundle(
        **{
            "type": "searchset",
            "total": len(patients),
            "entry": [{"resource": {**patient.dict()}} for patient in patients],
        }
    )

    return bundle


async def patient_update(id_: Id, resource: Patient, **kwargs: Any) -> Id:
    """Patient update FHIR interaction."""
    if id_ not in _DATABASE:
        raise FHIRResourceNotFoundError

    patient = deepcopy(resource)
    _DATABASE[id_] = patient

    return Id(patient.id)


def _app(provider: FHIRProvider) -> TestClient:
    """Create a FHIRStarter app, add the provider, reset the database, and return a TestClient."""
    config_file_contents = """
[search-parameters.Patient.custom]
type = "string"
description = "Custom search parameter"
uri = "uri"
include-in-capability-statement = true
    """

    with NamedTemporaryFile("w") as config_file:
        config_file.write(config_file_contents)
        config_file.seek(0)
        app = FHIRStarter(config_file_name=config_file.name)

    app.add_providers(provider)

    _DATABASE.clear()

    return TestClient(app)


@pytest.fixture
def client() -> TestClient:
    """Test fixture that creates an app that provides all FHIR interactions."""
    return _client()


def _client() -> TestClient:
    """Create an app that provides all FHIR interactions."""
    provider = FHIRProvider()
    provider.register_create_interaction(Patient)(patient_create)
    provider.register_read_interaction(Patient)(patient_read)
    provider.register_search_type_interaction(Patient)(patient_search_type)
    provider.register_update_interaction(Patient)(patient_update)

    return _app(provider)


@pytest.fixture
def client_create_and_read() -> TestClient:
    """Test fixture that creates an app that only provides FHIR create and read interactions."""
    return _client_create_and_read()


def _client_create_and_read() -> TestClient:
    """Create an app that only provides FHIR create and read interactions."""
    provider = FHIRProvider()
    provider.register_create_interaction(Patient)(patient_create)
    provider.register_read_interaction(Patient)(patient_read)

    return _app(provider)


@pytest.mark.parametrize(
    argnames="test_client,resource",
    argvalues=[
        (
            _client(),
            [
                {
                    "type": "Patient",
                    "interaction": [
                        {"code": "create"},
                        {"code": "read"},
                        {"code": "search-type"},
                        {"code": "update"},
                    ],
                    "searchParam": [
                        {
                            "name": "family",
                            "definition": "http://hl7.org/fhir/SearchParameter/individual-family",
                            "type": "string",
                            "documentation": "A portion of the family name of the patient",
                        },
                        {
                            "name": "general-practitioner",
                            "definition": "http://hl7.org/fhir/SearchParameter/Patient-general-practitioner",
                            "type": "reference",
                            "documentation": "Patient's nominated general practitioner, not the organization that manages the record",
                        },
                        {
                            "name": "custom",
                            "definition": "uri",
                            "type": "string",
                            "documentation": "Custom search parameter",
                        },
                        {
                            "name": "_lastUpdated",
                            "definition": "http://hl7.org/fhir/SearchParameter/Resource-lastUpdated",
                            "type": "date",
                            "documentation": "When the resource version last changed",
                        },
                    ],
                }
            ],
        ),
        (
            _client_create_and_read(),
            [
                {
                    "type": "Patient",
                    "interaction": [{"code": "create"}, {"code": "read"}],
                },
            ],
        ),
    ],
    ids=["all", "create_and_read"],
)
def test_capability_statement(
    test_client: TestClient, resource: Sequence[Mapping[str, Any]]
) -> None:
    """
    Test the capability statement.

    Two scenarios are parameterized: a server with create, read, search, and update supported, and
    a server with only create and read supported.
    """
    client = test_client
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
                "resource": resource,
            }
        ],
    }


def test_capability_statement_publisher(
    client_create_and_read: TestClient, monkeypatch: MonkeyPatch
) -> None:
    """Test the capability statement publisher value that is provided by an environment variable."""
    monkeypatch.setenv("CAPABILITY_STATEMENT_PUBLISHER", "Publisher")

    client = client_create_and_read

    response = client.get("/metadata")

    _assert_expected_response(response, status.HTTP_200_OK)
    assert response.json()["publisher"] == "Publisher"


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


@pytest.mark.parametrize(
    argnames="search_type_func",
    argvalues=[
        lambda client: client.get("/Patient", params={"family": "Baggins"}),
        lambda client: client.post("/Patient/_search", data={"family": "Baggins"}),
    ],
    ids=["get", "post"],
)
def test_search_type(
    client: TestClient,
    create_response: Response,
    search_type_func: Callable[[TestClient], Response],
) -> None:
    """Test the FHIR search interaction."""
    id_ = _id_from_create_response(create_response)
    search_type_response = search_type_func(client)

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
            severity="error",
            code="structure",
            details_text="1 validation error for Request\nbody -> extraField\n  extra fields not "
            "permitted (type=value_error.extra)",
        ).dict(),
    )


def validate_token(
    authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> None:
    if authorization.scheme != "Bearer" or authorization.credentials != _VALID_TOKEN:
        raise FHIRUnauthorizedError(
            code="unknown", details_text="Authentication failed"
        )


def provider_with_dependency() -> FHIRProvider:
    provider = FHIRProvider(dependencies=[Depends(validate_token)])
    provider.register_create_interaction(Patient)(patient_create)

    return provider


def provider_with_interaction_dependency() -> FHIRProvider:
    provider = FHIRProvider()
    provider.register_create_interaction(
        Patient, dependencies=[Depends(validate_token)]
    )(patient_create)

    return provider


@pytest.mark.parametrize(
    argnames="provider",
    argvalues=[provider_with_dependency(), provider_with_interaction_dependency()],
    ids=["provider", "interaction"],
)
def test_dependency(provider: FHIRProvider) -> None:
    """Test that injected token validation dependency works on the given provider."""
    client = _app(provider)

    create_response = client.post(
        "/Patient",
        json=_RESOURCE,
        headers={"Authorization": f"Bearer {_INVALID_TOKEN}"},
    )
    _assert_expected_response(
        create_response,
        status.HTTP_401_UNAUTHORIZED,
        content={
            "resourceType": "OperationOutcome",
            "issue": [
                {
                    "severity": "error",
                    "code": "unknown",
                    "details": {"text": "Authentication failed"},
                }
            ],
        },
    )

    create_response = client.post(
        "/Patient", json=_RESOURCE, headers={"Authorization": f"Bearer {_VALID_TOKEN}"}
    )
    _assert_expected_response(create_response, status.HTTP_201_CREATED)


def _generate_fhir_resource_id() -> Id:
    """Generate a UUID-based FHIR Resource ID."""
    return Id(str(uuid4()))


def _id_from_create_response(response: Response) -> str:
    """Extract the resource identifier from a FHIR create interaction response."""
    return response.headers["Location"].split("/")[4]


def _assert_expected_response(
    response: Response, status_code: int, content: dict[str, Any] | None = None
) -> None:
    """Assert the status code, content type header, and content of a response."""
    assert response.status_code == status_code
    assert response.headers["Content-Type"] == "application/fhir+json"
    if content:
        assert response.json() == content
