"""Screenshot evidence for failed Playwright UI tests."""

from __future__ import annotations

import logging
import tempfile
from pathlib import Path
from typing import Any

from playwright.sync_api import Page

LOGGER = logging.getLogger(__name__)


def is_eligible_ui_failure(item: Any, report: Any) -> bool:
    """Select failed UI test calls with an existing Playwright page."""
    if report.when != "call" or not report.failed:
        return False

    is_ui_test = (
        item.get_closest_marker("ui") is not None
        or "ui_tests" in Path(str(item.path)).parts
    )

    if not is_ui_test:
        return False

    page = item.funcargs.get("page")
    return isinstance(page, Page) and not page.is_closed()


def capture_failure_screenshot(
    *,
    item: Any,
    report: Any,
    output_directory: Path,
) -> Path | None:
    """Capture evidence without changing the original test outcome."""
    if not is_eligible_ui_failure(item, report):
        return None

    page = item.funcargs["page"]
    output_path: Path | None = None

    try:
        output_directory.mkdir(parents=True, exist_ok=True)

        import os

        fd, filename = tempfile.mkstemp(
            prefix="ui-failure-",
            suffix=".png",
            dir=output_directory,
        )
        os.close(fd)
        output_path = Path(filename)

        page.screenshot(
            path=str(output_path),
            full_page=True,
        )

        return output_path

    except Exception:
        if output_path is not None:
            output_path.unlink(missing_ok=True)

        LOGGER.warning(
            "Unable to capture screenshot for %s",
            report.nodeid,
            exc_info=True,
        )
        return None
