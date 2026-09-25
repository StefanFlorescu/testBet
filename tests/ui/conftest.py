"""Fixtures for Selenium UI tests."""

from collections.abc import Generator

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

from src.ui.page_factory import PageObjectFactory


@pytest.fixture
def browser(request: pytest.FixtureRequest) -> Generator[WebDriver]:
    """Create a fresh Chrome browser for one UI test and close it afterward no matter the test outcome."""

    options = Options()
    options.enable_bidi = True
    options.add_argument("--window-size=1440,1000")
    options.add_argument("--disable-notifications")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

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

@pytest.fixture
def reset_balance_page_factory(browser: WebDriver, reset_balance) -> PageObjectFactory:
    """Return the page-object factory for the current browser."""
    reset_balance()
    return PageObjectFactory(browser)
