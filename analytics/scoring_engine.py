"""Fundamental scoring engine (research aid, not a buy/sell signal)."""

from __future__ import annotations

from typing import Any, Dict, Optional


def _clamp(value: Optional[float], lo: float = 0.0, hi: float = 100.0) -> float:
    if value is None or value != value:  # NaN check
        return 50.0
    return max(lo, min(hi, float(value)))


def _score_thresholds(value: Optional[float], thresholds: list) -> float:
    """thresholds: list of (min_value, score) sorted descending by min_value."""
    if value is None or value != value:
        return 50.0
    for min_val, score in thresholds:
        if value >= min_val:
            return float(score)
    return float(thresholds[-1][1]) if thresholds else 50.0


def _score_lower_better(value: Optional[float], thresholds: list) -> float:
    """thresholds: list of (max_value, score) sorted ascending by max_value."""
    if value is None or value != value:
        return 50.0
    for max_val, score in thresholds:
        if value <= max_val:
            return float(score)
    return float(thresholds[-1][1]) if thresholds else 50.0


def score_growth(rev_growth: Optional[float], profit_growth: Optional[float]) -> float:
    g1 = _score_thresholds(rev_growth, [(20, 100), (10, 70), (0, 50), (-10, 30)])
    g2 = _score_thresholds(profit_growth, [(20, 100), (10, 70), (0, 50), (-10, 30)])
    return (g1 + g2) / 2


def score_profitability(roe, roce, net_margin, operating_margin) -> float:
    s1 = _score_thresholds(roe, [(20, 100), (15, 80), (10, 60), (5, 40)])
    s2 = _score_thresholds(roce, [(20, 100), (15, 80), (10, 60), (5, 40)])
    s3 = _score_thresholds(net_margin, [(15, 100), (10, 80), (5, 60)])
    s4 = _score_thresholds(operating_margin, [(20, 100), (15, 80), (10, 60)])
    return (s1 + s2 + s3 + s4) / 4


def score_leverage(de, interest_coverage) -> float:
    s1 = _score_lower_better(de, [(0.5, 100), (1.0, 80), (2.0, 60), (3.0, 40)])
    s2 = _score_thresholds(interest_coverage, [(5, 100), (2.5, 80), (1.5, 60)])
    return (s1 + s2) / 2


def score_liquidity(current_ratio) -> float:
    return _score_thresholds(current_ratio, [(2.0, 100), (1.5, 80), (1.0, 60), (0.8, 40)])


def score_cashflow(cash_conversion, fcf_margin) -> float:
    s1 = _score_thresholds(cash_conversion, [(1.0, 100), (0.8, 80), (0.5, 60)])
    s2 = _score_thresholds(fcf_margin, [(10, 100), (5, 80), (0, 60)])
    return (s1 + s2) / 2


def score_valuation(pe, peg) -> float:
    s1 = _score_lower_better(pe, [(15, 100), (25, 80), (35, 60), (50, 40)])
    s2 = _score_lower_better(peg, [(1.0, 100), (1.5, 80), (2.0, 60)])
    return (s1 + s2) / 2


WEIGHTS = {
    "growth": 0.20,
    "profitability": 0.25,
    "leverage": 0.15,
    "liquidity": 0.10,
    "cashflow": 0.15,
    "valuation": 0.15,
}


def compute_fundamental_score(latest_ratios: Dict[str, Any], valuation: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Compute a composite fundamental score (0-100)."""
    valuation = valuation or {}
    sub = {
        "growth": score_growth(latest_ratios.get("revenue_growth_pct"), latest_ratios.get("net_profit_growth_pct")),
        "profitability": score_profitability(
            latest_ratios.get("roe_pct"), latest_ratios.get("roce_pct"),
            latest_ratios.get("net_margin_pct"), latest_ratios.get("operating_margin_pct")),
        "leverage": score_leverage(latest_ratios.get("debt_to_equity"), latest_ratios.get("interest_coverage")),
        "liquidity": score_liquidity(latest_ratios.get("current_ratio")),
        "cashflow": score_cashflow(latest_ratios.get("cash_conversion"), latest_ratios.get("fcf_margin_pct")),
        "valuation": score_valuation(valuation.get("pe"), valuation.get("peg")),
    }

    total = sum(sub[k] * WEIGHTS[k] for k in WEIGHTS)
    total = round(_clamp(total), 2)

    if total >= 80:
        grade = "A"
    elif total >= 65:
        grade = "B"
    elif total >= 50:
        grade = "C"
    elif total >= 35:
        grade = "D"
    else:
        grade = "E"

    return {
        "total": total,
        "grade": grade,
        "sub_scores": {k: round(v, 2) for k, v in sub.items()},
        "weights": WEIGHTS,
    }
