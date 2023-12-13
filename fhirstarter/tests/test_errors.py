"""Test FHIRStarter error handling"""

import json
from collections.abc import Callable, Coroutine, Mapping
from typing import Any, cast

import pytest
from fastapi import HTTPException

from ..exceptions import (
    FHIRBadRequestError,
    FHIRConflictError,
    FHIRForbiddenError,
    FHIRGoneError,
    FHIRMethodNotAllowedError,
    FHIRNotAcceptableError,
    FHIRPreconditionFailedError,
    FHIRUnauthorizedError,
    FHIRUnprocessableEntityError,
    FHIRUnsupportedMediaTypeError,
)
from ..fhirstarter import FHIRProvider, FHIRStarter, Request, Response, status
from ..testclient import TestClient
from ..utils import make_operation_outcome
from .config import app
from .resources import Patient
from .utils import assert_expected_response, generate_fhir_resource_id


@pytest.mark.parametrize(
    argnames="client,request_body,response_body",
    argvalues=[
        (
            ("create", "read", "search-type", "update"),
            " ",
            make_operation_outcome(
                severity="error",
                code="structure",
                details_text="body -> 1 — JSON decode error (type=json_invalid; error=Expecting value)",
            ),
        ),
        (
            ("create", "read", "search-type", "update"),
            {"extraField": []},
            make_operation_outcome(
                severity="error",
                code="structure",
                details_text="body -> extraField — extra fields not permitted "
                "(type=value_error.extra)",
            ),
        ),
        (
            ("create", "read", "search-type", "update"),
            {"communication": [{}]},
            make_operation_outcome(
                severity="error",
                code="required",
                details_text="body -> communication -> 0 -> language — field required "
                "(type=value_error.missing)",
            ),
        ),
        (
            ("create", "read", "search-type", "update"),
            {"id": ""},
            make_operation_outcome(
                severity="error",
                code="value",
                details_text="body -> id — ensure this value has at least 1 characters "
                "(type=value_error.any_str.min_length; limit_value=1)",
            ),
        ),
        (
            ("create", "read", "search-type", "update"),
            {"name": 0},
            make_operation_outcome(
                severity="error",
                code="value",
                details_text="body -> name — value is not a valid list (type=type_error.list)",
            ),
        ),
        (
            ("create", "read", "search-type", "update"),
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
    indirect=["client"],
)
def test_validation_error(
    client: TestClient,
    request_body: Mapping[str, Any] | str,
    response_body: Mapping[str, Any],
) -> None:
    """
    Test FHIR create interaction that produces 400 bad request error due to a validation failure.
    """
    if isinstance(request_body, Mapping):
        request_body = json.dumps(request_body)

    create_response = client.post("/Patient", content=request_body)

    assert_expected_response(
        create_response,
        status.HTTP_400_BAD_REQUEST,
        content=response_body,
    )


def _handler_exception_async(
    exception: HTTPException,
) -> Callable[..., Coroutine[None, None, Patient]]:
    """Return an async Patient read handler."""

    async def patient_read(*_: Any) -> Patient:
        raise exception

    return patient_read


def _handler_exception(exception: HTTPException) -> Callable[..., Patient]:
    """Return a Patient read handler."""

    def patient_read(*_: Any) -> Patient:
        raise exception

    return patient_read


@pytest.mark.parametrize(
    argnames="exception,status_code,issue",
    argvalues=[
        (
            HTTPException(status_code=status.HTTP_400_BAD_REQUEST),
            status.HTTP_400_BAD_REQUEST,
            {
                "severity": "error",
                "code": "processing",
                "details": {"text": "Bad Request"},
            },
        ),
        (
            FHIRBadRequestError(code="processing", details_text="Error"),
            status.HTTP_400_BAD_REQUEST,
            {
                "severity": "error",
                "code": "processing",
                "details": {"text": "Error"},
            },
        ),
        (
            FHIRUnauthorizedError(details_text="Error"),
            status.HTTP_401_UNAUTHORIZED,
            {
                "severity": "error",
                "code": "unknown",
                "details": {"text": "Error"},
            },
        ),
        (
            FHIRForbiddenError(details_text="Error"),
            status.HTTP_403_FORBIDDEN,
            {
                "severity": "error",
                "code": "forbidden",
                "details": {"text": "Error"},
            },
        ),
        (
            FHIRMethodNotAllowedError(details_text="Error"),
            status.HTTP_405_METHOD_NOT_ALLOWED,
            {
                "severity": "error",
                "code": "not-supported",
                "details": {"text": "Error"},
            },
        ),
        (
            FHIRNotAcceptableError(details_text="Error"),
            status.HTTP_406_NOT_ACCEPTABLE,
            {
                "severity": "error",
                "code": "not-supported",
                "details": {"text": "Error"},
            },
        ),
        (
            FHIRConflictError(details_text="Error"),
            status.HTTP_409_CONFLICT,
            {
                "severity": "error",
                "code": "conflict",
                "details": {"text": "Error"},
            },
        ),
        (
            FHIRGoneError(details_text="Error"),
            status.HTTP_410_GONE,
            {
                "severity": "error",
                "code": "deleted",
                "details": {"text": "Error"},
            },
        ),
        (
            FHIRPreconditionFailedError(details_text="Error"),
            status.HTTP_412_PRECONDITION_FAILED,
            {
                "severity": "error",
                "code": "conflict",
                "details": {"text": "Error"},
            },
        ),
        (
            FHIRUnsupportedMediaTypeError(details_text="Error"),
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            {
                "severity": "error",
                "code": "not-supported",
                "details": {"text": "Error"},
            },
        ),
        (
            FHIRUnprocessableEntityError(code="invalid", details_text="Error"),
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            {
                "severity": "error",
                "code": "invalid",
                "details": {"text": "Error"},
            },
        ),
    ],
    ids=[
        "http",
        "bad request",
        "unauthorized",
        "forbidden",
        "method not allowed",
        "not acceptable",
        "conflict",
        "gone",
        "precondition failed",
        "unsupported media type",
        "unprocessable entity",
    ],
)
@pytest.mark.parametrize(
    argnames="handler_func",
    argvalues=[_handler_exception_async, _handler_exception],
    ids=["async", "nonasync"],
)
def test_exception(
    exception: HTTPException,
    status_code: int,
    issue: Mapping[str, Any],
    handler_func: Callable[
        [HTTPException],
        Callable[..., Coroutine[None, None, Patient]] | Callable[..., Patient],
    ],
) -> None:
    """Test exception handling for HTTP and FHIR exceptions."""
    handler = handler_func(exception)

    provider = FHIRProvider()
    provider.read(Patient)(handler)

    client = app(provider)

    response = client.get(f"/Patient/{generate_fhir_resource_id()}")

    assert_expected_response(
        response,
        status_code,
        content={
            "resourceType": "OperationOutcome",
            "issue": [issue],
        },
    )


@pytest.mark.parametrize(
    argnames="client",
    argvalues=[("create", "read", "search-type", "update")],
    ids=["all"],
    indirect=True,
)
def test_set_exception_callback(client: TestClient) -> None:
    """Test set_exception_callback."""
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
