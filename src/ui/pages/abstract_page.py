"""Shared Selenium page-object abstractions."""
from __future__ import annotations

from abc import ABC, abstractmethod

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import (
    visibility_of_all_elements_located,
    visibility_of_element_located,
)
from selenium.webdriver.support.ui import WebDriverWait
from src.logger import get_logger


logger = get_logger('Webdriver')
class Locator:
    """Elements locator descriptor class that waits for visible elements before returning them."""

    def __init__(
        self,
        by_locator: str,
        locator: str,
        timeout: None | float = None
    ) -> None:
        self._by_locator = by_locator
        self._locator = locator
        self._timeout = timeout
        self._found_elements: list[WebElement] = []

    def __get__(self, instance: AbstractPage, owner: type[AbstractPage] | None = None) -> Locator:
        _timeout = self._timeout if self._timeout else instance.implicit_timeout
        self._found_elements = WebDriverWait(instance._browser, _timeout).until(
            visibility_of_all_elements_located((self._by_locator, self._locator))
        )
        return self

    @property
    def first(self) -> WebElement:
        """Return the first visible matching element."""
        return self._found_elements[0]

    @property
    def all(self) -> list[WebElement]:
        """Return all visible matching elements."""
        return self._found_elements


class AbstractPage(ABC):
    """Base class shared by application page objects."""

    def __init__(self, browser: WebDriver) -> None:
        self._browser = browser

    @abstractmethod
    def open(self, url: str) -> None:
        """Open the page at the supplied URL."""

    @property
    def title(self) -> str:
        """Return the current page title."""
        return self._browser.title

    @property
    def implicit_timeout(self) -> float:
        """Return the browser's current implicit wait timeout in seconds."""
        return self._browser.timeouts.implicit_wait
    
    def text_is_visible(self, text: str) -> bool:
        try:
            _el = self.wait_until_visible((By.XPATH, f'//*[contains(text(), "{text}")]'))
            return _el.is_displayed()
        except Exception as ex:
            logger.error(f'Webdriver execption encountered: {ex}')
            return False

    def wait_until_visible(
        self,
        locator: tuple[str, str],
    ) -> WebElement:
        """Wait until one element is visible and return it."""
        _timeout = self.implicit_timeout
        return WebDriverWait(self._browser, _timeout).until(
            visibility_of_element_located(locator)
        )
