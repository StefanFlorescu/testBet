"""Typed framework settings loaded from environment variables and .env."""

import typing
from pathlib import Path

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Application and API settings used by the test framework."""

    web_base_url: AnyHttpUrl
    api_base_url: AnyHttpUrl
    user_id: str
    log_level: str = "INFO"
    log_file: Path = PROJECT_ROOT / "debug.log"
    api_documentation_url: AnyHttpUrl
    

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        validate_default=True,
    )

    def resolved_api_base_url(self) -> AnyHttpUrl:
        """Return the configured API URL or derive it from the application URL."""

        return self.api_base_url or self.web_base_url


# BaseSettings populates required fields from configured environment sources.
settings: typing.Final[Settings] = Settings()  # pyright: ignore[reportCallIssue]
