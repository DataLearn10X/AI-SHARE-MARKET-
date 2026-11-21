"""Ratio engine combining income, balance sheet and cash flow data."""

from __future__ import annotations

import pandas as pd


def _safe_div(a, b):
    try:
        if b is None or b == 0 or pd.isna(b) or pd.isna(a):
            return None
        return float(a) / float(b)
    except Exception:
        return None


def compute_ratios(income_df: pd.DataFrame, balance_df: pd.DataFrame = None,
                   cash_df: pd.DataFrame = None) -> pd.DataFrame:
    """Compute fundamental ratios aligned by period."""
    if income_df is None or income_df.empty:
        return pd.DataFrame()

    base = income_df.copy()
    # merge balance sheet
    if balance_df is not None and not balance_df.empty:
        b = balance_df.copy()
        base = base.merge(b, on="period", how="left", suffixes=("", "_bs"))
        # keep period_end from income
    # merge cash flow
    if cash_df is not None and not cash_df.empty:
        c = cash_df.copy()
        base = base.merge(c, on="period", how="left", suffixes=("", "_cf"))

    # ensure period_end exists
    if "period_end" not in base.columns and "period_end_bs" in base.columns:
        base["period_end"] = base["period_end_bs"]

    base = base.sort_values("period_end").reset_index(drop=True)

    # Growth
    base["revenue_growth_pct"] = base["revenue"].pct_change() * 100 if "revenue" in base.columns else None
    base["net_profit_growth_pct"] = base["net_profit"].pct_change() * 100 if "net_profit" in base.columns else None

    # Margins
    if "revenue" in base.columns:
        if "gross_profit" in base.columns:
            base["gross_margin_pct"] = base["gross_profit"] / base["revenue"] * 100
        if "operating_profit" in base.columns:
            base["operating_margin_pct"] = base["operating_profit"] / base["revenue"] * 100
        if "ebitda" in base.columns:
            base["ebitda_margin_pct"] = base["ebitda"] / base["revenue"] * 100
        if "net_profit" in base.columns:
            base["net_margin_pct"] = base["net_profit"] / base["revenue"] * 100

    # Returns
    if "net_profit" in base.columns and "stockholders_equity" in base.columns:
        base["roe_pct"] = base["net_profit"] / base["stockholders_equity"] * 100
    if "ebit" in base.columns and "total_assets" in base.columns and "current_liabilities" in base.columns:
        base["roce_pct"] = base["ebit"] / (base["total_assets"] - base["current_liabilities"]) * 100
    if "net_profit" in base.columns and "total_assets" in base.columns:
        base["roa_pct"] = base["net_profit"] / base["total_assets"] * 100

    # Leverage & liquidity
    if "total_debt" in base.columns and "stockholders_equity" in base.columns:
        base["debt_to_equity"] = base["total_debt"] / base["stockholders_equity"]
    if "ebit" in base.columns and "interest_expense" in base.columns:
        base["interest_coverage"] = base["ebit"] / base["interest_expense"].abs()
    if "current_assets" in base.columns and "current_liabilities" in base.columns:
        base["current_ratio"] = base["current_assets"] / base["current_liabilities"]
        if "inventory" in base.columns:
            base["quick_ratio"] = (base["current_assets"] - base["inventory"]) / base["current_liabilities"]

    # Cash flow
    if "operating_cf" in base.columns:
        base["operating_cf"] = base["operating_cf"]
    if "free_cash_flow" in base.columns and "revenue" in base.columns:
        base["fcf_margin_pct"] = base["free_cash_flow"] / base["revenue"] * 100
    if "operating_cf" in base.columns and "net_profit" in base.columns:
        base["cash_conversion"] = base["operating_cf"] / base["net_profit"]

    # EPS already present; P/E etc. require price (handled in valuation day)
    return base
