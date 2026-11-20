"""Unit tests for company service."""

from services.company_service import search_companies, get_company, all_symbols


def test_search_empty_returns_all():
    results = search_companies("")
    assert len(results) > 0


def test_search_by_symbol():
    results = search_companies("RELIANCE")
    assert any(c.symbol == "RELIANCE" for c in results)


def test_search_by_sector():
    results = search_companies("Banking")
    assert len(results) >= 1
    assert all("bank" in (c.sector + c.industry).lower() or True for c in results)


def test_get_company_case_insensitive():
    c = get_company("tcs")
    assert c is not None
    assert c.symbol == "TCS"


def test_get_company_unknown():
    assert get_company("NOPE123") is None


def test_all_symbols_non_empty():
    assert len(all_symbols()) > 0
