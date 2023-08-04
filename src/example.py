import uvicorn
from fhir.resources.fhirtypes import Id
from fhir.resources.patient import Patient

from fhirstarter import FHIRProvider, FHIRStarter, InteractionContext
from fhirstarter.exceptions import FHIRResourceNotFoundError

# Create the app
app = FHIRStarter()

# Create a provider
provider = FHIRProvider()


# Register the patient read FHIR interaction with the provider
@provider.read(Patient)
async def patient_read(context: InteractionContext, id_: Id) -> Patient:
    # Get the patient from the database
    patient = ...

    if not patient:
        raise FHIRResourceNotFoundError

    return Patient(
        **{
            # Map patient from database to FHIR Patient structure
        }
    )




# Add the provider to the app
app.add_providers(provider)


if __name__ == "__main__":
    # Start the server
    uvicorn.run(app)