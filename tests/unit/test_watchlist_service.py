"""Unit tests for watchlist service."""

from services.watchlist_service import add_to_watchlist, list_watchlist, remove_from_watchlist


def test_watchlist_add_list_remove():
    sym = "TESTWL"
    # ensure clean
    remove_from_watchlist(sym)
    assert add_to_watchlist(sym) is True
    assert sym in list_watchlist()
    # duplicate
    assert add_to_watchlist(sym) is False
    assert remove_from_watchlist(sym) is True
    assert sym not in list_watchlist()
