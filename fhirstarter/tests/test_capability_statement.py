"""Test the capability statement"""

from collections.abc import Mapping, MutableMapping, Sequence
from typing import Any, cast

import pytest
from fhir.resources.capabilitystatement import CapabilityStatement

from .. import status
from ..fhirstarter import FHIRStarter
from ..testclient import TestClient
from .config import client, client_create_and_read
from .utils import assert_expected_response


@pytest.mark.parametrize(
    argnames="test_client,resource",
    argvalues=[
        (
            client(),
            [
                {
                    "type": "Patient",
                    "interaction": [
                        {"code": "create"},
                        {"code": "read"},
                        {"code": "search-type"},
                        {"code": "update"},
                    ],
                    "searchParam": [
                        {
                            "name": "family",
                            "definition": "http://hl7.org/fhir/SearchParameter/individual-family",
                            "type": "string",
                            "documentation": "A portion of the family name of the patient",
                        },
                        {
                            "name": "general-practitioner",
                            "definition": "http://hl7.org/fhir/SearchParameter/"
                            "Patient-general-practitioner",
                            "type": "reference",
                            "documentation": "Patient's nominated general practitioner, not the "
                            "organization that manages the record",
                        },
                        {
                            "name": "nickname",
                            "definition": "https://hostname/nickname",
                            "type": "string",
                            "documentation": "Nickname",
                        },
                        {
                            "name": "_lastUpdated",
                            "definition": "http://hl7.org/fhir/SearchParameter/"
                            "Resource-lastUpdated",
                            "type": "date",
                            "documentation": "When the resource version last changed",
                        },
                    ],
                }
            ],
        ),
        (
            client_create_and_read(),
            [
                {
                    "type": "Patient",
                    "interaction": [{"code": "create"}, {"code": "read"}],
                },
            ],
        ),
    ],
    ids=["all", "create_and_read"],
)
def test_capability_statement(
    test_client: TestClient, resource: Sequence[Mapping[str, Any]]
) -> None:
    """
    Test the capability statement.

    Two scenarios are parameterized: a server with create, read, search, and update supported, and
    a server with only create and read supported.
    """
    app = cast(FHIRStarter, test_client.app)

    response = test_client.get("/metadata")

    assert_expected_response(
        response,
        status.HTTP_200_OK,
        content={
            "resourceType": "CapabilityStatement",
            "status": "active",
            "date": app._created.isoformat(),
            "kind": "instance",
            "fhirVersion": "4.0.1",
            "format": ["json"],
            "rest": [
                {
                    "mode": "server",
                    "resource": resource,
                }
            ],
        },
    )


def test_capability_statement_pretty(
    client_create_and_read_fixture: TestClient,
) -> None:
    """Test the capability statement with a pretty response."""
    test_client = client_create_and_read_fixture

    response = test_client.get("/metadata?_pretty=true")

    assert_expected_response(
        response,
        status.HTTP_200_OK,
        content=CapabilityStatement(**response.json()).json(
            indent=2, separators=(", ", ": ")
        ),
    )


@pytest.mark.parametrize(
    argnames="pretty",
    argvalues=["false", "true"],
    ids=["minified", "pretty"],
)
def test_capability_statement_xml(
    client_create_and_read_fixture: TestClient, pretty: str
) -> None:
    """Test the capability statement with an XML response."""
    test_client = client_create_and_read_fixture

    response = test_client.get(f"/metadata?_format=xml&_pretty={pretty}")

    assert_expected_response(
        response,
        status.HTTP_200_OK,
        content_type="application/fhir+xml",
        content=CapabilityStatement.parse_raw(
            response.content, content_type="text/xml"
        ).xml(pretty_print=(pretty == "true")),
    )


def test_set_capability_statement_modifier(
    client_create_and_read_fixture: TestClient,
) -> None:
    """Test the set_capability_statement_modifier method."""
    test_client = client_create_and_read_fixture
    app = cast(FHIRStarter, test_client.app)

    def modify_capability_statement(
        capability_statement: MutableMapping[str, Any], *_: Any
    ) -> MutableMapping[str, Any]:
        capability_statement["publisher"] = "Publisher"
        return capability_statement

    app.set_capability_statement_modifier(modify_capability_statement)

    response = test_client.get("/metadata")

    assert_expected_response(
        response,
        status.HTTP_200_OK,
        content={
            "resourceType": "CapabilityStatement",
            "status": "active",
            "date": app._created.isoformat(),
            "publisher": "Publisher",
            "kind": "instance",
            "fhirVersion": "4.0.1",
            "format": ["json"],
            "rest": [
                {
                    "mode": "server",
                    "resource": [
                        {
                            "type": "Patient",
                            "interaction": [{"code": "create"}, {"code": "read"}],
                        }
                    ],
                }
            ],
        },
    )
