"""Unit tests for valuation helpers."""

from analytics.valuation import compute_valuation


def test_compute_valuation():
    v = compute_valuation(price=100.0, eps=10.0, book_value_per_share=50.0,
                          growth_rate_pct=10.0, dividend_per_share=2.0)
    assert v["pe"] == 10.0
    assert v["pb"] == 2.0
    assert v["peg"] == 1.0
    assert v["dividend_yield_pct"] == 2.0


def test_compute_valuation_missing():
    v = compute_valuation(price=100.0, eps=None, book_value_per_share=None,
                          growth_rate_pct=None, dividend_per_share=None)
    assert v["pe"] is None
    assert v["pb"] is None
    assert v["peg"] is None
    assert v["dividend_yield_pct"] is None
