"""AI research agent grounded in verified financial data."""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from analytics.ratio_engine import compute_ratios
from analytics.scoring_engine import compute_fundamental_score
from services.balance_sheet_service import fetch_balance_sheet
from services.cash_flow_service import fetch_cash_flow
from services.company_service import get_company
from services.financial_statement_service import fetch_income_statement
from services.llm_service import generate_text
from services.valuation_service import get_valuation_inputs

logger = logging.getLogger(__name__)


def gather_context(symbol: str) -> Dict[str, Any]:
    """Gather verified data for a symbol into a structured dict."""
    symbol = symbol.strip().upper()
    company = get_company(symbol)
    profile = company.to_dict() if company else {"symbol": symbol}

    income = fetch_income_statement(symbol, quarterly=False)
    balance = fetch_balance_sheet(symbol, quarterly=False)
    cash = fetch_cash_flow(symbol, quarterly=False)
    ratios = compute_ratios(income, balance, cash)
    latest = ratios.iloc[-1].to_dict() if (ratios is not None and not ratios.empty) else {}
    valuation = get_valuation_inputs(symbol)
    score = compute_fundamental_score(latest, valuation) if latest else None

    latest_income = income.iloc[-1].to_dict() if (income is not None and not income.empty) else {}

    data = {
        "symbol": symbol,
        "profile": profile,
        "latest_period": latest.get("period"),
        "latest_income": latest_income,
        "latest_ratios": latest,
        "valuation": valuation or {},
        "score": score or {},
    }
    data["context_text"] = build_context_text(data)
    return data


def build_context_text(data: Dict[str, Any]) -> str:
    """Build a text context block from verified data."""
    symbol = data.get("symbol")
    profile = data.get("profile", {})
    income = data.get("latest_income", {})
    ratios = data.get("latest_ratios", {})
    val = data.get("valuation", {})
    score = data.get("score", {})

    lines = []
    lines.append(f"Company: {profile.get('name', symbol)} ({symbol})")
    lines.append(f"Sector: {profile.get('sector')} | Industry: {profile.get('industry')} | Exchange: {profile.get('exchange')}")
    lines.append(f"Data source: company master (sample seed) + yfinance (unofficial) financial statements.")
    lines.append("")
    lines.append("Latest financial period: " + str(ratios.get("period") or income.get("period") or "N/A"))
    lines.append("Income statement (latest period):")
    for k in ("revenue", "operating_profit", "ebitda", "net_profit", "eps"):
        if income.get(k) is not None:
            lines.append(f"  - {k}: {income.get(k)}")
    lines.append("Ratios (latest period):")
    for k in ("revenue_growth_pct", "net_profit_growth_pct", "operating_margin_pct", "ebitda_margin_pct",
              "net_margin_pct", "roe_pct", "roce_pct", "roa_pct", "debt_to_equity",
              "interest_coverage", "current_ratio", "cash_conversion"):
        if ratios.get(k) is not None:
            lines.append(f"  - {k}: {ratios.get(k)}")
    lines.append("Valuation:")
    for k in ("price", "pe", "pb", "peg", "dividend_yield_pct"):
        if val.get(k) is not None:
            lines.append(f"  - {k}: {val.get(k)}")
    lines.append(f"Fundamental score: {score.get('total')} (grade {score.get('grade')})")
    if score.get("sub_scores"):
        lines.append("Sub-scores: " + ", ".join(f"{k}={v}" for k, v in score["sub_scores"].items()))
    lines.append("")
    lines.append("IMPORTANT: Use only the verified numbers above. Do not invent or estimate any figure. "
                 "If a metric is missing, say it is unavailable.")
    return "\n".join(lines)


def answer_question(symbol: str, question: str) -> str:
    """Answer a research question grounded in verified data."""
    data = gather_context(symbol)
    context = data["context_text"]
    system = (
        "You are a financial research assistant. Answer using ONLY the provided verified data. "
        "Cite the metric and period. Do not invent numbers. If data is missing, say so. "
        "This is research, not investment advice."
    )
    prompt = f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
    llm_answer = generate_text(prompt, system=system)
    if llm_answer:
        return llm_answer.strip()
    # Fallback deterministic summary
    return _fallback_answer(data, question)


def _fallback_answer(data: Dict[str, Any], question: str) -> str:
    symbol = data.get("symbol")
    ratios = data.get("latest_ratios", {})
    val = data.get("valuation", {})
    score = data.get("score", {})
    lines = []
    lines.append(f"**{symbol} — Research Summary (no LLM configured)**")
    lines.append("")
    lines.append(f"- Period: {ratios.get('period', 'N/A')}")
    lines.append(f"- Revenue: {ratios.get('revenue', 'N/A')}")
    lines.append(f"- Net profit: {ratios.get('net_profit', 'N/A')}")
    lines.append(f"- Revenue growth: {ratios.get('revenue_growth_pct', 'N/A')}%")
    lines.append(f"- Net margin: {ratios.get('net_margin_pct', 'N/A')}%")
    lines.append(f"- ROE: {ratios.get('roe_pct', 'N/A')}% | ROCE: {ratios.get('roce_pct', 'N/A')}%")
    lines.append(f"- Debt/Equity: {ratios.get('debt_to_equity', 'N/A')}")
    lines.append(f"- P/E: {val.get('pe', 'N/A')} | P/B: {val.get('pb', 'N/A')} | PEG: {val.get('peg', 'N/A')}")
    lines.append(f"- Fundamental score: {score.get('total', 'N/A')} (grade {score.get('grade', 'N/A')})")
    lines.append("")
    lines.append("Configure an LLM (OPENAI_API_KEY / GROQ_API_KEY / OLLAMA) for natural-language answers.")
    lines.append(f"Question received: {question}")
    return "\n".join(lines)


def generate_report(symbol: str) -> str:
    """Generate a basic research report from verified data."""
    data = gather_context(symbol)
    context = data["context_text"]
    system = (
        "You are a financial research analyst. Write a structured research report using ONLY the provided verified data. "
        "Sections: Company Overview, Financial Performance, Profitability & Returns, Leverage & Liquidity, "
        "Valuation, Fundamental Score, Risks & Caveats, Conclusion. Cite periods. No invented numbers. "
        "This is research, not investment advice."
    )
    prompt = f"Context:\n{context}\n\nGenerate a research report for {symbol}."
    llm_report = generate_text(prompt, system=system)
    if llm_report:
        return llm_report.strip()
    # Fallback template
    return _fallback_report(data)


def _fallback_report(data: Dict[str, Any]) -> str:
    symbol = data.get("symbol")
    profile = data.get("profile", {})
    ratios = data.get("latest_ratios", {})
    val = data.get("valuation", {})
    score = data.get("score", {})
    return f"""# Research Report — {profile.get('name', symbol)} ({symbol})

## Company Overview
Sector: {profile.get('sector')} | Industry: {profile.get('industry')} | Exchange: {profile.get('exchange')}

## Financial Performance (Period: {ratios.get('period', 'N/A')})
- Revenue: {ratios.get('revenue', 'N/A')}
- Net profit: {ratios.get('net_profit', 'N/A')}
- Revenue growth: {ratios.get('revenue_growth_pct', 'N/A')}%
- Net profit growth: {ratios.get('net_profit_growth_pct', 'N/A')}%

## Profitability & Returns
- Operating margin: {ratios.get('operating_margin_pct', 'N/A')}%
- Net margin: {ratios.get('net_margin_pct', 'N/A')}%
- ROE: {ratios.get('roe_pct', 'N/A')}% | ROCE: {ratios.get('roce_pct', 'N/A')}% | ROA: {ratios.get('roa_pct', 'N/A')}%

## Leverage & Liquidity
- Debt/Equity: {ratios.get('debt_to_equity', 'N/A')}
- Current ratio: {ratios.get('current_ratio', 'N/A')}
- Interest coverage: {ratios.get('interest_coverage', 'N/A')}

## Valuation
- Price: {val.get('price', 'N/A')} | P/E: {val.get('pe', 'N/A')} | P/B: {val.get('pb', 'N/A')} | PEG: {val.get('peg', 'N/A')}
- Dividend yield: {val.get('dividend_yield_pct', 'N/A')}%

## Fundamental Score
- Score: {score.get('total', 'N/A')} / 100 (Grade {score.get('grade', 'N/A')})

## Risks & Caveats
- Data sourced from yfinance (unofficial) and local company master (sample seed).
- Missing values indicate unavailable data, not zero.

## Conclusion
This is an automated research summary based on verified data. Not investment advice.
"""
