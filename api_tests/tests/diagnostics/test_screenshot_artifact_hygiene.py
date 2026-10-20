"""Security and artifact hygiene checks for screenshots."""

from pathlib import Path

from core.diagnostics.screenshot_paths import screenshot_artifact_path


def test_sensitive_parameter_values_are_not_exposed_in_filename():
    """Screenshot filenames must not reveal sensitive test parameters."""
    node_id = "ui_tests/test_login.py::test_login[password=SuperSecret123]"

    path = screenshot_artifact_path(
        output_directory=Path("test-results/screenshots"),
        run_id="test-run",
        worker_id="gw0",
        node_id=node_id,
    )

    assert "SuperSecret123" not in path.name
    assert "password" not in path.name.lower()


def test_screenshot_filename_is_opaque():
    """Screenshot filenames must not contain readable pytest identifiers."""
    import re

    path = screenshot_artifact_path(
        output_directory=Path("test-results/screenshots"),
        run_id="test-run",
        worker_id="gw0",
        node_id="ui_tests/test_login.py::test_login[user@example.com]",
    )

    assert re.fullmatch(r"[0-9a-f]{16}\.png", path.name)
    assert "test_login" not in path.name
    assert "user@example.com" not in path.name
