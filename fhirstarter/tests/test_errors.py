"""Test FHIRStarter error handling"""

from fastapi import HTTPException
from fhir.resources.fhirtypes import Id
from fhir.resources.patient import Patient

from ..fhirstarter import FHIRProvider, status
from ..interactions import InteractionContext
from ..testclient import TestClient
from ..utils import make_operation_outcome
from .fixtures import app, client_fixture
from .utils import assert_expected_response, generate_fhir_resource_id


def test_validation_error(client_fixture: TestClient) -> None:
    """
    Test FHIR create interaction that produces 400 bad request error due to a validation failure.
    """
    client = client_fixture

    create_response = client.post("/Patient", json={"extraField": []})

    assert_expected_response(
        create_response,
        status.HTTP_400_BAD_REQUEST,
        content=make_operation_outcome(
            severity="error",
            code="structure",
            details_text="1 validation error for Request\nbody -> extraField\n  extra fields not "
            "permitted (type=value_error.extra)",
        ).dict(),
    )


def test_http_exception() -> None:
    """Test exception handling for HTTP Exceptions."""

    async def patient_read(context: InteractionContext, id_: Id) -> Patient:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    provider = FHIRProvider()
    provider.read(Patient)(patient_read)

    client = app(provider)

    response = client.get(f"/Patient/{generate_fhir_resource_id()}")

    assert_expected_response(
        response,
        status.HTTP_400_BAD_REQUEST,
        content={
            "resourceType": "OperationOutcome",
            "issue": [
                {
                    "severity": "error",
                    "code": "processing",
                    "details": {"text": "Bad Request"},
                }
            ],
        },
    )
