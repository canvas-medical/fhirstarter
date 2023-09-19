"""FHIRStarter test configuration"""

from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import cast

from ..exceptions import FHIRResourceNotFoundError
from ..fhirstarter import FHIRStarter
from ..interactions import InteractionContext
from ..providers import FHIRProvider
from ..resources import Bundle, Id
from ..testclient import TestClient
from .resources import HumanName, Patient
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

    with TemporaryDirectory() as path:
        config_file = Path(path) / "config.toml"
        with open(config_file, "w") as file_:
            file_.write(config_file_contents)

        app_ = FHIRStarter(config_file=config_file)

    app_.add_providers(provider)

    DATABASE.clear()

    return TestClient(app_)


def create_test_client_async(interactions: tuple[str, ...]) -> TestClient:
    """Given a list of interactions, create an app with async handlers and return a test client."""
    provider = FHIRProvider()

    for interaction in interactions:
        match interaction:
            case "create":
                provider.create(Patient)(patient_create_async)
            case "read":
                provider.read(Patient)(patient_read_async)
            case "search-type":
                provider.search_type(Patient)(patient_search_type_async)
            case "update":
                provider.update(Patient)(patient_update_async)

    return app(provider)


def create_test_client(interactions: tuple[str, ...]) -> TestClient:
    """Given a list of interactions, create an app and return a test client."""
    provider = FHIRProvider()

    for interaction in interactions:
        match interaction:
            case "create":
                provider.create(Patient)(patient_create)
            case "read":
                provider.read(Patient)(patient_read)
            case "search-type":
                provider.search_type(Patient)(patient_search_type)
            case "update":
                provider.update(Patient)(patient_update)

    return app(provider)
