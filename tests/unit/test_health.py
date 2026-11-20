"""Unit tests for health checks."""

from services.health import health_status


def test_health_status_ok():
    result = health_status()
    assert result["status"] == "ok"
    assert "python_version" in result
    assert "app_name" in result
