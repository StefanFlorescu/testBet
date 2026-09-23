"""Fixture smoke tests without network requests."""

import pytest
from pytest_check import check

from src.logger import get_logger

pytestmark = [pytest.mark.api, pytest.mark.health]

logger = get_logger("test_health")

def test_web_url_fixture(web_url: str) -> None:
    """Verify that the web URL fixture returns a user-specific URL."""
    check.is_true(web_url.startswith("https://"))
    check.is_in("?user-id=", web_url, "Expected user ID query parameter in web URL")
    logger.info(f"Web URL fixture returned: {web_url}")


def test_api_url_fixture(api_url: str) -> None:
    """Verify that the API URL fixture returns the API base path."""
    check.is_true(api_url.startswith("https://"))
    check.is_true(api_url.endswith("/api"), "Expected '/api' suffix in API URL")
    logger.info(f"API URL fixture returned: {api_url}")

def test_docs_endpoint_is_available(http_session, api_client) -> None:
    """Verify that the HTTP session fixture creates a session with headers."""
    session = http_session(is_auth=False) # Create a session without authentication headers
    client = api_client(session)
    response = client.get("/docs")
    check.equal(response.status_code, 200)
    logger.info(f"HTTP session fixture created a session with headers: {session.headers}")
    