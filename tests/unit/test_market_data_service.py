"""Unit tests for market data service (no network)."""

from unittest.mock import MagicMock

import pandas as pd

from services.market_data_service import MarketDataService


class FakeProvider:
    name = "fake"
    available = True

    def is_available(self):
        return self.available

    def get_quote(self, symbol):
        return {"symbol": symbol, "price": 100.0}

    def get_price_history(self, symbol, period="1y", interval="1d"):
        return pd.DataFrame({"close": [1.0, 2.0]})

    def get_company_info(self, symbol):
        return {"symbol": symbol, "name": "Fake Co"}


def test_provider_status():
    svc = MarketDataService(providers=[FakeProvider()])
    status = svc.provider_status()
    assert status[0]["name"] == "fake"
    assert status[0]["available"] is True


def test_get_quote_success():
    svc = MarketDataService(providers=[FakeProvider()])
    q = svc.get_quote("RELIANCE")
    assert q is not None
    assert q["price"] == 100.0
    assert q["source"] == "fake"


def test_cache_returns_same():
    svc = MarketDataService(providers=[FakeProvider()])
    q1 = svc.get_quote("TCS")
    q2 = svc.get_quote("TCS")
    assert q1 is q2


def test_fallback_when_unavailable():
    p = FakeProvider()
    p.available = False
    svc = MarketDataService(providers=[p])
    assert svc.get_quote("INFY") is None


def test_clear_cache():
    svc = MarketDataService(providers=[FakeProvider()])
    svc.get_quote("SBIN")
    svc.clear_cache()
    # after clear, new call should still work
    assert svc.get_quote("SBIN") is not None
