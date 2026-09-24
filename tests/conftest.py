"""Shared pytest fixtures."""

import random
from collections.abc import Callable, Generator
from urllib.parse import quote

import pytest
import requests

from src.client import ApiClient
from src.config import settings
from src.logger import configure_logging


@pytest.fixture(scope="session", autouse=True)
def configure_test_logging() -> None:
    """Configure stdout and file logging for the test session."""

    configure_logging()
    
@pytest.fixture(scope="session", autouse=True)
def server_availability() -> None:
    """Verify that the web application is reachable before running tests."""
    try:
        response = requests.get(str(settings.web_base_url), timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        pytest.exit(f"Web application is not reachable: {e}")



@pytest.fixture(scope="session")
def web_url() -> str:
    """Return the web application URL for the configured user."""
    return f"{str(settings.web_base_url).rstrip('/')}/?user-id={quote(settings.user_id)}"


@pytest.fixture(scope="session")
def api_url() -> str:
    """Return the base API URL."""
    return str(settings.api_base_url).rstrip("/")


@pytest.fixture(scope="session")
def valid_random_stakes() -> Callable[[], float]:
    """Return random stake values from 1.00 to 100.00 in 0.20 increments."""

    step_size = 0.20
    lower_limit = 1.00
    upper_limit = 100.00

    stakes = [
        round(lower_limit + idx * step_size, 2)
        for idx in range(
            int((upper_limit - lower_limit) / step_size) + 1
        )
    ]

    return lambda: random.choice(stakes)


@pytest.fixture
def http_session() -> Generator[Callable[..., requests.Session]]:
    """Create an isolated HTTP session for one test."""

    session: requests.Session | None = None
    
    def create_session(is_auth: bool = True, auth_value: str = settings.user_id) -> requests.Session:
        nonlocal session
        session = requests.Session()
        session.headers.update({"Accept": "application/json", "Content-Type": "application/json"})
        if is_auth:
            session.headers.update({"x-user-id": auth_value})
        return session

    try:
        yield create_session
    finally:
        if session: session.close()


@pytest.fixture
def api_client( api_url: str) -> Callable[[requests.Session], ApiClient]:
    """Create an API client backed by the test's HTTP session."""
    
    return lambda session: ApiClient(session=session, base_url=api_url)


@pytest.fixture
def get_matches(
    http_session: Callable[..., requests.Session],
    api_client: Callable[[requests.Session], ApiClient],
) -> Callable[[], requests.Response]:
    """Return a callable that requests the authenticated matches endpoint."""

    def request_matches() -> requests.Response:
        session = http_session(is_auth=True)
        return api_client(session).get("/matches")

    return request_matches


@pytest.fixture
def get_balance(
    http_session: Callable[..., requests.Session],
    api_client: Callable[[requests.Session], ApiClient],
) -> Callable[[], requests.Response]:
    """Return a callable that requests the authenticated balance endpoint."""

    def request_balance() -> requests.Response:
        session = http_session(is_auth=True)
        return api_client(session).get("/balance")

    return request_balance


@pytest.fixture
def reset_balance(
    http_session: Callable[..., requests.Session],
    api_client: Callable[[requests.Session], ApiClient],
) -> Callable[[], requests.Response]:
    """Return a callable that requests the authenticated reset endpoint."""

    def request_reset_balance() -> requests.Response:
        session = http_session()
        return api_client(session).post("/reset-balance")

    return request_reset_balance


@pytest.fixture
def place_bet(
    http_session: Callable[..., requests.Session],
    api_client: Callable[[requests.Session], ApiClient],
) -> Callable[..., requests.Response]:
    """Create requests to the place-bet endpoint from keyword payload fields."""

    session = http_session(is_auth=True)
    client = api_client(session)

    def request_place_bet(**kwargs: object) -> requests.Response:
        return client.post("/place-bet", json=kwargs)

    return request_place_bet
