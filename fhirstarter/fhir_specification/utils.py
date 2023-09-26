"""Utilities for working with the FHIR specification."""

import importlib.metadata
import importlib.resources
import json
import os
import zipfile
from copy import deepcopy
from functools import cache
from pathlib import Path
from typing import Any, Mapping, cast

import fhir.resources

from . import sequences

FHIR_SEQUENCE = os.getenv("FHIR_SEQUENCE", "R5")

# Set the FHIR version and the FHIR data directory location, and ensure that the specified FHIR
# sequence is supported by FHIRStarter
match FHIR_SEQUENCE:
    case "STU3":
        import fhir.resources.STU3

        FHIR_VERSION = fhir.resources.STU3.__fhir_version__
        FHIR_DIR = cast(Path, importlib.resources.files(sequences.STU3))
    case "R4":
        FHIR_VERSION = fhir.resources.__fhir_version__
        FHIR_DIR = cast(Path, importlib.resources.files(sequences.R4))
    case "R4B":
        import fhir.resources.R4B

        FHIR_VERSION = fhir.resources.R4B.__fhir_version__
        FHIR_DIR = cast(Path, importlib.resources.files(sequences.R4B))
    case "R5":
        FHIR_VERSION = fhir.resources.__fhir_version__
        FHIR_DIR = cast(Path, importlib.resources.files(sequences.R5))
    case _:
        raise AssertionError(
            f"Specified FHIR sequence must be one of: STU3, R4, R4B, R5"
        )


# Ensure that a compatible version of fhir.resources is installed
FHIR_RESOURCES_VERSION = importlib.metadata.version("fhir.resources")
if FHIR_SEQUENCE == "R4":
    assert FHIR_RESOURCES_VERSION == "6.4.0", (
        f"fhir.resources package version must be 6.4.0 for FHIR R4 sequence; installed version is "
        f"{FHIR_RESOURCES_VERSION}"
    )
else:
    assert FHIR_RESOURCES_VERSION >= "7.0.0", (
        f"fhir.resources package version must be 7.0.0 or greater for FHIR STU3, R4B, and R5 "
        f"sequences; installed version is {FHIR_RESOURCES_VERSION}"
    )
    assert fhir.resources.__fhir_version__ == "5.0.0", (
        f"fhir.resources package references unexpected FHIR version "
        f"{fhir.resources.__fhir_version__}"
    )


def is_resource_type(resource_type: str) -> bool:
    """Return True or False depending on whether the given string is a recognized resource type."""
    return resource_type in _load_resources_list()


@cache
def _load_resources_list() -> set[str]:
    """Load the list of resources from the JSON file."""
    with open(FHIR_DIR / "resource_types.json") as file_:
        return set(json.load(file_))


@cache
def load_examples(resource_type: str) -> dict[str, dict[str, str | dict[str, Any]]]:
    """Return the examples for a specific resource type."""
    with zipfile.ZipFile(FHIR_DIR / "examples.zip") as file_:
        return json.loads(file_.read(f"{resource_type.lower()}.json"))


def create_bundle_example(resource_example: Mapping[str, Any]) -> dict[str, Any]:
    """
    Create a bundle example for a specific resource type.

    The standard bundle example is modified based on the given resource example.
    """
    resource_type = resource_example["resourceType"]
    bundle_examples = load_examples("Bundle")
    bundle_example = deepcopy(
        cast(dict[str, Any], next(iter(bundle_examples.values()))["value"])
    )

    bundle_example["link"][0] = {
        "relation": "self",
        "url": f"https://example.com/base/{resource_type}?_count=1",
    }
    bundle_example["link"][1] = {
        "relation": "next",
        "url": f"https://example.com/base/{resource_type}?"
        "searchId=ff15fd40-ff71-4b48-b366-09c706bed9d0&page=2",
    }
    bundle_example["entry"] = [
        {
            "fullUrl": f"https://example.com/base/{resource_type}/{resource_example['id']}",
            "resource": resource_example,
            "search": {"mode": "match", "score": 1},
        }
    ]

    return bundle_example


def make_operation_outcome_example(
    severity: str, code: str, details_text: str
) -> dict[str, Any]:
    """Make an OperationOutcome example given a severity, code, and details text."""
    return {
        "resourceType": "OperationOutcome",
        "id": "101",
        "issue": [
            {
                "severity": severity,
                "code": code,
                "details": {"text": details_text},
            }
        ],
    }


def load_search_parameters() -> dict[str, Any]:
    """Load the search parameters file."""
    with zipfile.ZipFile(FHIR_DIR / "search-parameters.zip") as file_:
        return json.loads(file_.read("search-parameters.json"))


def load_extra_search_parameters() -> dict[str, dict[str, str | bool]]:
    """Load the extra search parameters file."""
    with open(FHIR_DIR / "extra-search-parameters.json") as file_:
        return json.load(file_)
