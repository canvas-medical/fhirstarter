"""
Functions for working with search parameters defined for search operations in the FHIR
specification.
"""

import inspect
import json
import os.path
import re
from collections.abc import Callable
from functools import cache
from inspect import Parameter
from typing import Any


@cache
def load_search_parameter_file() -> dict[str, Any]:
    """Load the search parameters JSON file."""
    file_name = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "search-parameters.json"
    )
    with open(file_name) as file_:
        return json.load(file_)


@cache
def get_search_parameter_metadata(resource_type: str) -> dict[str, dict[str, str]]:
    """Return search parameter metadata for the given resource type."""
    search_parameter_metadata = {}

    bundle = load_search_parameter_file()

    for entry in bundle["entry"]:
        resource = entry["resource"]

        if set(resource["base"]).intersection(
            {resource_type, "DomainResource", "Resource"}
        ):
            search_parameter_metadata[resource["name"]] = {
                "name": resource["name"],
                "type": resource["type"],
                "description": _remove_hyperlinks_from_markdown(
                    resource["description"]
                ),
            }

    return search_parameter_metadata


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
        if name not in {"request", "response"}
        and parameter.kind not in {Parameter.VAR_KEYWORD, Parameter.VAR_POSITIONAL}
    )


def _remove_hyperlinks_from_markdown(markdown: str) -> str:
    """Remove hyperlinks from markdown text, most likely from search parameter descriptions."""
    return re.sub(r"\[(.*?)\]\(.*?\)", r"\1", markdown)
