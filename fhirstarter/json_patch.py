import re
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Literal,
    Mapping,
    MutableSequence,
    Optional,
)

from pydantic import BaseModel, Extra, Field, ValidationError, root_validator, validator
from pydantic.error_wrappers import ErrorWrapper

_PATH_PATTERN = re.compile("^\/(?:[^/]+\/)*[^/]+$")


class JSONPatchOperation(BaseModel):
    """
    JSON Patch operation Pydantic model (https://datatracker.ietf.org/doc/html/rfc6902).
    """

    op: Literal["add", "remove", "replace", "move", "copy", "test"]
    from_: Optional[str] = Field(alias="from")
    path: str
    value: Optional[Any]

    class Config:
        extra = Extra.forbid
        schema_extra = {
            "example": {
                "op": "add",
                "path": "/text",
                "value": {
                    "status": "empty",
                    "div": '<div xmlns="http://www.w3.org/1999/xhtml">No human-readable text provided in this case</div>',
                },
            }
        }

    @validator("from_", "path")
    def validate_json_pointers(cls, json_pointer: str) -> str:
        """Ensure that the from and path fields contain valid JSON Pointers."""
        if not re.fullmatch(_PATH_PATTERN, json_pointer):
            raise ValueError(f"invalid JSON Pointer")
        return json_pointer

    @root_validator(pre=False, skip_on_failure=True)
    def validate_structure(cls, values: Mapping[str, Any]) -> Mapping[str, Any]:
        """
        Ensure that this operation has the correct fields based on the operation type (e.g. add,
        replace, etc.)
        """
        errors: List[ErrorWrapper] = []

        op = values["op"]

        cls._check_optional_field(
            op,
            field="from",
            value=values.get("from_"),
            allowed_ops=("move", "copy"),
            errors=errors,
        )
        cls._check_optional_field(
            op,
            field="value",
            value=values.get("value"),
            allowed_ops=("add", "replace", "test"),
            errors=errors,
        )

        if errors:
            raise ValidationError(errors, cls)

        return values

    @staticmethod
    def _check_optional_field(
        op: str,
        field: str,
        value: Any,
        allowed_ops: Iterable[str],
        errors: MutableSequence[ErrorWrapper],
    ) -> None:
        if value and op not in allowed_ops:
            errors.append(
                ErrorWrapper(ValueError("extra fields not permitted"), loc=(field,))
            )
        if not value and op in allowed_ops:
            errors.append(ErrorWrapper(ValueError("field required"), loc=(field,)))


JSONPatch = List[JSONPatchOperation]


def convert_json_patch(json_patch: JSONPatch) -> List[Dict[str, Any]]:
    """
    Convert the JSON Patch object to a list of dicts.

    This method will also rename the "from_" key in the operation dictionaries to "from".
    """
    return [
        {
            key.replace("from_", "from"): value
            for key, value in op.dict().items()
            if value
        }
        for op in json_patch
    ]
