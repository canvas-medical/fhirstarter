"""
An example FHIR server implementation using FHIRStarter, with examples showing how to create FHIR
interactions (i.e. endpoints) that perform create, read, search-type, and update operations.
"""
from collections.abc import MutableMapping
from copy import deepcopy
from pathlib import Path
from typing import Any, cast
from uuid import uuid4

import uvicorn
from fhir.resources.bundle import Bundle
from fhir.resources.fhirtypes import Id
from fhir.resources.humanname import HumanName
from fhir.resources.patient import Patient as PatientBase
from starlette.responses import RedirectResponse

from fhirstarter import FHIRProvider, FHIRStarter, InteractionContext, Request, Response
from fhirstarter.exceptions import FHIRResourceNotFoundError


# Optional: Provide a custom example for the automatic documentation by defining a subclass of the
# FHIR Patient Pydantic model. If a custom model is not provided, examples from the FHIR
# specification are used.
class Patient(PatientBase):
    class Config:
        schema_extra = {
            "example": {
                "resourceType": "Patient",
                "id": "example",
                "text": {
                    "status": "generated",
                    "div": '\u003cdiv xmlns\u003d"http://www.w3.org/1999/xhtml"\u003e\n\t\t\t\u003ctable\u003e\n\t\t\t\t\u003ctbody\u003e\n\t\t\t\t\t\u003ctr\u003e\n\t\t\t\t\t\t\u003ctd\u003eName\u003c/td\u003e\n\t\t\t\t\t\t\u003ctd\u003ePeter James \n              \u003cb\u003eChalmers\u003c/b\u003e (\u0026quot;Jim\u0026quot;)\n            \u003c/td\u003e\n\t\t\t\t\t\u003c/tr\u003e\n\t\t\t\t\t\u003ctr\u003e\n\t\t\t\t\t\t\u003ctd\u003eAddress\u003c/td\u003e\n\t\t\t\t\t\t\u003ctd\u003e534 Erewhon, Pleasantville, Vic, 3999\u003c/td\u003e\n\t\t\t\t\t\u003c/tr\u003e\n\t\t\t\t\t\u003ctr\u003e\n\t\t\t\t\t\t\u003ctd\u003eContacts\u003c/td\u003e\n\t\t\t\t\t\t\u003ctd\u003eHome: unknown. Work: (03) 5555 6473\u003c/td\u003e\n\t\t\t\t\t\u003c/tr\u003e\n\t\t\t\t\t\u003ctr\u003e\n\t\t\t\t\t\t\u003ctd\u003eId\u003c/td\u003e\n\t\t\t\t\t\t\u003ctd\u003eMRN: 12345 (Acme Healthcare)\u003c/td\u003e\n\t\t\t\t\t\u003c/tr\u003e\n\t\t\t\t\u003c/tbody\u003e\n\t\t\t\u003c/table\u003e\n\t\t\u003c/div\u003e',
                },
                "identifier": [
                    {
                        "use": "usual",
                        "type": {
                            "coding": [
                                {
                                    "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                                    "code": "MR",
                                }
                            ]
                        },
                        "system": "urn:oid:1.2.36.146.595.217.0.1",
                        "value": "12345",
                        "period": {"start": "2001-05-06"},
                        "assigner": {"display": "Acme Healthcare"},
                    }
                ],
                "active": True,
                "name": [
                    {
                        "use": "official",
                        "family": "Chalmers",
                        "given": ["Peter", "James"],
                    },
                    {"use": "usual", "given": ["Jim"]},
                    {
                        "use": "maiden",
                        "family": "Windsor",
                        "given": ["Peter", "James"],
                        "period": {"end": "2002"},
                    },
                ],
                "telecom": [
                    {"use": "home"},
                    {
                        "system": "phone",
                        "value": "(03) 5555 6473",
                        "use": "work",
                        "rank": 1,
                    },
                    {
                        "system": "phone",
                        "value": "(03) 3410 5613",
                        "use": "mobile",
                        "rank": 2,
                    },
                    {
                        "system": "phone",
                        "value": "(03) 5555 8834",
                        "use": "old",
                        "period": {"end": "2014"},
                    },
                ],
                "gender": "male",
                "birthDate": "1974-12-25",
                "_birthDate": {
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/StructureDefinition/patient-birthTime",
                            "valueDateTime": "1974-12-25T14:35:45-05:00",
                        }
                    ]
                },
                "deceasedBoolean": False,
                "address": [
                    {
                        "use": "home",
                        "type": "both",
                        "text": "534 Erewhon St PeasantVille, Rainbow, Vic  3999",
                        "line": ["534 Erewhon St"],
                        "city": "PleasantVille",
                        "district": "Rainbow",
                        "state": "Vic",
                        "postalCode": "3999",
                        "period": {"start": "1974-12-25"},
                    }
                ],
                "contact": [
                    {
                        "relationship": [
                            {
                                "coding": [
                                    {
                                        "system": "http://terminology.hl7.org/CodeSystem/v2-0131",
                                        "code": "N",
                                    }
                                ]
                            }
                        ],
                        "name": {
                            "family": "du Marché",
                            "_family": {
                                "extension": [
                                    {
                                        "url": "http://hl7.org/fhir/StructureDefinition/humanname-own-prefix",
                                        "valueString": "VV",
                                    }
                                ]
                            },
                            "given": ["Bénédicte"],
                        },
                        "telecom": [{"system": "phone", "value": "+33 (237) 998327"}],
                        "address": {
                            "use": "home",
                            "type": "both",
                            "line": ["534 Erewhon St"],
                            "city": "PleasantVille",
                            "district": "Rainbow",
                            "state": "Vic",
                            "postalCode": "3999",
                            "period": {"start": "1974-12-25"},
                        },
                        "gender": "female",
                        "period": {"start": "2012"},
                    }
                ],
                "managingOrganization": {"reference": "Organization/1"},
                "meta": {
                    "tag": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason",
                            "code": "HTEST",
                            "display": "test health data",
                        }
                    ]
                },
            }
        }


# Create the app with the provided config file
app = FHIRStarter(
    title="FHIRStarter Example Implementation",
    config_file_name=Path(__file__).parent / "config.toml",
)

# Create a "database"
DATABASE: dict[str, Patient] = {}

# Create a provider
provider = FHIRProvider()

# To register FHIR interactions with  a provider, the pieces of information the developer has to
# provider are:
# * FHIR interaction type (this affects what the endpoint will look like)
# * FHIR resource type (this affects validation of inputs and outputs, and what search parameters
#   are valid)
# * the handler (expected signature and annotations need to match the defined protocols, because
#   these values affect route creation in FastAPI)


# Register the patient create FHIR interaction with the provider
@provider.create(Patient)
async def patient_create(context: InteractionContext, resource: Patient) -> Id:
    patient = deepcopy(resource)
    patient.id = Id(uuid4().hex)
    DATABASE[patient.id] = patient

    return Id(patient.id)


# Register the patient read FHIR interaction with the provider
@provider.read(Patient)
async def patient_read(context: InteractionContext, id_: Id) -> Patient:
    patient = DATABASE.get(id_)
    if not patient:
        raise FHIRResourceNotFoundError

    return patient


# Register the patient search-type FHIR interaction with the provider
@provider.search_type(Patient)
async def patient_search_type(
    context: InteractionContext,
    birthdate: list[str] | None,
    general_practitioner: str | None,
    family: str | None,
    nickname: str | None,
    _last_updated: str | None,
) -> Bundle:
    patients = []
    for patient in DATABASE.values():
        for name in patient.name:
            if cast(HumanName, name).family == family:
                patients.append(patient)

    bundle = Bundle(
        **{
            "type": "searchset",
            "total": len(patients),
            "entry": [{"resource": patient.dict()} for patient in patients],
        }
    )

    return bundle


# Register the patient update FHIR interaction with the provider
@provider.update(Patient)
async def patient_update(context: InteractionContext, id_: Id, resource: Patient) -> Id:
    if id_ not in DATABASE:
        raise FHIRResourceNotFoundError

    patient = deepcopy(resource)
    DATABASE[id_] = patient

    return Id(patient.id)


# Add the provider to the app. This will automatically generate the API routes for the interactions
# provided by the providers (e.g. create, read, search-type, and update).
app.add_providers(provider)


# Customize the capability statement
def amend_capability_statement(
    capability_statement: MutableMapping[str, Any], request: Request, response: Response
) -> MutableMapping[str, Any]:
    capability_statement["publisher"] = "Canvas Medical"
    return capability_statement


app.set_capability_statement_modifier(amend_capability_statement)


# Redirect the main page to the API docs
@app.get("/", include_in_schema=False)
async def index() -> RedirectResponse:
    return RedirectResponse("/docs")


if __name__ == "__main__":
    # Start the server
    uvicorn.run(
        "example:app",
        use_colors=True,
        reload=True,
        reload_dirs=str(Path(__file__).parent.parent),
    )
