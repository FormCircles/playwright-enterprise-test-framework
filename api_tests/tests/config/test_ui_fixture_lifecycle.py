"""Regression tests for PETF UI fixture lifecycle."""

from __future__ import annotations

from unittest.mock import MagicMock

from playwright.sync_api import Page

from ui_tests.fixtures.ui_fixtures import login_page as login_page_fixture
from ui_tests.pages.base_page import BasePage
from ui_tests.pages.login_page import LoginPage


def test_login_page_fixture_returns_correct_abstraction() -> None:
    """The fixture constructs the framework's LoginPage abstraction."""
    page = MagicMock(spec=Page)
    base_url = "http://127.0.0.1:8080"

    login_page = login_page_fixture.__wrapped__(
        page=page,
        base_url=base_url,
    )

    assert isinstance(login_page, LoginPage)
    assert isinstance(login_page, BasePage)
    assert login_page.page is page
    assert login_page.base_url == base_url


def test_login_page_fixture_uses_configured_base_url() -> None:
    """The page object receives the selected execution target."""
    page = MagicMock(spec=Page)

    login_page = login_page_fixture.__wrapped__(
        page=page,
        base_url="https://staging.example.com/",
    )

    assert login_page.base_url == "https://staging.example.com"


def test_login_page_fixture_configures_page_timeouts() -> None:
    """The page abstraction configures the supplied Playwright page."""
    page = MagicMock(spec=Page)

    login_page_fixture.__wrapped__(
        page=page,
        base_url="http://127.0.0.1:8080",
    )

    page.set_default_timeout.assert_called_once_with(10_000)
    page.set_default_navigation_timeout.assert_called_once_with(10_000)


def test_login_page_fixture_does_not_close_page() -> None:
    """The fixture must not dispose of a Playwright-owned page."""
    page = MagicMock(spec=Page)

    login_page_fixture.__wrapped__(
        page=page,
        base_url="http://127.0.0.1:8080",
    )

    page.close.assert_not_called()
    page.context.close.assert_not_called()


def test_login_page_fixture_creates_independent_page_objects() -> None:
    """Separate fixture invocations must not share page objects."""
    first_page = MagicMock(spec=Page)
    second_page = MagicMock(spec=Page)

    first = login_page_fixture.__wrapped__(
        page=first_page,
        base_url="http://127.0.0.1:8080",
    )

    second = login_page_fixture.__wrapped__(
        page=second_page,
        base_url="http://127.0.0.1:8080",
    )

    assert first is not second
    assert first.page is first_page
    assert second.page is second_page
