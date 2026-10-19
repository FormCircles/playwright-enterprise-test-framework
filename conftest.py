from __future__ import annotations

from pathlib import Path

import pytest
import pytest_html
from xdist import is_xdist_worker

from core.cleanup.backend_reset import evaluate_reset_response
from core.config.pytest_options import explicit_base_url
from core.config.settings import Settings
from core.environment import assert_reset_allowed

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
from core.diagnostics.failure_screenshots import (
    capture_failure_screenshot,
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
        help=("Target test environment: dev, local, ci, docker, k8s, staging"),
    )


def pytest_sessionstart(session):
    """Validate CI execution target before any tests or fixtures run."""

    config = session.config
    environment = config.getoption("--env")

    if environment != "ci":
        return

    explicit_url = explicit_base_url(config)

    overrides = {"base_url": explicit_url} if explicit_url is not None else None

    try:
        Settings(environment, cli_overrides=overrides)
    except ValueError as exc:
        raise pytest.UsageError(str(exc)) from exc


@pytest.fixture(scope="session", autouse=True)
def reset_backend_after_test_session(
    request,
    settings,
):
    """Reset backend data after serial runs when supported."""

    running_in_worker = is_xdist_worker(request)
    test_admin_service = None

    if settings.password and not running_in_worker:
        test_admin_service = request.getfixturevalue("test_admin_service")

    yield

    if running_in_worker:
        print(
            "\nBackend reset skipped in xdist worker; per-test cleanup remains active."
        )
        return

    assert_reset_allowed(settings.env)

    if test_admin_service is None:
        print("\nBackend reset skipped because TEST_PASSWORD is not configured.")
        return

    response = test_admin_service.reset_test_data()
    reset_performed = evaluate_reset_response(response)

    if reset_performed:
        print("\nBackend test data reset completed.")
    else:
        print(
            "\nBackend reset endpoint is unavailable; per-test cleanup remains active."
        )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach sanitized diagnostics when a test phase fails."""

    outcome = yield
    report = outcome.get_result()

    if not report.failed:
        return

    screenshot_path = capture_failure_screenshot(
        item=item,
        report=report,
        output_directory=Path("test-results", "screenshots"),
    )

    if screenshot_path is not None:
        item.user_properties.append(("failure_screenshot", str(screenshot_path)))

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
