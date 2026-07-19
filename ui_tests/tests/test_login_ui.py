import pytest
from playwright.sync_api import Page

from ui_tests.pages.devices_page import DevicesPage
from ui_tests.pages.login_page import LoginPage


pytestmark = pytest.mark.ui


def test_login_success(
    page: Page,
    base_url: str,
    test_username: str,
    test_password: str,
) -> None:
    login_page = LoginPage(page, base_url)
    devices_page = DevicesPage(page, base_url)

    login_page.open()
    login_page.login(test_username, test_password)

    devices_page.assert_loaded()


def test_login_failure(
    page: Page,
    base_url: str,
    test_username: str,
) -> None:
    login_page = LoginPage(page, base_url)
    devices_page = DevicesPage(page, base_url)

    login_page.open()
    login_page.login(
        test_username,
        "intentionally-invalid-password",
    )

    assert not devices_page.is_loaded()
    login_page.assert_login_failed()


def test_devices_page_loads(
    page: Page,
    base_url: str,
    test_username: str,
    test_password: str,
) -> None:
    login_page = LoginPage(page, base_url)
    devices_page = DevicesPage(page, base_url)

    login_page.open()
    login_page.login(test_username, test_password)

    devices_page.assert_loaded()