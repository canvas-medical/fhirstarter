# fhirstarter

<p>
  <a href="https://github.com/canvas-medical/fhirstarter/actions/workflows/test.yml">
    <img src="https://github.com/canvas-medical/fhirstarter/actions/workflows/test.yml/badge.svg">
  </a>
  <a href="https://pypi.org/project/fhirstarter/">
    <img src="https://img.shields.io/pypi/v/fhirstarter">
  </a>
  <a href="https://pypi.org/project/fhirstarter/">
    <img src="https://img.shields.io/pypi/pyversions/fhirstarter">
  </a>
  <a href="https://pypi.org/project/fhirstarter/">
    <img src="https://img.shields.io/pypi/l/fhirstarter">
  </a>
  <a href="https://github.com/psf/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000">
  </a>
</p>

An ASGI FHIR API framework built on top of [FastAPI](https://fastapi.tiangolo.com) and
[FHIR Resources](https://pypi.org/project/fhir.resources/).

The only version of FHIR that is currently supported is 4.0.1.

## Installation

```bash
pip install fhirstarter
```

## Features

* Automatic, standardized API route creation
* Automatic validation of inputs and outputs through the use of FHIR Resources Pydantic models
* Automatically-generated capability statement that can be customized, and a capability statement
  API route
* An exception-handling framework that produces FHIR-friendly responses (i.e. OperationOutcomes)
* Automatically-generated, integrated documentation generated from the FHIR specification
* Custom search parameters for search endpoints

### Disclaimer

FHIRStarter was built based on the business needs of Canvas Medical. At any point in time, it may
not be broadly applicable to the industry at large. Canvas Medical open-sourced the project so that
it can be used by healthcare software developers whose needs it might also meet. Ongoing support and
development will be based on the business needs of Canvas Medical.

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

### Currently-supported functionality

FHIRStarter supports create, read, search-type, and update endpoints across all FHIR R4 resource
types, and will automatically generate the `/metadata` capabilities statement endpoint.

### Example

A detailed example is available here: [example.py](https://github.com/canvas-medical/fhirstarter/blob/main/fhirstarter/scripts/example.py).

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

### Custom search parameters

Custom search parameters can be defined in a configuration file that can be passed to the app on
creation.

```toml
[search-parameters.Patient.nickname]
type = "string"
description = "Nickname"
uri = "https://hostname/nickname"
include-in-capability-statement = true
```

Adding a custom search parameter via configuration allows this name to be used as an argument when
defining a search-type interaction handler and also adds this search parameter to the API
documentation for the search endpoint.

### Capability statement

It is possible to customize the capability statement by setting a capability statement modifier:

```python
def amend_capability_statement(
    capability_statement: MutableMapping[str, Any], request: Request, response: Response
) -> MutableMapping[str, Any]:
    capability_statement["publisher"] = "Canvas Medical"
    return capability_statement

app.set_capability_statement_modifier(amend_capability_statement)
```

### FastAPI dependency injection

FastAPI's dependency injection is exposed at various levels:

* **application**: the `__init__` method on the FHIRStarter class
* **provider**: the `__init__` method on the FHIRProvider class
* **handler**: the `create`, `read`, `search_type`, or `update` decorator used to add a handler to a provider

Dependencies specified at the application level will be injected into all routes in the application.

Dependencies specified at the provider level will be injected into all routes that are added to
the application from that specific provider.

Dependencies specified at the handler level only apply to that specific FHIR interaction.

## Forward compatibility

At some point in the future, it will be necessary to support FHIR R5. How this might be supported on
a server that continues to support R4 has not yet been determined (e.g. a header that specifies the
version, adding the FHIR version to the URL path, etc.). It may be necessary to support alteration
of how the URL path is specified through the provider construct. Currently, the FHIR version is not
part of the URL path, so the default behavior is that an API route defined as `/Patient` will be an
R4 endpoint.
