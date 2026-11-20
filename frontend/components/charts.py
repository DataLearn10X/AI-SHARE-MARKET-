"""Plotly chart helpers for price analysis."""

from __future__ import annotations

from typing import Optional

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

POSITIVE = "#22C55E"
NEGATIVE = "#EF4444"
ACCENT = "#14B8A6"
ACCENT2 = "#3B82F6"
TEXT = "#F8FAFC"
GRID = "#1f2a44"


def candlestick_chart(df: pd.DataFrame, title: str = "Price History",
                      show_volume: bool = True) -> Optional[go.Figure]:
    """Build an interactive candlestick chart with volume and moving averages."""
    if df is None or df.empty:
        return None

    df = df.copy()
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    rows = 2 if show_volume and "volume" in df.columns else 1
    fig = make_subplots(
        rows=rows, cols=1, shared_xaxes=True,
        row_heights=[0.72, 0.28] if rows == 2 else [1.0],
        vertical_spacing=0.04,
    )

    fig.add_trace(
        go.Candlestick(
            x=df["date"],
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            name="OHLC",
            increasing_line_color=POSITIVE,
            decreasing_line_color=NEGATIVE,
        ),
        row=1, col=1,
    )

    for col, color, name in (("sma_20", ACCENT, "SMA 20"), ("sma_50", ACCENT2, "SMA 50")):
        if col in df.columns:
            fig.add_trace(
                go.Scatter(x=df["date"], y=df[col], mode="lines",
                           name=name, line=dict(color=color, width=1.5)),
                row=1, col=1,
            )

    if rows == 2:
        colors = [POSITIVE if c >= o else NEGATIVE
                  for c, o in zip(df["close"], df["open"])]
        fig.add_trace(
            go.Bar(x=df["date"], y=df["volume"], name="Volume",
                   marker_color=colors, opacity=0.6),
            row=2, col=1,
        )

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
        height=560,
    )
    fig.update_xaxes(
        rangeselector=dict(
            buttons=[
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all", label="All"),
            ]
        ),
        gridcolor=GRID,
    )
    fig.update_yaxes(gridcolor=GRID)
    return fig
