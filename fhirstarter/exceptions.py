"""
Standard exception types for reporting errors.

The exception classes defined here provide a method which will return an OperationOutcome.
"""

from abc import ABC, abstractmethod

from fastapi import Request, status
from fastapi.exceptions import HTTPException

from .resources import OperationOutcome
from .utils import make_operation_outcome, parse_fhir_request


class FHIRException(HTTPException, ABC):
    """
    Abstract base class for all FHIR exceptions.

    This class provides a set_request method that provides concrete subclasses with the request
    object for additional context.
    """

    def __init__(self, status_code: int, details_text: str | None = None) -> None:
        super().__init__(status_code, detail=details_text)
        self._request: Request | None = None

    def set_request(self, request: Request) -> None:
        self._request = request

    @abstractmethod
    def operation_outcome(self) -> OperationOutcome:
        raise NotImplementedError


class FHIRHTTPException(FHIRException):
    """
    Abstract base class for FHIR errors that map neatly to OperationOutcome issue type codes.
    Example: HTTP status code 409 <-> OperationOutcome issue type code "conflict"

    If these mappings are not desired, FHIRGeneralError can be used to create the exact desired
    response.
    """

    _STATUS_CODE_MAPPINGS = {
        401: "unknown",
        403: "forbidden",
        405: "not-supported",
        406: "not-supported",
        409: "conflict",
        410: "deleted",
        412: "conflict",
        415: "not-supported",
    }

    def __init__(self, details_text: str | None = None):
        super().__init__(self._status_code(), details_text)

    def operation_outcome(self) -> OperationOutcome:
        return make_operation_outcome(
            severity="error",
            code=self._STATUS_CODE_MAPPINGS[self._status_code()],
            details_text=self.detail,
        )

    @classmethod
    @abstractmethod
    def _status_code(cls) -> int:
        raise NotImplementedError


class FHIRGeneralError(FHIRException):
    """
    General FHIR exception class.

    This class allows the caller to pass in a predefined OperationOutcome.
    """

    def __init__(
        self, status_code: int, severity: str, code: str, details_text: str
    ) -> None:
        super().__init__(status_code, details_text)
        self._operation_outcome_ = make_operation_outcome(severity, code, details_text)

    @classmethod
    def from_operation_outcome(
        cls, status_code: int, operation_outcome: OperationOutcome
    ) -> "FHIRGeneralError":
        error = FHIRGeneralError(status_code, "severity", "code", "details")
        error._operation_outcome_ = operation_outcome
        return error

    def operation_outcome(self) -> OperationOutcome:
        return self._operation_outcome_


class FHIRBadRequestError(FHIRException):
    """FHIR exception class for 400 bad request errors."""

    def __init__(self, code: str, details_text: str) -> None:
        super().__init__(status.HTTP_400_BAD_REQUEST, details_text)
        self._code = code

    def operation_outcome(self) -> OperationOutcome:
        return make_operation_outcome(
            severity="error", code=self._code, details_text=self.detail
        )


class FHIRUnauthorizedError(FHIRHTTPException):
    """FHIR exception class for 401 unauthorized errors."""

    @classmethod
    def _status_code(cls) -> int:
        return status.HTTP_401_UNAUTHORIZED


class FHIRForbiddenError(FHIRHTTPException):
    """FHIR exception class for 403 forbidden errors."""

    @classmethod
    def _status_code(cls) -> int:
        return status.HTTP_403_FORBIDDEN


class FHIRResourceNotFoundError(FHIRException):
    """FHIR exception class for 404 not found errors."""

    def __init__(self) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND)

    def operation_outcome(self) -> OperationOutcome:
        try:
            interaction_info = parse_fhir_request(self._request)
        except Exception as exception:
            raise AssertionError(
                "Unable to get resource type and resource ID from request; request must be set "
                "before the response is created"
            ) from exception
        else:
            return make_operation_outcome(
                "error",
                "not-found",
                f"Unknown {interaction_info.resource_type} resource "
                f"'{interaction_info.resource_id}'",
            )


class FHIRMethodNotAllowedError(FHIRHTTPException):
    """FHIR exception class for 405 method not allowed errors."""

    @classmethod
    def _status_code(cls) -> int:
        return status.HTTP_405_METHOD_NOT_ALLOWED


class FHIRNotAcceptableError(FHIRHTTPException):
    """FHIR exception class for 406 not acceptable errors."""

    @classmethod
    def _status_code(cls) -> int:
        return status.HTTP_406_NOT_ACCEPTABLE


class FHIRConflictError(FHIRHTTPException):
    """FHIR exception class for 409 conflict errors."""

    @classmethod
    def _status_code(cls) -> int:
        return status.HTTP_409_CONFLICT


class FHIRGoneError(FHIRHTTPException):
    """FHIR exception class for 410 gone errors."""

    @classmethod
    def _status_code(cls) -> int:
        return status.HTTP_410_GONE


class FHIRPreconditionFailedError(FHIRHTTPException):
    """FHIR exception class for 412 precondition failed errors."""

    @classmethod
    def _status_code(cls) -> int:
        return status.HTTP_412_PRECONDITION_FAILED


class FHIRUnsupportedMediaTypeError(FHIRHTTPException):
    """FHIR exception class for 415 unsupported media type errors."""

    @classmethod
    def _status_code(cls) -> int:
        return status.HTTP_415_UNSUPPORTED_MEDIA_TYPE


class FHIRUnprocessableEntityError(FHIRException):
    """FHIR exception class for 422 unprocessable entity errors."""

    def __init__(self, code: str, details_text: str) -> None:
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, details_text)
        self._code = code

    def operation_outcome(self) -> OperationOutcome:
        return make_operation_outcome(
            severity="error", code=self._code, details_text=self.detail
        )
