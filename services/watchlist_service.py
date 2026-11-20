"""Watchlist persistence service."""

from __future__ import annotations

from datetime import datetime
from typing import List

from database.db import get_connection


def list_watchlist() -> List[str]:
    conn = get_connection()
    rows = conn.execute("SELECT symbol FROM watchlist ORDER BY added_at DESC").fetchall()
    conn.close()
    return [r["symbol"] for r in rows]


def add_to_watchlist(symbol: str) -> bool:
    symbol = symbol.strip().upper()
    if not symbol:
        return False
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO watchlist (symbol, added_at) VALUES (?, ?)",
            (symbol, datetime.now().isoformat()),
        )
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()


def remove_from_watchlist(symbol: str) -> bool:
    conn = get_connection()
    cur = conn.execute("DELETE FROM watchlist WHERE symbol = ?", (symbol.strip().upper(),))
    conn.commit()
    changed = cur.rowcount > 0
    conn.close()
    return changed
