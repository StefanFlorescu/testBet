"""Shared Selenium page-object abstractions."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import (
    visibility_of_all_elements_located,
    visibility_of_element_located,
)
from selenium.webdriver.support.ui import WebDriverWait


class Locator:
    """Descriptor that waits for visible elements before returning them."""

    def __init__(
        self,
        by_locator: str,
        locator: str,
        timeout: float = 10.0,
    ) -> None:
        self._by_locator = by_locator
        self._locator = locator
        self._timeout = timeout
        self._found_elements: list[WebElement] = []

    def __get__(self, instance: AbstractPage, owner: type[AbstractPage] | None = None) -> Locator:

        self._found_elements = WebDriverWait(instance._browser, self._timeout).until(
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

    def wait_until_visible(
        self,
        locator: tuple[str, str],
        timeout: float = 10.0,
    ) -> WebElement:
        """Wait until one element is visible and return it."""

        return WebDriverWait(self._browser, timeout).until(
            visibility_of_element_located(locator)
        )
