"""Fundamental analysis helpers: growth, margins, CAGR."""

from __future__ import annotations

from typing import Optional

import pandas as pd


def add_growth_and_margins(df: pd.DataFrame) -> pd.DataFrame:
    """Add YoY growth and margin columns to an income-statement DataFrame."""
    if df is None or df.empty:
        return df
    df = df.copy().sort_values("period_end").reset_index(drop=True)

    if "revenue" in df.columns:
        df["revenue_growth_pct"] = df["revenue"].pct_change() * 100
    if "net_profit" in df.columns:
        df["net_profit_growth_pct"] = df["net_profit"].pct_change() * 100
    if "revenue" in df.columns and "operating_profit" in df.columns:
        df["operating_margin_pct"] = df["operating_profit"] / df["revenue"] * 100
    if "revenue" in df.columns and "ebitda" in df.columns:
        df["ebitda_margin_pct"] = df["ebitda"] / df["revenue"] * 100
    if "revenue" in df.columns and "net_profit" in df.columns:
        df["net_margin_pct"] = df["net_profit"] / df["revenue"] * 100
    return df


def calculate_cagr(start: float, end: float, years: int) -> Optional[float]:
    if start is None or end is None or years <= 0 or start == 0:
        return None
    try:
        return ((end / start) ** (1 / years) - 1) * 100
    except Exception:
        return None
