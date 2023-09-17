"""Script to populate the FHIR specification data for each of the sequences"""

import concurrent
import json
import sys
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup

DEFAULT_EXAMPLES: dict[str, dict[str, str | dict[str, Any]]] = {
    "STU3": {
        "BodySite": "skin-patch",
        "Measure": "measure-exclusive-breastfeeding",
        "MeasureReport": "measurereport-cms146-cat2-example",
        "Medication": "medexample015",
        "MedicationAdministration": "medadmin0302",
        "MedicationDispense": "meddisp0302",
        "MedicationRequest": "medrx0301",
        "MedicationStatement": "example001",
        "NutritionOrder": "renaldiet",
        "SupplyRequest": "simpleorder",
        "Task": "example1",
    },
    "R4": {
        "BodyStructure": "skin-patch",
        "ChargeItemDefinition": "device",
        "Measure": "hiv-indicators",
        "MeasureReport": "measurereport-cms146-cat2-example",
        "Medication": "medexample015",
        "MedicationAdministration": "medadmin0302",
        "MedicationDispense": "meddisp0302",
        "MedicationRequest": "medrx0301",
        "MedicationStatement": "example001",
        "NutritionOrder": "renaldiet",
        "SpecimenDefinition": "2364",
        "StructureDefinition": "example-section-library",
        "SupplyRequest": "simpleorder",
        "Task": "example1",
    },
    "R4B": {
        "BodyStructure": "skin-patch",
        "ChargeItemDefinition": "device",
        "Evidence": "example-stroke-0-3-alteplase-vs-no-alteplase-mRS3-6",
        "EvidenceVariable": "example-fatal-ICH-in-7-days",
        "Measure": "hiv-indicators",
        "MeasureReport": "measurereport-cms146-cat1-example",
        "Medication": "medexample015",
        "MedicationAdministration": "medadmin0302",
        "MedicationDispense": "meddisp0302",
        "MedicationRequest": "medrx0301",
        "MedicationStatement": "example001",
        "NutritionOrder": "renaldiet",
        "SpecimenDefinition": "2364",
        "StructureDefinition": "example-section-library",
        "SubscriptionTopic": "admission",
        "SupplyRequest": "simpleorder",
        "Task": "example1",
    },
    "R5": {
        "ActorDefinition": "server",
        "ArtifactAssessment": "risk-of-bias-example",
        "BodyStructure": "skin-patch",
        "ChargeItemDefinition": "device",
        "Citation": "citation-example-research-doi",
        "Evidence": "example-stroke-0-3-alteplase-vs-no-alteplase-mRS3-6",
        "EvidenceVariable": "example-fatal-ICH-in-7-days",
        "FormularyItem": "formularyitemexample01",
        "ImagingSelection": "example-3d-image-region-selection",
        "Measure": "hiv-indicators",
        "MeasureReport": "measurereport-cms146-cat1-example",
        "Medication": "medexample015",
        "MedicationAdministration": "medadmin0302",
        "MedicationDispense": "meddisp0302",
        "MedicationRequest": "medrx0301",
        "MedicationStatement": "example001",
        "NutritionOrder": "renaldiet",
        "Requirements": "example2",
        "ResearchStudy": "example-ctgov-study-record",
        "ResearchSubject": "example-crossover-placebo-to-drug",
        "StructureDefinition": "example-section-library",
        "SupplyRequest": "simpleorder",
        "Task": "example1",
    },
}

ADVERSE_EVENT_R5_EXAMPLE = {
    "summary": "Example of adverseevent	",
    "description": "Example of adverseevent	",
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
    # fhir_dir = Path(sys.argv[1])
    fhir_dir = Path(
        "/Users/christopher.sande/Projects/fhirstarter/fhirstarter/fhir_specification"
    )

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
            # TODO: StructureDefinition
            future_to_resource_type = {
                executor.submit(get_examples, sequence, resource_type): resource_type
                for resource_type in resource_types
                if resource_type != "StructureDefinition"
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

    # Download the examples page for the resource type
    response = requests.get(
        f"https://hl7.org/fhir/{sequence}/{resource_type.lower()}-examples.html"
    )
    if response.status_code != requests.codes.ok:
        raise RuntimeError(f"Failed to get list of examples for {resource_type}")

    # Get the parsed examples table
    soup = BeautifulSoup(response.text, features="html.parser")
    examples_table = soup.find_all("table")[-1]

    # Iterate over the examples and extract the description, identifier, and JSON file URL
    examples = {}
    for example in examples_table.find_all("tr"):
        # Skip any rows that don't have any URLs in them
        if len(example.find_all("a")) == 0:
            continue

        cells = example.find_all("td")

        description = cells[0].text
        id_ = cells[1].text

        filename = ""
        for a in example.find_all("a"):
            if a.text.lower() == "json":
                filename = a.attrs["href"].removesuffix(".html")
                break
        else:
            assert f"Unable to find JSON filename for {resource_type}"

        examples[id_] = {
            "summary": description,
            "description": description,
            "externalValue": f"https://hl7.org/fhir/{sequence}/{filename}",
        }

    # Make sure there is a default examples under the "example" key for every resource
    if "example" not in examples:
        # If any of the examples have the expected default file name, use that one, otherwise use
        # the specified default example
        for example_name, example in examples.items():
            if (
                example["externalValue"]
                == f"https://hl7.org/fhir/{sequence}/{resource_type.lower()}-example.json"
            ):
                default_example_name = example_name
                break
        else:
            default_example_name = DEFAULT_EXAMPLES[sequence][resource_type]

        examples["example"] = examples.pop(default_example_name)

    # Download the default example and inline it
    response = requests.get(examples["example"]["externalValue"])
    if response.status_code != requests.codes.ok:
        raise RuntimeError(f"Failed to get default example for {resource_type}")
    examples["example"]["value"] = response.json()
    del examples["example"]["externalValue"]

    return examples


if __name__ == "__main__":
    main()
