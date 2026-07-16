from __future__ import annotations

import pytest
from playwright.sync_api import APIRequestContext, Playwright

from api_tests.services.devices_service import DevicesService
from api_tests.services.health_service import HealthService
from api_tests.services.test_admin_service import TestAdminService
from core.api.api_client import APIClient


@pytest.fixture(scope="session")
def api_request_context(
    playwright: Playwright,
    base_url: str,
    settings,
) -> APIRequestContext:
    """Create a reusable Playwright API request context."""

    return playwright.request.new_context(
        base_url=base_url,
        timeout=settings.request_timeout_ms,
    )


@pytest.fixture(scope="session")
def auth_token(
    api_request_context: APIRequestContext,
    test_username: str,
    test_password: str,
) -> str:
    """Authenticate once and return a bearer token."""

    if not test_password:
        raise RuntimeError(
            "TEST_PASSWORD is required for authenticated tests."
        )

    response = api_request_context.post(
        "/api/login",
        data={
            "username": test_username,
            "password": test_password,
        },
    )

    assert response.status == 200, (
        f"Login failed. Status: {response.status}. "
        f"Response: {response.text()}"
    )

    return response.json()["access_token"]


@pytest.fixture(scope="session")
def auth_header(auth_token: str) -> dict[str, str]:
    """Return a reusable authorization header."""

    return {
        "Authorization": f"Bearer {auth_token}",
    }


@pytest.fixture(scope="session")
def api_client(
    api_request_context: APIRequestContext,
    auth_token: str,
) -> APIClient:
    """Return an authenticated API client."""

    return APIClient(
        request_context=api_request_context,
        auth_token=auth_token,
    )


@pytest.fixture
def devices_service(api_client: APIClient) -> DevicesService:
    """Return the device API service."""

    return DevicesService(api_client)


@pytest.fixture(scope="session")
def public_api_client(
    api_request_context: APIRequestContext,
) -> APIClient:
    """Return an unauthenticated API client."""

    return APIClient(
        request_context=api_request_context,
        auth_token=None,
    )


@pytest.fixture
def health_service(
    public_api_client: APIClient,
) -> HealthService:
    """Return the public health API service."""

    return HealthService(public_api_client)


@pytest.fixture(scope="session")
def test_admin_service(api_client: APIClient) -> TestAdminService:
    """Return the backend test-administration service."""

    return TestAdminService(api_client)


