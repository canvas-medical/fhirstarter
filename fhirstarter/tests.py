from copy import deepcopy
from uuid import uuid4

from fhir.resources.patient import Patient

from . import FHIRInteractionResult, FHIRProvider, FHIRStarter, status
from .exceptions import FHIRResourceNotFoundError
from .testclient import TestClient

_DATABASE: dict[str, Patient] = {}


provider = FHIRProvider()


def _generate_patient_id() -> str:
    return uuid4().hex


@provider.register_create_interaction(Patient)
async def patient_create(resource: Patient) -> FHIRInteractionResult[Patient]:
    patient = deepcopy(resource)
    patient.id = _generate_patient_id()
    _DATABASE[patient.id] = patient

    return FHIRInteractionResult[Patient](patient.id)


@provider.register_read_interaction(Patient)
async def patient_read(id_: str) -> FHIRInteractionResult[Patient]:
    patient = _DATABASE.get(id_)
    if not patient:
        raise FHIRResourceNotFoundError

    return FHIRInteractionResult[Patient](patient.id, patient)


app = FHIRStarter()
app.add_providers(provider)

client = TestClient(app)


def test_patient_create_and_read() -> None:
    response = client.post(
        "/Patient", json={"name": [{"family": "Baggins", "given": ["Bilbo"]}]}
    )

    assert response.status_code == status.HTTP_201_CREATED

    id_ = response.headers["Location"].split("/")[4]
    response = client.get(f"/Patient/{id_}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "resourceType": "Patient",
        "id": id_,
        "name": [{"family": "Baggins", "given": ["Bilbo"]}],
    }


def test_patient_read_not_found() -> None:
    id_ = _generate_patient_id()
    response = client.get(f"/Patient/{id_}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "resourceType": "OperationOutcome",
        "issue": [
            {
                "severity": "error",
                "code": "not-found",
                "details": {"text": f"Unknown Patient resource '{id_}'"},
            }
        ],
    }


def test_validation_error() -> None:
    response = client.post("/Patient", json={"extraField": []})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "resourceType": "OperationOutcome",
        "issue": [
            {
                "severity": "fatal",
                "code": "structure",
                "details": {
                    "text": "1 validation error for Request\nbody -> extraField\n  extra fields not permitted (type=value_error.extra)"
                },
            }
        ],
    }
