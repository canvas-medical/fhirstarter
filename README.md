# fhirstarter

A FHIR API framework built on top of [FastAPI](https://fastapi.tiangolo.com) and [FHIR Resources](https://pypi.org/project/fhir.resources/).

## Installation

```bash
pip install fhirstarter
```

## Features

* Automatic, standardized API route creation
* Automatic validation of inputs and outputs through the use of FHIR resource Pydantic models
* Automatically generated capability statement and capability statement API route
* An exception-handling framework that produces FHIR-friendly responses (i.e. OperationOutcomes)
* Automatically generated, integrated documentation generated from the FHIR specification.

## Background

FHIRStarter uses a provider pattern to enable developers to plug functions into the framework that implement FHIR interactions such as create, read, search, and update, and have FHIR-compatible API routes created automatically. FHIR interactions that are supplied must use the resource classes defined by the [FHIR Resources](https://pypi.org/project/fhir.resources/) Python package, which is a collection of Pydantic models for FHIR resources.

In order to stand up a FHIR server, all that is required is to create a FHIRStarter and a FHIRProvider instance, register a FHIR interaction with the provider, add the provider to the FHIRStarter instance, and pass the FHIRStarter instance to an ASGI server.

## Usage

```python
import uvicorn
from fhir.resources.fhirtypes import Id
from fhir.resources.patient import Patient
from fhirstarter import FHIRProvider, FHIRStarter
from fhirstarter.exceptions import FHIRResourceNotFoundError

# Create the app
app = FHIRStarter()

# Create a provider
provider = FHIRProvider()

# Register the patient read FHIR interaction with the provider
@provider.register_read_interaction(Patient)
async def patient_read(id_: Id, **kwargs: str) -> Patient:
    # Get the patient from the database
    patient = ...

    if not patient:
        raise FHIRResourceNotFoundError

    return Patient(
        **{
            ... # Map patient from database to FHIR Patient structure
        }
    )

# Add the provider to the app
app.add_providers(provider)

if __name__ == "__main__":
    # Start the server
    uvicorn.run(app)

```
