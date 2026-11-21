"""Database optimization: indexes and cache table."""

from __future__ import annotations

import sqlite3
import json
import time
from typing import Any, Optional

from database.db import get_connection


def optimize_database() -> None:
    """Create tables, indexes and run maintenance commands."""
    conn = get_connection()
    cur = conn.cursor()
    # Ensure all tables exist before indexing.
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            metric TEXT NOT NULL,
            operator TEXT NOT NULL,
            threshold REAL NOT NULL,
            active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS cache (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            expires_at REAL NOT NULL
        )
        """
    )
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
