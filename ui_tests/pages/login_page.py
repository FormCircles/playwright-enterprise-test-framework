from playwright.sync_api import Locator, Page

from ui_tests.pages.base_page import BasePage


class LoginPage(BasePage):
    """Page object for the login page."""

    PATH = "/"

    def __init__(
        self,
        page: Page,
        base_url: str,
        timeout_ms: int = 10_000,
    ) -> None:
        super().__init__(page, base_url, timeout_ms)

    @property
    def heading(self) -> Locator:
        return self.page.get_by_role("heading", name="Login", exact=True)

    @property
    def username_input(self) -> Locator:
        return self.page.locator('[name="username"]')

    @property
    def password_input(self) -> Locator:
        return self.page.locator('[name="password"]')

    @property
    def login_button(self) -> Locator:
        return self.page.get_by_role("button", name="Login", exact=True)

    @property
    def failure_heading(self) -> Locator:
        return self.page.get_by_role(
            "heading",
            name="Login Failed",
            exact=True,
        )

    def open(self) -> None:
        """Navigate to the login page."""
        self.navigate(self.PATH)

    
    def assert_loaded(self) -> None:
        """Verify that the login page is displayed."""
        self.assert_visible(self.username_input)
        self.assert_visible(self.password_input)
        self.assert_enabled(self.login_button)


    def login(self, username: str, password: str) -> None:
        """Submit the login form."""
        self.fill(self.username_input, username)
        self.fill(self.password_input, password)
        self.click(self.login_button)

    def assert_login_failed(self) -> None:
        """Assert that authentication failed."""
        self.assert_url_contains("/login")
        self.assert_visible(self.failure_heading)