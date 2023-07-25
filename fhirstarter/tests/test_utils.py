"""Test FHIR utils"""

import pytest

from .. import Request
from ..utils import InteractionInfo, parse_fhir_request
from .utils import generate_fhir_resource_id, make_request


@pytest.mark.parametrize(
    argnames="request_,expected_result",
    argvalues=[
        (
            make_request("GET", "/metadata"),
            InteractionInfo(  # type: ignore
                resource_type=None, interaction_type="capabilities", resource_id=None
            ),
        ),
        (
            make_request("POST", "/Patient"),
            InteractionInfo(  # type: ignore
                resource_type="Patient", interaction_type="create", resource_id=None
            ),
        ),
        (
            make_request("GET", f"/Patient/{(id_ := generate_fhir_resource_id())}"),
            InteractionInfo(  # type: ignore
                resource_type="Patient", interaction_type="read", resource_id=id_
            ),
        ),
        (
            make_request("GET", "/Patient"),
            InteractionInfo(  # type: ignore
                resource_type="Patient",
                interaction_type="search-type",
                resource_id=None,
            ),
        ),
        (
            make_request("POST", "/Patient/_search"),
            InteractionInfo(  # type: ignore
                resource_type="Patient",
                interaction_type="search-type",
                resource_id=None,
            ),
        ),
        (
            make_request("PUT", f"/Patient/{(id_ := generate_fhir_resource_id())}"),
            InteractionInfo(  # type: ignore
                resource_type="Patient", interaction_type="update", resource_id=id_
            ),
        ),
        (
            make_request(
                "GET", f"/FakeResource/{(id_ := generate_fhir_resource_id())}"
            ),
            InteractionInfo(  # type: ignore
                resource_type=None, interaction_type=None, resource_id=None
            ),
        ),
        (
            make_request("GET", f"/FakeResource"),
            InteractionInfo(  # type: ignore
                resource_type=None, interaction_type=None, resource_id=None
            ),
        ),
        (
            make_request(
                "GET", f"/Patient/{(id_ := generate_fhir_resource_id())}/extra"
            ),
            InteractionInfo(  # type: ignore
                resource_type=None, interaction_type=None, resource_id=None
            ),
        ),
        (
            make_request("POST", "/FakeResource"),
            InteractionInfo(  # type: ignore
                resource_type=None, interaction_type=None, resource_id=None
            ),
        ),
        (
            make_request("POST", "/FakeResource/_search"),
            InteractionInfo(  # type: ignore
                resource_type=None, interaction_type=None, resource_id=None
            ),
        ),
        (
            make_request("POST", "/FakeResource/extra"),
            InteractionInfo(  # type: ignore
                resource_type=None, interaction_type=None, resource_id=None
            ),
        ),
        (
            make_request(
                "PUT", f"/FakeResource/{(id_ := generate_fhir_resource_id())}"
            ),
            InteractionInfo(  # type: ignore
                resource_type=None, interaction_type=None, resource_id=None
            ),
        ),
        (
            make_request(
                "PUT", f"/FakeResource/{(id_ := generate_fhir_resource_id())}/extra"
            ),
            InteractionInfo(  # type: ignore
                resource_type=None, interaction_type=None, resource_id=None
            ),
        ),
        (
            make_request(
                "HEAD", f"/Patient/{(id_ := generate_fhir_resource_id())}/extra"
            ),
            InteractionInfo(  # type: ignore
                resource_type=None, interaction_type=None, resource_id=None
            ),
        ),
    ],
    ids=[
        "capabilities",
        "create",
        "read",
        "search-type",
        "search-type post",
        "update",
        "read unrecognized resource type",
        "search unrecognized resource type",
        "unrecognized GET path",
        "create unrecognized resource type",
        "search POST unrecognized resource type",
        "unrecognized POST path",
        "update unrecognized resource type",
        "unrecognized PUT path",
        "unsupported HTTP method",
    ],
)
def test_parse_fhir_request(
    request_: Request, expected_result: InteractionInfo
) -> None:
    assert parse_fhir_request(request_) == expected_result
