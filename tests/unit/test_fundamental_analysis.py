"""Unit tests for fundamental analysis helpers."""

import pandas as pd

from analytics.fundamental_analysis import add_growth_and_margins, calculate_cagr


def test_calculate_cagr():
    assert round(calculate_cagr(100, 121, 2), 2) == 10.0
    assert calculate_cagr(0, 100, 2) is None
    assert calculate_cagr(100, 200, 0) is None


def test_add_growth_and_margins():
    df = pd.DataFrame(
        {
            "period": ["FY2023", "FY2024"],
            "period_end": pd.to_datetime(["2023-03-31", "2024-03-31"]),
            "revenue": [100.0, 120.0],
            "operating_profit": [20.0, 26.0],
            "ebitda": [25.0, 32.0],
            "net_profit": [10.0, 14.0],
        }
    )
    out = add_growth_and_margins(df)
    assert "revenue_growth_pct" in out.columns
    assert "net_margin_pct" in out.columns
    assert round(out["revenue_growth_pct"].iloc[1], 2) == 20.0
