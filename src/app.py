import uvicorn
from fhir.resources.fhirtypes import Id
from fhir.resources.patient import Patient
from src.logging import configure_logging
from fhirstarter import FHIRProvider, FHIRStarter, InteractionContext
from fhirstarter.exceptions import FHIRResourceNotFoundError
from src.lifetime import register_shutdown_event, register_startup_event,set_multiproc_dir
from pydantic import BaseModel
from datetime import datetime
from uuid import uuid4
from copy import deepcopy
#Import for healtcheck
from fastapi import APIRouter
from starlette import status
from src.config import settings

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
# regsiter the create patient FHIR interaction with the provider
# Create a "database"
DATABASE: dict[str, Patient] = {}
@provider.create(Patient)
async def patient_create(context: InteractionContext, resource: Patient) -> Id:
    patient = deepcopy(resource)
    patient.id = Id(uuid4().hex)
    DATABASE[patient.id] = patient

    return Id(patient.id)


# Add the provider to the app
app.add_providers(provider)



# Define a healthcheck route
class HealthResponse(BaseModel):
    """Health Check Response Model."""
    app_name: str = settings.APP_NAME
    app_version: str = settings.APP_VERSION
    status: str = "pass"
    timestamp: datetime = datetime.now()

router = APIRouter()

@router.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
def health_check() -> HealthResponse:
    """Checks the health of a project.

    :return: 200 if the project is healthy.
    """
    return HealthResponse()

app.include_router(router, prefix="/api/v1")


if __name__ == "__main__":
    # Start the server
    
    set_multiproc_dir()
    register_startup_event(app)
    register_shutdown_event(app)
    uvicorn.run(app,use_colors=True)
