"""SQLite-backed cache service with TTL."""

from __future__ import annotations

import json
import time
from typing import Any, Optional

from database.db import get_connection
from database.optimize import optimize_database

optimize_database()


def cache_get(key: str) -> Optional[Any]:
    conn = get_connection()
    row = conn.execute(
        "SELECT value, expires_at FROM cache WHERE key = ?", (key,)
    ).fetchone()
    conn.close()
    if not row:
        return None
    if time.time() > row["expires_at"]:
        cache_delete(key)
        return None
    try:
        return json.loads(row["value"])
    except Exception:
        return None


def cache_set(key: str, value: Any, ttl_seconds: int = 300) -> None:
    conn = get_connection()
    conn.execute(
        "INSERT INTO cache (key, value, expires_at) VALUES (?, ?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value=excluded.value, expires_at=excluded.expires_at",
        (key, json.dumps(value), time.time() + ttl_seconds),
    )
    conn.commit()
    conn.close()


def cache_delete(key: str) -> None:
    conn = get_connection()
    conn.execute("DELETE FROM cache WHERE key = ?", (key,))
    conn.commit()
    conn.close()


def cache_clear() -> None:
    conn = get_connection()
    conn.execute("DELETE FROM cache")
    conn.commit()
    conn.close()


def cache_cleanup_expired() -> int:
    conn = get_connection()
    cur = conn.execute("DELETE FROM cache WHERE expires_at < ?", (time.time(),))
    conn.commit()
    n = cur.rowcount
    conn.close()
    return n
