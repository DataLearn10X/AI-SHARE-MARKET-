"""Valuation helpers."""

from __future__ import annotations

from typing import Optional


def compute_valuation(price: Optional[float], eps: Optional[float],
                     book_value_per_share: Optional[float],
                     growth_rate_pct: Optional[float],
                     dividend_per_share: Optional[float]) -> dict:
    """Compute P/E, P/B, PEG and dividend yield."""
    pe = (price / eps) if (price and eps and eps != 0) else None
    pb = (price / book_value_per_share) if (price and book_value_per_share and book_value_per_share != 0) else None
    peg = (pe / growth_rate_pct) if (pe is not None and growth_rate_pct and growth_rate_pct != 0) else None
    div_yield = (dividend_per_share / price * 100) if (dividend_per_share and price and price != 0) else None
    return {
        "price": price,
        "eps": eps,
        "book_value_per_share": book_value_per_share,
        "growth_rate_pct": growth_rate_pct,
        "dividend_per_share": dividend_per_share,
        "pe": pe,
        "pb": pb,
        "peg": peg,
        "dividend_yield_pct": div_yield,
    }
