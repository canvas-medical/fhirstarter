"""Script to populate the FHIR specification data for each of the sequences"""

import concurrent
import json
import sys
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Literal
from uuid import uuid4

import requests
from bs4 import BeautifulSoup, Tag

ADVERSE_EVENT_R5_EXAMPLE = {
    "summary": "Example of adverseevent",
    "description": "Example of adverseevent",
    "value": {
        "resourceType": "AdverseEvent",
        "id": "example",
        "text": {
            "status": "generated",
            "div": '<div xmlns="http://www.w3.org/1999/xhtml"><p><b>Generated Narrative</b></p><div style="display: inline-block; background-color: #d9e0e7; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%"><p style="margin-bottom: 0px">Resource &quot;example&quot; </p></div><p><b>identifier</b>: id: 49476534</p><p><b>actuality</b>: actual</p><p><b>category</b>: Medication Mishap <span style="background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki"> (<a href="codesystem-adverse-event-category.html">AdverseEventCategory</a>#medication-mishap)</span></p><p><b>event</b>: This was a mild rash on the left forearm <span style="background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki"> (<a href="https://browser.ihtsdotools.org/">SNOMED CT</a>#304386008 &quot;O/E - itchy rash&quot;)</span></p><p><b>subject</b>: <a href="patient-example.html">Patient/example</a> &quot;Peter CHALMERS&quot;</p><p><b>date</b>: 2017-01-29T12:34:56Z</p><p><b>seriousness</b>: Non-serious <span style="background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki"> (<a href="codesystem-adverse-event-seriousness.html">AdverseEventSeriousness</a>#Non-serious)</span></p><p><b>recorder</b>: <a href="practitioner-example.html">Practitioner/example</a> &quot;Adam CAREFUL&quot;</p><h3>SuspectEntities</h3><table class="grid"><tr><td>-</td><td><b>Instance</b></td></tr><tr><td>*</td><td><a href="todo.html">Medication/example</a></td></tr></table></div>',
        },
        "identifier": [
            {"system": "http://acme.com/ids/patients/risks", "value": "49476534"}
        ],
        "status": "completed",
        "actuality": "actual",
        "category": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/adverse-event-category",
                        "code": "medication-mishap",
                        "display": "Medication Mishap",
                    }
                ]
            }
        ],
        "code": {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": "304386008",
                    "display": "O/E - itchy rash",
                }
            ],
            "text": "This was a mild rash on the left forearm",
        },
        "subject": {"reference": "Patient/example"},
        "occurrenceDateTime": "2017-01-29T12:34:56+00:00",
        "seriousness": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/adverse-event-seriousness",
                    "code": "non-serious",
                    "display": "Non-serious",
                }
            ]
        },
        "recorder": {"reference": "Practitioner/example"},
        "suspectEntity": [{"instanceReference": {"reference": "Medication/example"}}],
    },
}


def main() -> None:
    fhir_dir = Path(sys.argv[1])

    print("")

    for sequence in ("STU3", "R4", "R4B", "R5"):
        print(f"Creating sequence data for {sequence}...")

        # Download the search parameters file
        response = requests.get(
            f"https://hl7.org/fhir/{sequence}/search-parameters.json"
        )

        # Make a zip file with the search parameters file
        with zipfile.ZipFile(
            fhir_dir / "sequences" / sequence / "search-parameters.zip",
            "w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=9,
        ) as file_:
            file_.writestr("search-parameters.json", response.content)

        # Load the list of resources
        with open(fhir_dir / "sequences" / sequence / "resource_types.json") as file_:
            resource_types = json.load(file_)

        # Get the examples for all resource types
        examples = {}
        with ThreadPoolExecutor() as executor:
            future_to_resource_type = {
                executor.submit(get_examples, sequence, resource_type): resource_type
                for resource_type in resource_types
            }
            for future in concurrent.futures.as_completed(future_to_resource_type):
                resource_type = future_to_resource_type[future]
                examples[resource_type] = future.result()

        # Create the examples zip file
        with zipfile.ZipFile(
            fhir_dir / "sequences" / sequence / "examples.zip",
            "w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=9,
        ) as file_:
            for resource_type in examples.keys():
                file_.writestr(
                    f"{resource_type.lower()}.json",
                    json.dumps(
                        examples[resource_type], indent=4, separators=(", ", ": ")
                    ),
                )

    print("\nDone")


def get_examples(sequence: str, resource_type: str) -> dict[str, Any]:
    if sequence == "R5" and resource_type == "AdverseEvent":
        return {
            "example": {
                "summary": "Example of adverseevent",
                "description": "Example of adverseevent",
                "value": ADVERSE_EVENT_R5_EXAMPLE,
            }
        }

    if resource_type == "StructureDefinition":
        # StructureDefinition is materially different than other resource types
        examples = _get_structuredefinition_examples(sequence)
    else:
        # Download the examples page for the resource type
        response = requests.get(
            f"https://hl7.org/fhir/{sequence}/{resource_type.lower()}-examples.html"
        )
        if response.status_code != requests.codes.ok:
            raise RuntimeError(f"Failed to get list of examples for {resource_type}")

        # Extract the description, identifier, and JSON file URL for each example
        soup = BeautifulSoup(response.text, features="html.parser")
        examples = _get_examples(sequence, resource_type, soup.find_all("table")[-1])

    # Inline the first example
    first_example = examples[next(iter(examples.keys()))]
    response = requests.get(first_example["externalValue"])
    if response.status_code != requests.codes.ok:
        raise RuntimeError(f"Failed to download example for {resource_type}")
    first_example["value"] = response.json()
    del first_example["externalValue"]

    return examples


def _get_structuredefinition_examples(sequence: str) -> dict[str, Any]:
    resource_type = "StructureDefinition"

    # Download the examples page for the resource type
    response = requests.get(
        f"https://hl7.org/fhir/{sequence}/{resource_type.lower()}-examples.html"
    )
    if response.status_code != requests.codes.ok:
        raise RuntimeError(f"Failed to get list of examples for {resource_type}")

    # Extract the description, identifier, and JSON file URL for each example
    soup = BeautifulSoup(response.text, features="html.parser")
    examples = _get_examples(
        sequence,
        resource_type,
        soup.find("div", attrs={"id": "tabs-1"}),
        description_prefix="Base Type",
        id_method="random",
    )
    examples |= _get_examples(
        sequence,
        resource_type,
        soup.find("div", attrs={"id": "tabs-2"}),
        description_prefix="Resource",
        id_method="random",
    )
    examples |= _get_examples(
        sequence,
        resource_type,
        soup.find("div", attrs={"id": "tabs-3"}),
        description_prefix="Constraint",
        id_method="random",
    )
    examples |= _get_examples(
        sequence,
        resource_type,
        soup.find("div", attrs={"id": "tabs-4"}),
        description_prefix="Extension",
        id_method="description",
    )
    examples |= _get_examples(
        sequence,
        resource_type,
        soup.find("div", attrs={"id": "tabs-5"}),
        description_prefix="Example",
        id_method="standard",
    )

    return examples


def _get_examples(
    sequence: str,
    resource_type: str,
    examples_table: Tag | None,
    description_prefix: str = "",
    id_method: Literal["standard", "random", "description"] = "standard",
) -> dict[str, Any]:
    examples: dict[str, Any] = {}

    if not examples_table:
        return examples

    # Iterate over the examples and extract the description, identifier, and JSON file URL
    for example in examples_table.find_all("tr"):
        # Skip any rows that don't have any URLs in them
        if len(example.find_all("a")) == 0:
            continue

        cells = example.find_all("td")

        # Get the description and ID based on the specified method
        match id_method:
            case "standard":
                description = cells[0].text
                id_ = cells[1].text
            case "random":
                description = cells[0].text
                id_ = uuid4().hex
            case "description":
                a = cells[0].find("a")
                description = id_ = a.text
            case _:
                raise AssertionError(
                    f"Unable to get description and ID for {resource_type} example"
                )

        # Add a description prefix if one is specified
        if description_prefix:
            description = f"{description_prefix}: {description}"

        # Find the JSON filename
        for a in example.find_all("a"):
            if a.text.lower() == "json":
                filename = a.attrs["href"].removesuffix(".html")
                break
        else:
            raise AssertionError(
                f"Unable to find JSON filename for {resource_type} example"
            )

        # Add the example in OpenAPI format
        examples[id_] = {
            "summary": description,
            "description": description,
            "externalValue": f"https://hl7.org/fhir/{sequence}/{filename}",
        }

    return examples


if __name__ == "__main__":
    main()
