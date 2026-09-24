"""Fixture smoke tests without network requests."""
from src.logger import get_logger
import pytest
from pytest_check import check

pytestmark = [pytest.mark.access, pytest.mark.api]

logger = get_logger('test_access')

no_auth_error = {"error": "missing_user_id"}
invalid_auth_error = {"error": "invalid_user_id"}
negative_auth_scenarios = [
    ( True, "/matches"),
    ( True, "/balance"),
    ( False, "/reset-balance"),
    ( False, "/place-bet" )
    ]

@pytest.mark.parametrize("is_get_method, endpoint", negative_auth_scenarios, 
                         ids=[f"{'GET' if method else 'POST'} {endpoint}" for method, endpoint in negative_auth_scenarios])
def test_endpoint_requires_authentication(http_session, api_client, is_get_method, endpoint,) -> None:
    """Verify that the endpoint requires authentication."""
    session = http_session(is_auth=False)  # Create a session without authentication headers
    client = api_client(session)
    response = client.get(endpoint) if is_get_method else client.post(endpoint)
    check.equal(
        response.status_code,
        401,
        f"Expected 401 for {endpoint}",
    )
    check.equal(
        response.json(),
        no_auth_error,
        f"Expected {no_auth_error} for {endpoint}",
    )
    
@pytest.mark.parametrize("is_get_method, endpoint", negative_auth_scenarios, 
                         ids=[f"{'GET' if method else 'POST'} {endpoint}" for method, endpoint in negative_auth_scenarios])
def test_endpoint_requires_valid_user_id(http_session, api_client, is_get_method, endpoint) -> None:
    """Verify that the endpoint requires authentication."""
    session = http_session(is_auth=True, auth_value="invalid-user-id")  # Create a session with a valid user ID
    client = api_client(session)
    response = client.get(endpoint) if is_get_method else client.post(endpoint)
    check.equal(
        response.status_code,
        401,
        f"Expected 401 status for {endpoint}",
    )
    check.equal(
        response.json(),
        invalid_auth_error,
        f"Expected {invalid_auth_error} for {endpoint}",
    )
