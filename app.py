"""AI Share Market Research Agent - Streamlit entry point."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import streamlit as st

from config.logging_config import logger
from config.settings import settings
from frontend.theme import apply_theme
from analytics.technical_indicators import apply_indicators
from frontend.components.advanced_chart import advanced_price_chart, macd_chart, rsi_chart
from frontend.components.charts import candlestick_chart
from frontend.components.ui import (
    alert,
    empty_state,
    loading_state,
    metric_card,
    page_header,
    profile_card,
    sample_note,
    section_header,
)
from analytics.balance_sheet_analysis import add_balance_sheet_metrics
from analytics.quarterly_analysis import add_quarterly_growth
from analytics.comparison import build_comparison
from analytics.scoring_engine import compute_fundamental_score
from analytics.valuation import compute_valuation
from analytics.ratio_engine import compute_ratios
from analytics.fundamental_analysis import add_growth_and_margins, calculate_cagr
from analytics.price_analysis import add_moving_averages, price_summary, resample_ohlcv
from agents.research_agent import answer_question
from agents.report_generator import generate_report
from services.company_service import search_companies, get_company
from services.portfolio_service import add_holding, list_holdings, remove_holding
from services.alert_service import add_alert, delete_alert, evaluate_alerts, list_alerts
from services.watchlist_service import add_to_watchlist, list_watchlist, remove_from_watchlist
from services.balance_sheet_service import fetch_balance_sheet
from services.cash_flow_service import fetch_cash_flow
from services.financial_statement_service import fetch_income_statement
from services.screener_service import build_universe, clear_cache
from services.valuation_service import get_valuation_inputs
from services.health import health_status
from services.market_data_service import market_data_service

st.set_page_config(
    page_title="AI Share Market Research Agent",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
logger.info("Application started: %s", settings.APP_NAME)

SECTIONS = [
    "Market Overview",
    "Search Indian Stocks",
    "Fundamental Analysis",
    "Price History",
    "Company Comparison",
    "Stock Screener",
    "AI Research Reports",
    "My Watchlist",
    "Portfolio",
    "Alerts",
]

SECTION_ICONS = {
    "Market Overview": "📊",
    "Search Indian Stocks": "🔍",
    "Fundamental Analysis": "📑",
    "Price History": "📈",
    "Company Comparison": "⚖️",
    "Stock Screener": "🧹",
    "AI Research Reports": "🤖",
    "My Watchlist": "⭐",
    "Portfolio": "💼",
    "Alerts": "🔔",
}

# --- Top navigation header ---
header_cols = st.columns([2, 3, 7])
with header_cols[0]:
    st.markdown("## 📈 AI Share Market")
    st.caption("Research Agent — v1.0")
with header_cols[1]:
    global_search = st.text_input("🔍 Search stocks", placeholder="RELIANCE, TCS, INFY...", label_visibility="collapsed", key="global_search")
with header_cols[2]:
    nav = st.radio(
        "Navigation",
        ["Dashboard", "Stock Analysis", "Compare Stocks", "Stock Screener", "AI Research", "Watchlist", "Portfolio", "Alerts", "About"],
        horizontal=True,
        label_visibility="collapsed",
    )

if global_search:
    res = search_companies(global_search)
    if res:
        st.info(f"Search results for '{global_search}': " + ", ".join(c.symbol for c in res[:8]))
    else:
        st.warning(f"No companies found for '{global_search}'.")

st.markdown("---")

with st.sidebar:
    st.markdown("### Application")
    st.caption(f"Environment: **{settings.APP_ENV}**")
    st.caption("Version: v1.0.0")
    with st.expander("Health Check", expanded=False):
        health = health_status()
        st.json(health)
        for p in market_data_service.provider_status():
            st.write(f"- {p['name']}: {'✅' if p['available'] else '⚠️'}")

page_header(
    "AI Share Market Research Agent",
    "Indian Stock Market Research Platform — v1.0",
)

with st.expander("Application Health Check", expanded=False):
    health = health_status()
    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Status", health["status"].upper(), sample=False)
    with c2:
        metric_card("Environment", health["environment"], sample=False)
    with c3:
        metric_card("Python", health["python_version"], sample=False)
    st.json(health)
    st.markdown("**Market Data Providers**")
    for p in market_data_service.provider_status():
        st.write(f"- {p['name']}: {'✅ available' if p['available'] else '⚠️ unavailable'}")


def render_market_overview() -> None:
    page_header("Market Overview", "High-level snapshot of Indian market indices (sample).")
    alert("Placeholder data — live market feeds will be connected in upcoming days.", "info")

    cols = st.columns(4)
    with cols[0]:
        metric_card("NIFTY 50", "22,450.30", "+0.42%", sample=True, delta_positive=True)
    with cols[1]:
        metric_card("SENSEX", "73,920.15", "+0.38%", sample=True, delta_positive=True)
    with cols[2]:
        metric_card("NIFTY Bank", "47,810.50", "-0.15%", sample=True, delta_positive=False)
    with cols[3]:
        metric_card("India VIX", "14.20", "-2.10%", sample=True, delta_positive=False)

    section_header("Top Gainers (sample)")
    st.table(
        {
            "Symbol": ["RELIANCE", "TCS", "INFY"],
            "Price (INR)": [2850.40, 3920.10, 1540.75],
            "Change %": ["+1.2%", "+0.9%", "+0.7%"],
        }
    )
    section_header("Top Losers (sample)")
    st.table(
        {
            "Symbol": ["HDFCBANK", "ICICIBANK", "SBIN"],
            "Price (INR)": [1620.30, 1085.60, 780.20],
            "Change %": ["-0.8%", "-0.6%", "-0.5%"],
        }
    )
    sample_note()


def render_search() -> None:
    page_header("Search Indian Stocks", "Find a company by symbol or name.")
    query = st.text_input("Enter stock symbol or company name", placeholder="e.g. RELIANCE, TCS, INFY")

    results = search_companies(query)
    if query and not results:
        empty_state(f"No companies found for '{query}'.")
        return

    if results:
        st.caption(f"Showing {len(results)} result(s) from local company master (sample seed).")
        st.table(
            {
                "Symbol": [c.symbol for c in results],
                "Company": [c.name for c in results],
                "Sector": [c.sector for c in results],
                "Industry": [c.industry for c in results],
                "Exchange": [c.exchange for c in results],
            }
        )

        symbols = [c.symbol for c in results]
        selected = st.selectbox("Select a company to view profile", symbols)
        company = get_company(selected)
        if company:
            profile_card(company.to_dict())
        sample_note("Company master is a sample seed list. Real NSE/BSE data integration pending (Day 4).")
    else:
        empty_state("Type a symbol or company name above to search.")


def render_fundamental() -> None:
    page_header("Fundamental Analysis", "View key fundamentals for a selected stock.")
    symbols = [c.symbol for c in search_companies("")]
    symbol = st.selectbox("Select stock", symbols, index=0)
    company = get_company(symbol)
    if company:
        profile_card(company.to_dict())
    alert(f"Showing placeholder fundamentals for {symbol}. Real data integration pending.", "info")

    if st.button("Fetch live quote (optional, requires network)"):
        with st.spinner("Fetching live quote..."):
            quote = market_data_service.get_quote(symbol)
        if quote:
            st.json(quote)
            sample_note("Live quote sourced from yfinance (optional). May be unavailable or delayed.")
        else:
            alert("Live quote unavailable. Provider may be offline or symbol not found.", "warning")
    loading_state("Fetching fundamentals (placeholder)")
    st.table(
        {
            "Metric": ["Market Cap", "P/E Ratio", "EPS", "Dividend Yield", "ROE", "Debt/Equity"],
            "Value": ["Rs. 19.2 L Cr", "28.5", "Rs. 98.4", "0.35%", "12.1%", "0.42"],
        }
    )

    section_header("Income Statement (live via yfinance)")
    quarterly = st.checkbox("Quarterly", value=False, key="fund_quarterly")
    if st.button("Fetch Income Statement", key="fetch_income"):
        with st.spinner("Fetching income statement..."):
            inc = fetch_income_statement(symbol, quarterly=quarterly)
        if inc is not None and not inc.empty:
            st.session_state["income_df"] = inc
            st.session_state["income_symbol"] = symbol
        else:
            st.session_state.pop("income_df", None)
            alert("Income statement unavailable for this symbol.", "warning")

    inc = st.session_state.get("income_df")
    if inc is not None and not inc.empty:
        disp = inc.copy()
        for col in ("revenue", "operating_profit", "ebitda", "net_profit"):
            if col in disp.columns:
                disp[col] = disp[col].apply(lambda x: f"{x:,.0f}" if pd.notna(x) else "N/A")
        st.table(disp[["period", "revenue", "operating_profit", "ebitda", "net_profit", "eps"]])

        inc_chart = inc.dropna(subset=["revenue"]).copy()
        inc2 = add_growth_and_margins(inc_chart)
        section_header("Revenue & Net Profit Trend")
        chart_df = inc2.set_index("period")[["revenue", "net_profit"]]
        st.line_chart(chart_df)

        section_header("Margins Trend")
        margin_df = inc2.set_index("period")[["operating_margin_pct", "ebitda_margin_pct", "net_margin_pct"]]
        st.line_chart(margin_df)

        valid = inc.dropna(subset=["revenue"])
        if len(valid) >= 2:
            years = (valid["period_end"].iloc[-1] - valid["period_end"].iloc[0]).days / 365.25
            if years >= 1:
                rev_cagr = calculate_cagr(float(valid["revenue"].iloc[0]), float(valid["revenue"].iloc[-1]), max(1, int(round(years))))
                if rev_cagr is not None and not pd.isna(rev_cagr):
                    st.caption(f"Revenue CAGR over span: {rev_cagr:.2f}%")
        sample_note("Financial statements sourced from yfinance (unofficial). Currency/units as reported.")
    else:
        empty_state("Click 'Fetch Income Statement' to load live data.")

    section_header("Balance Sheet (live via yfinance)")
    if st.button("Fetch Balance Sheet", key="fetch_bs"):
        with st.spinner("Fetching balance sheet..."):
            bs = fetch_balance_sheet(symbol, quarterly=False)
        if bs is not None and not bs.empty:
            st.session_state["bs_df"] = bs
        else:
            st.session_state.pop("bs_df", None)
            alert("Balance sheet unavailable for this symbol.", "warning")

    bs = st.session_state.get("bs_df")
    if bs is not None and not bs.empty:
        bs2 = add_balance_sheet_metrics(bs)
        disp = bs2.copy()
        for col in ("total_assets", "total_liabilities", "stockholders_equity", "total_debt", "cash_and_equivalents", "current_assets", "current_liabilities"):
            if col in disp.columns:
                disp[col] = disp[col].apply(lambda x: f"{x:,.0f}" if pd.notna(x) else "N/A")
        st.table(disp[["period", "total_assets", "total_liabilities", "stockholders_equity", "total_debt", "cash_and_equivalents", "current_assets", "current_liabilities"]])

        section_header("Balance Sheet Metrics")
        latest = bs2.iloc[-1]
        c1, c2, c3 = st.columns(3)
        with c1:
            de = latest.get("debt_to_equity")
            st.metric("Debt/Equity", f"{de:.2f}" if pd.notna(de) else "N/A")
        with c2:
            cr = latest.get("current_ratio")
            st.metric("Current Ratio", f"{cr:.2f}" if pd.notna(cr) else "N/A")
        with c3:
            wc = latest.get("working_capital")
            st.metric("Working Capital", f"{wc:,.0f}" if pd.notna(wc) else "N/A")
        sample_note("Balance sheet sourced from yfinance (unofficial).")
    else:
        empty_state("Click 'Fetch Balance Sheet' to load live data.")

    section_header("Cash Flow (live via yfinance)")
    if st.button("Fetch Cash Flow", key="fetch_cf"):
        with st.spinner("Fetching cash flow..."):
            cf = fetch_cash_flow(symbol, quarterly=False)
        if cf is not None and not cf.empty:
            st.session_state["cf_df"] = cf
        else:
            st.session_state.pop("cf_df", None)
            alert("Cash flow unavailable for this symbol.", "warning")

    cf = st.session_state.get("cf_df")
    if cf is not None and not cf.empty:
        disp = cf.copy()
        for col in ("operating_cf", "investing_cf", "financing_cf", "capital_expenditure", "free_cash_flow"):
            if col in disp.columns:
                disp[col] = disp[col].apply(lambda x: f"{x:,.0f}" if pd.notna(x) else "N/A")
        st.table(disp[["period", "operating_cf", "investing_cf", "financing_cf", "capital_expenditure", "free_cash_flow"]])

        section_header("Cash Flow Trend")
        trend = cf.set_index("period")[["operating_cf", "free_cash_flow"]]
        st.line_chart(trend)
        sample_note("Cash flow sourced from yfinance (unofficial).")
    else:
        empty_state("Click 'Fetch Cash Flow' to load live data.")

    section_header("Fundamental Ratios (computed)")
    if st.button("Compute Ratios", key="compute_ratios"):
        with st.spinner("Computing ratios..."):
            inc = fetch_income_statement(symbol, quarterly=False)
            bs = fetch_balance_sheet(symbol, quarterly=False)
            cf = fetch_cash_flow(symbol, quarterly=False)
            ratios = compute_ratios(inc, bs, cf)
        if ratios is not None and not ratios.empty:
            st.session_state["ratios_df"] = ratios
        else:
            st.session_state.pop("ratios_df", None)
            alert("Ratios unavailable (missing financial data).", "warning")

    ratios = st.session_state.get("ratios_df")
    if ratios is not None and not ratios.empty:
        show_cols = ["period", "revenue_growth_pct", "net_profit_growth_pct",
                     "operating_margin_pct", "ebitda_margin_pct", "net_margin_pct",
                     "roe_pct", "roce_pct", "roa_pct", "debt_to_equity",
                     "interest_coverage", "current_ratio", "cash_conversion", "fcf_margin_pct"]
        show_cols = [c for c in show_cols if c in ratios.columns]
        disp = ratios[show_cols].copy()
        for c in show_cols:
            if c != "period":
                disp[c] = disp[c].apply(lambda x: f"{x:,.2f}" if pd.notna(x) else "N/A")
        st.table(disp)

        section_header("ROE / ROCE / ROA Trend")
        trend = ratios.set_index("period")[["roe_pct", "roce_pct", "roa_pct"]]
        st.line_chart(trend)

        section_header("Margin Trend")
        m = ratios.set_index("period")[["operating_margin_pct", "ebitda_margin_pct", "net_margin_pct"]]
        st.line_chart(m)
        sample_note("Ratios computed from yfinance financial statements (unofficial).")
    else:
        empty_state("Click 'Compute Ratios' to calculate.")

    section_header("Valuation (P/E, P/B, PEG, Dividend Yield)")
    if st.button("Compute Valuation", key="compute_valuation"):
        with st.spinner("Computing valuation..."):
            val = get_valuation_inputs(symbol)
        if val:
            st.session_state["valuation"] = val
        else:
            st.session_state.pop("valuation", None)
            alert("Valuation unavailable.", "warning")

    val = st.session_state.get("valuation")
    if val:
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("P/E", f"{val['pe']:.2f}" if val.get("pe") is not None else "N/A")
        with c2:
            st.metric("P/B", f"{val['pb']:.2f}" if val.get("pb") is not None else "N/A")
        with c3:
            st.metric("PEG", f"{val['peg']:.2f}" if val.get("peg") is not None else "N/A")
        with c4:
            st.metric("Dividend Yield", f"{val['dividend_yield_pct']:.2f}%" if val.get("dividend_yield_pct") is not None else "N/A")

        st.caption(f"Price: {val.get('price')} | EPS: {val.get('eps')} | Book Value/Share: {val.get('book_value_per_share')} | Growth: {val.get('growth_rate_pct')}")
        if val.get("yfinance_pe") is not None:
            st.caption(f"Cross-check (yfinance): P/E {val['yfinance_pe']}, P/B {val['yfinance_pb']}, PEG {val['yfinance_peg']}, Div Yield {val['yfinance_dividend_yield_pct']}")
        sample_note("Valuation computed from live price + financial statements (unofficial).")
    else:
        empty_state("Click 'Compute Valuation' to calculate.")

    section_header("Fundamental Score (research aid, not a signal)")
    if st.button("Compute Score", key="compute_score"):
        with st.spinner("Computing score..."):
            inc = fetch_income_statement(symbol, quarterly=False)
            bs = fetch_balance_sheet(symbol, quarterly=False)
            cf = fetch_cash_flow(symbol, quarterly=False)
            ratios = compute_ratios(inc, bs, cf)
            val = get_valuation_inputs(symbol)
            if ratios is not None and not ratios.empty:
                latest = ratios.iloc[-1].to_dict()
                score = compute_fundamental_score(latest, val)
                st.session_state["score"] = score
            else:
                st.session_state.pop("score", None)
                alert("Score unavailable (missing financial data).", "warning")

    score = st.session_state.get("score")
    if score:
        st.metric("Fundamental Score", f"{score['total']} / 100", delta=score["grade"])
        sub = pd.DataFrame(list(score["sub_scores"].items()), columns=["Component", "Score"])
        st.bar_chart(sub.set_index("Component"))
        st.caption("Weights: " + ", ".join(f"{k} {int(v*100)}%" for k, v in score["weights"].items()))
        sample_note("Score is a heuristic research aid, not a buy/sell signal.")
    else:
        empty_state("Click 'Compute Score' to calculate.")

    section_header("Quarterly Results Analysis")
    if st.button("Fetch Quarterly Results", key="fetch_q"):
        with st.spinner("Fetching quarterly results..."):
            qdf = fetch_income_statement(symbol, quarterly=True)
        if qdf is not None and not qdf.empty:
            st.session_state["q_df"] = qdf
        else:
            st.session_state.pop("q_df", None)
            alert("Quarterly results unavailable.", "warning")

    qdf = st.session_state.get("q_df")
    if qdf is not None and not qdf.empty:
        q2 = add_quarterly_growth(qdf)
        disp = q2.copy()
        for col in ("revenue", "net_profit"):
            if col in disp.columns:
                disp[col] = disp[col].apply(lambda x: f"{x:,.0f}" if pd.notna(x) else "N/A")
        st.table(disp[["period", "revenue", "net_profit", "revenue_qoq_pct", "revenue_yoy_pct", "net_profit_qoq_pct", "net_profit_yoy_pct"]])

        section_header("Quarterly Revenue Trend")
        st.line_chart(q2.set_index("period")[["revenue"]])
        section_header("Quarterly Margins")
        st.line_chart(q2.set_index("period")[["operating_margin_pct", "net_margin_pct"]])
        sample_note("Quarterly results sourced from yfinance (unofficial).")
    else:
        empty_state("Click 'Fetch Quarterly Results' to load data.")

    sample_note()


def render_price_history() -> None:
    page_header("Price History", "Advanced interactive charting with technical indicators.")
    symbols = [c.symbol for c in search_companies("")]
    symbol = st.selectbox("Select stock", symbols, index=0, key="ph_symbol")

    col1, col2, col3 = st.columns(3)
    with col1:
        period_label = st.selectbox("Period", ["1D", "1W", "1M", "3M", "6M", "1Y", "2Y", "3Y", "5Y", "MAX"], index=5)
    with col2:
        chart_type = st.selectbox("Chart Type", ["Candlestick", "Line", "Area"], index=0)
    with col3:
        benchmark = st.checkbox("Compare with Nifty 50")

    indicators = st.multiselect(
        "Indicators",
        ["SMA 20", "SMA 50", "SMA 100", "SMA 200", "EMA 20", "RSI 14", "MACD", "Bollinger Bands"],
        default=[],
    )
    show_volume = st.checkbox("Show Volume", value=True)

    period_map = {
        "1D": "1d", "1W": "5d", "1M": "1mo", "3M": "3mo", "6M": "6mo",
        "1Y": "1y", "2Y": "2y", "3Y": "5y", "5Y": "5y", "MAX": "max",
    }
    period = period_map[period_label]

    if st.button("Load Price History", key="load_ph"):
        with st.spinner("Fetching price history..."):
            df = market_data_service.get_price_history(symbol, period=period, interval="1d")
            bench_df = None
            if benchmark:
                bench_df = market_data_service.get_price_history("^NSEI", period=period, interval="1d")
        if df is not None and not df.empty:
            df = df.dropna(subset=["close"]) if "close" in df.columns else df
            df = apply_indicators(df, indicators)
            st.session_state["price_df"] = df
            st.session_state["price_symbol"] = symbol
            st.session_state["bench_df"] = bench_df
            st.session_state["chart_type"] = chart_type
            st.session_state["indicators"] = indicators
            st.session_state["show_volume"] = show_volume
        else:
            st.session_state.pop("price_df", None)
            alert("Price history unavailable. Provider may be offline or symbol not found.", "warning")

    df = st.session_state.get("price_df")
    if df is not None and not df.empty:
        summary = price_summary(df)
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            metric_card("Last Close", f"{summary.get('last_close', 0):,.2f}", sample=True)
        with m2:
            pct = summary.get("change_pct", 0)
            metric_card("Change %", f"{pct:+.2f}%", sample=True, delta_positive=pct >= 0)
        with m3:
            metric_card("Period High", f"{summary.get('high', 0):,.2f}", sample=True)
        with m4:
            metric_card("Period Low", f"{summary.get('low', 0):,.2f}", sample=True)

        ct = st.session_state.get("chart_type", chart_type)
        inds = st.session_state.get("indicators", indicators)
        sv = st.session_state.get("show_volume", show_volume)
        bench_df = st.session_state.get("bench_df")
        fig = advanced_price_chart(df, chart_type=ct, indicators=inds, benchmark_df=bench_df,
                                   title=f"{st.session_state.get('price_symbol', symbol)} — {period_label}")
        if fig is not None:
            st.plotly_chart(fig, use_container_width=True)

        # RSI / MACD sub-charts
        if "RSI 14" in inds:
            rsi_df = apply_indicators(df.copy(), ["RSI 14"])
            rfig = rsi_chart(rsi_df)
            if rfig is not None:
                st.plotly_chart(rfig, use_container_width=True)
        if "MACD" in inds:
            macd_df = apply_indicators(df.copy(), ["MACD"])
            mfig = macd_chart(macd_df)
            if mfig is not None:
                st.plotly_chart(mfig, use_container_width=True)

        sample_note("Prices sourced from yfinance (optional, unofficial). All values are live-fetched, not verified exchange data. Delayed data, not real-time.")
    else:
        empty_state("Select options and click 'Load Price History'.")


def render_comparison() -> None:
    page_header("Company Comparison", "Side-by-side fundamental comparison (live).")
    symbols = [c.symbol for c in search_companies("")]
    selected = st.multiselect("Select 2-3 companies", symbols, default=["RELIANCE", "TCS"], max_selections=3)
    if len(selected) < 2:
        empty_state("Select at least two companies to compare.")
        return
    if st.button("Compare", key="compare_btn"):
        with st.spinner("Building comparison..."):
            comp = build_comparison(selected)
        if comp is not None and not comp.empty:
            st.session_state["comparison_df"] = comp
        else:
            st.session_state.pop("comparison_df", None)
            alert("Comparison unavailable.", "warning")

    comp = st.session_state.get("comparison_df")
    if comp is not None and not comp.empty:
        disp = comp.copy()
        for col in selected:
            disp[col] = disp[col].apply(lambda x: f"{x:,.2f}" if isinstance(x, (int, float)) and pd.notna(x) else ("N/A" if (isinstance(x, float) and pd.isna(x)) else x))
        st.table(disp)

        if "Fundamental Score" in comp["Metric"].values:
            score_row = comp[comp["Metric"] == "Fundamental Score"]
            if not score_row.empty:
                st.bar_chart(score_row.set_index("Metric")[selected])

        section_header("Revenue Comparison")
        rev_row = comp[comp["Metric"] == "Revenue"]
        if not rev_row.empty:
            st.bar_chart(rev_row.set_index("Metric")[selected])

        sample_note("Comparison built from yfinance financial statements (unofficial).")
    else:
        empty_state("Select companies and click Compare.")


def render_screener() -> None:
    page_header("Stock Screener", "Filter the Indian stock universe by fundamentals (live).")
    sectors = sorted(set(c.sector for c in search_companies("")))
    col1, col2, col3 = st.columns(3)
    with col1:
        sector = st.selectbox("Sector", ["All"] + sectors)
    with col2:
        min_pe = st.number_input("Min P/E", value=0.0, step=1.0)
    with col3:
        max_pe = st.number_input("Max P/E", value=60.0, step=1.0)

    col4, col5, col6 = st.columns(3)
    with col4:
        min_roe = st.number_input("Min ROE %", value=0.0, step=1.0)
    with col5:
        min_score = st.number_input("Min Fundamental Score", value=0.0, step=5.0)
    with col6:
        max_de = st.number_input("Max Debt/Equity", value=5.0, step=0.5)

    c1, c2 = st.columns(2)
    with c1:
        run = st.button("Run Screen")
    with c2:
        refresh = st.button("Refresh Universe")

    if refresh:
        clear_cache()
        st.session_state.pop("screener_df", None)

    if run:
        with st.spinner("Building screener universe (may take a while)..."):
            universe = build_universe(force_refresh=refresh)
        if universe is not None and not universe.empty:
            df = universe.copy()
            if sector != "All":
                df = df[df["Sector"] == sector]
            if "P/E" in df.columns:
                df = df[(df["P/E"].isna()) | ((df["P/E"] >= min_pe) & (df["P/E"] <= max_pe))]
            if "ROE %" in df.columns:
                df = df[(df["ROE %"].isna()) | (df["ROE %"] >= min_roe)]
            if "Score" in df.columns:
                df = df[(df["Score"].isna()) | (df["Score"] >= min_score)]
            if "Debt/Equity" in df.columns:
                df = df[(df["Debt/Equity"].isna()) | (df["Debt/Equity"] <= max_de)]
            st.session_state["screener_df"] = df
        else:
            st.session_state.pop("screener_df", None)
            alert("Screener universe unavailable.", "warning")

    res = st.session_state.get("screener_df")
    if res is not None and not res.empty:
        st.caption(f"{len(res)} result(s)")
        st.dataframe(res, use_container_width=True)
        sample_note("Screener built from yfinance financial statements (unofficial).")
    elif res is not None:
        empty_state("No stocks match the filters.")
    else:
        empty_state("Set filters and click 'Run Screen'.")


def render_ai_reports() -> None:
    page_header("AI Research Reports", "AI-assisted research grounded in verified data.")
    symbols = [c.symbol for c in search_companies("")]
    symbol = st.selectbox("Select stock", symbols, index=0, key="ai_symbol")

    section_header("Ask a Research Question")
    question = st.text_input("Question", placeholder="e.g. How is profitability trending?")
    if st.button("Ask", key="ask_ai") and question:
        with st.spinner("Researching..."):
            answer = answer_question(symbol, question)
        st.markdown(answer)
        sample_note("Answer uses verified financial data; LLM optional. Not investment advice.")

    section_header("Generate Research Report")
    if st.button("Generate Report", key="gen_report"):
        with st.spinner("Generating report..."):
            report, path = generate_report(symbol)
        st.markdown(report)
        st.download_button("Download Report (Markdown)", data=report, file_name=path.name, mime="text/markdown")
        st.caption(f"Saved to {path}")
        sample_note("Report generated from verified data. Not investment advice.")

    if not question:
        empty_state("Enter a question or generate a report.")


def render_watchlist() -> None:
    page_header("My Watchlist", "Persisted watchlist (SQLite).")
    new_item = st.text_input("Add symbol", placeholder="e.g. INFY", key="wl_add")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Add", key="wl_add_btn") and new_item:
            if add_to_watchlist(new_item):
                st.success(f"Added {new_item.upper()}")
            else:
                alert(f"{new_item.upper()} already in watchlist or invalid.", "warning")
    with c2:
        items = list_watchlist()
        to_remove = st.selectbox("Remove symbol", ["(none)"] + items, key="wl_remove")
        if st.button("Remove", key="wl_remove_btn") and to_remove != "(none)":
            if remove_from_watchlist(to_remove):
                st.success(f"Removed {to_remove}")

    section_header("Current Watchlist")
    items = list_watchlist()
    if items:
        rows = []
        for sym in items:
            q = market_data_service.get_quote(sym)
            rows.append({"Symbol": sym, "Live Price": q.get("price") if q else "N/A"})
        st.table(pd.DataFrame(rows))
    else:
        empty_state("Your watchlist is empty.")
    sample_note("Watchlist persisted in local SQLite (database/app.db).")


def render_portfolio() -> None:
    page_header("Portfolio", "Track holdings and P&L (persisted in SQLite).")
    symbols = [c.symbol for c in search_companies("")]
    with st.form("add_holding_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            sym = st.selectbox("Symbol", symbols)
        with col2:
            qty = st.number_input("Quantity", min_value=0.0, step=1.0)
        with col3:
            price = st.number_input("Buy Price (INR)", min_value=0.0, step=1.0)
        buy_date = st.text_input("Buy Date (YYYY-MM-DD)", placeholder="2025-01-01")
        notes = st.text_input("Notes", placeholder="optional")
        submitted = st.form_submit_button("Add Holding")
    if submitted:
        if add_holding(sym, qty, price, buy_date or None, notes or None):
            st.success(f"Added {qty} x {sym}")
        else:
            alert("Invalid holding (quantity/price must be > 0).", "warning")

    section_header("Holdings")
    holdings = list_holdings()
    if holdings:
        rows = []
        total_value = 0.0
        total_cost = 0.0
        for h in holdings:
            q = market_data_service.get_quote(h["symbol"])
            live = q.get("price") if q else None
            cost = h["quantity"] * h["buy_price"]
            value = h["quantity"] * live if live is not None else None
            pnl = (value - cost) if value is not None else None
            pnl_pct = (pnl / cost * 100) if (pnl is not None and cost) else None
            total_cost += cost
            if value is not None:
                total_value += value
            rows.append(
                {
                    "ID": h["id"],
                    "Symbol": h["symbol"],
                    "Qty": h["quantity"],
                    "Buy Price": h["buy_price"],
                    "Live Price": live if live is not None else "N/A",
                    "Cost": round(cost, 2),
                    "Value": round(value, 2) if value is not None else "N/A",
                    "P&L": round(pnl, 2) if pnl is not None else "N/A",
                    "P&L %": round(pnl_pct, 2) if pnl_pct is not None else "N/A",
                }
            )
        st.table(pd.DataFrame(rows))
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Total Cost", f"{total_cost:,.2f}")
        with c2:
            st.metric("Total Value", f"{total_value:,.2f}" if total_value else "N/A")
        with c3:
            pnl_total = total_value - total_cost if total_value else None
            st.metric("Total P&L", f"{pnl_total:,.2f}" if pnl_total is not None else "N/A")

        to_remove = st.selectbox("Remove holding by ID", [h["id"] for h in holdings], key="rm_hold")
        if st.button("Remove Holding", key="rm_hold_btn"):
            if remove_holding(int(to_remove)):
                st.success(f"Removed holding {to_remove}")
    else:
        empty_state("No holdings yet. Add one above.")
    sample_note("Prices from yfinance (optional, unofficial). Not investment advice.")


def render_alerts() -> None:
    page_header("Alerts & Monitoring", "Define thresholds and evaluate alerts.")
    symbols = [c.symbol for c in search_companies("")]
    metrics = ["Price", "Revenue Growth %", "Net Margin %", "ROE %", "ROCE %", "Debt/Equity", "P/E", "Fundamental Score"]
    operators = [">", "<", ">=", "<="]

    with st.form("add_alert_form"):
        col1, col2 = st.columns(2)
        with col1:
            sym = st.selectbox("Symbol", symbols)
            metric = st.selectbox("Metric", metrics)
        with col2:
            op = st.selectbox("Operator", operators)
            thr = st.number_input("Threshold", value=0.0, step=1.0)
        submitted = st.form_submit_button("Add Alert")
    if submitted:
        if add_alert(sym, metric, op, thr):
            st.success("Alert added")
        else:
            alert("Failed to add alert.", "warning")

    section_header("Configured Alerts")
    alerts = list_alerts()
    if alerts:
        st.table(pd.DataFrame(alerts))
        to_delete = st.selectbox("Delete alert by ID", [a["id"] for a in alerts], key="del_alert")
        if st.button("Delete Alert", key="del_alert_btn"):
            if delete_alert(int(to_delete)):
                st.success(f"Deleted alert {to_delete}")
    else:
        empty_state("No alerts configured.")

    section_header("Evaluate Alerts")
    if st.button("Evaluate Now", key="eval_alerts"):
        with st.spinner("Evaluating alerts (may take a while)..."):
            triggered = evaluate_alerts()
        st.session_state["triggered_alerts"] = triggered

    triggered = st.session_state.get("triggered_alerts")
    if triggered:
        st.warning(f"{len(triggered)} alert(s) triggered:")
        st.table(pd.DataFrame(triggered))
    elif triggered == []:
        st.success("No alerts triggered.")
    sample_note("Alerts evaluated against live yfinance data (unofficial). No auto-trading.")


if nav == "Dashboard":
    render_market_overview()
    section_header("Stock Search")
    render_search()
    section_header("Stock Search")
    render_search()

elif nav == "Stock Analysis":
    symbols = [c.symbol for c in search_companies("")]
    default_sym = st.session_state.get("analysis_symbol", symbols[0] if symbols else "")
    idx = symbols.index(default_sym) if default_sym in symbols else 0
    symbol = st.selectbox("Select Stock", symbols, index=idx, key="analysis_symbol_select")
    st.session_state["analysis_symbol"] = symbol

    tabs = st.tabs([
        "Overview", "Fundamentals", "Financials", "Price History", "Valuation",
        "Peers", "Shareholding", "Dividends & Events", "News", "AI Research"
    ])

    with tabs[0]:
        page_header(f"{symbol} — Overview", "Company profile and key metrics.")
        company = get_company(symbol)
        if company:
            profile_card(company.to_dict())
        # live quote overview
        q = market_data_service.get_quote(symbol)
        if q and q.get("price") is not None:
            st.metric("Live Price", q.get("price"))
        else:
            st.info("Live price unavailable.")
        sample_note("Profile from sample seed; price from yfinance (unofficial).")

    with tabs[1]:
        render_fundamental()

    with tabs[2]:
        page_header("Financials", "Income, balance sheet, cash flow, quarterly.")
        # reuse fundamental financial sections by calling a lightweight version:
        st.info("Use the Fundamental Analysis tab for full financial statements.")

    with tabs[3]:
        render_price_history()

    with tabs[4]:
        page_header("Valuation", "P/E, P/B, PEG, dividend yield.")
        st.info("Use Fundamental Analysis → Valuation section.")

    with tabs[5]:
        page_header("Peers", "Compare with industry peers.")
        render_comparison()

    with tabs[6]:
        page_header("Shareholding", "Shareholding pattern.")
        empty_state("Shareholding data not yet integrated. Coming in Phase 5.")

    with tabs[7]:
        page_header("Dividends & Events", "Dividend history and corporate actions.")
        empty_state("Dividend history and corporate actions coming in Phase 5.")

    with tabs[8]:
        page_header("News", "Company news and announcements.")
        empty_state("News integration coming in Phase 5.")

    with tabs[9]:
        render_ai_reports()

elif nav == "Compare Stocks":
    render_comparison()

elif nav == "Stock Screener":
    render_screener()

elif nav == "AI Research":
    render_ai_reports()

elif nav == "Watchlist":
    render_watchlist()

elif nav == "Portfolio":
    render_portfolio()

elif nav == "Alerts":
    render_alerts()

elif nav == "About":
    page_header("About", "AI Share Market Research Platform")
    st.markdown(
        "A research and educational tool for Indian (NSE/BSE) stocks. "
        "Not investment advice. Data sourced from yfinance (unofficial) and local sample seed."
    )
