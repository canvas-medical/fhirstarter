"""
Resources module that finesses imports of resources used by the framework so that they can be
referenced by the same names across the framework regardless of the FHIR version being used.
"""

from .fhir_specification import FHIR_SEQUENCE

if FHIR_SEQUENCE == "STU3":
    from fhir.resources.STU3.bundle import Bundle
    from fhir.resources.STU3.capabilitystatement import CapabilityStatement
    from fhir.resources.STU3.operationoutcome import OperationOutcome
    from fhir.resources.STU3.resource import Resource
elif FHIR_SEQUENCE == "R4B":
    from fhir.resources.R4B.bundle import Bundle
    from fhir.resources.R4B.capabilitystatement import CapabilityStatement
    from fhir.resources.R4B.operationoutcome import OperationOutcome
    from fhir.resources.R4B.resource import Resource
elif FHIR_SEQUENCE == "R5":
    from fhir.resources.bundle import Bundle
    from fhir.resources.capabilitystatement import CapabilityStatement
    from fhir.resources.operationoutcome import OperationOutcome
    from fhir.resources.resource import Resource

__all__ = ["Bundle", "CapabilityStatement", "OperationOutcome", "Resource"]
