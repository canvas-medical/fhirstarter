# fhirstarter

An ASGI FHIR API framework built on top of [FastAPI](https://fastapi.tiangolo.com) and [FHIR Resources](https://pypi.org/project/fhir.resources/).

The only version of FHIR that is currently supported is 4.0.1.

## Installation

```bash
pip install fhirstarter
```

## Features

* Automatic, standardized API route creation
* Automatic validation of inputs and outputs through the use of FHIR resource Pydantic models
* Automatically-generated capability statement and capability statement API route
* An exception-handling framework that produces FHIR-friendly responses (i.e. OperationOutcomes)
* Automatically-generated, integrated documentation generated from the FHIR specification

## Background

FHIRStarter uses a provider-decorator pattern. Developers can write functions that implement FHIR
interactions -- such as create, read, search-type, and update -- and plug them into the framework.
FHIRStarter then automatically creates FHIR-compatible API routes from these developer-provided
functions. FHIR interactions that are supplied must use the resource classes defined by the
[FHIR Resources](https://pypi.org/project/fhir.resources/) Python package, which is a collection of
Pydantic models for FHIR resources.

In order to stand up a FHIR server, all that is required is to create a FHIRStarter and a
FHIRProvider instance, register a FHIR interaction with the provider, add the provider to the
FHIRStarter instance, and pass the FHIRStarter instance to an ASGI server.

## Usage

A detailed example is available here: 
[fhirstarter/scripts/example.py](fhirstarter/scripts/example.py).

```python
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
```
