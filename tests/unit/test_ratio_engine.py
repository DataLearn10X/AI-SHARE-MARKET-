"""Unit tests for ratio engine."""

import pandas as pd

from analytics.ratio_engine import compute_ratios


def _income():
    return pd.DataFrame(
        {
            "period": ["FY2023", "FY2024"],
            "period_end": pd.to_datetime(["2023-03-31", "2024-03-31"]),
            "revenue": [100.0, 120.0],
            "operating_profit": [20.0, 26.0],
            "ebitda": [25.0, 32.0],
            "ebit": [18.0, 24.0],
            "interest_expense": [2.0, 2.5],
            "net_profit": [10.0, 14.0],
            "eps": [5.0, 7.0],
        }
    )


def _balance():
    return pd.DataFrame(
        {
            "period": ["FY2023", "FY2024"],
            "period_end": pd.to_datetime(["2023-03-31", "2024-03-31"]),
            "total_assets": [200.0, 240.0],
            "total_liabilities": [80.0, 90.0],
            "stockholders_equity": [120.0, 150.0],
            "total_debt": [40.0, 45.0],
            "current_assets": [60.0, 70.0],
            "current_liabilities": [30.0, 35.0],
        }
    )


def _cash():
    return pd.DataFrame(
        {
            "period": ["FY2023", "FY2024"],
            "period_end": pd.to_datetime(["2023-03-31", "2024-03-31"]),
            "operating_cf": [12.0, 16.0],
            "free_cash_flow": [8.0, 11.0],
        }
    )


def test_compute_ratios():
    r = compute_ratios(_income(), _balance(), _cash())
    assert not r.empty
    assert "roe_pct" in r.columns
    assert "roce_pct" in r.columns
    assert "debt_to_equity" in r.columns
    assert "current_ratio" in r.columns
    assert "interest_coverage" in r.columns
    assert "cash_conversion" in r.columns
    # ROE = 10/120*100 = 8.33 for first
    assert round(r["roe_pct"].iloc[0], 2) == 8.33


def test_compute_ratios_income_only():
    r = compute_ratios(_income())
    assert not r.empty
    assert "net_margin_pct" in r.columns
    assert "debt_to_equity" not in r.columns
