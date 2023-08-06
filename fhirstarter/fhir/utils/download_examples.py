"""Script to download FHIR resource examples."""

import json
import sys
from pathlib import Path

import requests

FILENAME_EXCEPTIONS: dict[str, dict[str, str]] = {
    "STU3": {
        "BodySite": "bodysite-example-skin-patch.json",
        "Measure": "measure-exclusive-breastfeeding.json",
        "MeasureReport": "measurereport-cms146-cat2-example.json",
        "Medication": "medicationexample15.json",
        "MedicationAdministration": "medicationadministration0302.json",
        "MedicationDispense": "medicationdispense0302.json",
        "MedicationRequest": "medicationrequest0301.json",
        "MedicationStatement": "medicationstatementexample1.json",
        "NutritionOrder": "nutritionorder-example-renaldiet.json",
        "SupplyRequest": "supplyrequest-example-simpleorder.json",
        "Task": "task-example1.json",
    },
    "R4": {
        "BodyStructure": "bodystructure-example-skin-patch.json",
        "ChargeItemDefinition": "chargeitemdefinition-device-example.json",
        "Measure": "measure-hiv-indicators.json",
        "MeasureReport": "measurereport-cms146-cat2-example.json",
        "Medication": "medicationexample15.json",
        "MedicationAdministration": "medicationadministration0302.json",
        "MedicationDispense": "medicationdispense0302.json",
        "MedicationRequest": "medicationrequest0301.json",
        "MedicationStatement": "medicationstatementexample1.json",
        "NutritionOrder": "nutritionorder-example-renaldiet.json",
        "SpecimenDefinition": "specimendefinition-example-serum-plasma.json",
        "StructureDefinition": "structuredefinition-example-section-library.json",
        "SupplyRequest": "supplyrequest-example-simpleorder.json",
        "Task": "task-example1.json",
    },
    "R4B": {},
    "R5": {},
}


def main() -> None:
    fhir_dir = sys.argv[1]
    sequence = sys.argv[2]

    resources_json_file = Path(fhir_dir) / sequence / "resources.json"
    output_dir = Path(fhir_dir) / sequence / "examples"

    with open(resources_json_file) as file_:
        resources = json.load(file_)

    for resource in resources:
        if filename := FILENAME_EXCEPTIONS[sequence].get(resource):
            url = f"https://hl7.org/fhir/{sequence}/{filename}"
        else:
            url = f"https://hl7.org/fhir/{sequence}/{resource.lower()}-example.json"

        response = requests.get(url)
        if response.status_code != requests.codes.ok:
            raise RuntimeError(f"Failed to get example for {resource}")

        with open(Path(output_dir) / f"{resource.lower()}-example.json", "wb") as file_:
            file_.write(response.content)


if __name__ == "__main__":
    main()
