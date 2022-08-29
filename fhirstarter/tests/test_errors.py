"""Test FHIRStarter error handling"""

from ..fhirstarter import status
from ..testclient import TestClient
from ..utils import make_operation_outcome
from .fixtures import client_fixture
from .utils import assert_expected_response


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
