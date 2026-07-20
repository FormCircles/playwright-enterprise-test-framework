"""Page object for the application login page."""

from playwright.sync_api import Locator, Page

from ui_tests.pages.base_page import BasePage


class LoginPage(BasePage):
    """Model the login page and its supported interactions."""

    PATH = "/"

    def __init__(
        self,
        page: Page,
        base_url: str,
        timeout_ms: int = 10_000,
    ) -> None:
        super().__init__(
            page=page,
            base_url=base_url,
            timeout_ms=timeout_ms,
        )

        self.heading: Locator = page.get_by_role(
            "heading",
            name="Login",
            exact=True,
        )
        self.username_input: Locator = page.locator(
            'input[name="username"]'
        )
        self.password_input: Locator = page.locator(
            'input[name="password"]'
        )
        self.login_button: Locator = page.get_by_role(
            "button",
            name="Login",
            exact=True,
        )
        self.failure_heading: Locator = page.get_by_role(
            "heading",
            name="Login Failed",
            exact=True,
        )

    def open(self) -> None:
        """Open the login page."""
        self.navigate(self.PATH)

    def login(self, username: str, password: str) -> None:
        """Submit the login form using the supplied credentials."""
        self.fill(self.username_input, username)
        self.fill(self.password_input, password)
        self.click(self.login_button)

    def assert_loaded(self) -> None:
        """Verify that the login page and its form controls are displayed."""
        self.assert_visible(self.heading)
        self.assert_visible(self.username_input)
        self.assert_visible(self.password_input)
        self.assert_enabled(self.login_button)

    def assert_login_failed(self) -> None:
        """Verify that the application rejected the login attempt."""
        self.assert_url_contains("/login")
        self.assert_visible(self.failure_heading)