"""Fixtures for Selenium UI tests."""

from collections.abc import Generator

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

from src.ui.page_factory import PageObjectFactory


@pytest.fixture
def browser(request: pytest.FixtureRequest) -> Generator[WebDriver]:
    """Create a fresh Chrome browser for one UI test and close it afterward."""

    options = Options()
    options.enable_bidi = True
    options.add_argument("--window-size=1440,1000")
    options.add_argument("--disable-notifications")

    if not request.config.getoption("--headed"):
        options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(10)

    try:
        yield driver
    finally:
        driver.quit()


@pytest.fixture
def page_factory(browser: WebDriver) -> PageObjectFactory:
    """Return the page-object factory for the current browser."""

    return PageObjectFactory(browser)
