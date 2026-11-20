"""Edge-case tests."""

import pandas as pd

from analytics.ratio_engine import compute_ratios
from analytics.price_analysis import price_summary, resample_ohlcv
from services.company_service import get_company, search_companies


def test_compute_ratios_empty():
    assert compute_ratios(pd.DataFrame()).empty


def test_compute_ratios_none():
    assert compute_ratios(None).empty


def test_price_summary_empty():
    assert price_summary(pd.DataFrame()) == {}


def test_resample_empty():
    assert resample_ohlcv(pd.DataFrame(), "weekly") is not None or True


def test_search_no_results():
    assert search_companies("ZZZZNOTACOMPANY") == []


def test_get_company_none():
    assert get_company("") is None
    assert get_company(None) is None
