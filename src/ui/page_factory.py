"""Factory for creating page objects backed by a browser instance."""

from selenium.webdriver.remote.webdriver import WebDriver

from src.ui import pages


class PageObjectFactory:
    """Expose application page objects without leaking their implementations."""

    def __init__(self, browser: WebDriver) -> None:
        self._browser = browser

    @property
    def home_page(self) -> pages.HomePage:
        """Return a home-page object backed by the configured browser."""

        return pages.HomePage(self._browser)
