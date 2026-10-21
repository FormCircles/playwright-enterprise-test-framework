"""Shared UI page-object fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest
from playwright.sync_api import Page

from core.diagnostics.trace_paths import (
    reserve_trace_directory,
    trace_artifact_directory,
)
from ui_tests.pages.login_page import LoginPage


@pytest.fixture
def output_path(request, testrun_uid, worker_id) -> str:
    """Reserve a worker-safe directory for native Playwright artifacts."""
    base = trace_artifact_directory(
        output_directory=Path("test-results", "playwright").absolute(),
        run_id=testrun_uid,
        worker_id=worker_id,
        node_id=request.node.nodeid,
    )
    path = reserve_trace_directory(base)
    request.node._petf_trace_artifact_path = str(path)
    return str(path)


@pytest.fixture(scope="function")
def login_page(page: Page, base_url: str) -> LoginPage:
    """Wrap the Playwright-owned test page in a LoginPage abstraction.

    Playwright owns the page and its cleanup. This fixture only
    constructs the page object for the current test.
    """
    return LoginPage(page=page, base_url=base_url)
