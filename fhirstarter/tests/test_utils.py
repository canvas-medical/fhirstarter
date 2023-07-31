"""Test FHIR utils"""

import pytest

from ..utils import InteractionInfo, parse_fhir_request
from .utils import generate_fhir_resource_id, make_request


@pytest.mark.parametrize(
    argnames="mount_path",
    argvalues=["", "/subapi"],
    ids=["without mount", "with mount"],
)
@pytest.mark.parametrize(
    argnames="request_method,path,expected_result",
    argvalues=[
        (
            "GET",
            "/metadata",
            InteractionInfo(  # type: ignore
                resource_type=None, interaction_type="capabilities", resource_id=None
            ),
        ),
        (
            "POST",
            "/Patient",
            InteractionInfo(  # type: ignore
                resource_type="Patient", interaction_type="create", resource_id=None
            ),
        ),
        (
            "GET",
            f"/Patient/{(id_ := generate_fhir_resource_id())}",
            InteractionInfo(  # type: ignore
                resource_type="Patient", interaction_type="read", resource_id=id_
            ),
        ),
        (
            "GET",
            "/Patient",
            InteractionInfo(  # type: ignore
                resource_type="Patient",
                interaction_type="search-type",
                resource_id=None,
            ),
        ),
        (
            "POST",
            "/Patient/_search",
            InteractionInfo(  # type: ignore
                resource_type="Patient",
                interaction_type="search-type",
                resource_id=None,
            ),
        ),
        (
            "PUT",
            f"/Patient/{(id_ := generate_fhir_resource_id())}",
            InteractionInfo(  # type: ignore
                resource_type="Patient", interaction_type="update", resource_id=id_
            ),
        ),
        (
            "GET",
            f"/FakeResource/{(id_ := generate_fhir_resource_id())}",
            InteractionInfo(  # type: ignore
                resource_type=None, interaction_type=None, resource_id=None
            ),
        ),
        (
            "GET",
            f"/FakeResource",
            InteractionInfo(  # type: ignore
                resource_type=None, interaction_type=None, resource_id=None
            ),
        ),
        (
            "GET",
            f"/Patient/{(id_ := generate_fhir_resource_id())}/extra",
            InteractionInfo(  # type: ignore
                resource_type=None, interaction_type=None, resource_id=None
            ),
        ),
        (
            "POST",
            "/FakeResource",
            InteractionInfo(  # type: ignore
                resource_type=None, interaction_type=None, resource_id=None
            ),
        ),
        (
            "POST",
            "/FakeResource/_search",
            InteractionInfo(  # type: ignore
                resource_type=None, interaction_type=None, resource_id=None
            ),
        ),
        (
            "POST",
            "/FakeResource/extra",
            InteractionInfo(  # type: ignore
                resource_type=None, interaction_type=None, resource_id=None
            ),
        ),
        (
            "PUT",
            f"/FakeResource/{(id_ := generate_fhir_resource_id())}",
            InteractionInfo(  # type: ignore
                resource_type=None, interaction_type=None, resource_id=None
            ),
        ),
        (
            "PUT",
            f"/FakeResource/{(id_ := generate_fhir_resource_id())}/extra",
            InteractionInfo(  # type: ignore
                resource_type=None, interaction_type=None, resource_id=None
            ),
        ),
        (
            "HEAD",
            f"/Patient/{(id_ := generate_fhir_resource_id())}/extra",
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
    mount_path: str, request_method: str, path: str, expected_result: InteractionInfo
) -> None:
    assert (
        parse_fhir_request(make_request(request_method, f"{mount_path}{path}"))
        == expected_result
    )
