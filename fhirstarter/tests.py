from fhir.resources.patient import Patient

from fhirstarter import FHIRProvider, FHIRStarter, status
from fhirstarter.exceptions import FHIRResourceNotFoundError
from fhirstarter.testclient import TestClient

provider = FHIRProvider()


@provider.register_read_interaction(Patient)
async def read(id_: str) -> Patient:
    if id_ != "found":
        raise FHIRResourceNotFoundError

    patient = Patient(**{"name": [{"family": "Baggins", "given": ["Bilbo"]}]})

    return patient


app = FHIRStarter()
app.add_providers(provider)

client = TestClient(app)


def test_patient_read() -> None:
    response = client.get("/Patient/found")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "resourceType": "Patient",
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
