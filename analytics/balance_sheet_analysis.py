"""Balance sheet and cash flow analysis helpers."""

from __future__ import annotations

import pandas as pd


def add_balance_sheet_metrics(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return df
    df = df.copy()
    if "stockholders_equity" in df.columns and "total_debt" in df.columns:
        df["debt_to_equity"] = df["total_debt"] / df["stockholders_equity"]
    if "current_assets" in df.columns and "current_liabilities" in df.columns:
        df["current_ratio"] = df["current_assets"] / df["current_liabilities"]
        df["working_capital"] = df["current_assets"] - df["current_liabilities"]
    return df


def add_cash_flow_metrics(df: pd.DataFrame, income_df: pd.DataFrame = None) -> pd.DataFrame:
    if df is None or df.empty:
        return df
    df = df.copy()
    if "free_cash_flow" in df.columns and "operating_cf" in df.columns:
        df["capex_to_ocf"] = df["capital_expenditure"] / df["operating_cf"] if "capital_expenditure" in df.columns else None
    return df
