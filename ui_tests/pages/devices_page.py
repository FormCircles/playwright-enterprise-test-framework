"""Page object for the Devices page."""

from playwright.sync_api import Locator, Page

from ui_tests.pages.base_page import BasePage


class DevicesPage(BasePage):
    """Model the Devices page and its supported assertions."""

    PATH = "/devices"

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
            name="Devices",
            exact=True,
        )

    def assert_loaded(self) -> None:
        """Verify that the Devices page is displayed."""
        self.assert_url_contains(self.PATH)
        self.assert_visible(self.heading)

    def open(self) -> None:
        """Open the Devices page."""
        self.navigate(self.PATH)

    def is_loaded(self) -> bool:
        """Return whether the browser is currently on the Devices page."""
        return self.PATH in self.page.url

    @property
    def device_items(self) -> Locator:
        return self.page.locator("li")

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