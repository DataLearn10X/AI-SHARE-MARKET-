"""Market data service with provider fallback and in-memory caching."""

from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, Optional

import pandas as pd

from backend.api.market_data_provider import MarketDataProvider
from backend.api.nse_provider import NSEProvider
from backend.api.yfinance_provider import YFinanceProvider
from services.cache_service import cache_get, cache_set

logger = logging.getLogger(__name__)

CACHE_TTL_SECONDS = 300  # 5 minutes


class _TimedCache:
    def __init__(self, ttl: int = CACHE_TTL_SECONDS):
        self.ttl = ttl
        self._store: dict = {}

    def get(self, key: str):
        entry = self._store.get(key)
        if not entry:
            return None
        value, expires = entry
        if time.time() > expires:
            del self._store[key]
            return None
        return value

    def set(self, key: str, value) -> None:
        self._store[key] = (value, time.time() + self.ttl)

    def clear(self) -> None:
        self._store.clear()


class MarketDataService:
    def __init__(self, providers: Optional[List[MarketDataProvider]] = None):
        if providers is None:
            providers = [YFinanceProvider(), NSEProvider()]
        self.providers = providers
        self._cache = _TimedCache()

    def provider_status(self) -> List[Dict[str, Any]]:
        return [{"name": p.name, "available": p.is_available()} for p in self.providers]

    def _try_providers(self, method: str, symbol: str, **kwargs):
        cache_key = f"{method}:{symbol}:{sorted(kwargs.items())}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            logger.debug("Cache hit (memory) for %s", cache_key)
            return cached

        # Persistent DB cache for lightweight dict results.
        if method in ("get_quote", "get_company_info"):
            db_cached = cache_get(cache_key)
            if db_cached is not None:
                logger.debug("Cache hit (db) for %s", cache_key)
                self._cache.set(cache_key, db_cached)
                return db_cached

        for provider in self.providers:
            if not provider.is_available():
                continue
            try:
                fn = getattr(provider, method)
                result = fn(symbol, **kwargs)
            except Exception as exc:
                logger.warning("%s.%s failed: %s", provider.name, method, exc)
                result = None
            if result is not None:
                # attach provenance
                if isinstance(result, dict):
                    result.setdefault("source", provider.name)
                    result.setdefault("fetched_at", time.time())
                    cache_set(cache_key, result, CACHE_TTL_SECONDS)
                self._cache.set(cache_key, result)
                return result
        logger.info("No provider returned data for %s.%s", method, symbol)
        return None

    def get_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        return self._try_providers("get_quote", symbol)

    def get_price_history(self, symbol: str, period: str = "1y",
                          interval: str = "1d") -> Optional[pd.DataFrame]:
        return self._try_providers("get_price_history", symbol, period=period, interval=interval)

    def get_company_info(self, symbol: str) -> Optional[Dict[str, Any]]:
        return self._try_providers("get_company_info", symbol)

    def clear_cache(self) -> None:
        self._cache.clear()


market_data_service = MarketDataService()
