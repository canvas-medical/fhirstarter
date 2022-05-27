from fhirstarter import FHIRProvider, FHIRStarter, status
from fhirstarter.exceptions import FHIRResourceNotFoundError
from fhirstarter.resources import Patient
from fhirstarter.testclient import TestClient


class PatientProvider(FHIRProvider):
    def resource_obj_type(self) -> type:
        return Patient

    @staticmethod
    async def read(id_: str) -> Patient:
        if id_ != "found":
            raise FHIRResourceNotFoundError

        patient = Patient(**{"name": [{"family": "Baggins", "given": ["Bilbo"]}]})

        return patient


app = FHIRStarter()
app.add_providers(PatientProvider())

client = TestClient(app)


def test_patient_read():
    assert client.get("/Patient/found").status_code == status.HTTP_200_OK


def test_patient_read_not_found():
    assert client.get("/Patient/notfound").status_code == status.HTTP_404_NOT_FOUND
