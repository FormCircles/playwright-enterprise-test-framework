import pytest
from playwright.sync_api import Page

from ui_tests.pages.devices_page import DevicesPage
from ui_tests.pages.login_page import LoginPage


pytestmark = pytest.mark.ui


@pytest.mark.ui
@pytest.mark.smoke
def test_login_page_loads(
    page: Page,
    base_url: str,
) -> None:
    """Verify that the login page loads with its primary controls."""
    login_page = LoginPage(page, base_url)

    login_page.open()
    login_page.assert_loaded()

import pytest
from playwright.sync_api import Page

from ui_tests.pages.devices_page import DevicesPage
from ui_tests.pages.login_page import LoginPage


@pytest.mark.ui
@pytest.mark.auth
@pytest.mark.regression
def test_login_success(
    page: Page,
    base_url: str,
    test_username: str,
    test_password: str,
) -> None:
    """Verify that a valid user can successfully log in."""

    login_page = LoginPage(page, base_url)
    devices_page = DevicesPage(page, base_url)

    login_page.open()
    login_page.assert_loaded()

    login_page.login(
        test_username,
        test_password,
    )

    devices_page.assert_loaded()


@pytest.mark.auth
@pytest.mark.regression
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


@pytest.mark.ui
@pytest.mark.auth
@pytest.mark.regression
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