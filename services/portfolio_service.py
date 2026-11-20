"""Portfolio persistence service."""

from __future__ import annotations

from datetime import datetime
from typing import List, Dict, Any

from database.db import get_connection


def list_holdings() -> List[Dict[str, Any]]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, symbol, quantity, buy_price, buy_date, notes FROM portfolio ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_holding(symbol: str, quantity: float, buy_price: float, buy_date: str = None, notes: str = None) -> bool:
    symbol = symbol.strip().upper()
    if not symbol or quantity <= 0 or buy_price <= 0:
        return False
    conn = get_connection()
    conn.execute(
        "INSERT INTO portfolio (symbol, quantity, buy_price, buy_date, notes, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (symbol, quantity, buy_price, buy_date, notes, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()
    return True


def remove_holding(holding_id: int) -> bool:
    conn = get_connection()
    cur = conn.execute("DELETE FROM portfolio WHERE id = ?", (holding_id,))
    conn.commit()
    changed = cur.rowcount > 0
    conn.close()
    return changed
