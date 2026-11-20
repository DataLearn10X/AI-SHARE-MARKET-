"""Unit tests for cache service."""

from services.cache_service import cache_get, cache_set, cache_delete, cache_clear


def test_cache_set_get():
    cache_set("test_key", {"a": 1}, ttl_seconds=60)
    assert cache_get("test_key") == {"a": 1}


def test_cache_delete():
    cache_set("del_key", 42, ttl_seconds=60)
    cache_delete("del_key")
    assert cache_get("del_key") is None


def test_cache_clear():
    cache_set("k1", 1, ttl_seconds=60)
    cache_clear()
    assert cache_get("k1") is None
