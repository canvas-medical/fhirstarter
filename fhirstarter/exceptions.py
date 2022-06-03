from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from fastapi import status
from fastapi.responses import JSONResponse
from fhir.resources.operationoutcome import OperationOutcome

from fhirstarter.provider import FHIRInteraction


@dataclass
class FHIRExceptionContext:
    interaction: FHIRInteraction
    kwargs: dict[str, Any]


class FHIRException(Exception, ABC):
    def __init__(self, *args: Any) -> None:
        super().__init__(*args)
        self._context: FHIRExceptionContext | None = None

    def response(self, context: FHIRExceptionContext) -> JSONResponse:
        self._context = context
        return JSONResponse(
            self._operation_outcome().dict(), status_code=self._status_code()
        )

    @property
    def context(self) -> FHIRExceptionContext | None:
        return self._context

    @abstractmethod
    def _status_code(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def _operation_outcome(self) -> OperationOutcome:
        raise NotImplementedError


class FHIRError(FHIRException):
    def __init__(
        self, status_code: int, severity: str, code: str, details_text: str, *args: Any
    ) -> None:
        super().__init__(*args)
        self._status_code_ = status_code
        self._operation_outcome_ = make_operation_outcome(severity, code, details_text)

    @classmethod
    def from_operation_outcome(
        cls, status_code: int, operation_outcome: OperationOutcome
    ) -> "FHIRError":
        error = FHIRError(status_code, "severity", "code", "details")
        error._operation_outcome_ = operation_outcome
        return error

    def _status_code(self) -> int:
        return self._status_code_

    def _operation_outcome(self) -> OperationOutcome:
        return self._operation_outcome_


class FHIRResourceNotFoundError(FHIRException):
    def __init__(self, *args: Any) -> None:
        super().__init__(*args)

    def _status_code(self) -> int:
        return status.HTTP_404_NOT_FOUND

    def _operation_outcome(self) -> OperationOutcome:
        try:
            resource_type = self.context.interaction.resource_type.get_resource_type()  # type: ignore
            resource_id = self.context.kwargs["id_"]  # type: ignore
        except Exception as exception:
            raise AssertionError(
                "Unable to get resource type and resource ID from exception context; "
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
