from __future__ import annotations

import pytest
from playwright.sync_api import APIRequestContext, Playwright

from api_tests.services.devices_service import DevicesService
from api_tests.services.health_service import HealthService
from core.api.api_client import APIClient
import os


@pytest.fixture(scope="session")
def api_request_context(
        playwright: Playwright,
        base_url: str,
) -> APIRequestContext:
    """
    Shared Playwright API request context for the test session.

    Base URL is configured here so service/client calls can use relative paths
    like '/api/login' and '/health'.
    """

    resolved_base_url = os.getenv("BASE_URL", base_url)

    context = playwright.request.new_context(
        base_url=resolved_base_url,
        extra_http_headers={
            "Accept": "application/json",
        },
    )
    yield context
    context.dispose()


@pytest.fixture(scope="session")
def auth_token(api_request_context: APIRequestContext) -> str:
    """
    Authenticate once per session and return a bearer token.

    Adjust username/password if your mock app uses different credentials.
    """
    response = api_request_context.post(
        "/api/login",
        data={
            "username": "admin",
            "password": "password",
        },
    )

    assert response.ok, (
        f"Login failed. Status: {response.status}\n"
        f"Response: {response.text()}"
    )

    payload = response.json()

    assert "access_token" in payload, (
        f"Login response missing access_token. Payload: {payload}"
    )

    return payload["access_token"]


@pytest.fixture(scope="session")
def api_client(
    api_request_context: APIRequestContext,
    auth_token: str,
) -> APIClient:
    """
    Reusable authenticated API client.
    """
    return APIClient(api_request_context, auth_token=auth_token)


@pytest.fixture
def devices_service(api_client: APIClient) -> DevicesService:
    """
    Domain service fixture for device-related API operations.
    """
    return DevicesService(api_client)


@pytest.fixture
def health_service(api_client: APIClient) -> HealthService:
    """
    Domain service fixture for health endpoint validation.
    """
    return HealthService(api_client)