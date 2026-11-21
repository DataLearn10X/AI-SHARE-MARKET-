"""Balance sheet service (via yfinance)."""

from __future__ import annotations

import logging
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)

try:
    import yfinance as yf  # type: ignore
    _YF_AVAILABLE = True
except Exception:  # pragma: no cover
    yf = None  # type: ignore
    _YF_AVAILABLE = False


def _ns_symbol(symbol: str) -> str:
    symbol = symbol.strip().upper()
    if "." not in symbol:
        return f"{symbol}.NS"
    return symbol


def _get_row(raw: pd.DataFrame, *names: str):
    for name in names:
        if name in raw.index:
            return raw.loc[name]
    return None


def fetch_balance_sheet(symbol: str, quarterly: bool = False) -> Optional[pd.DataFrame]:
    if not _YF_AVAILABLE:
        return None
    try:
        ticker = yf.Ticker(_ns_symbol(symbol))
        raw = ticker.quarterly_balance_sheet if quarterly else ticker.balance_sheet
        if raw is None or raw.empty:
            return None

        records = []
        for col in raw.columns:
            def val(*names):
                s = _get_row(raw, *names)
                if s is None:
                    return None
                try:
                    return float(s[col])
                except Exception:
                    return None

            period_end = pd.to_datetime(col)
            label = (f"Q{((period_end.month - 1) // 3) + 1} {period_end.year}"
                     if quarterly else f"FY{period_end.year}")
            records.append(
                {
                    "period": label,
                    "period_end": period_end,
                    "total_assets": val("Total Assets"),
                    "total_liabilities": val("Total Liabilities Net Minority Interest"),
                    "stockholders_equity": val("Stockholders Equity", "Total Equity Gross Minority Interest", "Common Stock Equity"),
                    "total_debt": val("Total Debt"),
                    "cash_and_equivalents": val("Cash And Cash Equivalents", "Cash Cash Equivalents And Short Term Investments"),
                    "current_assets": val("Current Assets"),
                    "current_liabilities": val("Current Liabilities"),
                    "inventory": val("Inventory"),
                    "source": "yfinance",
                }
            )
        df = pd.DataFrame(records).dropna(subset=["period_end"]).sort_values("period_end").reset_index(drop=True)
        return df if not df.empty else None
    except Exception as exc:
        logger.warning("Balance sheet fetch failed for %s: %s", symbol, exc)
        return None
