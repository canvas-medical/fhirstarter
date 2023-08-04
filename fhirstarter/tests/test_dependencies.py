"""Test FHIRStarter dependency injection"""

import pytest
from _pytest.fixtures import FixtureRequest
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fhir.resources.patient import Patient

from ..exceptions import FHIRUnauthorizedError
from ..fhirstarter import FHIRProvider, status
from .config import app, patient_create, patient_create_async
from .utils import assert_expected_response, resource

_VALID_TOKEN = "valid"
_INVALID_TOKEN = "invalid"


def validate_token(
    authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> None:
    """
    Ensure that the authorization credentials are bearer credentials with a valid access token.
    """
    if authorization.scheme != "Bearer" or authorization.credentials != _VALID_TOKEN:
        raise FHIRUnauthorizedError(details_text="Authentication failed")


@pytest.fixture
def provider_with_dependency(async_endpoints: bool) -> FHIRProvider:
    """Create a provider with a provider-level dependency."""
    provider = FHIRProvider(dependencies=[Depends(validate_token)])
    provider.create(Patient)(
        patient_create_async if async_endpoints else patient_create
    )

    return provider


@pytest.fixture
def provider_with_interaction_dependency(async_endpoints: bool) -> FHIRProvider:
    """Create a provider with an interaction-level dependency."""
    provider = FHIRProvider()
    provider.create(Patient, dependencies=[Depends(validate_token)])(
        patient_create_async if async_endpoints else patient_create
    )

    return provider


@pytest.fixture(params=[True, False], ids=["provider", "interaction"])
def provider(
    request: FixtureRequest,
    provider_with_dependency: FHIRProvider,
    provider_with_interaction_dependency: FHIRProvider,
) -> FHIRProvider:
    """Parametrized fixture that returns a provider with a dependency added at different layers."""
    return (
        provider_with_dependency
        if request.param
        else provider_with_interaction_dependency
    )


def test_dependency(provider: FHIRProvider) -> None:
    """Test that injected token validation dependency works on the given provider."""
    client = app(provider)

    create_response = client.post(
        "/Patient",
        json=resource(),
        headers={"Authorization": f"Bearer {_INVALID_TOKEN}"},
    )
    assert_expected_response(
        create_response,
        status.HTTP_401_UNAUTHORIZED,
        content={
            "resourceType": "OperationOutcome",
            "issue": [
                {
                    "severity": "error",
                    "code": "unknown",
                    "details": {"text": "Authentication failed"},
                }
            ],
        },
    )

    create_response = client.post(
        "/Patient",
        json=resource(),
        headers={"Authorization": f"Bearer {_VALID_TOKEN}"},
    )
    assert_expected_response(create_response, status.HTTP_201_CREATED)
