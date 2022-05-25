from abc import ABC, abstractmethod
from typing import Any

from fastapi import status
from fastapi.responses import JSONResponse
from fhir.resources.operationoutcome import OperationOutcome
from multimethod import multimethod


class FHIRException(Exception, ABC):
    def response(self) -> JSONResponse:
        return JSONResponse(
            self._operation_outcome().dict(), status_code=self._status_code()
        )

    @abstractmethod
    def _status_code(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def _operation_outcome(self) -> OperationOutcome:
        raise NotImplementedError


class FHIRError(FHIRException):
    @multimethod
    def __init__(
        self, status_code: int, severity: str, code: str, details_text: str, *args: Any
    ) -> None:
        self.__init__(
            status_code, make_operation_outcome(severity, code, details_text), *args
        )

    @multimethod
    def __init__(
        self, status_code: int, operation_outcome: OperationOutcome, *args: Any
    ) -> None:
        super().__init__(*args)
        self._status_code = status_code
        self._operation_outcome = operation_outcome

    def _status_code(self) -> int:
        return self._status_code

    def _operation_outcome(self) -> OperationOutcome:
        return self._operation_outcome


class FHIRResourceError(FHIRException, ABC):
    def __init__(self, *args: Any) -> None:
        super().__init__(*args)
        self._resource_type = None

    def set_resource_type(self, resource_type: str) -> None:
        self._resource_type = resource_type


class FHIRResourceNotFoundError(FHIRResourceError):
    def __init__(self, resource_id: str, *args: Any) -> None:
        super().__init__(*args)
        self._resource_id = resource_id

    def _status_code(self) -> int:
        return status.HTTP_404_NOT_FOUND

    def _operation_outcome(self) -> OperationOutcome:
        assert (
            self._resource_type is not None
        ), "Resource type must be set before the response is constructed"
        return make_operation_outcome(
            "error",
            "not-found",
            f"Unknown {self._resource_type} resource '{self._resource_id}'",
        )


def make_operation_outcome(
    severity: str, code: str, details_text: str
) -> OperationOutcome:
    return OperationOutcome(
        **{
            "issue": [
                {
                    "severity": severity,
                    "code": code,
                    "details": {"text": details_text},
                }
            ]
        }
    )
