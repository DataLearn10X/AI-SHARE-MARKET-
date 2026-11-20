"""Unit tests for price analytics."""

import pandas as pd

from analytics.price_analysis import add_moving_averages, price_summary, resample_ohlcv


def _sample_df():
    return pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=10, freq="D"),
            "open": [100 + i for i in range(10)],
            "high": [105 + i for i in range(10)],
            "low": [95 + i for i in range(10)],
            "close": [102 + i for i in range(10)],
            "volume": [1000 * (i + 1) for i in range(10)],
        }
    )


def test_add_moving_averages():
    df = add_moving_averages(_sample_df(), [3, 5])
    assert "sma_3" in df.columns
    assert "sma_5" in df.columns


def test_price_summary():
    s = price_summary(_sample_df())
    assert "last_close" in s
    assert s["change_pct"] > 0


def test_resample_weekly():
    df = _sample_df()
    # extend to ~14 days for weekly resampling
    df2 = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=14, freq="D"),
            "open": list(range(14)),
            "high": list(range(1, 15)),
            "low": list(range(14)),
            "close": list(range(1, 15)),
            "volume": [100] * 14,
        }
    )
    out = resample_ohlcv(df2, "weekly")
    assert not out.empty
    assert "close" in out.columns


def test_resample_daily_noop():
    df = _sample_df()
    out = resample_ohlcv(df, "daily")
    assert len(out) == len(df)
