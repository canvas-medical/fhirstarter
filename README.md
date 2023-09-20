# fhirstarter

<p>
  <a href="https://github.com/canvas-medical/fhirstarter/actions?query=workflow%3Atests+event%3Apush+branch%3Amain" target="_blank">
    <img src="https://github.com/canvas-medical/fhirstarter/workflows/tests/badge.svg?event=push&branch=main" alt="tests">
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

An ASGI [FHIR](https://hl7.org/fhir/) API framework built on top of [FastAPI](https://fastapi.tiangolo.com) and
[FHIR Resources](https://pypi.org/project/fhir.resources/).

Supports FHIR sequences:
* [STU (v3.0.2)](https://hl7.org/fhir/STU3/)
* [R4 (v4.0.1)](https://hl7.org/fhir/R4/)
* [R4B (v4.3.0)](https://hl7.org/fhir/R4B/)
* [R5 (v5.0.0)](https://hl7.org/fhir/R5/)

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

FHIRStarter was built based on the business needs of
[Canvas Medical](https://www.canvasmedical.com). At any point in time, it may not be broadly
applicable to the industry at large. Canvas Medical open-sourced the project so that it can be used
by healthcare software developers whose needs it might also meet. Ongoing support and development
will be based on the business needs of Canvas Medical.

## Background

FHIRStarter uses a provider-decorator pattern. Developers can write functions, or handlers, that
implement FHIR interactions -- such as create, read, search-type, and update -- and plug them into
the framework. FHIRStarter then automatically creates FHIR-compatible API routes from these
developer-provided functions. FHIR interactions that are supplied must use the resource classes
defined by the [FHIR Resources](https://pypi.org/project/fhir.resources/) Python package, which is a
collection of Pydantic models for FHIR resources.

In order to stand up a FHIR server, all that is required is to create a FHIRStarter and a
FHIRProvider instance, register a FHIR interaction with the provider, add the provider to the
FHIRStarter instance, and pass the FHIRStarter instance to an ASGI server.

## Usage

### Currently-supported functionality

FHIRStarter supports create, read, search-type, and update endpoints across all FHIR resource
types, and will automatically generate the `/metadata` capabilities statement endpoint.

Handlers can be written as coroutines with `async/await` syntax, or as plain functions. FastAPI
supports both, as does FHIRStarter.

Using uvloop can improve performance of the underlying event loop on supported platforms. 
FHIRStarter does not mandate the use of uvloop, but it may be enabled by importing uvloop and
adding a snippet like this to your application startup script:

```python
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
```

### Configuration for specific FHIR sequences

FHIRStarter will work out of the box as an R5 server. If a different sequence is desired, it must be
specified with an environment variable:

```shell
FHIR_SEQUENCE=R4B
```

The latest version of the [FHIR Resources](https://pypi.org/project/fhir.resources/) package only
supports FHIR STU3, R4B, and R5. FHIR R4 is supported by an earlier version. Because of this, if a
developer desires to use FHIR R4, then the developer must pin version **6.4.0** of fhir.resources in
their project. FHIRStarter will check the version of fhir.resources against the specified FHIR
version in the environment variable to ensure that they are compatible.

Model imports are also affected by which version of fhir.resources is installed. For STU3 and R4B,
model imports will look like this:

```python
from fhir.resources.STU3.patient import Patient
```
```python
from fhir.resources.R4B.patient import Patient
```

For R4 and R5, model imports will look like this:

```python
from fhir.resources.patient import Patient
```

### Example

A detailed example is available here: [example.py](https://github.com/canvas-medical/fhirstarter/blob/main/fhirstarter/examples/example.py).

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

FastAPI's [dependency injection system](https://fastapi.tiangolo.com/tutorial/dependencies/) is exposed at various levels:

* **application**: the `__init__` method on the FHIRStarter class
* **provider**: the `__init__` method on the FHIRProvider class
* **handler**: the `create`, `read`, `search_type`, or `update` decorator used to add a handler to a provider

Dependencies specified at the application level will be injected into all routes in the application.

Dependencies specified at the provider level will be injected into all routes that are added to
the application from that specific provider.

Dependencies specified at the handler level only apply to that specific FHIR interaction.
