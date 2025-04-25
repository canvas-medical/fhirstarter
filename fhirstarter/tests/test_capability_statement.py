"""Test the capability statement"""

from typing import Any, Mapping, MutableMapping, Sequence, cast

import pytest

from .. import status
from ..fhir_specification import FHIR_SEQUENCE, FHIR_VERSION
from ..fhirstarter import FHIRStarter
from ..resources import CapabilityStatement
from ..testclient import TestClient
from .utils import assert_expected_response, json_dumps_pretty


@pytest.mark.parametrize(
    argnames="client,resource",
    argvalues=[
        (
            ["read", "update", "patch", "delete", "create", "search-type"],
            [
                {
                    "type": "Patient",
                    "interaction": [
                        {"code": "read"},
                        {"code": "update"},
                        {"code": "patch"},
                        {"code": "delete"},
                        {"code": "create"},
                        {"code": "search-type"},
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
            ["read", "create"],
            [
                {
                    "type": "Patient",
                    "interaction": [{"code": "read"}, {"code": "create"}],
                },
            ],
        ),
    ],
    ids=["all", "read and create"],
    indirect=["client"],
)
def test_capability_statement(
    client: TestClient, resource: Sequence[Mapping[str, Any]]
) -> None:
    """
    Test the capability statement.

    Two scenarios are parameterized: a server with all interaction types supported, and a server
    with only create and read supported.
    """
    app = cast(FHIRStarter, client.app)

    response = client.get("/metadata")

    assert_expected_response(
        response,
        status.HTTP_200_OK,
        content=_fhir_sequence_adjust(
            {
                "resourceType": "CapabilityStatement",
                "status": "active",
                "date": app._created,
                "kind": "instance",
                "fhirVersion": FHIR_VERSION,
                "acceptUnknown": "no",
                "format": ["json"],
                "rest": [
                    {
                        "mode": "server",
                        "resource": resource,
                    }
                ],
            }
        ),
    )


def test_capability_statement_pretty(client_create_and_read: TestClient) -> None:
    """Test the capability statement with a pretty response."""
    response = client_create_and_read.get("/metadata?_pretty=true")

    assert_expected_response(
        response,
        status.HTTP_200_OK,
        content=json_dumps_pretty(CapabilityStatement(**response.json()).model_dump()),
    )


@pytest.mark.parametrize(
    argnames="pretty",
    argvalues=["false", "true"],
    ids=["minified", "pretty"],
)
def test_capability_statement_xml(
    client_create_and_read: TestClient, pretty: str
) -> None:
    """Test the capability statement with an XML response."""
    response = client_create_and_read.get(f"/metadata?_format=xml&_pretty={pretty}")

    assert_expected_response(
        response,
        status.HTTP_200_OK,
        content_type="application/fhir+xml",
        content=CapabilityStatement.model_validate_xml(response.content).model_dump_xml(
            pretty_print=(pretty == "true")
        ),
    )


def test_set_capability_statement_modifier(client_create_and_read: TestClient) -> None:
    """Test the set_capability_statement_modifier method."""
    app = cast(FHIRStarter, client_create_and_read.app)

    def modify_capability_statement(
        capability_statement: MutableMapping[str, Any], *_: Any
    ) -> MutableMapping[str, Any]:
        capability_statement["publisher"] = "Publisher"
        return capability_statement

    app.set_capability_statement_modifier(modify_capability_statement)

    response = client_create_and_read.get("/metadata")

    assert_expected_response(
        response,
        status.HTTP_200_OK,
        content=_fhir_sequence_adjust(
            {
                "resourceType": "CapabilityStatement",
                "status": "active",
                "date": app._created,
                "publisher": "Publisher",
                "kind": "instance",
                "fhirVersion": FHIR_VERSION,
                "acceptUnknown": "no",
                "format": ["json"],
                "rest": [
                    {
                        "mode": "server",
                        "resource": [
                            {
                                "type": "Patient",
                                "interaction": [{"code": "read"}, {"code": "create"}],
                            }
                        ],
                    }
                ],
            }
        ),
    )


def _fhir_sequence_adjust(
    capability_statement: MutableMapping[str, Any]
) -> MutableMapping[str, Any]:
    """
    Adjust a capability statement for the purposes of comparison.
    Example: For R4B and R5, the "acceptUnknown" value is no longer present.
    """
    if FHIR_SEQUENCE != "STU3":
        del capability_statement["acceptUnknown"]

    return capability_statement
