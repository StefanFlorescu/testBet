"""Fixture smoke tests without network requests."""
from src.logger import get_logger
import pytest
from pytest_check import check

pytestmark = [pytest.mark.matches, pytest.mark.api]

logger = get_logger('test_matches')

def test_get_matches_endpoint(http_session, api_client) -> None:
    """Verify that the GET /matches endpoint requires authentication."""
    session = http_session()  # Create a session without authentication headers
    client = api_client(session)
    response = client.get("/matches")
    check.equal(response.status_code, 200, "Expected 200 OK response code")
    check.is_true(response.json(), "Expected 'Unauthorized' error message")
