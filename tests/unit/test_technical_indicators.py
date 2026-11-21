"""Unit tests for technical indicators."""

import pandas as pd

from analytics.technical_indicators import apply_indicators, add_rsi, add_macd, add_bollinger


def _df():
    return pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=40, freq="D"),
            "open": [100 + i for i in range(40)],
            "high": [105 + i for i in range(40)],
            "low": [95 + i for i in range(40)],
            "close": [102 + i for i in range(40)],
            "volume": [1000] * 40,
        }
    )


def test_apply_indicators():
    df = apply_indicators(_df(), ["SMA 20", "EMA 20", "RSI 14", "MACD", "Bollinger Bands"])
    assert "sma_20" in df.columns
    assert "ema_20" in df.columns
    assert "rsi_14" in df.columns
    assert "macd" in df.columns
    assert "bb_upper" in df.columns


def test_rsi_range():
    df = add_rsi(_df(), 14)
    rsi = df["rsi_14"].dropna()
    assert (rsi >= 0).all() and (rsi <= 100).all()
