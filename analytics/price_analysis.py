"""Price analytics helpers (moving averages, resampling, returns)."""

from __future__ import annotations

from typing import List

import pandas as pd


def ensure_datetime(df: pd.DataFrame) -> pd.DataFrame:
    if "date" in df.columns:
        df = df.copy()
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df


def add_moving_averages(df: pd.DataFrame, windows: List[int] = (20, 50)) -> pd.DataFrame:
    """Add SMA columns (e.g. sma_20) to a price DataFrame."""
    if df is None or df.empty or "close" not in df.columns:
        return df
    df = df.copy()
    for w in windows:
        df[f"sma_{w}"] = df["close"].rolling(window=w, min_periods=1).mean()
    return df


def resample_ohlcv(df: pd.DataFrame, interval: str) -> pd.DataFrame:
    """Resample an OHLCV DataFrame to the requested interval."""
    if df is None or df.empty:
        return df
    df = ensure_datetime(df)
    df = df.dropna(subset=["date"]).copy()
    if df.empty:
        return df

    rule_map = {
        "daily": None,
        "weekly": "W",
        "monthly": "M",
        "yearly": "Y",
    }
    rule = rule_map.get(interval.lower())
    if not rule:
        return df

    df = df.set_index("date")
    agg = {
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "volume": "sum",
    }
    # keep only available columns
    agg = {k: v for k, v in agg.items() if k in df.columns}
    resampled = df.resample(rule).agg(agg).dropna(subset=["close"])
    resampled = resampled.reset_index()
    # preserve symbol/source if present
    for col in ("symbol", "source"):
        if col in df.columns:
            resampled[col] = df[col].iloc[-1] if not df[col].empty else None
    return resampled


def compute_returns(df: pd.DataFrame) -> pd.DataFrame:
    """Add daily return percentage column."""
    if df is None or df.empty or "close" not in df.columns:
        return df
    df = df.copy()
    df["return_pct"] = df["close"].pct_change() * 100
    return df


def price_summary(df: pd.DataFrame) -> dict:
    """Compute simple summary metrics from a price DataFrame."""
    if df is None or df.empty or "close" not in df.columns:
        return {}
    first = float(df["close"].iloc[0])
    last = float(df["close"].iloc[-1])
    change = last - first
    pct = (change / first * 100) if first else 0.0
    return {
        "first_close": first,
        "last_close": last,
        "change": change,
        "change_pct": pct,
        "high": float(df["high"].max()) if "high" in df.columns else None,
        "low": float(df["low"].min()) if "low" in df.columns else None,
        "avg_volume": float(df["volume"].mean()) if "volume" in df.columns else None,
    }
