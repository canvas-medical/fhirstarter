from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from fastapi import status
from fastapi.responses import JSONResponse
from fhir.resources.operationoutcome import OperationOutcome
from multimethod import multimethod

from fhirstarter.provider import FHIRProvider


@dataclass
class FHIRExceptionContext:
    provider: FHIRProvider
    operation: str
    kwargs: dict[str, Any]


class FHIRException(Exception, ABC):
    def __init__(self, *args: Any) -> None:
        super().__init__(*args)
        self._context = None

    def response(self) -> JSONResponse:
        return JSONResponse(
            self._operation_outcome().dict(), status_code=self._status_code()
        )

    @property
    def context(self) -> FHIRExceptionContext:
        return self._context

    @context.setter
    def context(self, value: FHIRExceptionContext) -> None:
        self._context = value

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


class FHIRResourceNotFoundError(FHIRException):
    def __init__(self, *args: Any) -> None:
        super().__init__(*args)

    def _status_code(self) -> int:
        return status.HTTP_404_NOT_FOUND

    def _operation_outcome(self) -> OperationOutcome:
        try:
            resource_type = self.context.provider.resource_type()
            resource_id = self.context.kwargs["id_"]
        except Exception as exception:
            raise AssertionError(
                "Unable to get response type and response ID from exception context; "
                "exception context must be set before the response is constructed"
            ) from exception
        else:
            return make_operation_outcome(
                "error",
                "not-found",
                f"Unknown {resource_type} resource '{resource_id}'",
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
