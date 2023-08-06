"""Script to populate the resource examples directory for each of the sequences"""

import json
import sys
from pathlib import Path
from typing import Any

import requests

EXAMPLE_EXCEPTIONS: dict[str, dict[str, str | dict[str, Any]]] = {
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
    "R4B": {
        "BodyStructure": "bodystructure-example-skin-patch.json",
        "ChargeItemDefinition": "chargeitemdefinition-device-example.json",
        "Evidence": "evidence-example-stroke-0-3-alteplase-vs-no-alteplase-mRS3-6.json",
        "EvidenceVariable": "evidencevariable-example-fatal-ICH-in-7-days.json",
        "Measure": "measure-hiv-indicators.json",
        "MeasureReport": "measurereport-cms146-cat1-example.json",
        "Medication": "medicationexample15.json",
        "MedicationAdministration": "medicationadministration0302.json",
        "MedicationDispense": "medicationdispense0302.json",
        "MedicationRequest": "medicationrequest0301.json",
        "MedicationStatement": "medicationstatementexample1.json",
        "NutritionOrder": "nutritionorder-example-renaldiet.json",
        "SpecimenDefinition": "specimendefinition-example-serum-plasma.json",
        "StructureDefinition": "structuredefinition-example-section-library.json",
        "SubscriptionTopic": "subscriptiontopic-example-admission.json",
        "SupplyRequest": "supplyrequest-example-simpleorder.json",
        "Task": "task-example1.json",
    },
    "R5": {
        "ActorDefinition": "actordefinition-server.json",
        "AdverseEvent": {
            "resourceType": "AdverseEvent",
            "id": "example",
            "identifier": {
                "system": "http://acme.com/ids/patients/risks",
                "value": "49476534",
            },
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
            "subject": {"reference": "Patient/example"},
            "occurrenceDateTime": "2017-01-29T12:34:56+00:00",
            "seriousness": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/adverse-event-seriousness",
                        "code": "Non-serious",
                        "display": "Non-serious",
                    }
                ]
            },
            "recorder": {"reference": "Practitioner/example"},
            "suspectEntity": [{"instance": {"reference": "Medication/example"}}],
        },
        "ArtifactAssessment": "artifactassessment-risk-of-bias-example.json",
        "BodyStructure": "bodystructure-example-skin-patch.json",
        "ChargeItemDefinition": "chargeitemdefinition-device-example.json",
        "Citation": "citation-example-research-doi.json",
        "Evidence": "evidence-example-stroke-0-3-alteplase-vs-no-alteplase-mRS3-6.json",
        "EvidenceVariable": "evidencevariable-example-fatal-ICH-in-7-days.json",
        "FormularyItem": "formularyitemexample01.json",
        "ImagingSelection": "imagingselection-example-3d-image-region-selection.json",
        "Measure": "measure-hiv-indicators.json",
        "MeasureReport": "measurereport-cms146-cat1-example.json",
        "Medication": "medicationexample15.json",
        "MedicationAdministration": "medicationadministration0302.json",
        "MedicationDispense": "medicationdispense0302.json",
        "MedicationRequest": "medicationrequest0301.json",
        "MedicationStatement": "medicationstatementexample1.json",
        "NutritionOrder": "nutritionorder-example-renaldiet.json",
        "Requirements": "Requirements-example2.json",
        "ResearchStudy": "researchstudy-example-ctgov-study-record.json",
        "ResearchSubject": "researchsubject-example-crossover-placebo-to-drug.json",
        "StructureDefinition": "structuredefinition-example-section-library.json",
        "SupplyRequest": "supplyrequest-example-simpleorder.json",
        "Task": "task-example1.json",
    },
}


def main() -> None:
    fhir_dir = sys.argv[1]
    sequence = sys.argv[2]

    resources_json_file = Path(fhir_dir) / sequence / "resources.json"
    output_dir = Path(fhir_dir) / sequence / "examples"

    with open(resources_json_file) as file_:
        resources = json.load(file_)

    for resource in resources:
        example_exception = EXAMPLE_EXCEPTIONS[sequence].get(resource)

        if isinstance(example_exception, dict):
            content = json.dumps(
                example_exception, indent=2, separators=(",", " : ")
            ).encode()
        else:
            if example_exception:
                url = f"https://hl7.org/fhir/{sequence}/{example_exception}"
            else:
                url = f"https://hl7.org/fhir/{sequence}/{resource.lower()}-example.json"

            response = requests.get(url)
            if response.status_code != requests.codes.ok:
                raise RuntimeError(f"Failed to get example for {resource}")
            content = response.content

        with open(Path(output_dir) / f"{resource.lower()}-example.json", "wb") as file_:
            file_.write(content)


if __name__ == "__main__":
    main()
