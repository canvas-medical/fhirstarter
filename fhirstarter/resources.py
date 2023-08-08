"""
Resources module that finesses imports of resources used by the framework so that they can be
referenced by the same names across the framework regardless of the FHIR version being used.

The finesse required here is due to what is supported and not supported by various versions of the
fhir.resources package. Versions including and after 7.0.0 no longer support the R4 sequence, but do
support the STU3, R4B, and R5 sequences. Version 6.5.0 supports the R4 sequence.

Due to this, the allowed versions of the fhir.resources package will be restricted based on the FHIR
sequence being used.
"""

from .fhir_specification import FHIR_SEQUENCE

if FHIR_SEQUENCE in ("R4", "R5"):
    from fhir.resources.bundle import Bundle
    from fhir.resources.capabilitystatement import CapabilityStatement
    from fhir.resources.fhirtypes import Id
    from fhir.resources.operationoutcome import OperationOutcome
    from fhir.resources.resource import Resource
elif FHIR_SEQUENCE == "STU3":
    from fhir.resources.STU3.bundle import Bundle
    from fhir.resources.STU3.capabilitystatement import CapabilityStatement
    from fhir.resources.STU3.fhirtypes import Id
    from fhir.resources.STU3.operationoutcome import OperationOutcome
    from fhir.resources.STU3.resource import Resource
elif FHIR_SEQUENCE == "R4B":
    from fhir.resources.R4B.bundle import Bundle
    from fhir.resources.R4B.capabilitystatement import CapabilityStatement
    from fhir.resources.R4B.fhirtypes import Id
    from fhir.resources.R4B.operationoutcome import OperationOutcome
    from fhir.resources.R4B.resource import Resource

__all__ = ["Bundle", "CapabilityStatement", "Id", "OperationOutcome", "Resource"]
