"""
An example FHIR server implementation using FHIRStarter, with examples showing how to create FHIR interactions
(i.e. endpoints) that perform read, update, patch, delete, create, and search-type actions.
"""

import contextlib
import json
from pathlib import Path
from typing import Any, Dict, List, MutableMapping, Union
from uuid import uuid4

import jsonpatch
import uvicorn
from fhir.resources.bundle import Bundle
from fhir.resources.fhirtypes import Id
from fhir.resources.patient import Patient
from fhir.resources.practitioner import Practitioner
from starlette.responses import RedirectResponse

import fhirstarter
from fhirstarter import (
    FHIRProvider,
    FHIRStarter,
    InteractionContext,
    JSONPatch,
    Request,
    Response,
    convert_json_patch,
    examples,
)
from fhirstarter.exceptions import (
    FHIRResourceNotFoundError,
    FHIRUnprocessableEntityError,
)

# Create the app with the provided config file
app = FHIRStarter(
    title="FHIRStarter Example Implementation",
    config_file=Path(examples.__file__).parent / "config.toml",
)

# Create a "database"
DATABASE: Dict[str, Dict[str, str]] = {"Patient": {}, "Practitioner": {}}

# Create a provider
provider = FHIRProvider()

# To register FHIR interactions with  a provider, the pieces of information the developer has to
# provide are:
# * FHIR interaction type (this affects what the endpoint will look like)
# * FHIR resource type (this affects validation of inputs and outputs, and what search parameters
#   are valid)
# * the handler (expected signature and annotations need to match the defined protocols, because
#   these values affect route creation in FastAPI)


# Register the patient read FHIR interaction with the provider
@provider.read(Patient)
async def patient_read(context: InteractionContext, id_: Id) -> Patient:
    patient = DATABASE["Patient"].get(id_)
    if not patient:
        raise FHIRResourceNotFoundError

    return Patient(**json.loads(patient))


# Register the patient update FHIR interaction with the provider
@provider.update(Patient)
async def patient_update(context: InteractionContext, id_: Id, resource: Patient) -> Id:
    if id_ not in DATABASE["Patient"]:
        raise FHIRResourceNotFoundError

    DATABASE["Patient"][id_] = resource.json(separators=(",", ":"))

    return Id(id_)


# Register the patient patch FHIR interaction with the provider
@provider.patch(Patient)
async def patient_patch(
    context: InteractionContext, id_: Id, json_patch: JSONPatch
) -> Id:
    patient = json.loads(DATABASE["Patient"].get(id_, "{}"))
    if not patient:
        raise FHIRResourceNotFoundError

    # Convert the JSONPatch object to a list of dicts using the helper function, and use the
    # jsonpatch package to apply the patch to the patient resource
    patch = convert_json_patch(json_patch)
    jsonpatch.apply_patch(patient, jsonpatch.JsonPatch(patch), in_place=True)

    # Validate the change
    try:
        Patient.validate(patient)
    except Exception as exception:
        raise FHIRUnprocessableEntityError(
            code="invalid", details_text="Validation of patched resource failed"
        ) from exception

    DATABASE["Patient"][id_] = json.dumps(patient, separators=(",", ":"))

    return Id(id_)


@provider.delete(Patient)
async def patient_delete(context: InteractionContext, id_: Id) -> None:
    with contextlib.suppress(KeyError):
        del DATABASE["Patient"][id_]

    return None


# Register the patient create FHIR interaction with the provider
@provider.create(Patient)
async def patient_create(context: InteractionContext, resource: Patient) -> Id:
    id_ = str(uuid4())

    resource.id = id_
    DATABASE["Patient"][id_] = resource.json(separators=(",", ":"))

    return Id(id_)


# Register the patient search-type FHIR interaction with the provider
@provider.search_type(Patient)
async def patient_search_type(
    context: InteractionContext,
    birthdate: Union[List[str], None],
    general_practitioner: Union[str, None],
    family: Union[str, None],
    nickname: Union[str, None],
    _last_updated: Union[str, None],
) -> Bundle:
    patients = []
    for patient_serialized in DATABASE["Patient"].values():
        patient = json.loads(patient_serialized)
        for name in patient.get("name", {}):
            if name.get("family") == family:
                patients.append(patient)

    bundle = Bundle(
        **{
            "type": "searchset",
            "total": len(patients),
            "entry": [{"resource": patient} for patient in patients],
        }
    )

    return bundle


# Optional: Provide a custom example for the automatic documentation by defining a subclass of the
# FHIR Practitioner Pydantic model. If a custom model is not provided, examples from the FHIR
# specification are used.
class PractitionerCustom(Practitioner):
    class Config:
        schema_extra = {
            "example": {
                "resourceType": "Practitioner",
                "id": "example",
                "name": [{"family": "Careful", "given": ["Adam"], "prefix": ["Dr"]}],
            }
        }


# Register the practitioner read FHIR interaction with the provider using the custom subclass
@provider.read(PractitionerCustom)
async def practitioner_read(context: InteractionContext, id_: Id) -> PractitionerCustom:
    practitioner = DATABASE["Practitioner"].get(id_)
    if not practitioner:
        raise FHIRResourceNotFoundError

    return PractitionerCustom(**json.loads(practitioner))


# Add the provider to the app. This will automatically generate the API routes for the interactions
# provided by the providers (e.g. create, read, search-type, and update).
app.add_providers(provider)


# Customize the capability statement
def amend_capability_statement(
    capability_statement: MutableMapping[str, Any], request: Request, response: Response
) -> MutableMapping[str, Any]:
    capability_statement["publisher"] = "Canvas Medical"
    return capability_statement


app.set_capability_statement_modifier(amend_capability_statement)


# Redirect the main page to the API docs
@app.get("/", include_in_schema=False)
async def index() -> RedirectResponse:
    return RedirectResponse("/docs")


if __name__ == "__main__":
    # Start the server
    fhirstarter_dir = Path(fhirstarter.__file__).parent
    uvicorn.run(
        "example:app",
        use_colors=True,
        reload=True,
        reload_dirs=str(fhirstarter_dir.parent),
    )
