from playwright.sync_api import Locator, Page

from ui_tests.pages.base_page import BasePage


class DevicesPage(BasePage):
    """Page object for the Devices page."""

    PATH = "/devices"

    def __init__(
        self,
        page: Page,
        base_url: str,
        timeout_ms: int = 10_000,
    ) -> None:
        super().__init__(page, base_url, timeout_ms)

    @property
    def heading(self) -> Locator:
        return self.page.get_by_role(
            "heading",
            name="Devices",
            exact=True,
        )

    @property
    def device_items(self) -> Locator:
        return self.page.locator("li")

    def open(self) -> None:
        """Navigate to the Devices page."""
        self.navigate(self.PATH)

    def is_loaded(self) -> bool:
        """Return whether the current URL is the Devices page."""
        return "/devices" in self.page.url

    def assert_loaded(self) -> None:
        """Assert that the Devices page loaded successfully."""
        self.assert_url_contains("/devices")
        self.assert_visible(self.heading)

    def device_count(self) -> int:
        """Return the number of displayed device items."""
        return self.device_items.count()

    def assert_has_devices(self) -> None:
        """Assert that at least one device is displayed."""
        count = self.device_count()

        assert count > 0, (
            "Expected at least one device to be displayed, "
            "but the device list was empty"
        )

        self.assert_visible(self.device_items.first)