"""FHIRStarter test fixtures"""

import pytest
from _pytest.fixtures import FixtureRequest

from ..testclient import TestClient
from .config import create_test_client


@pytest.fixture(scope="session", params=[True, False], ids=["async", "nonasync"])
def async_endpoints(request: FixtureRequest) -> bool:
    """Parametrized fixture to ensure that all tests are tested in both async and nonasync modes."""
    return request.param


@pytest.fixture
def client(request: FixtureRequest, async_endpoints: bool) -> TestClient:
    """Return a test client with specified interactions enabled."""
    return create_test_client(
        interactions=request.param, async_endpoints=async_endpoints
    )


@pytest.fixture
def client_all(async_endpoints: bool) -> TestClient:
    """Return a test client with all interactions enabled."""
    return create_test_client(
        interactions=("create", "read", "search-type", "update"),
        async_endpoints=async_endpoints,
    )


@pytest.fixture
def client_create_and_read(async_endpoints: bool) -> TestClient:
    """Return a test client with the create and read interactions enabled."""
    return create_test_client(
        interactions=("create", "read"), async_endpoints=async_endpoints
    )
