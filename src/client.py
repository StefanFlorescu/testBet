"""Shared API client implementation."""

from collections.abc import Mapping
from typing import Any

import requests

from src.logger import get_logger


class ApiClient:
    """HTTP client used by API tests and endpoint wrappers."""

    def __init__(
        self,
        session: requests.Session,
        base_url: str,
        headers: Mapping[str, str] | None = None,
        timeout: float = 10.0,
    ) -> None:
        self.session = session
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self.timeout = timeout
        self.logger = get_logger(self.__class__.__name__)

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json: Any = None,
        data: Any = None,
        headers: Mapping[str, str] | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        """Send a request to an API endpoint and return its response."""

        url = path if path.startswith(("http://", "https://")) else (
            f"{self.base_url}/{path.lstrip('/')}"
        )
        request_kwargs = {
            "params": params,
            "json": json,
            "data": data,
            "headers": headers,
            "timeout": self.timeout,
            **kwargs,
        }
        self.logger.info("%s %s", method.upper(), url)
        response = self.session.request(method, url, **request_kwargs)
        self.logger.info(
            "%s %s -> %s",
            method.upper(),
            url,
            response.status_code,
        )
        self.logger.debug("Request headers: %s", response.request.headers)
        self.logger.debug("Request body: %s", response.request.body)
        self.logger.debug("Response headers: %s", response.headers)
        self.logger.debug("Response body: %s", response.text)
        return response

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        """Send a GET request."""

        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> requests.Response:
        """Send a POST request."""

        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> requests.Response:
        """Send a PUT request."""

        return self.request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> requests.Response:
        """Send a PATCH request."""

        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> requests.Response:
        """Send a DELETE request."""

        return self.request("DELETE", path, **kwargs)

    def head(self, path: str, **kwargs: Any) -> requests.Response:
        """Send a HEAD request."""

        return self.request("HEAD", path, **kwargs)

    def options(self, path: str, **kwargs: Any) -> requests.Response:
        """Send an OPTIONS request."""

        return self.request("OPTIONS", path, **kwargs)
