import re
from typing import Any, Dict, Iterable, List, Literal, MutableSequence, Optional

from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator
from pydantic_core import InitErrorDetails

_PATH_PATTERN = re.compile("^\/(?:[^/]+\/)*[^/]+$")


class JSONPatchOperation(BaseModel):
    """
    JSON Patch operation Pydantic model (https://datatracker.ietf.org/doc/html/rfc6902).
    """

    op: Literal["add", "remove", "replace", "move", "copy", "test"]
    from_: str = Field(default=None, alias="from")
    path: str
    value: Optional[Any]

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "examples": [
                {
                    "op": "add",
                    "path": "/text",
                    "value": {
                        "status": "empty",
                        "div": '<div xmlns="http://www.w3.org/1999/xhtml">No human-readable text provided in this case</div>',
                    },
                }
            ]
        },
    }

    @field_validator("from_", "path")
    @classmethod
    def validate_json_pointers(cls, json_pointer: str) -> str:
        """Ensure that the from and path fields contain valid JSON Pointers."""
        if not re.fullmatch(_PATH_PATTERN, json_pointer):
            raise ValueError(f"invalid JSON Pointer")
        return json_pointer

    @model_validator(mode="after")
    def validate_structure(self) -> "JSONPatchOperation":
        """
        Ensure that this operation has the correct fields based on the operation type (e.g. add,
        replace, etc.)
        """
        errors: List[InitErrorDetails] = []

        self._check_optional_field(
            field="from",
            value=self.from_,
            ops=("move", "copy"),
            errors=errors,
        )
        self._check_optional_field(
            field="value",
            value=self.value,
            ops=("add", "replace", "test"),
            errors=errors,
        )

        if errors:
            raise ValidationError.from_exception_data(title="", line_errors=errors)

        return self

    def _check_optional_field(
        self,
        field: str,
        value: Any,
        ops: Iterable[str],
        errors: MutableSequence[InitErrorDetails],
    ) -> None:
        """
        Check optional fields.

        Give a field name, value, and list of ops:
        * If the value is not None, make sure it's allowed
        * If the value is None, make sure it's not required
        """
        if value is not None and self.op not in ops:
            errors.append(
                InitErrorDetails(type="extra_forbidden", loc=(field,), input=value)
            )
        if value is None and self.op in ops:
            errors.append(InitErrorDetails(type="missing", loc=(field,), input=value))


JSONPatch = List[JSONPatchOperation]


def convert_json_patch(json_patch: JSONPatch) -> List[Dict[str, Any]]:
    """
    Convert the JSON Patch object to a list of dicts.

    This method will also rename the "from_" key in the operation dictionaries to "from".
    """
    return [
        {
            key.replace("from_", "from"): value
            for key, value in op.model_dump().items()
            if value
        }
        for op in json_patch
    ]
