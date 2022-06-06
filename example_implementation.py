from uuid import uuid4

import uvicorn
from fhir.resources.fhirtypes import Id
from fhir.resources.patient import Patient
from starlette.responses import RedirectResponse

from fhirstarter import FHIRInteractionResult, FHIRProvider, FHIRStarter
from fhirstarter.exceptions import FHIRResourceNotFoundError

# Create a "database"
DATABASE: dict[str, Patient] = {}

# Create the provider
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
async def patient_create(resource: Patient) -> FHIRInteractionResult[Patient]:
    # All Canvas-to-FHIR mapping code for a Patient create operation goes here. For a create
    # operation, an integration message is sent to the integration message router
    resource.id = uuid4().hex
    DATABASE[resource.id] = resource

    return FHIRInteractionResult[Patient](resource.id)


# Register the patient read FHIR interaction with the provider
@provider.register_read_interaction(Patient)
async def patient_read(id_: Id) -> FHIRInteractionResult[Patient]:
    # All Canvas-to-FHIR mapping code for a Patient read operation goes here. For a read
    # operation, a GraphQL request is issued, and then the result is mapped on to the FHIR
    # Patient resource to be returned.
    patient = DATABASE.get(id_)
    if not patient:
        raise FHIRResourceNotFoundError

    return FHIRInteractionResult[Patient](patient.id, patient)


# Create the app
app = FHIRStarter(title="FHIRStarter Example Implementation")

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
