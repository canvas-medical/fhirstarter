from uuid import uuid4

from fhir.resources.patient import Patient

from . import FHIRInteractionResult, FHIRProvider, FHIRStarter, status
from .exceptions import FHIRResourceNotFoundError
from .testclient import TestClient

_ID = uuid4().hex

provider = FHIRProvider()


@provider.register_read_interaction(Patient)
async def read(id_: str) -> FHIRInteractionResult[Patient]:
    if id_ != "found":
        raise FHIRResourceNotFoundError

    patient = Patient(
        **{"id": _ID, "name": [{"family": "Baggins", "given": ["Bilbo"]}]}
    )

    return FHIRInteractionResult[Patient](patient.id, patient)


app = FHIRStarter()
app.add_providers(provider)

client = TestClient(app)


def test_patient_read() -> None:
    response = client.get("/Patient/found")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "resourceType": "Patient",
        "id": _ID,
        "name": [{"family": "Baggins", "given": ["Bilbo"]}],
    }


def test_patient_read_not_found() -> None:
    response = client.get("/Patient/notfound")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "resourceType": "OperationOutcome",
        "issue": [
            {
                "severity": "error",
                "code": "not-found",
                "details": {"text": "Unknown Patient resource 'notfound'"},
            }
        ],
    }
