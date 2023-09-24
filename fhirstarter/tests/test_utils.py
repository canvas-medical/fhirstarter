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
    argnames="_,request_method,path,expected_result",
    argvalues=(
        argvalues := [
            (
                "capabilitites",
                "GET",
                "/metadata",
                InteractionInfo(  # type: ignore[call-arg]
                    resource_type=None,
                    interaction_type="capabilities",
                    resource_id=None,
                ),
            ),
            (
                "create",
                "POST",
                "/Patient",
                InteractionInfo(  # type: ignore[call-arg]
                    resource_type="Patient", interaction_type="create", resource_id=None
                ),
            ),
            (
                "read",
                "GET",
                f"/Patient/{(id_ := generate_fhir_resource_id())}",
                InteractionInfo(  # type: ignore[call-arg]
                    resource_type="Patient", interaction_type="read", resource_id=id_
                ),
            ),
            (
                "search-type",
                "GET",
                "/Patient",
                InteractionInfo(  # type: ignore[call-arg]
                    resource_type="Patient",
                    interaction_type="search-type",
                    resource_id=None,
                ),
            ),
            (
                "search-type post",
                "POST",
                "/Patient/_search",
                InteractionInfo(  # type: ignore[call-arg]
                    resource_type="Patient",
                    interaction_type="search-type",
                    resource_id=None,
                ),
            ),
            (
                "update",
                "PUT",
                f"/Patient/{(id_ := generate_fhir_resource_id())}",
                InteractionInfo(  # type: ignore[call-arg]
                    resource_type="Patient", interaction_type="update", resource_id=id_
                ),
            ),
            (
                "read unrecognized resource type",
                "GET",
                f"/FakeResource/{(id_ := generate_fhir_resource_id())}",
                InteractionInfo(  # type: ignore[call-arg]
                    resource_type=None, interaction_type=None, resource_id=None
                ),
            ),
            (
                "search unrecognized resource type",
                "GET",
                f"/FakeResource",
                InteractionInfo(  # type: ignore[call-arg]
                    resource_type=None, interaction_type=None, resource_id=None
                ),
            ),
            (
                "unrecognized GET path",
                "GET",
                f"/Patient/{(id_ := generate_fhir_resource_id())}/extra",
                InteractionInfo(  # type: ignore[call-arg]
                    resource_type=None, interaction_type=None, resource_id=None
                ),
            ),
            (
                "create unrecognized resource type",
                "POST",
                "/FakeResource",
                InteractionInfo(  # type: ignore[call-arg]
                    resource_type=None, interaction_type=None, resource_id=None
                ),
            ),
            (
                "search POST unrecognized resource type",
                "POST",
                "/FakeResource/_search",
                InteractionInfo(  # type: ignore[call-arg]
                    resource_type=None, interaction_type=None, resource_id=None
                ),
            ),
            (
                "unrecognized POST path",
                "POST",
                "/FakeResource/extra",
                InteractionInfo(  # type: ignore[call-arg]
                    resource_type=None, interaction_type=None, resource_id=None
                ),
            ),
            (
                "update unrecognized resource type",
                "PUT",
                f"/FakeResource/{(id_ := generate_fhir_resource_id())}",
                InteractionInfo(  # type: ignore[call-arg]
                    resource_type=None, interaction_type=None, resource_id=None
                ),
            ),
            (
                "unrecognized PUT path",
                "PUT",
                f"/FakeResource/{(id_ := generate_fhir_resource_id())}/extra",
                InteractionInfo(  # type: ignore[call-arg]
                    resource_type=None, interaction_type=None, resource_id=None
                ),
            ),
            (
                "unsupported HTTP method",
                "HEAD",
                f"/Patient/{(id_ := generate_fhir_resource_id())}/extra",
                InteractionInfo(  # type: ignore[call-arg]
                    resource_type=None, interaction_type=None, resource_id=None
                ),
            ),
        ]
    ),
    ids=[id_ for id_, *_ in argvalues],
)
def test_parse_fhir_request(
    _: str,
    mount_path: str,
    request_method: str,
    path: str,
    expected_result: InteractionInfo,
) -> None:
    assert (
        parse_fhir_request(make_request(request_method, f"{mount_path}{path}"))
        == expected_result
    )
