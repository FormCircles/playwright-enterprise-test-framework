from __future__ import annotations

import pytest
import pytest_html

from pathlib import Path
from core.cleanup.backend_reset import evaluate_reset_response
from core.environment import assert_reset_allowed
from xdist import is_xdist_worker

pytest_plugins = [
    "core.fixtures.api_fixtures",
    "core.fixtures.base_fixtures",
    "core.fixtures.data_fixtures",
    "core.fixtures.ui_fixtures",
]

from core.diagnostics.failure_diagnostics import (
    build_failure_diagnostics,
    write_failure_diagnostics,
)

DIAGNOSTICS_DIRECTORY = Path(
    "test-results",
    "diagnostics",
)



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
    """Reset backend data after serial runs when supported."""

    running_in_worker = is_xdist_worker(request)
    test_admin_service = None

    if settings.password and not running_in_worker:
        test_admin_service = request.getfixturevalue(
            "test_admin_service"
        )

    yield

    if running_in_worker:
        print(
            "\nBackend reset skipped in xdist worker; "
            "per-test cleanup remains active."
        )
        return

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



@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach sanitized diagnostics when a test phase fails."""

    outcome = yield
    report = outcome.get_result()

    if not report.failed:
        return

    diagnostics = build_failure_diagnostics(
        item=item,
        report=report,
    )

    rendered_diagnostics = diagnostics.render()

    output_path = write_failure_diagnostics(
        diagnostics=diagnostics,
        output_directory=DIAGNOSTICS_DIRECTORY,
    )

    if item.config.pluginmanager.hasplugin("html"):
        extras = getattr(report, "extras", [])

        extras.append(
            pytest_html.extras.text(
                rendered_diagnostics,
                name="Failure diagnostics",
            )
        )

        report.extras = extras

    item.user_properties.append(
        (
            "failure_diagnostics",
            str(output_path),
        )
    )