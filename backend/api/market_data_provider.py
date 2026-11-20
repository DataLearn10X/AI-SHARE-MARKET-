"""Base interface for market data providers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

import pandas as pd


class MarketDataProvider(ABC):
    """Abstract base class for market data providers."""

    name: str = "base"

    @abstractmethod
    def is_available(self) -> bool:
        """Return True if the provider can be used (deps installed etc.)."""

    @abstractmethod
    def get_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Return a quote dict or None."""

    @abstractmethod
    def get_price_history(self, symbol: str, period: str = "1y",
                          interval: str = "1d") -> Optional[pd.DataFrame]:
        """Return OHLCV DataFrame or None."""

    @abstractmethod
    def get_company_info(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Return company info dict or None."""
