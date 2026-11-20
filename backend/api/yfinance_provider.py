"""Yahoo Finance provider (optional dependency)."""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

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


class YFinanceProvider:
    name = "yfinance"

    def is_available(self) -> bool:
        return _YF_AVAILABLE

    def get_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        if not self.is_available():
            return None
        try:
            ticker = yf.Ticker(_ns_symbol(symbol))
            info = ticker.fast_info if hasattr(ticker, "fast_info") else {}
            price = None
            try:
                price = float(info.last_price)
            except Exception:
                price = None
            if price is None:
                hist = ticker.history(period="5d")
                if not hist.empty:
                    price = float(hist["Close"].iloc[-1])
            result = {
                "symbol": symbol.strip().upper(),
                "price": price,
                "currency": "INR",
                "source": self.name,
            }
            return result
        except Exception as exc:
            logger.warning("yfinance quote failed for %s: %s", symbol, exc)
            return None

    def get_price_history(self, symbol: str, period: str = "1y",
                          interval: str = "1d") -> Optional[pd.DataFrame]:
        if not self.is_available():
            return None
        try:
            ticker = yf.Ticker(_ns_symbol(symbol))
            df = ticker.history(period=period, interval=interval)
            if df is None or df.empty:
                return None
            df = df.reset_index()
            # normalise column names
            rename = {"Date": "date", "Datetime": "date", "Open": "open",
                      "High": "high", "Low": "low", "Close": "close",
                      "Volume": "volume"}
            df = df.rename(columns=rename)
            if "close" in df.columns:
                df = df.dropna(subset=["close"])
            df["symbol"] = symbol.strip().upper()
            df["source"] = self.name
            return df if not df.empty else None
        except Exception as exc:
            logger.warning("yfinance history failed for %s: %s", symbol, exc)
            return None

    def get_company_info(self, symbol: str) -> Optional[Dict[str, Any]]:
        if not self.is_available():
            return None
        try:
            ticker = yf.Ticker(_ns_symbol(symbol))
            info = ticker.info or {}
            if not info:
                return None
            return {
                "symbol": symbol.strip().upper(),
                "name": info.get("longName") or info.get("shortName"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "website": info.get("website"),
                "description": info.get("longBusinessSummary"),
                "source": self.name,
            }
        except Exception as exc:
            logger.warning("yfinance company info failed for %s: %s", symbol, exc)
            return None
