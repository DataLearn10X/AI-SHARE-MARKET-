"""Company overview service (yfinance info)."""

from __future__ import annotations

import logging
from typing import Optional

import yfinance as yf  # type: ignore

logger = logging.getLogger(__name__)


def _ns_symbol(symbol: str) -> str:
    symbol = symbol.strip().upper()
    if "." not in symbol:
        return f"{symbol}.NS"
    return symbol


def get_company_overview(symbol: str) -> Optional[dict]:
    try:
        info = yf.Ticker(_ns_symbol(symbol)).info or {}
        if not info:
            return None
        return {
            "name": info.get("longName") or info.get("shortName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "description": info.get("longBusinessSummary"),
            "market_cap": info.get("marketCap"),
            "enterprise_value": info.get("enterpriseValue"),
            "exchange": info.get("exchange"),
            "currency": info.get("currency"),
            "website": info.get("website"),
            "employees": info.get("fullTimeEmployees"),
            "country": info.get("country"),
            "source": "yfinance",
        }
    except Exception as exc:
        logger.warning("company overview failed for %s: %s", symbol, exc)
        return None
