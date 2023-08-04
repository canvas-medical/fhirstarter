"""FHIRStarter test configuration"""

from copy import deepcopy
from tempfile import NamedTemporaryFile
from typing import cast

from fhir.resources.bundle import Bundle
from fhir.resources.fhirtypes import Id
from fhir.resources.humanname import HumanName
from fhir.resources.patient import Patient

from ..exceptions import FHIRResourceNotFoundError
from ..fhirstarter import FHIRStarter
from ..interactions import InteractionContext
from ..providers import FHIRProvider
from ..testclient import TestClient
from .utils import generate_fhir_resource_id

# In-memory "database" used to simulate persistence of created FHIR resources
DATABASE: dict[str, Patient] = {}

_VALID_TOKEN = "valid"
_INVALID_TOKEN = "invalid"


async def patient_create_async(context: InteractionContext, resource: Patient) -> Id:
    """Patient create FHIR interaction."""
    return patient_create(context, resource)


def patient_create(_: InteractionContext, resource: Patient) -> Id:
    """Patient create FHIR interaction."""
    patient = deepcopy(resource)
    patient.id = generate_fhir_resource_id()
    DATABASE[patient.id] = patient

    return Id(patient.id)


async def patient_read_async(context: InteractionContext, id_: Id) -> Patient:
    """Patient read FHIR interaction."""
    return patient_read(context, id_)


def patient_read(_: InteractionContext, id_: Id) -> Patient:
    """Patient read FHIR interaction."""
    patient = DATABASE.get(id_)
    if not patient:
        raise FHIRResourceNotFoundError

    return patient


async def patient_search_type_async(
    context: InteractionContext,
    family: str | None,
    general_practitioner: str | None,
    nickname: str | None,
    _last_updated: str | None,
) -> Bundle:
    """Patient search-type FHIR interaction."""
    return patient_search_type(
        context, family, general_practitioner, nickname, _last_updated
    )


def patient_search_type(
    _: InteractionContext,
    family: str | None,
    general_practitioner: str | None,
    nickname: str | None,
    _last_updated: str | None,
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
            "entry": [{"resource": patient.dict()} for patient in patients],
        }
    )

    return bundle


async def patient_update_async(
    context: InteractionContext, id_: Id, resource: Patient
) -> Id:
    """Patient update FHIR interaction."""
    return patient_update(context, id_, resource)


def patient_update(_: InteractionContext, id_: Id, resource: Patient) -> Id:
    """Patient update FHIR interaction."""
    if id_ not in DATABASE:
        raise FHIRResourceNotFoundError

    patient = deepcopy(resource)
    DATABASE[id_] = patient

    return Id(patient.id)


def app(provider: FHIRProvider) -> TestClient:
    """Create a FHIRStarter app, add the provider, reset the database, and return a TestClient."""
    config_file_contents = """
[search-parameters.Patient.nickname]
type = "string"
description = "Nickname"
uri = "https://hostname/nickname"
include-in-capability-statement = true
    """

    with NamedTemporaryFile("w") as config_file:
        config_file.write(config_file_contents)
        config_file.seek(0)
        app = FHIRStarter(config_file_name=config_file.name)

    app.add_providers(provider)

    DATABASE.clear()

    return TestClient(app)


def create_test_client(
    interactions: tuple[str, ...], async_endpoints: bool
) -> TestClient:
    """Given a list of interactions and an async flag, create an app and return a test client."""
    provider = FHIRProvider()

    for interaction in interactions:
        match interaction, async_endpoints:
            case "create", True:
                provider.create(Patient)(patient_create_async)
            case "create", False:
                provider.create(Patient)(patient_create)
            case "read", True:
                provider.read(Patient)(patient_read_async)
            case "read", False:
                provider.read(Patient)(patient_read)
            case "search-type", True:
                provider.search_type(Patient)(patient_search_type_async)
            case "search-type", False:
                provider.search_type(Patient)(patient_search_type)
            case "update", True:
                provider.update(Patient)(patient_update_async)
            case "update", False:
                provider.update(Patient)(patient_update)

    return app(provider)
