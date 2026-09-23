from src.logger import get_logger, configure_logging
from src.config import settings


def main():
    configure_logging()
    logger = get_logger(__name__)
    logger.info("Hello from testbet!")
    logger.info(f"Web Base URL: {settings.web_base_url}")
    logger.info(f"API Base URL: {settings.api_base_url}")
    logger.info(f"User ID: {settings.user_id}")


if __name__ == "__main__":
    main()
