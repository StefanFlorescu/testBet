"""Shared pytest fixtures."""

from collections.abc import Callable, Generator
from urllib.parse import quote

import pytest
import requests
import typing

from src.client import ApiClient
from src.config import settings
from src.logger import configure_logging


@pytest.fixture(scope="session", autouse=True)
def configure_test_logging() -> None:
    """Configure stdout and file logging for the test session."""

    configure_logging()



@pytest.fixture(scope="session")
def web_url() -> str:
    """Return the web application URL for the configured user."""
    return f"{str(settings.web_base_url).rstrip('/')}/?user-id={quote(settings.user_id)}"


@pytest.fixture(scope="session")
def api_url() -> str:
    """Return the base API URL."""
    return str(settings.api_base_url).rstrip("/")


@pytest.fixture
def http_session() -> Generator[Callable[[bool], requests.Session], requests.Session]:
    """Create an isolated HTTP session for one test."""

    session: requests.Session | None = None
    
    def create_session(is_auth: bool = True) -> requests.Session:
        nonlocal session
        session = requests.Session()
        session.headers.update({"Accept": "application/json", "Content-Type": "application/json"})
        if is_auth:
            session.headers.update({"x-user-id": settings.user_id})
        return session

    try:
        yield create_session
    finally:
        if session: session.close()


@pytest.fixture
def api_client( api_url: str) -> Callable[[requests.Session], ApiClient]:
    """Create an API client backed by the test's HTTP session."""
    
    return lambda session: ApiClient(session=session, base_url=api_url)
