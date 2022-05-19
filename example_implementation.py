import uvicorn
from fhir.resources.patient import Patient

from fhirstarter import FHIRProvider, FHIRStarter


# Define a provider for a resource (the functions will define what FHIR operations are supported for
# the resource).
class PatientProvider(FHIRProvider):
    def resource_obj_type(self) -> type:
        return Patient

    @staticmethod
    async def read(id_: str) -> Patient:
        # All Canvas-to-FHIR mapping code for a Patient read operation goes here. For a read
        # operation, a GraphQL request is issued, and then the result is mapped on to the FHIR
        # Patient resource to be returned.

        patient = Patient(**{"name": [{"family": "Baggins", "given": ["Bilbo"]}]})

        return patient


# Create the app
app = FHIRStarter()

# Add the patient provider to the app. This will automatically generate the API routes that the
# providers need (e.g. create, read, search, and update).
app.add_providers(PatientProvider())

if __name__ == "__main__":
    # Start the server
    uvicorn.run(app)
