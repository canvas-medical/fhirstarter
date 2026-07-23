"""Test FHIR utils"""

from typing import Any

import orjson
import pytest

from ..utils import (
    ParsedRequest,
    format_response,
    parse_fhir_request,
    prune_empty_elements,
)
from .resources import Patient
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
                "/FakeResource",
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
                "/Patient/$export",
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
                "/Patient/$export",
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
                "/$export",
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
                "/$export",
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


# A deeply nested (four-plus levels) structure that exercises the recursive pruner:
# empty containers are buried several levels down, empties-of-empties collapse upward,
# and real data plus falsy scalars survive at every level.
_DEEP_INPUT = {
    "resourceType": "Bundle",
    "total": 0,  # falsy scalar — kept
    "entry": [  # level 1
        {
            "resource": {  # level 2
                "resourceType": "Patient",
                "active": False,  # falsy scalar — kept
                "photo": [{}, {}],  # collapses entirely -> removed
                "contact": [  # level 3
                    {  # level 4
                        "name": {"family": "Doe", "given": []},  # given [] pruned
                        "telecom": [{}],  # [{}] -> [] -> removed
                        "relationship": [],  # pruned
                    },
                    {"telecom": [{"system": ""}]},  # "" kept -> item survives
                ],
                # A whole branch of nothing: coding [] -> language {} -> item {} ->
                # communication [] -> removed entirely.
                "communication": [{"language": {"coding": []}}],
            }
        },
        # note[0].extension [] -> note[0] {} -> note [] -> removed
        {"resource": {"resourceType": "Observation", "note": [{"extension": []}]}},
    ],
}

_DEEP_EXPECTED = {
    "resourceType": "Bundle",
    "total": 0,
    "entry": [
        {
            "resource": {
                "resourceType": "Patient",
                "active": False,
                "contact": [
                    {"name": {"family": "Doe"}},
                    {"telecom": [{"system": ""}]},
                ],
            }
        },
        {"resource": {"resourceType": "Observation"}},
    ],
}


@pytest.mark.parametrize(
    argnames="value,expected",
    argvalues=[
        pytest.param(
            {"resourceType": "Patient", "communication": []},
            {"resourceType": "Patient"},
            id="empty list removed",
        ),
        pytest.param(
            {"resourceType": "Patient", "text": {}},
            {"resourceType": "Patient"},
            id="empty dict removed",
        ),
        pytest.param(
            {"total": 0, "active": False, "note": ""},
            {"total": 0, "active": False, "note": ""},
            id="falsy scalars preserved",
        ),
        pytest.param(
            {"name": [{"given": [], "family": "Doe"}], "x": [{}]},
            {"name": [{"family": "Doe"}]},
            id="empties-of-empties collapse",
        ),
        pytest.param(
            [{}, {"a": 1}],
            [{"a": 1}],
            id="empty list items pruned",
        ),
        pytest.param(
            {
                "resourceType": "Patient",
                "name": [{"family": "Baggins", "given": ["Bilbo"]}],
            },
            {
                "resourceType": "Patient",
                "name": [{"family": "Baggins", "given": ["Bilbo"]}],
            },
            id="non-empty untouched",
        ),
        pytest.param(_DEEP_INPUT, _DEEP_EXPECTED, id="deeply nested hierarchical"),
    ],
)
def testprune_empty_elements(value: Any, expected: Any) -> None:
    assert prune_empty_elements(value) == expected


def test_format_response_prunes_empty_elements() -> None:
    """
    format_response must strip empty containers that Pydantic v2's model_dump leaves in,
    so the JSON body conforms to FHIR (empty arrays/objects must be omitted).

    This is the real chokepoint every JSON response flows through. Before the pruner was
    added, model_dump() emitted "communication": [] and it was serialized as-is.
    """
    patient = Patient(**{"name": [{"family": "Baggins"}], "communication": []})

    response = format_response(patient, status_code=200)
    body = orjson.loads(response.body)

    assert "communication" not in body
    assert body == {"resourceType": "Patient", "name": [{"family": "Baggins"}]}
