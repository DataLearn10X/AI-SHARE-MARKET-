"""Unit tests for validation helpers."""

from services.validation import (
    is_valid_symbol,
    is_positive_number,
    is_non_negative_number,
    is_valid_date,
    sanitize_symbol,
)


def test_is_valid_symbol():
    assert is_valid_symbol("RELIANCE") is True
    assert is_valid_symbol("TCS") is True
    assert is_valid_symbol("") is False
    assert is_valid_symbol("123BAD!") is False


def test_is_positive_number():
    assert is_positive_number(5) is True
    assert is_positive_number(0) is False
    assert is_positive_number(-1) is False
    assert is_positive_number("abc") is False


def test_is_non_negative_number():
    assert is_non_negative_number(0) is True
    assert is_non_negative_number(5) is True
    assert is_non_negative_number(-1) is False


def test_is_valid_date():
    assert is_valid_date("2025-01-01") is True
    assert is_valid_date("") is True
    assert is_valid_date("01-01-2025") is False
    assert is_valid_date("not-a-date") is False


def test_sanitize_symbol():
    assert sanitize_symbol(" reliance ") == "RELIANCE"
    assert sanitize_symbol(None) == ""
