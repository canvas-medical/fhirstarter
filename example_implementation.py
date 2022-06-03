import uvicorn
from fhir.resources.patient import Patient
from starlette.responses import RedirectResponse

from fhirstarter import FHIRProvider, FHIRStarter
from fhirstarter.exceptions import FHIRResourceNotFoundError

# Create the provider
provider = FHIRProvider()


# Register the patient read FHIR interaction with the provider.
#
# The pieces of information the developer has to provide in order to create a route are:
# - FHIR interaction type (this affects what the endpoint will look like)
# - FHIR resource type (this affects validation of inputs and outputs, and what search parameters
#   are valid)
# - the actual callable (expected signature and annotations need to match the defined protocols,
#   because thes values affect route creation in FastAPI)
@provider.register_read_interaction(Patient)
async def patient_read(id_: str) -> Patient:
    # All Canvas-to-FHIR mapping code for a Patient read operation goes here. For a read
    # operation, a GraphQL request is issued, and then the result is mapped on to the FHIR
    # Patient resource to be returned.

    if id_ != "bilbo":
        raise FHIRResourceNotFoundError

    patient = Patient(**{"name": [{"family": "Baggins", "given": ["Bilbo"]}]})

    return patient


# Create the app
app = FHIRStarter(title="FHIRStarter Example Implementation")

# Add the provider to the app. This will automatically generate the API routes that the providers
# need (e.g. create, read, search, and update).
app.add_providers(provider)


@app.get("/", include_in_schema=False)
async def index() -> RedirectResponse:
    """Redirect main page to API docs."""
    return RedirectResponse("/docs")


if __name__ == "__main__":
    # Start the server
    uvicorn.run("example_implementation:app", reload=True)
