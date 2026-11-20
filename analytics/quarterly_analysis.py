"""Quarterly results analysis helpers."""

from __future__ import annotations

import pandas as pd


def add_quarterly_growth(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return df
    df = df.copy().sort_values("period_end").reset_index(drop=True)
    if "revenue" in df.columns:
        df["revenue_qoq_pct"] = df["revenue"].pct_change() * 100
        df["revenue_yoy_pct"] = df["revenue"].pct_change(4) * 100
    if "net_profit" in df.columns:
        df["net_profit_qoq_pct"] = df["net_profit"].pct_change() * 100
        df["net_profit_yoy_pct"] = df["net_profit"].pct_change(4) * 100
    if "revenue" in df.columns and "operating_profit" in df.columns:
        df["operating_margin_pct"] = df["operating_profit"] / df["revenue"] * 100
    if "revenue" in df.columns and "net_profit" in df.columns:
        df["net_margin_pct"] = df["net_profit"] / df["revenue"] * 100
    return df
