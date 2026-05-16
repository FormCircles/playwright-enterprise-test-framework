import pytest
import json

from core.fixtures.base_fixtures import *
from core.fixtures.api_fixtures import *
from core.fixtures.ui_fixtures import *
from core.fixtures.data_fixtures import *

from core.config.settings import Settings

@pytest.fixture(scope="session")
def auth_header(api_request_context, base_url):
    """
    Logs in and returns the Authorization header for future requests.
    """
    response = api_request_context.post(
        f"{base_url}/api/login",
        data=json.dumps({
            "username": "admin",
            "password": "password"
        }),
        headers={"Content-Type": "application/json"}
    )
    assert response.status == 200, f"login failed: {response.text()}"
    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="session")
def config(request):
    env = request.config.getoption("--env")
    return Settings(env)

def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Target test environment: dev, qa, staging"
    )


@pytest.fixture(scope="session")
def settings(pytestconfig):
    env = pytestconfig.getoption("--env")
    return Settings(env)


@pytest.fixture(scope="session")
def base_url(settings):
    return settings.base_url