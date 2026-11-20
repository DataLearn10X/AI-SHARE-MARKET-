"""Basic application health checks."""

from __future__ import annotations

import sys
from typing import Dict, Any

from config.settings import settings


def health_status() -> Dict[str, Any]:
    """Return a small health report for the application."""
    return {
        "status": "ok",
        "app_name": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "python_version": sys.version.split()[0],
        "debug": settings.APP_DEBUG,
    }
