"""Logging configuration and utilities."""

import logging
import sys
from typing import Optional

from app.config.settings import settings


def setup_logging(level: Optional[str] = None) -> None:
    """
    Configure application-wide logging.

    Args:
        level: Optional logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
               If not provided, uses DEBUG in debug mode, INFO otherwise
    """
    if level is None:
        level = "DEBUG" if settings.debug else "INFO"

    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )

    # Set third-party loggers to WARNING to reduce noise
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the given name.

    Args:
        name: Logger name (typically __name__ of the module)

    Returns:
        Configured logger instance

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("This is an info message")
        >>> logger.error("This is an error message")
    """
    return logging.getLogger(name)
