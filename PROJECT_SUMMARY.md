# PROJECT SUMMARY
## AI Share Market Research Agent

> A comprehensive reference document for the project. Read this (along with README.md) before every development session.

---

## 1. Why This Project Is Being Developed

Indian retail investors lack a single, structured, free research workspace for NSE/BSE companies. Financial data is scattered across exchanges, annual reports and third-party portals with inconsistent formats. This project builds an AI-assisted research platform that organises financial information, computes standard ratios, visualises trends and generates research summaries — all from verified data.

## 2. What Problem It Solves

- Scattered and inconsistent financial data
- High manual effort in multi-year statement analysis
- Difficulty interpreting ratios and valuation
- Lack of structured company comparison
- No free, integrated research workspace with AI assistance
- Risk of misinterpretation and fabricated figures

## 3. Who Will Use It

- Retail and long-term investors
- Fundamental analysts and learners
- Financial data analysts
- Students and educators

Not for intraday traders, algorithmic traders or automated execution.

## 4. What the Final Application Should Look Like

A premium financial research terminal (dark theme) with:

- Clean sidebar navigation across modules (Market Overview, Search, Profile, Financials, Ratios, Valuation, Scoring, Comparison, Screener, AI Research, Reports, Portfolio, Watchlist, Alerts)
- Dashboard cards for indices and key metrics
- Interactive Plotly charts (candlestick, volume, trends, comparisons)
- High-quality tables with sorting/filtering
- Loading and error states
- Responsive layout

Color system: background `#0B1220`, cards `#172033`, accent `#14B8A6`, positive `#22C55E`, negative `#EF4444`.

## 5. How the Complete Application Will Work

1. User searches for a company (NSE/BSE symbol or name).
2. App fetches company profile and financial data from available sources (with fallbacks).
3. Data is normalised, stored with provenance metadata.
4. Deterministic formulas compute ratios, growth, valuation and scores.
5. UI renders tables and interactive charts.
6. AI layer retrieves verified data and generates explanations/reports with citations.
7. User can compare companies, screen stocks, manage portfolio/watchlist and set alerts.

All AI outputs are grounded in verified data and clearly labelled as interpretation.

## 6. What Data It Needs

- Historical market prices (OHLCV, indices)
- Company profiles (sector, industry, description)
- Financial statements (income, balance sheet, cash flow) — consolidated/standalone
- Quarterly results
- Corporate actions (dividends, splits)
- Shareholding patterns
- Sector/industry peer data

## 7. Where Data Will Come From

- NSE India and BSE India (primary, official)
- yfinance (convenience, unofficial)
- Screener.in (financials, with ToS respect)
- Company annual reports and investor relations (authoritative fundamentals)
- Exchange corporate announcements
- Other legitimate providers with free tiers

Fallback: if all sources fail, mark data unavailable — never fabricate.

## 8. How Financial Calculations Will Work

Deterministic formulas (see README Section 7) applied to verified inputs:

- Growth: Revenue/Profit YoY, CAGR
- Margins: EBITDA, Operating, Net
- Returns: ROE, ROCE, ROA
- Leverage/Liquidity: D/E, Interest Coverage, Current Ratio
- Cash Flow: OCF, FCF, Cash Conversion
- Valuation: EPS, P/E, P/B, PEG, Dividend Yield

Missing inputs → N/A. Consolidated preferred over standalone when available, clearly labelled.

## 9. How AI Will Analyse the Information

- Retrieve relevant structured data from the data layer
- Prompt LLM with context, citations and strict instructions
- Generate explanations, summaries, comparisons, risk identification, reports
- Validate numeric claims against source data where feasible
- Label all AI content as interpretation; cite source + period
- Never invent numbers; say "data unavailable" when missing
- Optional LangGraph for multi-step research workflows

## 10. How Users Will Interact with the Application

- Streamlit web UI (browser-based)
- Sidebar navigation between modules
- Search box for stocks
- Selectors, filters, date ranges, interval switches
- Forms for portfolio/watchlist/alerts
- Natural-language questions to AI agent
- Export reports (Markdown/PDF)

## 11. Complete 20-Day Development Roadmap

(See README Section 12 for full deliverables and acceptance criteria.)

| Day | Focus |
|---|---|
| 1 | Project architecture, folder structure, Python environment |
| 2 | Streamlit dashboard and professional UI |
| 3 | NSE/BSE stock search and company profiles |
| 4 | Stock market API integration |
| 5 | Historical price data and charts |
| 6 | Revenue, profit and growth analysis |
| 7 | Balance sheet and cash flow analysis |
| 8 | ROE, ROCE, margins, debt ratios |
| 9 | P/E, P/B and valuation analysis |
| 10 | Fundamental scoring engine |
| 11 | Company comparison engine |
| 12 | Stock screener |
| 13 | AI research agent |
| 14 | Quarterly results analysis |
| 15 | AI research report generation |
| 16 | Portfolio and watchlist |
| 17 | Alerts and monitoring |
| 18 | Database optimization and caching |
| 19 | Testing, error handling and validation |
| 20 | Final UI, documentation and GitHub deployment |

## 12. Expected Final Deliverables

- Working Streamlit application with all modules
- Modular Python codebase with tests
- SQLite (upgradable to PostgreSQL) database
- Data access layer with fallbacks
- Financial ratio and scoring engines
- AI research agent and report generator
- Portfolio, watchlist and alerts
- Documentation (README, architecture, API notes)
- GitHub repository with deployment guide

## 13. Main Technical Challenges

- Unofficial/unstable data sources (NSE/BSE endpoints, yfinance)
- Data normalisation across sources and units
- Consolidated vs standalone handling
- Missing/incomplete data and restatements
- LLM hallucination prevention
- Performance with large datasets and charts
- Keeping app working throughout incremental development

## 14. How Data Accuracy Will Be Maintained

- Store source, period, currency, unit, publication date, last-updated for every record
- Prefer official/audited sources (exchanges, annual reports)
- Upsert keyed on (symbol, period, source) to prevent duplicates
- Data quality status: verified / estimated / unavailable / stale
- Freshness checks and stale-data flags
- Formula validation tests against known values
- AI grounded in verified data with citations
- Never fabricate; disclose missing data

## 15. Future Scope

- Advanced multi-agent research (LangGraph)
- RAG over annual reports
- PDF financial statement extraction
- Industry benchmarking
- Anomaly detection
- Advanced portfolio analytics
- Automated research alerts

---

## PROJECT DEVELOPMENT RULES

1. Develop only the day requested by the user.
2. Read `README.md` and `PROJECT_SUMMARY.md` before every development session.
3. Follow the documented architecture.
4. Do not change the agreed design system without reason.
5. Do not break previously working features.
6. Test every newly developed module.
7. Update documentation after each development day.
8. Maintain a working application throughout development.
9. Do not use fabricated data as actual market information.
10. Clearly disclose missing or unavailable data.
11. Prefer free tools and APIs.
12. Ask before introducing paid APIs or services.
13. Do not implement automatic buy/sell trading.

## DAILY SESSION FORMAT

At the end of each development day, report:

1. What was developed.
2. Files created or modified.
3. Features completed.
4. Tests performed.
5. Errors resolved.
6. Known limitations.
7. What was learned.
8. Next day's plan.

---

## FINAL VERIFICATION CHECKLIST

- [x] Both files exist: `README.md`, `PROJECT_SUMMARY.md`
- [x] All 20 roadmap days included
- [x] UI/UX requirements documented (palette, layout, charts)
- [x] Financial data requirements documented (sources, fallback, schema)
- [x] AI and security requirements documented
- [x] Documents consistent with each other

---

*This is a research and educational tool. It does not guarantee investment returns, does not provide buy/sell signals, and is not financial advice. Investment decisions remain the user's responsibility.*
