"""Foundation unit tests for CareerPath Intelligence."""

import pytest
from careerpath import __version__
from careerpath.config.settings import settings
from careerpath.config.logging import logger


def test_package_version():
    """Verify package version is loaded."""
    assert __version__ == "0.1.0"


def test_settings_initialization():
    """Verify application settings initialize cleanly."""
    assert settings.APP_NAME == "CareerPath Intelligence"
    assert settings.APP_VERSION == "0.1.0"
    assert settings.SIMILARITY_THRESHOLD == 0.65
    assert settings.DEFAULT_TOP_K == 5


def test_logging_setup():
    """Verify logger setup."""
    assert logger.name == "careerpath"
    logger.info("Foundation test log verification.")
