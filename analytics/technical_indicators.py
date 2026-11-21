"""Technical indicators for price analysis."""

from __future__ import annotations

import pandas as pd
import numpy as np


def add_sma(df: pd.DataFrame, window: int) -> pd.DataFrame:
    if df is None or df.empty or "close" not in df.columns:
        return df
    df = df.copy()
    df[f"sma_{window}"] = df["close"].rolling(window=window, min_periods=1).mean()
    return df


def add_ema(df: pd.DataFrame, window: int) -> pd.DataFrame:
    if df is None or df.empty or "close" not in df.columns:
        return df
    df = df.copy()
    df[f"ema_{window}"] = df["close"].ewm(span=window, adjust=False).mean()
    return df


def add_rsi(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    if df is None or df.empty or "close" not in df.columns:
        return df
    df = df.copy()
    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=window, min_periods=window).mean()
    avg_loss = loss.rolling(window=window, min_periods=window).mean()
    rs = avg_gain / avg_loss.replace(0, pd.NA)
    df[f"rsi_{window}"] = 100 - (100 / (1 + rs))
    return df


def add_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    if df is None or df.empty or "close" not in df.columns:
        return df
    df = df.copy()
    ema_fast = df["close"].ewm(span=fast, adjust=False).mean()
    ema_slow = df["close"].ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    df["macd"] = macd
    df["macd_signal"] = signal_line
    df["macd_hist"] = macd - signal_line
    return df


def add_bollinger(df: pd.DataFrame, window: int = 20, num_std: float = 2.0) -> pd.DataFrame:
    if df is None or df.empty or "close" not in df.columns:
        return df
    df = df.copy()
    sma = df["close"].rolling(window=window, min_periods=1).mean()
    std = df["close"].rolling(window=window, min_periods=1).std()
    df["bb_mid"] = sma
    df["bb_upper"] = sma + num_std * std
    df["bb_lower"] = sma - num_std * std
    return df


def apply_indicators(df: pd.DataFrame, indicators: list) -> pd.DataFrame:
    if df is None or df.empty:
        return df
    df = df.copy()
    if "SMA 20" in indicators:
        df = add_sma(df, 20)
    if "SMA 50" in indicators:
        df = add_sma(df, 50)
    if "SMA 100" in indicators:
        df = add_sma(df, 100)
    if "SMA 200" in indicators:
        df = add_sma(df, 200)
    if "EMA 20" in indicators:
        df = add_ema(df, 20)
    if "RSI 14" in indicators:
        df = add_rsi(df, 14)
    if "MACD" in indicators:
        df = add_macd(df)
    if "Bollinger Bands" in indicators:
        df = add_bollinger(df)
    return df
