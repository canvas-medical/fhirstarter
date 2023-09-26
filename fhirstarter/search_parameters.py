"""
Functions for working with search parameters defined for search operations in the FHIR
specification.
"""

import inspect
import re
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from functools import cache
from typing import Any

from fastapi import Request, Response

from .fhir_specification.utils import (
    load_extra_search_parameters,
    load_search_parameters,
)
from .interactions import InteractionContext


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
        search_parameters = _load_search_parameters_file()
        return (
            search_parameters.get(resource_type, {})
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


@dataclass
class SupportedSearchParameter:
    name: str
    multiple: bool


def supported_search_parameters(
    search_function: Callable[..., Any]
) -> tuple[SupportedSearchParameter, ...]:
    """
    Given a callable, return a list of the parameter names in the function (excluding variadic
    keyword and variadic positional arguments).

    This function is used to determine what search parameters are supported by the handler supplied
    for a registered FHIR search interaction.
    """
    # TODO: There is probably a more sophisticated way of figuring out if list[str] is part of an
    #  annotation, but this is sufficient for now.
    return tuple(
        SupportedSearchParameter(
            name=name, multiple="list[str]" in str(parameter.annotation)  # type: ignore[call-arg]
        )
        for name, parameter in inspect.signature(search_function).parameters.items()
        if parameter.annotation != InteractionContext
    )


def search_parameter_sort_key(
    name: str,
    search_parameter_metadata: dict[str, dict[str, str]],
    parameter_annotation: type | None = None,
) -> tuple[bool, bool, bool, bool, bool, str]:
    """
    Return a sort key for a search parameter.

    This function allows for consistent sorting of search parameters throughout the package.

    Sort order is:
    1. Request and response annotations
    2. Parameters that do not start with underscore
    3. Parameters that are search or search result parameters (i.e. _format and _pretty go to the
       bottom)
    4. Parameters that are part of the capability statement (this favors search parameters like
       _has over search result parameters like _sort)
    5. Alphabetical by name

    """
    return (
        parameter_annotation != Request,
        parameter_annotation != Response,
        name.startswith("_"),
        var_name_to_qp_name(name) not in search_parameter_metadata,
        not search_parameter_metadata.get(var_name_to_qp_name(name), {}).get(
            "include-in-capability-statement", False
        ),
        var_name_to_qp_name(name),
    )


@cache
def _load_search_parameters_file() -> dict[str, dict[str, dict[str, str | bool]]]:
    """
    Load the search parameters JSON file.

    Organize the search parameter file by resource type and return a dict with the data. Initialize
    the search parameters dict with values that aren't present in the JSON file.
    """
    search_parameters = {"Resource": load_extra_search_parameters()}

    bundle = load_search_parameters()

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
                _, description = description_for_resource_type.split(": ", maxsplit=1)
                return description.removesuffix("\r")
        else:
            raise AssertionError("Resource type must exist in the description")

    return description
