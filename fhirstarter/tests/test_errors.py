"""Test FHIRStarter error handling"""

import json
from collections.abc import Mapping
from typing import Any, cast

import pytest
from fastapi import HTTPException
from fhir.resources.patient import Patient

from ..fhirstarter import FHIRProvider, FHIRStarter, Request, Response, status
from ..testclient import TestClient
from ..utils import make_operation_outcome
from .config import app
from .utils import assert_expected_response, generate_fhir_resource_id


@pytest.mark.parametrize(
    argnames="request_body,response_body",
    argvalues=[
        (
            " ",
            make_operation_outcome(
                severity="error",
                code="structure",
                details_text="body -> 1 — Expecting value: line 1 column 2 (char 1) "
                "(type=value_error.jsondecode; msg=Expecting value; doc= ; pos=1; lineno=1; "
                "colno=2)",
            ),
        ),
        (
            {"extraField": []},
            make_operation_outcome(
                severity="error",
                code="structure",
                details_text="body -> extraField — extra fields not permitted "
                "(type=value_error.extra)",
            ),
        ),
        (
            {"communication": [{}]},
            make_operation_outcome(
                severity="error",
                code="required",
                details_text="body -> communication -> 0 -> language — field required "
                "(type=value_error.missing)",
            ),
        ),
        (
            {"id": ""},
            make_operation_outcome(
                severity="error",
                code="value",
                details_text="body -> id — ensure this value has at least 1 characters "
                "(type=value_error.any_str.min_length; limit_value=1)",
            ),
        ),
        (
            {"name": 0},
            make_operation_outcome(
                severity="error",
                code="value",
                details_text="body -> name — value is not a valid list (type=type_error.list)",
            ),
        ),
        (
            {"extraField": [], "communication": [{}]},
            {
                "resourceType": "OperationOutcome",
                "issue": [
                    {
                        "severity": "error",
                        "code": "required",
                        "details": {
                            "text": "body -> communication -> 0 -> language — field required "
                            "(type=value_error.missing)"
                        },
                    },
                    {
                        "severity": "error",
                        "code": "structure",
                        "details": {
                            "text": "body -> extraField — extra fields not permitted "
                            "(type=value_error.extra)"
                        },
                    },
                ],
            },
        ),
    ],
    ids=[
        "JSON decode error",
        "extra value",
        "missing value",
        "value error",
        "type error",
        "multiple errors",
    ],
)
def test_validation_error(
    client_fixture: TestClient,
    request_body: Mapping[str, Any] | str,
    response_body: Mapping[str, Any],
) -> None:
    """
    Test FHIR create interaction that produces 400 bad request error due to a validation failure.
    """
    client = client_fixture

    if isinstance(request_body, Mapping):
        request_body = json.dumps(request_body)

    create_response = client.post("/Patient", content=request_body)

    assert_expected_response(
        create_response,
        status.HTTP_400_BAD_REQUEST,
        content=response_body,
    )


def test_http_exception() -> None:
    """Test exception handling for HTTP Exceptions."""

    async def patient_read(*_: Any) -> Patient:
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


def test_set_exception_callback(client_fixture: TestClient) -> None:
    """Test set_exception_callback."""
    client = client_fixture
    test_app = cast(FHIRStarter, client.app)

    async def callback(_: Request, response_: Response, __: Exception) -> Response:
        # Change the status code from 404 to 400 so that we can test that the callback was actually
        # called.
        response_.status_code = status.HTTP_400_BAD_REQUEST
        return response_

    test_app.set_exception_callback(callback)

    id_ = generate_fhir_resource_id()
    response = client.get(f"/Patient/{id_}")

    assert_expected_response(
        response,
        status.HTTP_400_BAD_REQUEST,
        content={
            "resourceType": "OperationOutcome",
            "issue": [
                {
                    "severity": "error",
                    "code": "not-found",
                    "details": {"text": f"Unknown Patient resource '{id_}'"},
                }
            ],
        },
    )
