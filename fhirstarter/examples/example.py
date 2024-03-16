"""
An example FHIR server implementation using FHIRStarter, with examples showing how to create FHIR
interactions (i.e. endpoints) that perform create, read, search-type, and update operations.
"""

import importlib.resources
from collections.abc import MutableMapping
from copy import deepcopy
from pathlib import Path
from typing import Any, cast
from uuid import uuid4

import uvicorn
from fhir.resources.bundle import Bundle
from fhir.resources.fhirtypes import Id
from fhir.resources.humanname import HumanName
from fhir.resources.patient import Patient
from fhir.resources.practitioner import Practitioner
from starlette.responses import RedirectResponse

import fhirstarter
from fhirstarter import (
    FHIRProvider,
    FHIRStarter,
    InteractionContext,
    Request,
    Response,
    examples,
)
from fhirstarter.exceptions import FHIRResourceNotFoundError

# Create the app with the provided config file
app = FHIRStarter(
    title="FHIRStarter Example Implementation",
    config_file=cast(Path, importlib.resources.files(examples)) / "config.toml",
)

# Create a "database"
DATABASE: dict[str, Patient] = {}

# Create a provider
provider = FHIRProvider()

# To register FHIR interactions with  a provider, the pieces of information the developer has to
# provide are:
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


# Optional: Provide a custom example for the automatic documentation by defining a subclass of the
# FHIR Practitioner Pydantic model. If a custom model is not provided, examples from the FHIR
# specification are used.
class PractitionerCustom(Practitioner):
    class Config:
        schema_extra = {
            "example": {
                "resourceType": "Practitioner",
                "id": "example",
                "name": [{"family": "Careful", "given": ["Adam"], "prefix": ["Dr"]}],
            }
        }


# Register the practitioner read FHIR interaction with the provider using the custom subclass
@provider.read(PractitionerCustom)
async def practitioner_read(context: InteractionContext, id_: Id) -> PractitionerCustom:
    return PractitionerCustom(**PractitionerCustom.Config.schema_extra["example"])


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
    fhirstarter_dir = cast(Path, importlib.resources.files(fhirstarter))
    uvicorn.run(
        "example:app",
        use_colors=True,
        reload=True,
        reload_dirs=str(fhirstarter_dir.parent),
    )
