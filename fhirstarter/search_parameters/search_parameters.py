import inspect
import json
import os.path
from collections import defaultdict
from collections.abc import Callable
from functools import cache
from typing import Any

_RESERVED_NAMES = {"class", "format", "global", "request", "response", "result", "type"}


@cache
def load_search_parameters() -> defaultdict[str, dict[str, dict[str, str]]]:
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
                "description": resource["description"],
            }

    return search_parameters


def fhir_sp_name_to_var_sp_name(name: str) -> str:
    if name in _RESERVED_NAMES:
        name += "_"
    return name.replace("-", "_")


def var_sp_name_to_fhir_sp_name(name: str) -> str:
    if name.endswith("_"):
        name = name[:-1]
    return name.replace("_", "-")


def supported_search_parameters(search_function: Callable[..., Any]) -> tuple[str, ...]:
    return tuple(
        key
        for key in inspect.signature(search_function).parameters.keys()
        if key != "kwargs"
    )
