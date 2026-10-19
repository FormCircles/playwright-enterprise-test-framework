"""Shared UI page-object fixtures."""

from __future__ import annotations

import pytest
from playwright.sync_api import Page

from ui_tests.pages.login_page import LoginPage


@pytest.fixture(scope="function")
def login_page(page: Page, base_url: str) -> LoginPage:
    """Wrap the Playwright-owned test page in a LoginPage abstraction.

    Playwright owns the page and its cleanup. This fixture only
    constructs the page object for the current test.
    """
    return LoginPage(page=page, base_url=base_url)
