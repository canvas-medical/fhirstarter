"""FHIRStarter test fixtures"""

from collections.abc import Callable

import pytest
from _pytest.fixtures import FixtureRequest

from ..testclient import TestClient
from .config import create_test_client, create_test_client_async


@pytest.fixture(
    scope="session",
    params=[create_test_client_async, create_test_client],
    ids=["async", "nonasync"],
)
def create_test_client_func(request: FixtureRequest) -> bool:
    """Parametrized fixture to ensure that all tests are tested in both async and nonasync modes."""
    return request.param


@pytest.fixture
def client(
    request: FixtureRequest,
    create_test_client_func: Callable[[tuple[str, ...]], TestClient],
) -> TestClient:
    """Return a test client with specified interactions enabled."""
    return create_test_client_func(request.param)


@pytest.fixture
def client_all(
    create_test_client_func: Callable[[tuple[str, ...]], TestClient]
) -> TestClient:
    """Return a test client with all interactions enabled."""
    return create_test_client_func(("create", "read", "search-type", "update"))


@pytest.fixture
def client_create_and_read(
    create_test_client_func: Callable[[tuple[str, ...]], TestClient]
) -> TestClient:
    """Return a test client with the create and read interactions enabled."""
    return create_test_client_func(("create", "read"))
