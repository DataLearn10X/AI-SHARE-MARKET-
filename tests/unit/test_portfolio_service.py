"""Unit tests for portfolio service."""

from services.portfolio_service import add_holding, list_holdings, remove_holding


def test_portfolio_add_list_remove():
    ok = add_holding("TESTPF", 10, 100.0, "2025-01-01", "test")
    assert ok is True
    holdings = list_holdings()
    assert any(h["symbol"] == "TESTPF" for h in holdings)
    hid = next(h["id"] for h in holdings if h["symbol"] == "TESTPF")
    assert remove_holding(hid) is True
    assert not any(h["symbol"] == "TESTPF" for h in list_holdings())


def test_portfolio_invalid():
    assert add_holding("X", 0, 100.0) is False
    assert add_holding("X", 10, 0) is False
