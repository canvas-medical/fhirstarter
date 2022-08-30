"""Functions for loading files from the FHIR specification."""

import json
from pathlib import Path
from typing import Any


def load_example(resource_type: str) -> dict[str, Any]:
    """Load the example for the specified resource type."""

    return _load_json_file(
        Path(__file__).parent / "examples" / f"{resource_type.lower()}-example.json"
    )


def load_search_parameters() -> dict[str, Any]:
    """Load the search parameters file."""
    return _load_json_file(Path(__file__).parent / "search-parameters.json")


def _load_json_file(file_path: Path) -> dict[str, Any]:
    with open(file_path) as file_:
        return json.load(file_)
