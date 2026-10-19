"""Regression tests for UI screenshot-on-failure behavior."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
from playwright.sync_api import Page

from core.diagnostics.failure_screenshots import (
    capture_failure_screenshot as _capture_failure_screenshot,
)
from core.diagnostics.failure_screenshots import (
    is_eligible_ui_failure,
)


def capture_failure_screenshot(**kwargs):
    """Supply stable test identities to the screenshot helper."""
    return _capture_failure_screenshot(
        run_id="test-run",
        worker_id="gw0",
        **kwargs,
    )


def make_item(*, ui=True, page=None):
    item = MagicMock()
    item.path = Path(
        "ui_tests/tests/test_login_ui.py" if ui else "api_tests/tests/test_devices.py"
    )
    item.get_closest_marker.return_value = None
    item.funcargs = {}

    if page is not None:
        item.funcargs["page"] = page

    return item


def make_report(*, failed=True, when="call"):
    return SimpleNamespace(
        failed=failed,
        when=when,
        nodeid="test_example.py::test_failure",
    )


def test_ui_failure_is_eligible():
    page = MagicMock(spec=Page)
    page.is_closed.return_value = False

    assert is_eligible_ui_failure(
        make_item(page=page),
        make_report(),
    )


@pytest.mark.parametrize(
    ("ui", "failed", "when"),
    [
        (True, False, "call"),
        (True, True, "setup"),
        (True, True, "teardown"),
        (False, True, "call"),
    ],
)
def test_ineligible_reports_are_skipped(ui, failed, when, tmp_path):
    page = MagicMock(spec=Page)
    page.is_closed.return_value = False

    result = capture_failure_screenshot(
        item=make_item(ui=ui, page=page),
        report=make_report(failed=failed, when=when),
        output_directory=tmp_path,
    )

    assert result is None
    page.screenshot.assert_not_called()


def test_missing_page_is_skipped(tmp_path):
    assert (
        capture_failure_screenshot(
            item=make_item(),
            report=make_report(),
            output_directory=tmp_path,
        )
        is None
    )


def test_closed_page_is_skipped(tmp_path):
    page = MagicMock(spec=Page)
    page.is_closed.return_value = True

    assert (
        capture_failure_screenshot(
            item=make_item(page=page),
            report=make_report(),
            output_directory=tmp_path,
        )
        is None
    )


def test_eligible_failure_captures_screenshot(tmp_path):
    page = MagicMock(spec=Page)
    page.is_closed.return_value = False

    def write_screenshot(*, path, full_page):
        assert full_page is True
        Path(path).write_bytes(b"fake png")

    page.screenshot.side_effect = write_screenshot

    result = capture_failure_screenshot(
        item=make_item(page=page),
        report=make_report(),
        output_directory=tmp_path,
    )

    assert result is not None
    assert result.exists()
    assert result.read_bytes() == b"fake png"
    page.screenshot.assert_called_once()


def test_capture_failure_does_not_propagate(tmp_path):
    page = MagicMock(spec=Page)
    page.is_closed.return_value = False
    page.screenshot.side_effect = RuntimeError("capture failed")

    result = capture_failure_screenshot(
        item=make_item(page=page),
        report=make_report(),
        output_directory=tmp_path,
    )

    assert result is None
    assert list(tmp_path.rglob("*.png")) == []


def test_storage_failure_does_not_propagate(tmp_path):
    page = MagicMock(spec=Page)
    page.is_closed.return_value = False

    with patch("pathlib.Path.mkdir", side_effect=OSError("storage unavailable")):
        result = capture_failure_screenshot(
            item=make_item(page=page),
            report=make_report(),
            output_directory=tmp_path,
        )

    assert result is None
    page.screenshot.assert_not_called()


def test_repeated_captures_have_distinct_paths(tmp_path):
    page = MagicMock(spec=Page)
    page.is_closed.return_value = False

    paths = []

    for _ in range(3):
        result = capture_failure_screenshot(
            item=make_item(page=page),
            report=make_report(),
            output_directory=tmp_path,
        )
        assert result is not None
        paths.append(result)

    assert len(set(paths)) == 3


def test_repeated_capture_preserves_existing_screenshot(tmp_path):
    """Repeated captures must not overwrite earlier evidence."""
    page = MagicMock(spec=Page)
    page.is_closed.return_value = False

    def write_screenshot(*, path, full_page):
        assert full_page is True
        Path(path).write_bytes(b"new screenshot")

    page.screenshot.side_effect = write_screenshot

    item = make_item(page=page)
    report = make_report()

    first = capture_failure_screenshot(
        item=item,
        report=report,
        output_directory=tmp_path,
    )

    assert first is not None
    assert first.exists()

    first.write_bytes(b"original screenshot")

    second = capture_failure_screenshot(
        item=item,
        report=report,
        output_directory=tmp_path,
    )

    assert second is not None
    assert second.exists()
    assert first != second
    assert first.read_bytes() == b"original screenshot"
    assert second.read_bytes() == b"new screenshot"
    assert page.screenshot.call_count == 2


@pytest.mark.parametrize(
    ("run_id", "screenshot_worker_id"),
    [
        (None, "gw0"),
        ("test-run", None),
        ("", "gw0"),
        ("test-run", ""),
    ],
)
def test_missing_screenshot_identity_skips_capture(
    tmp_path, run_id, screenshot_worker_id
):
    """Missing run or worker identity must not interrupt pytest."""
    page = MagicMock(spec=Page)
    page.is_closed.return_value = False

    result = _capture_failure_screenshot(
        item=make_item(page=page),
        report=make_report(),
        output_directory=tmp_path,
        run_id=run_id,
        worker_id=screenshot_worker_id,
    )

    assert result is None
    page.screenshot.assert_not_called()
    assert list(tmp_path.rglob("*.png")) == []
