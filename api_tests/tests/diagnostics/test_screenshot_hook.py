"""Integration checks for screenshot handling in the pytest report hook."""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import conftest


def test_failed_report_records_screenshot_and_diagnostics(tmp_path):
    report = SimpleNamespace(
        failed=True,
        when="call",
        nodeid="ui_tests/tests/test_login_ui.py::test_login",
    )

    item = MagicMock()
    item.user_properties = []
    item.config.pluginmanager.hasplugin.return_value = False

    diagnostics = MagicMock()
    diagnostics.render.return_value = "Failure diagnostics"

    screenshot_path = tmp_path / "failure.png"
    diagnostics_path = tmp_path / "diagnostics.txt"

    with (
        patch.object(
            conftest,
            "capture_failure_screenshot",
            return_value=screenshot_path,
        ) as capture,
        patch.object(
            conftest,
            "build_failure_diagnostics",
            return_value=diagnostics,
        ),
        patch.object(
            conftest,
            "write_failure_diagnostics",
            return_value=diagnostics_path,
        ),
    ):
        hook = conftest.pytest_runtest_makereport(item, None)
        next(hook)

        with __import__("pytest").raises(StopIteration):
            hook.send(SimpleNamespace(get_result=lambda: report))

    capture.assert_called_once()
    assert (
        "failure_screenshot",
        str(screenshot_path),
    ) in item.user_properties
    assert (
        "failure_diagnostics",
        str(diagnostics_path),
    ) in item.user_properties
