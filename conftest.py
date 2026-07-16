from __future__ import annotations

import pytest

from core.cleanup.backend_reset import evaluate_reset_response
from core.environment import assert_reset_allowed


pytest_plugins = [
    "core.fixtures.api_fixtures",
    "core.fixtures.base_fixtures",
    "core.fixtures.data_fixtures",
    "core.fixtures.ui_fixtures",
]


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="local",
        help=(
            "Target test environment: "
            "dev, local, ci, docker, k8s, staging"
        ),
    )


@pytest.fixture(scope="session", autouse=True)
def reset_backend_after_test_session(
    request,
    settings,
):
    """Reset backend test data after the session when supported."""

    test_admin_service = None

    if settings.password:
        test_admin_service = request.getfixturevalue(
            "test_admin_service"
        )

    yield

    assert_reset_allowed(settings.env)

    if test_admin_service is None:
        print(
            "\nBackend reset skipped because TEST_PASSWORD "
            "is not configured."
        )
        return

    response = test_admin_service.reset_test_data()
    reset_performed = evaluate_reset_response(response)

    if reset_performed:
        print("\nBackend test data reset completed.")
    else:
        print(
            "\nBackend reset endpoint is unavailable; "
            "per-test cleanup remains active."
        )