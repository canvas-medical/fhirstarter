"""
Functions for working with search parameters defined for search operations in the FHIR
specification.
"""

import inspect
import json
import os.path
import re
from collections import defaultdict
from collections.abc import Callable
from functools import cache
from inspect import Parameter
from typing import Any

_RESERVED_NAMES = {"class", "format", "global", "request", "response", "result", "type"}


@cache
def load_search_parameters() -> defaultdict[str, dict[str, dict[str, str]]]:
    """
    Parse and load the search parameters JSON file from the FHIR specification.

    Return a dict organized by resource type and search parameter name that contains search
    parameter name, type, and description.
    """
    search_parameters: defaultdict[str, dict[str, dict[str, str]]] = defaultdict(dict)

    file_name = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "search-parameters.json"
    )
    with open(file_name) as file_:
        bundle = json.load(file_)

    for entry in bundle["entry"]:
        resource = entry["resource"]

        for resource_type in resource["base"]:
            search_parameters[resource_type][resource["name"]] = {
                "name": resource["name"],
                "type": resource["type"],
                "description": _remove_hyperlinks_from_markdown(
                    resource["description"]
                ),
            }

    return search_parameters


def fhir_sp_name_to_var_sp_name(name: str) -> str:
    """Convert a FHIR search parameter name to a Python-friendly variable name."""
    if name in _RESERVED_NAMES:
        name += "_"
    return name.replace("-", "_")


def var_sp_name_to_fhir_sp_name(name: str) -> str:
    """Convert a Python-friendly variable name to a FHIR search parameter name."""
    if name.endswith("_"):
        name = name[:-1]
    return name.replace("_", "-")


def supported_search_parameters(search_function: Callable[..., Any]) -> tuple[str, ...]:
    """
    Given a callable, return a list of the parameter names in the function (excluding variadic
    keyword and variadic positional arguments).

    This function is used to determine what search parameters are supported by the callable supplied
    for a registered FHIR search interaction.
    """
    return tuple(
        name
        for name, parameter in inspect.signature(search_function).parameters.items()
        if parameter.kind not in {Parameter.VAR_KEYWORD, Parameter.VAR_POSITIONAL}
    )


def _remove_hyperlinks_from_markdown(markdown: str) -> str:
    """Remove hyperlinks from markdown text, most likely from search parameter descriptions."""
    return re.sub(r"\[(.*?)\]\(.*?\)", r"\1", markdown)
