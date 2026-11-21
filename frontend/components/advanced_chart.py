"""Advanced Plotly price chart helpers."""

from __future__ import annotations

from typing import List, Optional

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

POSITIVE = "#22C55E"
NEGATIVE = "#EF4444"
ACCENT = "#14B8A6"
ACCENT2 = "#3B82F6"
TEXT = "#F8FAFC"
GRID = "#1f2a44"
BENCH = "#F59E0B"


def _prepare(df):
    df = df.copy()
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df


def advanced_price_chart(df: pd.DataFrame, chart_type: str = "Candlestick",
                        indicators: Optional[List[str]] = None,
                        benchmark_df: Optional[pd.DataFrame] = None,
                        title: str = "Price Chart") -> Optional[go.Figure]:
    indicators = indicators or []
    if df is None or df.empty:
        return None
    df = _prepare(df)

    rows = 2 if "volume" in df.columns else 1
    fig = make_subplots(rows=rows, cols=1, shared_xaxes=True,
                        row_heights=[0.72, 0.28] if rows == 2 else [1.0],
                        vertical_spacing=0.04)

    if chart_type == "Candlestick":
        fig.add_trace(go.Candlestick(
            x=df["date"], open=df["open"], high=df["high"], low=df["low"], close=df["close"],
            name="OHLC", increasing_line_color=POSITIVE, decreasing_line_color=NEGATIVE), row=1, col=1)
    elif chart_type == "Line":
        fig.add_trace(go.Scatter(x=df["date"], y=df["close"], mode="lines", name="Close",
                                 line=dict(color=ACCENT, width=2)), row=1, col=1)
    elif chart_type == "Area":
        fig.add_trace(go.Scatter(x=df["date"], y=df["close"], mode="lines", name="Close",
                                 fill="tozeroy", line=dict(color=ACCENT, width=2)), row=1, col=1)

    # overlays
    overlay_map = {
        "SMA 20": ("sma_20", ACCENT, "SMA 20"),
        "SMA 50": ("sma_50", ACCENT2, "SMA 50"),
        "SMA 100": ("sma_100", "#A78BFA", "SMA 100"),
        "SMA 200": ("sma_200", "#F472B6", "SMA 200"),
        "EMA 20": ("ema_20", "#FBBF24", "EMA 20"),
    }
    for ind, (col, color, name) in overlay_map.items():
        if ind in indicators and col in df.columns:
            fig.add_trace(go.Scatter(x=df["date"], y=df[col], mode="lines", name=name,
                                     line=dict(color=color, width=1.5)), row=1, col=1)

    if "Bollinger Bands" in indicators and "bb_upper" in df.columns:
        fig.add_trace(go.Scatter(x=df["date"], y=df["bb_upper"], mode="lines", name="BB Upper",
                                 line=dict(color="#94A3B8", width=1, dash="dot")), row=1, col=1)
        fig.add_trace(go.Scatter(x=df["date"], y=df["bb_lower"], mode="lines", name="BB Lower",
                                 line=dict(color="#94A3B8", width=1, dash="dot"),
                                 fill="tonexty", fillcolor="rgba(148,163,184,0.08)"), row=1, col=1)

    # benchmark
    if benchmark_df is not None and not benchmark_df.empty:
        b = _prepare(benchmark_df)
        # normalize to first value for comparison
        if "close" in b.columns and not b["close"].empty:
            base = b["close"].iloc[0]
            norm = b["close"] / base * df["close"].iloc[0] if not df["close"].empty else b["close"]
            fig.add_trace(go.Scatter(x=b["date"], y=norm, mode="lines", name="Benchmark (normalized)",
                                     line=dict(color=BENCH, width=1.5, dash="dash")), row=1, col=1)

    if rows == 2:
        colors = [POSITIVE if c >= o else NEGATIVE for c, o in zip(df["close"], df["open"])]
        fig.add_trace(go.Bar(x=df["date"], y=df["volume"], name="Volume",
                             marker_color=colors, opacity=0.5), row=2, col=1)

    fig.update_layout(
        title=title,
        template="plotly_dark",
        paper_bgcolor="#172033",
        plot_bgcolor="#111827",
        font=dict(color=TEXT),
        xaxis_rangeslider_visible=False,
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=20, t=50, b=40),
        height=600,
    )
    fig.update_xaxes(gridcolor=GRID, rangeselector=dict(buttons=[
        dict(count=1, label="1m", step="month", stepmode="backward"),
        dict(count=3, label="3m", step="month", stepmode="backward"),
        dict(count=6, label="6m", step="month", stepmode="backward"),
        dict(count=1, label="1y", step="year", stepmode="backward"),
        dict(step="all", label="All"),
    ]))
    fig.update_yaxes(gridcolor=GRID)
    return fig


def rsi_chart(df: pd.DataFrame, window: int = 14) -> Optional[go.Figure]:
    col = f"rsi_{window}"
    if df is None or df.empty or col not in df.columns:
        return None
    df = _prepare(df)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["date"], y=df[col], mode="lines", name=f"RSI {window}",
                             line=dict(color=ACCENT, width=2)))
    fig.add_hline(y=70, line_dash="dash", line_color=NEGATIVE)
    fig.add_hline(y=30, line_dash="dash", line_color=POSITIVE)
    fig.update_layout(title=f"RSI ({window})", template="plotly_dark",
                      paper_bgcolor="#172033", plot_bgcolor="#111827",
                      font=dict(color=TEXT), height=250, margin=dict(l=40, r=20, t=40, b=30))
    fig.update_yaxes(range=[0, 100], gridcolor=GRID)
    return fig


def macd_chart(df: pd.DataFrame) -> Optional[go.Figure]:
    if df is None or df.empty or "macd" not in df.columns:
        return None
    df = _prepare(df)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["date"], y=df["macd"], mode="lines", name="MACD",
                             line=dict(color=ACCENT, width=2)))
    fig.add_trace(go.Scatter(x=df["date"], y=df["macd_signal"], mode="lines", name="Signal",
                             line=dict(color=ACCENT2, width=1.5)))
    colors = [POSITIVE if v >= 0 else NEGATIVE for v in df["macd_hist"].fillna(0)]
    fig.add_trace(go.Bar(x=df["date"], y=df["macd_hist"], name="Histogram", marker_color=colors, opacity=0.6))
    fig.update_layout(title="MACD", template="plotly_dark", paper_bgcolor="#172033",
                      plot_bgcolor="#111827", font=dict(color=TEXT), height=250,
                      margin=dict(l=40, r=20, t=40, b=30))
    fig.update_yaxes(gridcolor=GRID)
    return fig
