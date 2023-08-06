"""Script to download FHIR resource examples."""

import json
import sys
from pathlib import Path

import requests


def main() -> None:
    fhir_dir = sys.argv[1]
    sequence = sys.argv[2]

    resources_json_file = Path(fhir_dir) / sequence / "resources.json"
    output_dir = Path(fhir_dir) / sequence / "examples"

    with open(resources_json_file) as file_:
        resources = json.load(file_)

    failed = []
    for resource in resources:
        response = requests.get(
            f"https://hl7.org/fhir/{sequence}/{resource.lower()}-example.json"
        )
        if response.status_code != requests.codes.ok:
            failed.append(resource)
        else:
            with open(
                Path(output_dir) / f"{resource.lower()}-example.json", "wb"
            ) as file_:
                file_.write(response.content)

    if failed:
        print(f"Failed to obtain examples for: {failed}")


if __name__ == "__main__":
    main()
