from __future__ import annotations

import pytest

from core.config.settings import Settings


def _explicit_base_url(pytestconfig) -> str | None:
    """Return a BASE_URL explicitly supplied through pytest options."""
    import os
    import shlex

    invocation_args = list(pytestconfig.invocation_params.args)
    addopts_args = shlex.split(os.environ.get("PYTEST_ADDOPTS", ""))

    def count_options(arguments: list[str]) -> int:
        count = 0

        for index, argument in enumerate(arguments):
            if argument == "--base-url":
                if index + 1 >= len(arguments):
                    raise ValueError("--base-url requires a value.")
                count += 1
            elif argument.startswith("--base-url="):
                count += 1

        return count

    occurrences = (
        count_options(invocation_args)
        + count_options(addopts_args)
    )

    if occurrences == 0:
        return None

    return pytestconfig.getoption("--base-url")


@pytest.fixture(scope="session")
def settings(pytestconfig):
    """Load settings using deterministic configuration precedence."""

    environment = pytestconfig.getoption("--env")
    base_url_override = _explicit_base_url(pytestconfig)

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