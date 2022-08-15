"""
Functions for working with search parameters defined for search operations in the FHIR
specification.
"""

import inspect
import json
import re
from collections.abc import Callable, Mapping
from copy import deepcopy
from functools import cache
from inspect import Parameter
from pathlib import Path
from typing import Any

from ..interactions import InteractionContext

_EXTRA_SEARCH_PARAMETERS = {
    "Resource": {
        "_list": {
            "type": "string",
            "description": "All resources in nominated list (by id, Type/id, url or one of the magic List types)",
            "uri": "http://hl7.org/fhir/SearchParameter/Resource-list",
            "include-in-capability-statement": True,
        },
        "_sort": {
            "type": "string",
            "description": "Order to sort results in (can repeat for inner sort orders)\r\n\r\nAllowable Content: Name of a valid search parameter",
            "include-in-capability-statement": False,
        },
        "_count": {
            "type": "number",
            "description": "Number of results per page\r\n\r\nAllowable Content: Whole number",
            "include-in-capability-statement": False,
        },
        "_include": {
            "type": "string",
            "description": "Other resources to include in the search results that search matches point to\r\n\r\nAllowable Content: SourceType:searchParam(:targetType)",
            "include-in-capability-statement": False,
        },
        "_revinclude": {
            "type": "string",
            "description": "Other resources to include in the search results when they refer to search matches\r\n\r\nAllowable Content: SourceType:searchParam(:targetType)",
            "include-in-capability-statement": False,
        },
        "_summary": {
            "type": "string",
            "description": "Just return the summary elements (for resources where this is defined)\r\n\r\nAllowable Content: true | false (false is default)",
            "include-in-capability-statement": False,
        },
        "_contained": {
            "type": "string",
            "description": "Whether to return resources contained in other resources in the search matches\r\n\r\nAllowable Content: true | false | both (false is default)",
            "include-in-capability-statement": False,
        },
        "_containedType": {
            "type": "string",
            "description": "If returning contained resources, whether to return the contained or container resources\r\n\r\nAllowable Content: container | contained",
            "include-in-capability-statement": False,
        },
    }
}


class SearchParameters:
    def __init__(
        self,
        custom_search_parameters: Mapping[str, Mapping[str, Mapping[str, str]]]
        | None = None,
    ):
        self._custom_search_parameters = custom_search_parameters or {}

    def get_metadata(self, resource_type: str) -> dict[str, dict[str, str]]:
        """
        Return search parameter metadata for the given resource type.

        For a given resource type, the search parameter metadata is a union between the search
        parameter metadata for the resource type itself, DomainResource, Resource, and custom search
        parameter metadata.
        """
        search_parameters = _load_search_parameter_file()
        return (
            search_parameters[resource_type]
            | search_parameters["DomainResource"]
            | search_parameters["Resource"]
            | self._custom_search_parameters.get(resource_type, {})
        )


def var_name_to_qp_name(name: str) -> str:
    """
    Convert a Python-friendly variable name to a FHIR query parameter name.

    Search parameters for specific resources in FHIR are lowercase strings that may have dashes in
    them. The Python-friendly versions of them have underscores instead of dashes. Underscores may
    be at the end of the variable name as well, if they conflict with a Python reserved word.

    Search parameters for all resources in FHIR start with underscore, and are camelcase. The
    Python-friendly versions of these have their uppercase characters replaced with an underscore
    plus the lowercase version of the character.
    """
    if name.startswith("_"):
        return f"_{re.sub('_[a-z]', lambda m: m.group(0)[1:].upper(), name[1:])}"

    if name.endswith("_"):
        name = name[:-1]
    return name.replace("_", "-")


def supported_search_parameters(search_function: Callable[..., Any]) -> tuple[str, ...]:
    """
    Given a callable, return a list of the parameter names in the function (excluding variadic
    keyword and variadic positional arguments).

    This function is used to determine what search parameters are supported by the handler supplied
    for a registered FHIR search interaction.
    """
    return tuple(
        name
        for name, parameter in inspect.signature(search_function).parameters.items()
        if parameter.annotation != InteractionContext
        and parameter.kind not in {Parameter.VAR_KEYWORD, Parameter.VAR_POSITIONAL}
    )


@cache
def _load_search_parameter_file() -> dict[str, dict[str, dict[str, str]]]:
    """
    Load the search parameters JSON file.

    Organize the search parameter file by resource type and return a dict with the data. Initialize
    the search parameters dict with values that aren't present in the JSON file.
    """
    search_parameters: dict = deepcopy(_EXTRA_SEARCH_PARAMETERS)

    file_path = Path(__file__).parent / "search-parameters.json"
    with file_path.open() as file_:
        bundle = json.load(file_)

    for entry in bundle["entry"]:
        resource = entry["resource"]

        for resource_type in resource["base"]:
            search_parameters.setdefault(resource_type, {})
            search_parameters[resource_type][resource["name"]] = {
                "type": resource["type"],
                "description": _transform_description(
                    resource["description"], resource_type
                ),
                "uri": entry["fullUrl"],
                "include-in-capability-statement": True,
            }

    return search_parameters


def _transform_description(description: str, resource_type: str) -> str:
    """
    Remove other descriptions in the case where the text contains descriptions for multiple resource
    types, and return only the description for the specified resource type.
    """
    if description.startswith("Multiple Resources:"):
        for description_for_resource_type in description.split("\n"):
            if description_for_resource_type.startswith(f"* [{resource_type}]"):
                _, description = description_for_resource_type.split(": ")
                return description.removesuffix("\r")
        else:
            raise AssertionError("Resource type must exist in the description")

    return description
