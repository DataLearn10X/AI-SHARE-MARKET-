"""Unit tests for balance sheet analysis."""

import pandas as pd

from analytics.balance_sheet_analysis import add_balance_sheet_metrics


def test_add_balance_sheet_metrics():
    df = pd.DataFrame(
        {
            "period": ["FY2024", "FY2025"],
            "total_debt": [100.0, 120.0],
            "stockholders_equity": [200.0, 240.0],
            "current_assets": [50.0, 60.0],
            "current_liabilities": [25.0, 30.0],
        }
    )
    out = add_balance_sheet_metrics(df)
    assert "debt_to_equity" in out.columns
    assert "current_ratio" in out.columns
    assert "working_capital" in out.columns
    assert round(out["current_ratio"].iloc[0], 2) == 2.0
