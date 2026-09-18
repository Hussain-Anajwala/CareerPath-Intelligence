"""Logging configuration for CareerPath Intelligence."""

import logging
import sys
from careerpath.config.settings import settings


def setup_logging() -> logging.Logger:
    """Configures structured logging for the application."""
    logger = logging.getLogger("careerpath")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


logger = setup_logging()
