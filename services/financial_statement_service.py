"""Financial statement service (income statement via yfinance)."""

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


def _get_row(raw: pd.DataFrame, *names: str) -> Optional[pd.Series]:
    for name in names:
        if name in raw.index:
            return raw.loc[name]
    return None


def fetch_income_statement(symbol: str, quarterly: bool = False) -> Optional[pd.DataFrame]:
    """Fetch a normalised income statement for a symbol.

    Returns a DataFrame sorted by period ascending with columns:
    period, period_end, revenue, operating_profit, ebitda, net_profit, eps, source.
    """
    if not _YF_AVAILABLE:
        return None
    try:
        ticker = yf.Ticker(_ns_symbol(symbol))
        raw = ticker.quarterly_financials if quarterly else ticker.financials
        if raw is None or raw.empty:
            return None

        revenue_s = _get_row(raw, "Total Revenue", "Operating Revenue")
        op_s = _get_row(raw, "Operating Income")
        ebitda_s = _get_row(raw, "EBITDA")
        ebit_s = _get_row(raw, "EBIT")
        interest_s = _get_row(raw, "Interest Expense")
        shares_s = _get_row(raw, "Diluted Average Shares", "Basic Average Shares")
        net_s = _get_row(raw, "Net Income", "Net Income Common Stockholders")
        eps_s = _get_row(raw, "Diluted EPS", "Basic EPS")

        records = []
        for col in raw.columns:
            def val(s):
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
                    "revenue": val(revenue_s),
                    "operating_profit": val(op_s),
                    "ebitda": val(ebitda_s),
                    "ebit": val(ebit_s),
                    "interest_expense": val(interest_s),
                    "shares_outstanding": val(shares_s),
                    "net_profit": val(net_s),
                    "eps": val(eps_s),
                    "source": "yfinance",
                }
            )

        df = pd.DataFrame(records)
        df = df.dropna(subset=["period_end"]).sort_values("period_end").reset_index(drop=True)
        if df.empty:
            return None
        return df
    except Exception as exc:
        logger.warning("Income statement fetch failed for %s: %s", symbol, exc)
        return None
