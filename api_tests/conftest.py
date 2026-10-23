"""Reference API consumer fixture and reset registration."""

from __future__ import annotations

import pytest
from xdist import is_xdist_worker

from api_tests.fixtures.api_fixtures import (  # noqa: F401
    api_client,
    auth_header,
    auth_token,
    devices_service,
    health_service,
    test_admin_service,
)
from api_tests.fixtures.data_fixtures import (  # noqa: F401
    created_device,
    device_cleanup,
    device_factory,
)
from core.cleanup.backend_reset import evaluate_reset_response
from core.environment import assert_reset_allowed


@pytest.fixture(scope="session", autouse=True)
def reset_backend_after_test_session(
    request,
    settings,
):
    """Reset backend data after serial runs when supported."""

    running_in_worker = is_xdist_worker(request)
    admin_service_instance = None

    if settings.password and not running_in_worker:
        admin_service_instance = request.getfixturevalue("test_admin_service")

    yield

    if running_in_worker:
        print(
            "\nBackend reset skipped in xdist worker; per-test cleanup remains active."
        )
        return

    assert_reset_allowed(settings.env)

    if admin_service_instance is None:
        print("\nBackend reset skipped because TEST_PASSWORD is not configured.")
        return

    response = admin_service_instance.reset_test_data()
    reset_performed = evaluate_reset_response(response)

    if reset_performed:
        print("\nBackend test data reset completed.")
    else:
        print(
            "\nBackend reset endpoint is unavailable; per-test cleanup remains active."
        )
