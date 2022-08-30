"""Test the capability statement"""

from collections.abc import Mapping, Sequence
from typing import Any, cast

import pytest
from fhir.resources.capabilitystatement import CapabilityStatement
from funcy import omit

from .. import status
from ..fhirstarter import FHIRStarter
from ..testclient import TestClient
from .fixtures import client, client_create_and_read, client_create_and_read_fixture
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
                            "definition": "http://hl7.org/fhir/SearchParameter/Patient-general-practitioner",
                            "type": "reference",
                            "documentation": "Patient's nominated general practitioner, not the organization that manages the record",
                        },
                        {
                            "name": "nickname",
                            "definition": "https://hostname/nickname",
                            "type": "string",
                            "documentation": "Nickname",
                        },
                        {
                            "name": "_lastUpdated",
                            "definition": "http://hl7.org/fhir/SearchParameter/Resource-lastUpdated",
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
    client = test_client
    app = cast(FHIRStarter, client.app)

    response = client.get("/metadata")

    assert_expected_response(response, status.HTTP_200_OK)
    assert omit(response.json(), ["id"]) == {
        "resourceType": "CapabilityStatement",
        "status": "active",
        "date": app._created.isoformat(),
        "kind": "instance",
        "publisher": "Publisher",
        "fhirVersion": "4.0.1",
        "format": ["json"],
        "rest": [
            {
                "mode": "server",
                "resource": resource,
            }
        ],
    }


def test_capability_statement_publisher(
    client_create_and_read_fixture: TestClient,
) -> None:
    """Test the capability statement publisher value that is provided by a config file."""
    client = client_create_and_read_fixture

    response = client.get("/metadata")

    assert_expected_response(response, status.HTTP_200_OK)
    assert response.json()["publisher"] == "Publisher"


def test_capability_statement_no_publisher() -> None:
    """Test the capability statement with no publisher."""
    client = TestClient(FHIRStarter())

    response = client.get("/metadata")

    assert_expected_response(response, status.HTTP_200_OK)
    assert "publisher" not in response.json()


def test_capability_statement_pretty(
    client_create_and_read_fixture: TestClient,
) -> None:
    """Test the capability statement with a pretty response."""
    client = client_create_and_read_fixture

    response = client.get("/metadata?_pretty=true")

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
    client = client_create_and_read_fixture

    response = client.get(f"/metadata?_format=xml&_pretty={pretty}")

    assert_expected_response(
        response,
        status.HTTP_200_OK,
        content_type="application/fhir+xml",
        content=CapabilityStatement.parse_raw(
            response.content, content_type="text/xml"
        ).xml(pretty_print=(pretty == "true")),
    )
