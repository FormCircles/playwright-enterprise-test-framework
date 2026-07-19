"""Shared base page abstraction for Playwright UI page objects."""

from urllib.parse import urljoin

from playwright.sync_api import Locator, Page, expect


class BasePage:
    """Base class containing common Playwright UI actions and assertions."""

    def __init__(
        self,
        page: Page,
        base_url: str,
        timeout_ms: int = 10_000,
    ) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/")
        self.timeout_ms = timeout_ms

        self.page.set_default_timeout(timeout_ms)
        self.page.set_default_navigation_timeout(timeout_ms)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def navigate(self, path: str = "") -> None:
        """Navigate to a path relative to the configured base URL."""
        url = self._build_url(path)
        self.page.goto(url, wait_until="domcontentloaded")

    def reload(self) -> None:
        """Reload the current page."""
        self.page.reload(wait_until="domcontentloaded")

    def wait_for_page_ready(self) -> None:
        """Wait until the page DOM has finished loading."""
        self.page.wait_for_load_state("domcontentloaded")

    def wait_for_url(self, url_pattern: str) -> None:
        """Wait until the browser URL matches the supplied pattern."""
        self.page.wait_for_url(url_pattern, timeout=self.timeout_ms)

    # ------------------------------------------------------------------
    # Common UI actions
    # ------------------------------------------------------------------

    def click(self, locator: Locator) -> None:
        """Wait for an element to become actionable and click it."""
        expect(locator).to_be_visible(timeout=self.timeout_ms)
        expect(locator).to_be_enabled(timeout=self.timeout_ms)
        locator.click()

    def fill(self, locator: Locator, value: str) -> None:
        """Clear an input and enter the supplied value."""
        expect(locator).to_be_visible(timeout=self.timeout_ms)
        expect(locator).to_be_editable(timeout=self.timeout_ms)
        locator.fill(value)

    def get_text(self, locator: Locator) -> str:
        """Return normalized visible text from an element."""
        expect(locator).to_be_visible(timeout=self.timeout_ms)
        return locator.inner_text().strip()

    # ------------------------------------------------------------------
    # Common assertions
    # ------------------------------------------------------------------

    def assert_visible(self, locator: Locator) -> None:
        """Assert that an element is visible."""
        expect(locator).to_be_visible(timeout=self.timeout_ms)

    def assert_hidden(self, locator: Locator) -> None:
        """Assert that an element is hidden or absent."""
        expect(locator).to_be_hidden(timeout=self.timeout_ms)

    def assert_enabled(self, locator: Locator) -> None:
        """Assert that an element is enabled."""
        expect(locator).to_be_enabled(timeout=self.timeout_ms)

    def assert_disabled(self, locator: Locator) -> None:
        """Assert that an element is disabled."""
        expect(locator).to_be_disabled(timeout=self.timeout_ms)

    def assert_text(self, locator: Locator, expected_text: str) -> None:
        """Assert that an element contains the expected text."""
        expect(locator).to_contain_text(
            expected_text,
            timeout=self.timeout_ms,
        )

    def assert_exact_text(self, locator: Locator, expected_text: str) -> None:
        """Assert that an element has exactly the expected text."""
        expect(locator).to_have_text(
            expected_text,
            timeout=self.timeout_ms,
        )

    def assert_title(self, expected_title: str) -> None:
        """Assert that the page has the expected title."""
        expect(self.page).to_have_title(
            expected_title,
            timeout=self.timeout_ms,
        )

    def assert_url(self, expected_url: str) -> None:
        """Assert that the page has the expected URL."""
        expect(self.page).to_have_url(
            expected_url,
            timeout=self.timeout_ms,
        )

    def assert_url_contains(self, expected_value: str) -> None:
        """Assert that the current URL contains a value."""
        current_url = self.page.url

        assert expected_value in current_url, (
            f"Expected URL to contain {expected_value!r}, "
            f"but current URL was {current_url!r}"
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_url(self, path: str) -> str:
        """Build an absolute URL from a path relative to the base URL."""
        if not path:
            return self.base_url

        normalized_path = path.lstrip("/")
        return urljoin(f"{self.base_url}/", normalized_path)