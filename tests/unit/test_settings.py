"""Unit tests for settings."""

from config.settings import settings


def test_settings_defaults():
    assert settings.APP_NAME == "AI Share Market Research Agent"
    assert settings.APP_ENV in {"development", "production", "staging"}
    assert isinstance(settings.APP_DEBUG, bool)
