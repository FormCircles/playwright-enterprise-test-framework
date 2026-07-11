import json

import pytest

from api_tests.services.devices_service import DevicesService
from core.api.api_client import APIClient
from core.config.settings import Settings
from core.fixtures.api_fixtures import *
from core.fixtures.base_fixtures import *
from core.fixtures.data_fixtures import *
from core.fixtures.ui_fixtures import *


@pytest.fixture(scope="session")
def auth_token(api_request_context, base_url):
    """
    Log in once per test session and return the bearer token.
    """
    response = api_request_context.post(
        f"{base_url}/api/login",
        data=json.dumps(
            {
                "username": "admin",
                "password": "password",
            }
        ),
        headers={"Content-Type": "application/json"},
    )

    assert response.status == 200, f"Login failed: {response.text()}"

    return response.json()["access_token"]


@pytest.fixture(scope="session")
def auth_header(auth_token):
    """
    Return the Authorization header for tests that still require it.
    """
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture(scope="session")
def api_client(api_request_context, auth_token):
    """
    Return an authenticated reusable API client.
    """
    return APIClient(
        request_context=api_request_context,
        auth_token=auth_token,
    )


@pytest.fixture(scope="session")
def devices_service(api_client):
    """
    Return the reusable DevicesService.
    """
    return DevicesService(api_client)


@pytest.fixture(scope="session")
def config(request):
    env = request.config.getoption("--env")
    return Settings(env)


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Target test environment: dev, qa, staging",
    )


@pytest.fixture(scope="session")
def settings(pytestconfig):
    env = pytestconfig.getoption("--env")
    return Settings(env)


@pytest.fixture(scope="session")
def base_url(settings):
    return settings.base_url