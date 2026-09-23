"""Logging configuration for the test automation framework."""

import logging
import sys
import typing
from pathlib import Path
from .config import settings


LOG_LEVEL: typing.Final = "INFO"
LOG_FORMAT: typing.Final = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
PROJECT_ROOT: typing.Final = Path(__file__).resolve().parent.parent


def configure_logging() -> None:
    """Configure framework logging from the LOG_LEVEL environment variable."""

    level = getattr(logging, settings.log_level, None)

    if not isinstance(level, int):
        raise ValueError(f"Invalid LOG_LEVEL: {settings.log_level}")

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    formatter = logging.Formatter(LOG_FORMAT)
    configured_handlers = {handler.name for handler in root_logger.handlers}

    if "stdout" not in configured_handlers:
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.set_name("stdout")
        stdout_handler.setFormatter(formatter)
        root_logger.addHandler(stdout_handler)

    if "file" not in configured_handlers:
        file_handler = logging.FileHandler(settings.log_file, encoding="utf-8")
        file_handler.set_name("file")
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """Return a named logger for framework or test code."""

    return logging.getLogger(name)
