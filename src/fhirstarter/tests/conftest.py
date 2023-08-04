"""FHIRStarter test fixtures"""

import pytest
from requests.models import Response

from ..testclient import TestClient
from .config import client, client_create_and_read
from .utils import resource


@pytest.fixture
def client_fixture() -> TestClient:
    """Test fixture that creates an app that provides all FHIR interactions."""
    return client()


@pytest.fixture
def client_create_and_read_fixture() -> TestClient:
    """Test fixture that creates an app that only provides FHIR create and read interactions."""
    return client_create_and_read()


@pytest.fixture
def create_response_fixture(client_fixture: TestClient) -> Response:
    """Test fixture that provides a response from a FHIR create interaction."""
    test_client = client_fixture
    return test_client.post("/Patient", json=resource())
