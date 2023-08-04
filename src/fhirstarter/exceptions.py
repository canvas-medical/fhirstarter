"""
Standard exception types for reporting errors.

The exception classes defined here provide a response method which will return a Response
containing an OperationOutcome and an HTTP status code.
"""

from abc import ABC, abstractmethod

from fastapi import Request, status
from fastapi.exceptions import HTTPException
from fhir.resources.operationoutcome import OperationOutcome

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


class FHIRUnauthorizedError(FHIRException):
    """FHIR exception class for 401 authentication errors."""

    def __init__(self, details_text: str) -> None:
        super().__init__(status.HTTP_401_UNAUTHORIZED, details_text)

    def operation_outcome(self) -> OperationOutcome:
        return make_operation_outcome(
            severity="error", code="unknown", details_text=self.detail
        )


class FHIRForbiddenError(FHIRException):
    """FHIR exception class for 403 forbidden errors."""

    def __init__(self, details_text: str) -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, details_text)

    def operation_outcome(self) -> OperationOutcome:
        return make_operation_outcome(
            severity="error", code="forbidden", details_text=self.detail
        )


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
