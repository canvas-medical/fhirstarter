"""Utilities for working with the FHIR specification."""

import json
from pathlib import Path
from typing import Any


def is_resource_type(resource_type: str) -> bool:
    return resource_type in _RESOURCE_TYPES


def load_example(resource_type: str) -> dict[str, Any]:
    """Load the example for the specified resource type."""
    return _load_json_file(
        Path(__file__).parent / "examples" / f"{resource_type.lower()}-example.json"
    )


def load_bundle_example(resource_type: str) -> dict[str, Any]:
    """
    Load a bundle example for a specific resource type.

    The standard bundle example is modified based on the given resource type.
    """
    resource_example = load_example(resource_type)
    bundle_example = load_example("Bundle")

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
            "fullUrl": f"https://example.com/base/{resource_type}/3123",
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
    return _load_json_file(Path(__file__).parent / "search-parameters.json")


def _load_json_file(file_path: Path) -> dict[str, Any]:
    with open(file_path) as file_:
        return json.load(file_)


_RESOURCE_TYPES = {
    "Account",
    "ActivityDefinition",
    "AdverseEvent",
    "AllergyIntolerance",
    "Appointment",
    "AppointmentResponse",
    "AuditEvent",
    "Basic",
    "Binary",
    "BiologicallyDerivedProduct",
    "BodyStructure",
    "Bundle",
    "CapabilityStatement",
    "CarePlan",
    "CareTeam",
    "CatalogEntry",
    "ChargeItem",
    "ChargeItemDefinition",
    "Claim",
    "ClaimResponse",
    "ClinicalImpression",
    "CodeSystem",
    "Communication",
    "CommunicationRequest",
    "CompartmentDefinition",
    "Composition",
    "ConceptMap",
    "Condition",
    "Consent",
    "Contract",
    "Coverage",
    "CoverageEligibilityRequest",
    "CoverageEligibilityResponse",
    "DetectedIssue",
    "Device",
    "DeviceDefinition",
    "DeviceMetric",
    "DeviceRequest",
    "DeviceUseStatement",
    "DiagnosticReport",
    "DocumentManifest",
    "DocumentReference",
    "EffectEvidenceSynthesis",
    "Encounter",
    "Endpoint",
    "EnrollmentRequest",
    "EnrollmentResponse",
    "EpisodeOfCare",
    "EventDefinition",
    "Evidence",
    "EvidenceVariable",
    "ExampleScenario",
    "ExplanationOfBenefit",
    "FamilyMemberHistory",
    "Flag",
    "Goal",
    "GraphDefinition",
    "Group",
    "GuidanceResponse",
    "HealthcareService",
    "ImagingStudy",
    "Immunization",
    "ImmunizationEvaluation",
    "ImmunizationRecommendation",
    "ImplementationGuide",
    "InsurancePlan",
    "Invoice",
    "Library",
    "Linkage",
    "List",
    "Location",
    "Measure",
    "MeasureReport",
    "Media",
    "Medication",
    "MedicationAdministration",
    "MedicationDispense",
    "MedicationKnowledge",
    "MedicationRequest",
    "MedicationStatement",
    "MedicinalProduct",
    "MedicinalProductAuthorization",
    "MedicinalProductContraindication",
    "MedicinalProductIndication",
    "MedicinalProductIngredient",
    "MedicinalProductInteraction",
    "MedicinalProductManufactured",
    "MedicinalProductPackaged",
    "MedicinalProductPharmaceutical",
    "MedicinalProductUndesirableEffect",
    "MessageDefinition",
    "MessageHeader",
    "MolecularSequence",
    "NamingSystem",
    "NutritionOrder",
    "Observation",
    "ObservationDefinition",
    "OperationDefinition",
    "OperationOutcome",
    "Organization",
    "OrganizationAffiliation",
    "Parameters",
    "Patient",
    "PaymentNotice",
    "PaymentReconciliation",
    "Person",
    "PlanDefinition",
    "Practitioner",
    "PractitionerRole",
    "Procedure",
    "Provenance",
    "Questionnaire",
    "QuestionnaireResponse",
    "RelatedPerson",
    "RequestGroup",
    "ResearchDefinition",
    "ResearchElementDefinition",
    "ResearchStudy",
    "ResearchSubject",
    "RiskAssessment",
    "RiskEvidenceSynthesis",
    "Schedule",
    "SearchParameter",
    "ServiceRequest",
    "Slot",
    "Specimen",
    "SpecimenDefinition",
    "StructureDefinition",
    "StructureMap",
    "Subscription",
    "Substance",
    "SubstanceNucleicAcid",
    "SubstancePolymer",
    "SubstanceProtein",
    "SubstanceReferenceInformation",
    "SubstanceSourceMaterial",
    "SubstanceSpecification",
    "SupplyDelivery",
    "SupplyRequest",
    "Task",
    "TerminologyCapabilities",
    "TestReport",
    "TestScript",
    "ValueSet",
    "VerificationResult",
    "VisionPrescription",
}
