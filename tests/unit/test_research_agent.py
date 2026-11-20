"""Unit tests for research agent helpers."""

from agents.research_agent import build_context_text


def test_build_context_text():
    data = {
        "symbol": "RELIANCE",
        "profile": {"name": "Reliance Industries Limited", "sector": "Energy", "industry": "Oil & Gas", "exchange": "NSE"},
        "latest_ratios": {"period": "FY2025", "revenue": 100.0, "net_profit": 10.0, "roe_pct": 12.0},
        "valuation": {"pe": 20.0, "pb": 2.0},
        "score": {"total": 70.0, "grade": "B", "sub_scores": {"growth": 60.0}},
    }
    text = build_context_text(data)
    assert "RELIANCE" in text
    assert "FY2025" in text
    assert "verified data" in text.lower() or "verified" in text.lower()
