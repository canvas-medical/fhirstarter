"""
An example FHIR server implementation using FHIRStarter, with examples showing how to create FHIR
interactions (i.e. endpoints) that perform create, read, search, and update operations.
"""

from copy import deepcopy
from uuid import uuid4

import uvicorn
from fhir.resources.bundle import Bundle
from fhir.resources.fhirtypes import Id
from fhir.resources.patient import Patient
from starlette.responses import RedirectResponse

from fhirstarter import FHIRProvider, FHIRStarter
from fhirstarter.exceptions import FHIRResourceNotFoundError

# Create the app
app = FHIRStarter(title="FHIRStarter Example Implementation")

# Create a "database"
DATABASE: dict[str, Patient] = {}

# Create a provider
provider = FHIRProvider()

# To register FHIR interactions with  a provider, the pieces of information the developer has to
# provider are:
# - FHIR interaction type (this affects what the endpoint will look like)
# - FHIR resource type (this affects validation of inputs and outputs, and what search parameters
#   are valid)
# - the actual callable (expected signature and annotations need to match the defined protocols,
#   because these values affect route creation in FastAPI)


# Register the patient create FHIR interaction with the provider
@provider.register_create_interaction(Patient)
async def patient_create(resource: Patient, **kwargs: str) -> Id:
    patient = deepcopy(resource)
    patient.id = Id(uuid4().hex)
    DATABASE[patient.id] = patient

    return Id(patient.id)


# Register the patient read FHIR interaction with the provider
@provider.register_read_interaction(Patient)
async def patient_read(id_: Id, **kwargs: str) -> Patient:
    patient = DATABASE.get(id_)
    if not patient:
        raise FHIRResourceNotFoundError

    return patient


# Register the patient search FHIR interaction with the provider
@provider.register_search_interaction(Patient)
async def patient_search(family: str | None = None, **kwargs: str) -> Bundle:
    patients = []
    for patient in DATABASE.values():
        for name in patient.name:
            if name.family == family:
                patients.append(patient)

    bundle = Bundle(
        **{
            "type": "searchset",
            "total": len(patients),
            "entry": [{"resource": {**patient.dict()}} for patient in patients],
        }
    )

    return bundle


# Register the patient update FHIR interaction with the provider
@provider.register_update_interaction(Patient)
async def patient_update(id_: Id, resource: Patient, **kwargs: str) -> Id:
    if id_ not in DATABASE:
        raise FHIRResourceNotFoundError

    patient = deepcopy(resource)
    DATABASE[id_] = patient

    return Id(patient.id)


# Add the provider to the app. This will automatically generate the API routes for the interactions
# provided by the providers (e.g. create, read, search, and update).
app.add_providers(provider)


# Redirect the main page to the API docs
@app.get("/", include_in_schema=False)
async def index() -> RedirectResponse:
    return RedirectResponse("/docs")


if __name__ == "__main__":
    # Start the server
    uvicorn.run("example_implementation:app", reload=True)
