"""Database optimization: indexes and cache table."""

from __future__ import annotations

import sqlite3
import json
import time
from typing import Any, Optional

from database.db import get_connection


def optimize_database() -> None:
    """Create indexes and run maintenance commands."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CREATE INDEX IF NOT EXISTS idx_watchlist_symbol ON watchlist(symbol)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_portfolio_symbol ON portfolio(symbol)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_alerts_symbol ON alerts(symbol)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_alerts_metric ON alerts(metric)")
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS cache (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            expires_at REAL NOT NULL
        )
        """
    )
    cur.execute("CREATE INDEX IF NOT EXISTS idx_cache_expires ON cache(expires_at)")
    conn.commit()
    try:
        conn.execute("ANALYZE")
    except Exception:
        pass
    conn.close()


optimize_database()
