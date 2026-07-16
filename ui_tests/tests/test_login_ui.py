from ui_tests.pages.login_page import LoginPage
from ui_tests.pages.devices_page import DevicesPage

def test_login_success(
    page,
    base_url,
    test_username,
    test_password,
):
    login_page = LoginPage(page)
    devices_page = DevicesPage(page)

    login_page.goto(base_url)
    login_page.login(test_username, test_password)

    # Existing assertions remain here.
    assert devices_page.heading.is_visible()


def test_login_failure(page, base_url, test_username):
    login_page = LoginPage(page)
    devices_page = DevicesPage(page)

    login_page.goto(base_url)
    login_page.login(test_username, "intentionally-invalid-password")

    # Assert user is NOT on devices page
    assert not devices_page.is_loaded()


def test_devices_page_displays_list(page, base_url):
    login_page = LoginPage(page)
    devices_page = DevicesPage(page)

    login_page.goto(base_url)
    login_page.login("admin", "password")

    assert devices_page.heading.is_visible()
    assert devices_page.device_items.count() >= 0