"""Test FHIR utils"""

import pytest

from ..utils import ParsedRequest, parse_fhir_request
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
                ParsedRequest(  # type: ignore[call-arg]
                    request_type="interaction",
                    resource_type=None,
                    resource_id=None,
                    interaction_type="capabilities",
                ),
            ),
            (
                "read",
                "GET",
                f"/Patient/{(id_ := generate_fhir_resource_id())}",
                ParsedRequest(  # type: ignore[call-arg]
                    request_type="interaction",
                    resource_type="Patient",
                    resource_id=id_,
                    interaction_type="read",
                ),
            ),
            (
                "read unrecognized resource type",
                "GET",
                f"/FakeResource/{(id_ := generate_fhir_resource_id())}",
                ParsedRequest(),
            ),
            (
                "update",
                "PUT",
                f"/Patient/{(id_ := generate_fhir_resource_id())}",
                ParsedRequest(  # type: ignore[call-arg]
                    request_type="interaction",
                    resource_type="Patient",
                    resource_id=id_,
                    interaction_type="update",
                ),
            ),
            (
                "update unrecognized resource type",
                "PUT",
                f"/FakeResource/{(id_ := generate_fhir_resource_id())}",
                ParsedRequest(),
            ),
            (
                "patch",
                "PATCH",
                f"/Patient/{(id_ := generate_fhir_resource_id())}",
                ParsedRequest(  # type: ignore[call-arg]
                    request_type="interaction",
                    resource_type="Patient",
                    resource_id=id_,
                    interaction_type="patch",
                ),
            ),
            (
                "patch unrecognized resource type",
                "PATCH",
                f"/FakeResource/{(id_ := generate_fhir_resource_id())}",
                ParsedRequest(),
            ),
            (
                "delete",
                "DELETE",
                f"/Patient/{(id_ := generate_fhir_resource_id())}",
                ParsedRequest(  # type: ignore[call-arg]
                    request_type="interaction",
                    resource_type="Patient",
                    resource_id=id_,
                    interaction_type="delete",
                ),
            ),
            (
                "delete unrecognized resource type",
                "DELETE",
                f"/FakeResource/{(id_ := generate_fhir_resource_id())}",
                ParsedRequest(),
            ),
            (
                "create",
                "POST",
                "/Patient",
                ParsedRequest(  # type: ignore[call-arg]
                    request_type="interaction",
                    resource_type="Patient",
                    resource_id=None,
                    interaction_type="create",
                ),
            ),
            (
                "create unrecognized resource type",
                "POST",
                "/FakeResource",
                ParsedRequest(),
            ),
            (
                "search-type",
                "GET",
                "/Patient",
                ParsedRequest(  # type: ignore[call-arg]
                    request_type="interaction",
                    resource_type="Patient",
                    resource_id=None,
                    interaction_type="search-type",
                ),
            ),
            (
                "search-type post",
                "POST",
                "/Patient/_search",
                ParsedRequest(  # type: ignore[call-arg]
                    request_type="interaction",
                    resource_type="Patient",
                    resource_id=None,
                    interaction_type="search-type",
                ),
            ),
            (
                "search unrecognized resource type",
                "GET",
                f"/FakeResource",
                ParsedRequest(),
            ),
            (
                "search POST unrecognized resource type",
                "POST",
                "/FakeResource/_search",
                ParsedRequest(),
            ),
            (
                "operation GET",
                "GET",
                f"/Patient/{(id_ := generate_fhir_resource_id())}/$export",
                ParsedRequest(  # type: ignore[call-arg]
                    request_type="operation",
                    resource_type="Patient",
                    resource_id=id_,
                    operation_name="export",
                ),
            ),
            (
                "operation POST",
                "POST",
                f"/Patient/{(id_ := generate_fhir_resource_id())}/$export",
                ParsedRequest(  # type: ignore[call-arg]
                    request_type="operation",
                    resource_type="Patient",
                    resource_id=id_,
                    operation_name="export",
                ),
            ),
            (
                "operation-type GET",
                "GET",
                f"/Patient/$export",
                ParsedRequest(  # type: ignore[call-arg]
                    request_type="operation",
                    resource_type="Patient",
                    resource_id=None,
                    operation_name="export",
                ),
            ),
            (
                "operation-type POST",
                "POST",
                f"/Patient/$export",
                ParsedRequest(  # type: ignore[call-arg]
                    request_type="operation",
                    resource_type="Patient",
                    resource_id=None,
                    operation_name="export",
                ),
            ),
            (
                "operation-system GET",
                "GET",
                f"/$export",
                ParsedRequest(  # type: ignore[call-arg]
                    request_type="operation",
                    resource_type=None,
                    resource_id=None,
                    operation_name="export",
                ),
            ),
            (
                "operation-system POST",
                "POST",
                f"/$export",
                ParsedRequest(  # type: ignore[call-arg]
                    request_type="operation",
                    resource_type=None,
                    resource_id=None,
                    operation_name="export",
                ),
            ),
            (
                "operation PUT (invalid request)",
                "PUT",
                f"/Patient/{(id_ := generate_fhir_resource_id())}/$export",
                ParsedRequest(),
            ),
            (
                "unrecognized GET path",
                "GET",
                f"/Patient/{(id_ := generate_fhir_resource_id())}/extra",
                ParsedRequest(),
            ),
            (
                "unrecognized PUT path",
                "PUT",
                f"/FakeResource/{(id_ := generate_fhir_resource_id())}/extra",
                ParsedRequest(),
            ),
            (
                "unrecognized POST path",
                "POST",
                "/FakeResource/extra",
                ParsedRequest(),
            ),
            (
                "unrecognized PATCH path",
                "PATCH",
                f"/FakeResource/{(id_ := generate_fhir_resource_id())}/extra",
                ParsedRequest(),
            ),
            (
                "unrecognized DELETE path",
                "DELETE",
                f"/FakeResource/{(id_ := generate_fhir_resource_id())}/extra",
                ParsedRequest(),
            ),
            (
                "unsupported HTTP method",
                "HEAD",
                f"/Patient/{(id_ := generate_fhir_resource_id())}/extra",
                ParsedRequest(),
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
    expected_result: ParsedRequest,
) -> None:
    assert (
        parse_fhir_request(make_request(request_method, f"{mount_path}{path}"))
        == expected_result
    )
