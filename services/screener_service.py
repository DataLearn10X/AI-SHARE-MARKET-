"""Stock screener service: builds a metrics universe from the company master."""

from __future__ import annotations

import logging
import time
from typing import Optional

import pandas as pd

from analytics.ratio_engine import compute_ratios
from analytics.scoring_engine import compute_fundamental_score
from services.balance_sheet_service import fetch_balance_sheet
from services.cash_flow_service import fetch_cash_flow
from services.company_service import load_company_master
from services.financial_statement_service import fetch_income_statement
from services.valuation_service import get_valuation_inputs

logger = logging.getLogger(__name__)

_CACHE_TTL = 600  # 10 minutes
_cache: dict = {"data": None, "expires": 0.0}


def build_universe(force_refresh: bool = False) -> pd.DataFrame:
    """Build (or return cached) screener universe DataFrame."""
    now = time.time()
    if not force_refresh and _cache["data"] is not None and now < _cache["expires"]:
        return _cache["data"].copy()

    rows = []
    for company in load_company_master():
        try:
            inc = fetch_income_statement(company.symbol, quarterly=False)
            bs = fetch_balance_sheet(company.symbol, quarterly=False)
            cf = fetch_cash_flow(company.symbol, quarterly=False)
            ratios = compute_ratios(inc, bs, cf)
            latest = ratios.iloc[-1].to_dict() if (ratios is not None and not ratios.empty) else {}
            val = get_valuation_inputs(company.symbol)
            score = compute_fundamental_score(latest, val) if latest else None

            rows.append(
                {
                    "Symbol": company.symbol,
                    "Company": company.name,
                    "Sector": company.sector,
                    "Revenue": latest.get("revenue"),
                    "Net Profit": latest.get("net_profit"),
                    "Rev Growth %": latest.get("revenue_growth_pct"),
                    "Net Margin %": latest.get("net_margin_pct"),
                    "ROE %": latest.get("roe_pct"),
                    "ROCE %": latest.get("roce_pct"),
                    "Debt/Equity": latest.get("debt_to_equity"),
                    "P/E": val.get("pe") if val else None,
                    "P/B": val.get("pb") if val else None,
                    "Score": score.get("total") if score else None,
                }
            )
        except Exception as exc:
            logger.warning("Screener failed for %s: %s", company.symbol, exc)
            rows.append({"Symbol": company.symbol, "Company": company.name, "Sector": company.sector})

    df = pd.DataFrame(rows)
    _cache["data"] = df.copy()
    _cache["expires"] = now + _CACHE_TTL
    return df


def clear_cache() -> None:
    _cache["data"] = None
    _cache["expires"] = 0.0
