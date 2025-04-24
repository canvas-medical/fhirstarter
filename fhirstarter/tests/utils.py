"""Test utilities"""

from typing import Any, Dict, Mapping, Union
from urllib.parse import urlparse
from uuid import uuid4

import orjson
from funcy import omit
from requests.models import Response

from .. import Request

_RESOURCE = {
    "resourceType": "Patient",
    "id": "",
    "name": [{"family": "Baggins", "given": ["Bilbo"]}],
}


def resource(id_: Union[str, None] = None) -> Dict[str, Any]:
    """
    Return a test patient resource.

    This will either return a resource with the provided ID inserted, or return a resource with no
    ID.
    """
    if id_:
        return {**_RESOURCE, "id": id_}
    else:
        return omit(_RESOURCE, ["id"])


def generate_fhir_resource_id() -> str:
    """Generate a UUID-based FHIR Resource ID."""
    return str(uuid4())


def id_from_location_header(response: Response) -> str:
    """Extract the resource identifier from a FHIR create interaction response."""
    return response.headers["Location"].split("/")[2]


def json_dumps_pretty(value: Any) -> str:
    """Dump the value to JSON in pretty format."""
    return orjson.dumps(value, option=orjson.OPT_INDENT_2).decode()


def make_request(
    method: str,
    path: str,
) -> Request:
    """Make a request for the purpose of testing."""
    parsed_path = urlparse(path)

    path = parsed_path.path
    query_string = parsed_path.query

    return Request(
        scope={
            "type": "http",
            "http_version": "1.1",
            "method": method,
            "path": path,
            "raw_path": path.encode(),
            "root_path": "",
            "scheme": "http",
            "server": ("testserver", 80),
            "headers": [],
            "path_params": {},
            "query_string": query_string,
        }
    )


def assert_expected_response(
    response: Response,
    status_code: int,
    content_type: str = "application/fhir+json",
    content: Union[Mapping[str, Any], str, None] = None,
) -> None:
    """Assert the status code, content type header, and content of a response."""
    assert response.status_code == status_code
    assert (
        (
            response.headers["Content-Length"] == "0"
            and "Content-Type" not in response.headers
        )
        or int(response.headers["Content-Length"]) > 0
        and response.headers["Content-Type"] == content_type
    )
    if content:
        if isinstance(content, Mapping):
            assert response.json() == content
        elif isinstance(content, str):
            assert response.content.decode() == content
        else:
            assert response.content == content  # type: ignore[unreachable]
