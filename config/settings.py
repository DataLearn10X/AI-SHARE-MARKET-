"""Application configuration loaded from environment variables."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Project root is the parent of this config package's parent.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE)


def _get(key: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(key, default)
    if value is None:
        return default
    value = value.strip()
    return value if value != "" else default


class Settings:
    """Central application settings."""

    APP_NAME: str = _get("APP_NAME", "AI Share Market Research Agent") or "AI Share Market Research Agent"
    APP_ENV: str = _get("APP_ENV", "development") or "development"
    APP_DEBUG: bool = (_get("APP_DEBUG", "true") or "true").lower() in {"1", "true", "yes", "on"}
    LOG_LEVEL: str = _get("LOG_LEVEL", "INFO") or "INFO"

    STREAMLIT_PORT: int = int(_get("STREAMLIT_SERVER_PORT", "8501") or "8501")
    STREAMLIT_ADDRESS: str = _get("STREAMLIT_SERVER_ADDRESS", "0.0.0.0") or "0.0.0.0"

    # Market data providers (optional, free tiers)
    ALPHA_VANTAGE_API_KEY: Optional[str] = _get("ALPHA_VANTAGE_API_KEY")
    FINNHUB_API_KEY: Optional[str] = _get("FINNHUB_API_KEY")
    NEWS_API_KEY: Optional[str] = _get("NEWS_API_KEY")

    # AI / LLM providers (optional)
    OPENAI_API_KEY: Optional[str] = _get("OPENAI_API_KEY")
    GROQ_API_KEY: Optional[str] = _get("GROQ_API_KEY")
    OLLAMA_BASE_URL: Optional[str] = _get("OLLAMA_BASE_URL", "http://localhost:11434")

    DATABASE_URL: str = _get("DATABASE_URL", "sqlite:///./database/app.db") or "sqlite:///./database/app.db"

    @classmethod
    def is_production(cls) -> bool:
        return cls.APP_ENV.lower() == "production"


settings = Settings()
