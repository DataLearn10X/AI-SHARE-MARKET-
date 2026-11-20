"""Unit tests for scoring engine."""

from analytics.scoring_engine import compute_fundamental_score


def test_compute_fundamental_score():
    ratios = {
        "revenue_growth_pct": 15.0,
        "net_profit_growth_pct": 12.0,
        "roe_pct": 18.0,
        "roce_pct": 20.0,
        "net_margin_pct": 12.0,
        "operating_margin_pct": 18.0,
        "debt_to_equity": 0.5,
        "interest_coverage": 6.0,
        "current_ratio": 1.8,
        "cash_conversion": 1.1,
        "fcf_margin_pct": 8.0,
    }
    val = {"pe": 20.0, "peg": 1.2}
    s = compute_fundamental_score(ratios, val)
    assert 0 <= s["total"] <= 100
    assert s["grade"] in {"A", "B", "C", "D", "E"}
    assert "growth" in s["sub_scores"]
    assert len(s["sub_scores"]) == 6


def test_compute_fundamental_score_empty():
    s = compute_fundamental_score({}, None)
    assert 0 <= s["total"] <= 100
    assert s["grade"] in {"A", "B", "C", "D", "E"}
