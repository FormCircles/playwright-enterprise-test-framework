"""Screenshot evidence for failed Playwright UI tests."""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

from playwright.sync_api import Page

from core.diagnostics.screenshot_paths import screenshot_artifact_path

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
    run_id: str | None = None,
    worker_id: str | None = None,
) -> Path | None:
    """Capture evidence without changing the original test outcome."""
    if not is_eligible_ui_failure(item, report):
        return None

    if not run_id or not worker_id:
        LOGGER.warning("Screenshot identity unavailable for %s", report.nodeid)
        return None

    page = item.funcargs["page"]
    output_path: Path | None = None

    try:
        base_path = screenshot_artifact_path(
            output_directory=output_directory,
            run_id=run_id,
            worker_id=worker_id,
            node_id=report.nodeid,
        )
        base_path.parent.mkdir(parents=True, exist_ok=True)

        for attempt in range(100):
            candidate = (
                base_path
                if attempt == 0
                else base_path.with_name(
                    f"{base_path.stem}-{attempt}{base_path.suffix}"
                )
            )
            try:
                fd = os.open(
                    candidate,
                    os.O_CREAT | os.O_EXCL | os.O_WRONLY,
                    0o600,
                )
            except FileExistsError:
                continue

            output_path = candidate
            os.close(fd)
            break
        else:
            raise OSError("Screenshot collision limit exceeded")

        page.screenshot(path=str(output_path), full_page=True)
        return output_path

    except Exception:
        if output_path is not None:
            try:
                output_path.unlink(missing_ok=True)
            except OSError:
                LOGGER.warning("Unable to remove incomplete screenshot")

        LOGGER.warning(
            "Unable to capture screenshot for %s",
            report.nodeid,
            exc_info=True,
        )
        return None
