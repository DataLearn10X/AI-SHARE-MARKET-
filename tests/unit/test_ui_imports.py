"""Smoke tests for UI modules."""

from frontend.theme import get_css
from frontend.components import ui


def test_get_css_returns_string():
    css = get_css()
    assert isinstance(css, str)
    assert "--asm-bg" in css
    assert "#0B1220" in css


def test_ui_module_imports():
    assert hasattr(ui, "metric_card")
    assert hasattr(ui, "page_header")
