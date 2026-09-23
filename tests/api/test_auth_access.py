"""Fixture smoke tests without network requests."""
from src.logger import get_logger
import pytest
from pytest_check import check

pytestmark = [pytest.mark.access, pytest.mark.api]

logger = get_logger('test_access')

endpoints = [
    ( True, "/matches", 401, {"error": "missing_user_id"}),
    ( True, "/balance", 401, {"error": "missing_user_id"}),
    ( False, "/reset-balance", 401, {"error": "missing_user_id"}),
    ( False, "/place-bet", 401, {"error": "missing_user_id"})
    ]
    

@pytest.mark.parametrize("is_get_method, endpoint, expected_status, expected_response", endpoints, 
                         ids=[f"{'GET' if method else 'POST'} {endpoint}" for method, endpoint, _, _ in endpoints])
def test_endpoint_requires_authentication(http_session, api_client, is_get_method, endpoint, expected_status, expected_response) -> None:
    """Verify that the endpoint requires authentication."""
    session = http_session(is_auth=False)  # Create a session without authentication headers
    client = api_client(session)
    response = client.get(endpoint) if is_get_method else client.post(endpoint)
    check.equal(
        response.status_code,
        expected_status,
        f"Expected {expected_status} for {endpoint}",
    )
    check.equal(
        response.json(),
        expected_response,
        f"Expected {expected_response} for {endpoint}",
    )
    
