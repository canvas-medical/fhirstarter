"""
Standard exception types for reporting errors.

The exception classes defined here provide a response method which will return a Response
containing an OperationOutcome and an HTTP status code.
"""

from abc import ABC, abstractmethod
from typing import Any

from fastapi import Request, status
from fastapi.responses import Response
from fhir.resources.operationoutcome import OperationOutcome

from .utils import (
    format_parameters_from_request,
    format_response,
    make_operation_outcome,
)


class FHIRException(Exception, ABC):
    """
    Abstract base class for all FHIR exceptions.

    This class provides a set_request method that provides concrete subclasses with the request
    object for additional context.
    """

    def __init__(self, *args: Any) -> None:
        super().__init__(*args)
        self._request: Request | None = None

    def response(self) -> Response:
        try:
            format_parameters = format_parameters_from_request(self._request)
        except Exception as exception:
            raise AssertionError(
                "Unable to get format parameters from request; request must be set before the "
                "response is created"
            ) from exception
        else:
            return format_response(
                resource=self._operation_outcome(),
                status_code=self._status_code(),
                format_parameters=format_parameters,
            )

    def set_request(self, request: Request) -> None:
        self._request = request

    @abstractmethod
    def _status_code(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def _operation_outcome(self) -> OperationOutcome:
        raise NotImplementedError


class FHIRGeneralError(FHIRException):
    """
    General FHIR exception class.

    This class allows the caller to pass in a predefined OperationOutcome.
    """

    def __init__(
        self, status_code: int, severity: str, code: str, details_text: str, *args: Any
    ) -> None:
        super().__init__(*args)
        self._status_code_ = status_code
        self._operation_outcome_ = make_operation_outcome(severity, code, details_text)

    @classmethod
    def from_operation_outcome(
        cls, status_code: int, operation_outcome: OperationOutcome
    ) -> "FHIRGeneralError":
        error = FHIRGeneralError(status_code, "severity", "code", "details")
        error._operation_outcome_ = operation_outcome
        return error

    def _status_code(self) -> int:
        return self._status_code_

    def _operation_outcome(self) -> OperationOutcome:
        return self._operation_outcome_


class FHIRUnauthorizedError(FHIRException):
    """FHIR exception class for authentication errors."""

    def __init__(self, code: str, details_text: str, *args: Any) -> None:
        super().__init__(*args)
        self._code = code
        self._details_text = details_text

    def _status_code(self) -> int:
        return status.HTTP_401_UNAUTHORIZED

    def _operation_outcome(self) -> OperationOutcome:
        return make_operation_outcome(
            severity="error", code=self._code, details_text=self._details_text
        )


class FHIRResourceNotFoundError(FHIRException):
    """FHIR exception class for 404 not found errors."""

    def _status_code(self) -> int:
        return status.HTTP_404_NOT_FOUND

    def _operation_outcome(self) -> OperationOutcome:
        try:
            _, resource_type_str, id_ = self._request.url.components.path.split("/")  # type: ignore
        except Exception as exception:
            raise AssertionError(
                "Unable to get resource type and resource ID from request; request must be set"
                "before the response is created"
            ) from exception
        else:
            return make_operation_outcome(
                "error",
                "not-found",
                f"Unknown {resource_type_str} resource '{id_}'",
            )
