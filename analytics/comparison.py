"""Company comparison helpers."""

from __future__ import annotations

from typing import List

import pandas as pd

from analytics.ratio_engine import compute_ratios
from analytics.scoring_engine import compute_fundamental_score
from services.balance_sheet_service import fetch_balance_sheet
from services.cash_flow_service import fetch_cash_flow
from services.financial_statement_service import fetch_income_statement
from services.valuation_service import get_valuation_inputs


METRIC_LABELS = [
    ("revenue", "Revenue"),
    ("net_profit", "Net Profit"),
    ("revenue_growth_pct", "Revenue Growth %"),
    ("net_profit_growth_pct", "Net Profit Growth %"),
    ("operating_margin_pct", "Operating Margin %"),
    ("net_margin_pct", "Net Margin %"),
    ("roe_pct", "ROE %"),
    ("roce_pct", "ROCE %"),
    ("debt_to_equity", "Debt/Equity"),
    ("current_ratio", "Current Ratio"),
    ("pe", "P/E"),
    ("pb", "P/B"),
    ("fundamental_score", "Fundamental Score"),
]


def _latest(row_dict, key):
    v = row_dict.get(key)
    if v is None:
        return None
    try:
        if pd.isna(v):
            return None
    except Exception:
        pass
    return v


def build_comparison(symbols: List[str]) -> pd.DataFrame:
    """Build a comparison DataFrame: rows=metrics, columns=symbols."""
    data = {s: {} for s in symbols}
    for sym in symbols:
        inc = fetch_income_statement(sym, quarterly=False)
        bs = fetch_balance_sheet(sym, quarterly=False)
        cf = fetch_cash_flow(sym, quarterly=False)
        ratios = compute_ratios(inc, bs, cf)
        latest = ratios.iloc[-1].to_dict() if (ratios is not None and not ratios.empty) else {}
        val = get_valuation_inputs(sym)
        score = None
        if latest:
            score = compute_fundamental_score(latest, val)

        # revenue/net profit latest
        if inc is not None and not inc.empty:
            data[sym]["revenue"] = _latest(inc.iloc[-1].to_dict(), "revenue")
            data[sym]["net_profit"] = _latest(inc.iloc[-1].to_dict(), "net_profit")
        for key, _ in METRIC_LABELS:
            if key in latest:
                data[sym][key] = _latest(latest, key)
        if val:
            data[sym]["pe"] = val.get("pe")
            data[sym]["pb"] = val.get("pb")
        if score:
            data[sym]["fundamental_score"] = score.get("total")

    rows = []
    for key, label in METRIC_LABELS:
        row = {"Metric": label}
        for sym in symbols:
            v = data[sym].get(key)
            row[sym] = v
        rows.append(row)
    return pd.DataFrame(rows)
