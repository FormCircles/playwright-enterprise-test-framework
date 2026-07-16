from __future__ import annotations

import pytest

from core.config.settings import Settings


@pytest.fixture(scope="session")
def settings(pytestconfig):
    """Load settings for the selected execution environment."""

    environment = pytestconfig.getoption("--env")
    return Settings(environment)


@pytest.fixture(scope="session")
def base_url(settings):
    """Return the selected environment base URL."""

    return settings.base_url


@pytest.fixture(scope="session")
def test_username(settings):
    """Return the configured automation username."""

    return settings.username


@pytest.fixture(scope="session")
def test_password(settings):
    """Return the configured password, which may be empty."""

    return settings.password