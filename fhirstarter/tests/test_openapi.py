"""Test OpenAPI modifications"""

from typing import cast

from .. import FHIRProvider, FHIRStarter, InteractionContext
from .config import create_test_client_async
from .openapi_schema import EXPECTED_SCHEMA
from .resources import Appointment, Bundle, Id, Practitioner


class PractitionerCustom(Practitioner):
    class Config:
        schema_extra = {
            "example": {
                "resourceType": "Practitioner",
                "id": "example",
                "name": [{"family": "Careful", "given": ["Adam"], "prefix": ["Dr"]}],
            }
        }


async def practitioner_read(context: InteractionContext, id_: Id) -> PractitionerCustom:
    raise NotImplementedError


async def practitioner_search_type(context: InteractionContext) -> Bundle:
    raise NotImplementedError


async def appointment_search_type(context: InteractionContext) -> Bundle:
    raise NotImplementedError


def test_openapi_modifications() -> None:
    """
    Test that the schema modifications that FHIRStarter performs have the expected result.

    This test just compares the entire schema against an expected result. If it passes, then it
    indicates that all the modifications that FHIRStarter makes are working as expected:
    * Inlining of search by post schemas
    * Adding resource schemas that aren't added automatically (resources that only support search
      will have Bundle loaded automatically, but not the resource that will appear inside the
      bundle)
    * Ensure that examples are properly loaded for all interactions
    * Adjust content types (from application/json to application/fhir+json)
    * Remove default FastAPI responses
    """
    client = create_test_client_async(("create", "read", "search-type", "update"))
    app = cast(FHIRStarter, client.app)

    provider = FHIRProvider()

    # Add read and search-type for a resource that uses both the standard model and a model with a
    # custom example
    provider.read(Practitioner)(practitioner_read)
    provider.search_type(PractitionerCustom)(practitioner_search_type)

    # Add a resource that only supports search-type
    provider.search_type(Appointment)(appointment_search_type)

    app.add_providers(provider)

    assert app.openapi() == EXPECTED_SCHEMA
