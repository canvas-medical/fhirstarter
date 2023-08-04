"""Test FHIRStarter dependency injection"""

import pytest
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fhir.resources.patient import Patient

from ..exceptions import FHIRUnauthorizedError
from ..fhirstarter import FHIRProvider, status
from .config import app, patient_create
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


def provider_with_dependency() -> FHIRProvider:
    """Create a provider with a provider-level dependency."""
    provider = FHIRProvider(dependencies=[Depends(validate_token)])
    provider.create(Patient)(patient_create)

    return provider


def provider_with_interaction_dependency() -> FHIRProvider:
    """Create a provider with an interaction-level dependency."""
    provider = FHIRProvider()
    provider.create(Patient, dependencies=[Depends(validate_token)])(patient_create)

    return provider


@pytest.mark.parametrize(
    argnames="provider",
    argvalues=[provider_with_dependency(), provider_with_interaction_dependency()],
    ids=["provider", "interaction"],
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
