from __future__ import annotations

import pytest

from core.config.settings import Settings
from core.config.pytest_options import explicit_base_url


@pytest.fixture(scope="session")
def settings(pytestconfig):
    """Load settings using deterministic configuration precedence."""

    environment = pytestconfig.getoption("--env")
    base_url_override = explicit_base_url(pytestconfig)

    overrides = (
        {"base_url": base_url_override}
        if base_url_override is not None
        else None
    )

    return Settings(
        environment,
        cli_overrides=overrides,
    )


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