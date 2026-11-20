"""Alerts and monitoring service."""

from __future__ import annotations

import sqlite3
from datetime import datetime
from typing import List, Dict, Any

from database.db import get_connection
from services.market_data_service import market_data_service
from analytics.ratio_engine import compute_ratios
from services.balance_sheet_service import fetch_balance_sheet
from services.cash_flow_service import fetch_cash_flow
from services.financial_statement_service import fetch_income_statement
from services.valuation_service import get_valuation_inputs
from analytics.scoring_engine import compute_fundamental_score


def _init_alerts_table() -> None:
    conn = get_connection()
    conn.execute(
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
    conn.commit()
    conn.close()


_init_alerts_table()


def list_alerts() -> List[Dict[str, Any]]:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM alerts ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_alert(symbol: str, metric: str, operator: str, threshold: float) -> bool:
    if operator not in (">", "<", ">=", "<="):
        return False
    conn = get_connection()
    conn.execute(
        "INSERT INTO alerts (symbol, metric, operator, threshold, active, created_at) VALUES (?, ?, ?, ?, 1, ?)",
        (symbol.strip().upper(), metric, operator, threshold, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()
    return True


def delete_alert(alert_id: int) -> bool:
    conn = get_connection()
    cur = conn.execute("DELETE FROM alerts WHERE id = ?", (alert_id,))
    conn.commit()
    changed = cur.rowcount > 0
    conn.close()
    return changed


def _metric_value(symbol: str, metric: str):
    symbol = symbol.strip().upper()
    if metric == "Price":
        q = market_data_service.get_quote(symbol)
        return q.get("price") if q else None
    income = fetch_income_statement(symbol, quarterly=False)
    balance = fetch_balance_sheet(symbol, quarterly=False)
    cash = fetch_cash_flow(symbol, quarterly=False)
    ratios = compute_ratios(income, balance, cash)
    latest = ratios.iloc[-1].to_dict() if (ratios is not None and not ratios.empty) else {}
    val = get_valuation_inputs(symbol)
    score = compute_fundamental_score(latest, val) if latest else None

    mapping = {
        "Revenue Growth %": latest.get("revenue_growth_pct"),
        "Net Margin %": latest.get("net_margin_pct"),
        "ROE %": latest.get("roe_pct"),
        "ROCE %": latest.get("roce_pct"),
        "Debt/Equity": latest.get("debt_to_equity"),
        "P/E": val.get("pe") if val else None,
        "Fundamental Score": score.get("total") if score else None,
    }
    return mapping.get(metric)


def evaluate_alerts() -> List[Dict[str, Any]]:
    triggered = []
    for a in list_alerts():
        if not a["active"]:
            continue
        value = _metric_value(a["symbol"], a["metric"])
        if value is None:
            continue
        op = a["operator"]
        thr = a["threshold"]
        ok = False
        if op == ">" and value > thr:
            ok = True
        elif op == "<" and value < thr:
            ok = True
        elif op == ">=" and value >= thr:
            ok = True
        elif op == "<=" and value <= thr:
            ok = True
        if ok:
            triggered.append({"id": a["id"], "symbol": a["symbol"], "metric": a["metric"],
                             "operator": op, "threshold": thr, "value": value})
    return triggered
