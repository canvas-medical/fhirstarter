import uvicorn
from fhir.resources.fhirtypes import Id
from fhir.resources.patient import Patient
from src.logging import configure_logging
from fhirstarter import FHIRProvider, FHIRStarter, InteractionContext
from fhirstarter.exceptions import FHIRResourceNotFoundError
from src.lifetime import register_shutdown_event, register_startup_event,set_multiproc_dir

# Create the app
configure_logging()
app = FHIRStarter()
class Test:
    def __init__(self):
        pass
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

# Register the vread FHIR interaction with the provider
@provider.vread(Patient)
async def patient_vread(context: InteractionContext, id_: Id, version_id: str) -> Patient:
    # Get the patient from the database with the specified version_id
    patient = ...

    if not patient:
        raise FHIRResourceNotFoundError

    return Patient(
        **{
            # Map patient from database to FHIR Patient structure for the specified version
        }
    )

# Add the provider to the app
app.add_providers(provider)
 # Adds startup and shutdown events.


if __name__ == "__main__":
    # Start the server
    
    set_multiproc_dir()
    register_startup_event(app)
    register_shutdown_event(app)
    uvicorn.run(app)
