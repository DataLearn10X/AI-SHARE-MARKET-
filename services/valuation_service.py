"""Valuation service gathering inputs from market data and financial statements."""

from __future__ import annotations

import logging
from typing import Optional

import yfinance as yf  # type: ignore

from analytics.valuation import compute_valuation
from services.financial_statement_service import fetch_income_statement
from services.market_data_service import market_data_service

logger = logging.getLogger(__name__)


def _ns_symbol(symbol: str) -> str:
    symbol = symbol.strip().upper()
    if "." not in symbol:
        return f"{symbol}.NS"
    return symbol


def get_valuation_inputs(symbol: str) -> Optional[dict]:
    symbol = symbol.strip().upper()
    quote = market_data_service.get_quote(symbol)
    price = quote.get("price") if quote else None

    info = {}
    try:
        info = yf.Ticker(_ns_symbol(symbol)).info or {}
    except Exception as exc:
        logger.warning("valuation info failed for %s: %s", symbol, exc)

    if price is None:
        price = info.get("currentPrice") or info.get("regularMarketPrice")

    income = fetch_income_statement(symbol, quarterly=False)
    eps = None
    growth_rate = None
    shares = info.get("sharesOutstanding")
    if income is not None and not income.empty:
        eps = income["eps"].dropna().iloc[-1] if not income["eps"].dropna().empty else None
        # earnings growth: use net profit growth YoY
        if "net_profit" in income.columns and len(income) >= 2:
            last = income["net_profit"].dropna()
            if len(last) >= 2:
                growth_rate = (last.iloc[-1] / last.iloc[-2] - 1) * 100

    bvps = info.get("bookValue")
    if bvps is None and income is not None:
        eq = None
        # try balance sheet not fetched here; fall back to info
        pass

    dividend = info.get("dividendRate") or info.get("trailingAnnualDividendRate")

    result = compute_valuation(
        price=float(price) if price is not None else None,
        eps=float(eps) if eps is not None else None,
        book_value_per_share=float(bvps) if bvps is not None else None,
        growth_rate_pct=float(growth_rate) if growth_rate is not None else None,
        dividend_per_share=float(dividend) if dividend is not None else None,
    )
    # EV/EBITDA and P/S from info + financials
    ev = info.get("enterpriseValue")
    ebitda = None
    if income is not None and not income.empty and "ebitda" in income.columns:
        ebitda = income["ebitda"].dropna().iloc[-1] if not income["ebitda"].dropna().empty else None
    result["ev_ebitda"] = (ev / ebitda) if (ev and ebitda and ebitda != 0) else None
    result["price_to_sales"] = info.get("priceToSalesTrailing12Months")
    result["earnings_yield_pct"] = (eps / price * 100) if (eps and price and price != 0) else None
    result["gross_margin_pct"] = info.get("grossMargins", 0) * 100 if info.get("grossMargins") is not None else None
    result["operating_margin_pct"] = info.get("operatingMargins", 0) * 100 if info.get("operatingMargins") is not None else None
    result["net_margin_pct"] = info.get("profitMargins", 0) * 100 if info.get("profitMargins") is not None else None
    result["revenue_growth_pct"] = info.get("revenueGrowth", 0) * 100 if info.get("revenueGrowth") is not None else None
    result["earnings_growth_pct"] = info.get("earningsGrowth", 0) * 100 if info.get("earningsGrowth") is not None else None
    result["quick_ratio"] = info.get("quickRatio")
    result["current_ratio"] = info.get("currentRatio")
    result["market_cap"] = info.get("marketCap")
    result["enterprise_value"] = ev
    result["shares_outstanding"] = shares
    result["yfinance_pe"] = info.get("trailingPE")
    result["yfinance_pb"] = info.get("priceToBook")
    result["yfinance_peg"] = info.get("pegRatio")
    result["yfinance_dividend_yield_pct"] = info.get("dividendYield")
    result["source"] = "yfinance + financial statements"
    return result
