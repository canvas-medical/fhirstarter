import pytest
from fastapi import status
from fastapi.testclient import TestClient
from fhir.resources.patient import Patient

from fhirstarter import FHIRProvider, FHIRStarter
from fhirstarter.exceptions import FHIRResourceNotFoundError


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


@pytest.mark.anyio
def test_patient_read():
    assert client.get("/Patient/found").status_code == status.HTTP_200_OK


@pytest.mark.anyio
def test_patient_read_not_found():
    assert client.get("/Patient/notfound").status_code == status.HTTP_404_NOT_FOUND
