"""
Resources module that finesses imports of resources used by the framework so that they can be
referenced by the same names across the testing framework regardless of the FHIR version being used.

The rationale behind this is the same as the one for the resources.py file that lives at the package
root.
"""

import os

FHIR_SEQUENCE = os.getenv("FHIR_SEQUENCE", "R5")

if FHIR_SEQUENCE in ("R4", "R5"):
    from fhir.resources.appointment import Appointment
    from fhir.resources.bundle import Bundle
    from fhir.resources.fhirtypes import Id
    from fhir.resources.humanname import HumanName
    from fhir.resources.patient import Patient
    from fhir.resources.practitioner import Practitioner
elif FHIR_SEQUENCE == "STU3":
    from fhir.resources.STU3.appointment import Appointment
    from fhir.resources.STU3.bundle import Bundle
    from fhir.resources.STU3.fhirtypes import Id
    from fhir.resources.STU3.humanname import HumanName
    from fhir.resources.STU3.patient import Patient
    from fhir.resources.STU3.practitioner import Practitioner
elif FHIR_SEQUENCE == "R4B":
    from fhir.resources.R4B.appointment import Appointment
    from fhir.resources.R4B.bundle import Bundle
    from fhir.resources.R4B.fhirtypes import Id
    from fhir.resources.R4B.humanname import HumanName
    from fhir.resources.R4B.patient import Patient
    from fhir.resources.R4B.practitioner import Practitioner

__all__ = ["Patient", "HumanName", "Appointment", "Bundle", "Id", "Practitioner"]
