"""FHIRStarter test configuration"""

from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict, Tuple, Union, cast

import jsonpatch

from ..exceptions import FHIRResourceNotFoundError
from ..fhirstarter import FHIRStarter
from ..interactions import InteractionContext
from ..json_patch import JSONPatch, convert_json_patch
from ..providers import FHIRProvider
from ..resources import Bundle
from ..testclient import TestClient
from .resources import HumanName, Patient
from .utils import generate_fhir_resource_id

# In-memory "database" used to simulate persistence of created FHIR resources
DATABASE: Dict[str, Patient] = {}

_VALID_TOKEN = "valid"
_INVALID_TOKEN = "invalid"


async def patient_read_async(context: InteractionContext, id_: str) -> Patient:
    """Patient read FHIR interaction."""
    return patient_read(context, id_)


def patient_read(_: InteractionContext, id_: str) -> Patient:
    """Patient read FHIR interaction."""
    patient = DATABASE.get(id_)
    if not patient:
        raise FHIRResourceNotFoundError

    return patient


async def patient_update_async(
    context: InteractionContext, id_: str, resource: Patient
) -> str:
    """Patient update FHIR interaction."""
    return patient_update(context, id_, resource)


def patient_update(_: InteractionContext, id_: str, resource: Patient) -> str:
    """Patient update FHIR interaction."""
    if id_ not in DATABASE:
        raise FHIRResourceNotFoundError

    patient = deepcopy(resource)
    DATABASE[id_] = patient

    return patient.id


async def patient_patch_async(
    context: InteractionContext, id_: str, json_patch: JSONPatch
) -> str:
    """Patient patch FHIR interaction."""
    return patient_patch(context, id_, json_patch)


def patient_patch(_: InteractionContext, id_: str, json_patch: JSONPatch) -> str:
    """Patient patch FHIR interaction."""
    if id_ not in DATABASE:
        raise FHIRResourceNotFoundError

    patient = DATABASE[id_].model_dump()

    jsonpatch.apply_patch(
        patient, jsonpatch.JsonPatch(convert_json_patch(json_patch)), in_place=True
    )

    DATABASE[id_] = Patient(**patient)

    return id_


async def patient_delete_async(context: InteractionContext, id_: str) -> None:
    """Patient delete FHIR interaction."""
    return patient_delete(context, id_)


def patient_delete(_: InteractionContext, id_: str) -> None:
    """Patient delete FHIR interaction."""
    if id_ not in DATABASE:
        return

    del DATABASE[id_]

    return None


async def patient_create_async(context: InteractionContext, resource: Patient) -> str:
    """Patient create FHIR interaction."""
    return patient_create(context, resource)


def patient_create(_: InteractionContext, resource: Patient) -> str:
    """Patient create FHIR interaction."""
    patient = deepcopy(resource)
    patient.id = generate_fhir_resource_id()
    DATABASE[patient.id] = patient

    return patient.id


async def patient_search_type_async(
    context: InteractionContext,
    family: Union[str, None],
    general_practitioner: Union[str, None],
    nickname: Union[str, None],
    _last_updated: Union[str, None],
) -> Bundle:
    """Patient search-type FHIR interaction."""
    return patient_search_type(
        context, family, general_practitioner, nickname, _last_updated
    )


def patient_search_type(
    _: InteractionContext,
    family: Union[str, None],
    general_practitioner: Union[str, None],
    nickname: Union[str, None],
    _last_updated: Union[str, None],
) -> Bundle:
    """Patient search-type FHIR interaction."""
    patients = []
    for patient in DATABASE.values():
        for name in patient.name:
            if cast(HumanName, name).family == family:
                patients.append(patient)

    bundle = Bundle(
        **{
            "type": "searchset",
            "total": len(patients),
            "entry": [{"resource": patient.model_dump()} for patient in patients],
        }
    )

    return bundle


def app(provider: FHIRProvider) -> TestClient:
    """Create a FHIRStarter app, add the provider, reset the database, and return a TestClient."""
    config_file_contents = """
[app.external-documentation-examples]
enabled = true
cache-size = 2048  # number of entries
cache-ttl-hours = 6

[search-parameters.Patient.nickname]
type = "string"
description = "Nickname"
uri = "https://hostname/nickname"
include-in-capability-statement = true
    """

    with TemporaryDirectory() as path:
        config_file = Path(path) / "config.toml"
        with open(config_file, "w") as file_:
            file_.write(config_file_contents)

        app_ = FHIRStarter(config_file=config_file)

    app_.add_providers(provider)

    DATABASE.clear()

    return TestClient(app_)


def create_test_client_async(interactions: Tuple[str, ...]) -> TestClient:
    """Given a list of interactions, create an app with async handlers and return a test client."""
    provider = FHIRProvider()

    for interaction in interactions:
        if interaction == "read":
            provider.read(Patient)(patient_read_async)
        elif interaction == "update":
            provider.update(Patient)(patient_update_async)
        elif interaction == "patch":
            provider.patch(Patient)(patient_patch_async)
        elif interaction == "delete":
            provider.delete(Patient)(patient_delete_async)
        elif interaction == "create":
            provider.create(Patient)(patient_create_async)
        elif interaction == "search-type":
            provider.search_type(Patient)(patient_search_type_async)

    return app(provider)


def create_test_client(interactions: Tuple[str, ...]) -> TestClient:
    """Given a list of interactions, create an app and return a test client."""
    provider = FHIRProvider()

    for interaction in interactions:
        if interaction == "read":
            provider.read(Patient)(patient_read)
        elif interaction == "update":
            provider.update(Patient)(patient_update)
        elif interaction == "patch":
            provider.patch(Patient)(patient_patch)
        elif interaction == "delete":
            provider.delete(Patient)(patient_delete)
        elif interaction == "create":
            provider.create(Patient)(patient_create)
        elif interaction == "search-type":
            provider.search_type(Patient)(patient_search_type)

    return app(provider)
