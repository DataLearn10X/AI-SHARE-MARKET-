"""Unit tests for quarterly analysis."""

import pandas as pd

from analytics.quarterly_analysis import add_quarterly_growth


def test_add_quarterly_growth():
    df = pd.DataFrame(
        {
            "period": [f"Q{i}" for i in range(1, 9)],
            "period_end": pd.date_range("2023-03-31", periods=8, freq="QE"),
            "revenue": [100.0, 110, 120, 130, 105, 115, 125, 135],
            "net_profit": [10.0, 12, 14, 16, 11, 13, 15, 17],
            "operating_profit": [20.0] * 8,
        }
    )
    out = add_quarterly_growth(df)
    assert "revenue_qoq_pct" in out.columns
    assert "revenue_yoy_pct" in out.columns
    assert "net_profit_qoq_pct" in out.columns
    assert pd.notna(out["revenue_yoy_pct"].iloc[4])
