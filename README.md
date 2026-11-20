# AI Share Market Research Agent

> **Status:** v1.0 — 20-day development complete
> **Focus:** Indian stock market research for NSE and BSE companies
> **Type:** Research and educational tool — not a trading or investment advisory system

---

## 1. Project Overview

The **AI Share Market Research Agent** is an Indian stock market research platform focused on companies listed on the **NSE (National Stock Exchange)** and **BSE (Bombay Stock Exchange)**.

It is designed to be a single, structured research workspace where an investor can:

- Research companies and their businesses
- Analyse multi-year financial statements
- Understand business performance and growth
- Evaluate company fundamentals using standard ratios
- Compare companies side by side
- Discover stocks using screening criteria
- Generate AI-assisted research reports
- Monitor portfolios and watchlists

The platform combines **financial data ingestion**, **deterministic financial calculations**, **interactive visualisation**, and **AI-assisted explanation** into one application. AI is used to *explain and summarise* verified data — never to invent numbers.

### Core Principles

- **No fabricated financial data** — every number must trace to a verified source or be clearly labelled as unavailable/estimated.
- **Research, not advice** — the tool does not recommend buying or selling.
- **Free and open-source first** — prefer free tools, libraries and APIs.
- **Modular and maintainable** — clean Python codebase with clear module boundaries.
- **Transparent data provenance** — every record stores source, period, currency, unit and last-updated timestamp.

---

## 2. Problem Statement

Indian retail investors often struggle with:

- Finding reliable, structured financial information in one place
- Analysing multiple years of financial statements manually
- Understanding and interpreting financial ratios
- Comparing companies on consistent metrics
- Evaluating business growth and profitability trends
- Understanding quarterly results and their implications
- Identifying valuation risks (overvaluation, debt stress, cash-flow weakness)
- Producing structured research notes or reports

Financial data is scattered across exchange websites, company annual reports, and third-party portals, each with different formats and update cadences. This creates high manual effort and increases the risk of misinterpretation.

### Solution

The AI Share Market Research Agent reduces manual research effort by organising financial information into a **single research workspace** with:

- Standardised financial statements and ratios
- Consistent, formula-based calculations
- Interactive charts and comparison tables
- A screening engine for discovery
- AI-generated research summaries grounded in verified data

---

## 3. Target Users

- **Retail investors** — long-term equity investors seeking structured research
- **Long-term investors** — focused on fundamentals, growth and valuation
- **Fundamental analysts** — equity research learners and practitioners
- **Financial data analysts** — exploring Indian corporate financials
- **Students and educators** — learning financial statement analysis

The platform is **not** intended for intraday traders, algorithmic traders or automated order execution.

---

## 4. Technology Stack

All technologies below are free and open-source (or have free tiers). No paid service is required for the core platform.

| Technology | Purpose |
|---|---|
| **Python 3.x** | Core language for backend, analytics and data processing |
| **Streamlit** | Web application framework and UI layer |
| **Pandas** | Tabular data manipulation, cleaning, transformation |
| **NumPy** | Numerical operations and array-based computation |
| **Plotly** | Interactive charts (zoom, pan, hover, range selection) |
| **SQLite** (initial) | Local, file-based database for caching and persistence |
| **PostgreSQL** (later) | Scalable database when multi-user/concurrent needs arise |
| **Financial data APIs / sources** | Market prices, fundamentals, corporate data (see Section 6) |
| **LLM integration** | AI explanations, summaries and report generation (provider-agnostic) |
| **LangGraph** (optional, advanced) | Multi-step AI agent orchestration for research workflows |
| **Git & GitHub** | Version control, collaboration, deployment |

### Technology Rationale

- **Python** is the lingua franca of data and finance tooling, with mature libraries for analysis.
- **Streamlit** enables rapid development of data-driven web apps with minimal frontend code.
- **Pandas/NumPy** provide robust, well-tested data manipulation.
- **Plotly** delivers interactive, publication-quality charts with minimal configuration.
- **SQLite** is zero-configuration and sufficient for a single-user/local-first tool; PostgreSQL is the upgrade path.
- **LLM integration is provider-agnostic** — supports OpenAI, Groq, Ollama (local) etc. via environment variables; no single vendor lock-in.
- **LangGraph** is optional and only introduced for advanced multi-agent research flows.

> No unnecessary technologies are introduced. Each component maps to a concrete requirement.

---

## 5. Complete Application Modules

Each module below documents: Purpose, Input data, Processing logic, Expected output, Charts/tables, Dependencies, Validation requirements.

### A. Market Overview
- **Purpose:** High-level snapshot of Indian market indices and market mood.
- **Input data:** Index prices (NIFTY 50, SENSEX, NIFTY Bank, India VIX), top gainers/losers.
- **Processing logic:** Aggregate and format index values and daily changes; compute gainers/losers lists.
- **Expected output:** Index cards with current value and % change; tables of top gainers/losers.
- **Charts/tables:** Index metric cards, gainer/loser tables.
- **Dependencies:** Market price data source.
- **Validation:** Values must be labelled with source and timestamp; stale data flagged.

### B. NSE/BSE Stock Search
- **Purpose:** Find a company by symbol or name.
- **Input data:** User query string, company master list.
- **Processing logic:** Filter companies by symbol/name/exchange; return matches.
- **Expected output:** List of matching stocks with symbol, company name, sector, exchange.
- **Charts/tables:** Search results table.
- **Dependencies:** Company master data.
- **Validation:** Sanitise input; handle no-results gracefully; avoid injection.

### C. Company Profile
- **Purpose:** Static company information and business overview.
- **Input data:** Symbol; company master/registry data.
- **Processing logic:** Fetch and display company metadata.
- **Expected output:** Name, sector, industry, exchange, listing date, website, description.
- **Charts/tables:** Key-value profile card.
- **Dependencies:** Company information source.
- **Validation:** Handle missing fields; label unavailable data.

### D. Historical Price Analysis
- **Purpose:** Analyse historical price movement.
- **Input data:** OHLCV (open, high, low, close, volume) time series.
- **Processing logic:** Compute returns, volatility, moving averages; support interval aggregation (daily/weekly/monthly/yearly).
- **Expected output:** Price history table and charts.
- **Charts/tables:** Candlestick chart, volume bars, line charts with moving averages.
- **Dependencies:** Historical price data source.
- **Validation:** Ensure date continuity; handle missing trading days; label source and period.

### E. Financial Statement Analysis
- **Purpose:** Present standardised income statement, balance sheet and cash flow.
- **Input data:** Raw financial statements from source.
- **Processing logic:** Parse, normalise line items, align periods, handle units (Crores/Lakhs).
- **Expected output:** Clean financial statement tables by year/quarter.
- **Charts/tables:** Statement tables with period columns.
- **Dependencies:** Financial statement source.
- **Validation:** Identify consolidated vs standalone; never mix without labelling.

### F. Revenue and Profit Growth
- **Purpose:** Track growth in revenue and profitability over time.
- **Input data:** Revenue, net profit, operating profit by period.
- **Processing logic:** Compute YoY/QoQ growth rates; CAGR over selected window.
- **Expected output:** Growth metrics and trend charts.
- **Charts/tables:** Revenue vs profit trend, growth rate bar chart.
- **Dependencies:** Income statement data.
- **Validation:** Require at least 2 periods for growth; handle missing data.

### G. Balance Sheet Analysis
- **Purpose:** Analyse assets, liabilities and equity structure.
- **Input data:** Balance sheet line items.
- **Processing logic:** Compute totals, debt, equity, working capital; derive ratios.
- **Expected output:** Balance sheet table and derived metrics.
- **Charts/tables:** Asset/liability composition, debt trend.
- **Dependencies:** Balance sheet data.
- **Validation:** Assets = Liabilities + Equity sanity check where possible.

### H. Cash Flow Analysis
- **Purpose:** Analyse operating, investing and financing cash flows.
- **Input data:** Cash flow statement line items.
- **Processing logic:** Compute free cash flow, cash conversion, OCF/Net Profit.
- **Expected output:** Cash flow tables and trends.
- **Charts/tables:** OCF/ICF/FCF trend, FCF bar chart.
- **Dependencies:** Cash flow data.
- **Validation:** Label sign conventions; handle missing line items.

### I. Fundamental Ratios
- **Purpose:** Compute and display standard fundamental ratios.
- **Input data:** Financial statement line items.
- **Processing logic:** Apply defined formulas (Section 7).
- **Expected output:** Ratio tables with values and interpretation bands.
- **Charts/tables:** Ratio trend charts.
- **Dependencies:** Financial statements.
- **Validation:** Guard divide-by-zero; label N/A when inputs missing.

### J. Valuation Analysis
- **Purpose:** Assess valuation multiples.
- **Input data:** Price, EPS, book value, growth, dividend.
- **Processing logic:** Compute P/E, P/B, PEG, dividend yield; compare to historical/sector where available.
- **Expected output:** Valuation metrics and comparison.
- **Charts/tables:** Valuation multiple charts.
- **Dependencies:** Price data + fundamentals.
- **Validation:** Price must be dated; multiples N/A if denominator missing.

### K. Fundamental Scoring Engine
- **Purpose:** Produce a composite fundamental score (0–100) per company.
- **Input data:** Growth, profitability, leverage, liquidity, valuation metrics.
- **Processing logic:** Normalise and weight sub-scores; aggregate; store breakdown.
- **Expected output:** Score, sub-scores, grade band, explanation.
- **Charts/tables:** Score breakdown chart, radar chart.
- **Dependencies:** All fundamental metrics.
- **Validation:** Clearly state scoring methodology; score is a research aid, not a buy/sell signal.

### L. Company Comparison
- **Purpose:** Side-by-side comparison of 2+ companies.
- **Input data:** Metrics for selected companies.
- **Processing logic:** Align periods and metrics; compute deltas and ratios.
- **Expected output:** Comparison table and charts.
- **Charts/tables:** Grouped bar charts, comparison table.
- **Dependencies:** Company data + metrics.
- **Validation:** Ensure same period/currency/units for compared companies.

### M. Stock Screener
- **Purpose:** Discover stocks matching user-defined criteria.
- **Input data:** Universe of stocks with computed metrics.
- **Processing logic:** Apply filters (ranges, thresholds, sectors); sort and paginate.
- **Expected output:** Filtered stock list.
- **Charts/tables:** Screener results table with export.
- **Dependencies:** Metrics database.
- **Validation:** Validate filter inputs; limit result size; prevent expensive queries.

### N. AI Research Agent
- **Purpose:** Natural-language research assistant grounded in verified data.
- **Input data:** User question + retrieved financial data.
- **Processing logic:** Retrieve relevant data, prompt LLM with context, return cited answer.
- **Expected output:** Answer with source citations and periods.
- **Charts/tables:** Inline data references.
- **Dependencies:** LLM provider, data layer.
- **Validation:** LLM must not invent numbers; verify outputs against data; label interpretations.

### O. Quarterly Results Analysis
- **Purpose:** Analyse latest quarterly performance.
- **Input data:** Quarterly financials.
- **Processing logic:** Compute QoQ/YoY changes, margin trends, beat/miss vs prior.
- **Expected output:** Quarterly summary and trends.
- **Charts/tables:** Quarterly revenue/profit charts.
- **Dependencies:** Quarterly results source.
- **Validation:** Align quarter labels; handle restatements.

### P. AI Research Report Generator
- **Purpose:** Generate a structured research report for a company.
- **Input data:** All fundamentals, price, news (optional), scoring.
- **Processing logic:** Assemble data, generate sections via LLM with citations.
- **Expected output:** Markdown/PDF report with sections: overview, financials, valuation, risks, outlook.
- **Charts/tables:** Embedded charts/tables.
- **Dependencies:** AI agent, data layer, report templates.
- **Validation:** Every numeric claim must cite source/period; label as AI interpretation.

### Q. Portfolio Management
- **Purpose:** Track holdings, value and performance.
- **Input data:** User-entered holdings (symbol, qty, buy price, date).
- **Processing logic:** Compute current value, P&L, returns, allocation.
- **Expected output:** Portfolio dashboard.
- **Charts/tables:** Allocation pie chart, P&L table.
- **Dependencies:** Price data, user input.
- **Validation:** Validate inputs; no broker integration or auto-trading.

### R. Watchlist
- **Purpose:** Track selected stocks for quick access.
- **Input data:** User-selected symbols.
- **Processing logic:** Store and display with latest price and key metrics.
- **Expected output:** Watchlist table.
- **Charts/tables:** Watchlist table.
- **Dependencies:** Stock master, price data.
- **Validation:** Prevent duplicates; handle delisted symbols.

### S. Alerts and Monitoring
- **Purpose:** Notify on price/fundamental thresholds.
- **Input data:** User-defined alert rules.
- **Processing logic:** Evaluate rules on data refresh; generate alerts.
- **Expected output:** Alert list/notifications.
- **Charts/tables:** Alerts table.
- **Dependencies:** Data refresh, rule engine.
- **Validation:** Validate thresholds; avoid spam; no auto-trading.

---

## 6. Financial Data Sources

### 6.1 Classification of Data Needs

| Category | Examples |
|---|---|
| Historical market prices | OHLCV, indices |
| Financial statements | Income statement, balance sheet, cash flow |
| Quarterly results | Quarterly revenue, profit, margins |
| Corporate actions | Dividends, splits, bonuses |
| Shareholding patterns | Promoter/FII/DII/public holdings |
| Company information | Sector, industry, description |
| Sector and industry data | Peer groups, sector averages |

### 6.2 Potential Sources (Evaluation)

| Source | Available Data | Access Method | Limitations | Reliability | Alternative |
|---|---|---|---|---|---|
| **NSE India** (nseindia.com) | Prices, corporate filings, announcements, shareholding | Web pages / undocumented endpoints | No official public API; endpoints may change; rate limiting; terms apply | High (primary exchange) | BSE India |
| **BSE India** (bseindia.com) | Prices, filings, results, announcements | Web pages / endpoints | Similar restrictions; structure changes | High | NSE India |
| **Yahoo Finance (yfinance)** | Prices, some fundamentals, dividends | Python library | Unofficial; may break; data gaps; not exchange-official | Medium | NSE/BSE direct |
| **Screener.in** | Financials, ratios, screening | Web pages (scraping) | Terms of service; scraping restrictions; rate limits | Medium-High | Company annual reports |
| **Company annual reports** | Audited financial statements | PDF download from company IR | Manual/automated PDF extraction; format varies | High (audited) | Exchange filings |
| **Company investor relations websites** | Results, presentations, filings | Web pages/PDFs | Varies by company | High | Exchange announcements |
| **Exchange corporate announcements** | Results, board meetings, dividends | Web listings | Need parsing; no unified API | High | Company IR |
| **Other legitimate providers** | Varies | APIs (free tiers) | Free-tier limits; terms | Varies | Multiple fallbacks |

> **Important:** Never assume all data is freely accessible. Never invent API endpoints or credentials. Never bypass website restrictions (robots.txt, terms of service, rate limits). Clearly distinguish verified data from estimates and unavailable data.

### 6.3 Data-Source Fallback Strategy

1. **Primary:** Official exchange data (NSE/BSE) where accessible.
2. **Secondary:** Reputable aggregators (yfinance, Screener.in) for convenience.
3. **Tertiary:** Company annual reports / investor relations (authoritative for fundamentals).
4. **Fallback:** Mark data as unavailable; never fabricate.

Each fetch attempt should log source, status and timestamp. If primary fails, try secondary; if all fail, store `data_quality_status = unavailable`.

### 6.4 Financial Data Record Schema (ideal)

Every financial data record should store:

- `company_symbol`
- `data_source`
- `reporting_period` (e.g., FY2024, Q3 FY2024)
- `data_publication_date`
- `currency` (INR)
- `unit` (Crores / Lakhs / per share)
- `last_updated_timestamp`
- `data_quality_status` (verified / estimated / unavailable / stale)

---

## 7. Fundamental Analysis Requirements

All formulas below are deterministic and must be computed from verified inputs. Where an input is missing, the metric is **N/A** (never estimated silently).

### Growth
- **Revenue Growth (YoY):** `(Revenue_t - Revenue_{t-1}) / Revenue_{t-1} × 100`
- **Net Profit Growth (YoY):** `(NetProfit_t - NetProfit_{t-1}) / NetProfit_{t-1} × 100`
- **CAGR:** `(EndValue / StartValue)^(1/n) - 1`

### Profitability
- **EBITDA Margin:** `EBITDA / Revenue × 100`
- **Operating Margin:** `Operating Profit / Revenue × 100`
- **Net Profit Margin:** `Net Profit / Revenue × 100`

### Returns
- **ROE (Return on Equity):** `Net Profit / Shareholders' Equity × 100`
- **ROCE (Return on Capital Employed):** `EBIT / Capital Employed × 100` where `Capital Employed = Total Assets - Current Liabilities`
- **ROA (Return on Assets):** `Net Profit / Total Assets × 100`

### Leverage & Liquidity
- **Debt-to-Equity:** `Total Debt / Shareholders' Equity`
- **Interest Coverage:** `EBIT / Interest Expense`
- **Current Ratio:** `Current Assets / Current Liabilities`

### Cash Flow
- **Operating Cash Flow (OCF):** as reported
- **Free Cash Flow (FCF):** `Operating Cash Flow - Capital Expenditure`
- **Cash Conversion:** `OCF / Net Profit`

### Per-Share & Valuation
- **EPS (Earnings Per Share):** `Net Profit / Shares Outstanding`
- **P/E (Price-to-Earnings):** `Price per Share / EPS`
- **P/B (Price-to-Book):** `Price per Share / Book Value per Share`
- **PEG (Price/Earnings-to-Growth):** `P/E / Earnings Growth Rate`
- **Dividend Yield:** `Annual Dividend per Share / Price per Share × 100`

### Interpretation Notes

- **Growth:** Positive and consistent growth indicates expansion; volatile or negative growth warrants investigation.
- **Margins:** Higher and stable margins indicate pricing power and cost control; compare within sector.
- **ROE/ROCE/ROA:** Higher is generally better; very high ROE may be driven by leverage — check D/E.
- **Debt-to-Equity:** Lower is safer; capital-intensive sectors (utilities, infra) naturally carry higher debt.
- **Current Ratio:** >1 generally healthy; very high may indicate inefficient capital use.
- **Interest Coverage:** >2.5 generally comfortable; <1.5 is a warning.
- **FCF:** Positive and growing FCF indicates quality earnings; persistent negative FCF needs scrutiny.
- **P/E, P/B, PEG:** Lower may indicate undervaluation but can also signal weak prospects; PEG ~1 often considered fair. Always compare to sector peers and historical range.
- **Dividend Yield:** Attractive for income investors; very high yields may signal distress.

### Sector-Specific Considerations

- Banks/NBFCs: use different metrics (NIM, GNPA, CAR) — standard industrial ratios may mislead; flag sector.
- Capital-intensive sectors: higher acceptable D/E.
- IT/services: high ROE/ROCE typical; growth rates matter more.
- Always compare companies within the same sector.

### Consolidated vs Standalone

Support both consolidated and standalone statements wherever available. Always clearly identify which is used. Prefer consolidated when available for group companies. Never mix consolidated and standalone in the same comparison without explicit labelling.

---

## 8. Premium UI/UX Design System

The application must look like a professional financial research terminal.

### Design Direction
Modern premium financial analytics platform.

### Color Palette

| Token | Hex | Usage |
|---|---|---|
| Main background | `#0B1220` | App background |
| Secondary background | `#111827` | Sidebar, panels |
| Card background | `#172033` | Cards, containers |
| Primary accent | `#14B8A6` | Primary actions, highlights |
| Secondary accent | `#3B82F6` | Secondary actions, links |
| Positive | `#22C55E` | Gains, positive deltas |
| Negative | `#EF4444` | Losses, negative deltas |
| Primary text | `#F8FAFC` | Headings, primary text |
| Secondary text | `#94A3B8` | Captions, secondary text |

### Design Requirements

- Clean, professional sidebar navigation
- Consistent spacing and grid layout
- Rounded cards with subtle borders
- Clear typography hierarchy
- High-quality, readable tables
- Premium dashboard layout
- Responsive design (desktop-first, mobile-friendly)
- Consistent colour usage across modules
- Minimal, purposeful animations only
- Avoid overcrowded screens — use tabs/expansion
- Clear loading states (spinners/skeletons)
- Clear error states with actionable messages

---

## 9. Advanced Chart Requirements

Use **Plotly** (or another suitable interactive chart library).

Charts must support:

- Smooth rendering and responsive sizing
- Interactive zoom and pan
- Hover tooltips with values and dates
- Date range selection
- Interval switching: daily, weekly, monthly, yearly where supported
- Candlestick charts for prices
- Volume bars
- Moving averages (SMA/EMA)
- Revenue and net profit trend charts
- Margin trend charts
- ROE and ROCE trend charts
- Cash flow trend charts
- Valuation comparison charts
- Multi-company comparison charts

### Performance

- Prevent unnecessary chart reloads (cache data, use Streamlit caching)
- Use efficient data processing and aggregation
- Lazy-load heavy charts
- Charts must display clear units, dates and data-source information

---

## 10. AI Research Engine

### Capabilities (future)

- Natural-language stock research queries
- Financial statement explanations
- Company comparison narratives
- Quarterly result summaries
- Risk identification (debt stress, margin erosion, cash-flow weakness)
- Financial trend explanations
- Research report generation

### Grounding Rules

- AI must use **verified financial data**, never invent numbers.
- Every numeric claim must cite source and reporting period.
- Clearly label AI interpretations separately from factual data.
- Show confidence limitations and missing data.
- Provide "I don't have this data" rather than hallucinating.

### Implementation Approach

- Retrieve relevant structured data from the data layer
- Construct prompts with context, citations and instructions
- Use a provider-agnostic LLM interface (OpenAI/Groq/Ollama)
- Validate LLM output against source data where feasible
- Optional: LangGraph for multi-step research workflows (advanced)

---

## 11. Security and Data Quality

- **API key management:** All secrets via environment variables (`.env`); never commit.
- **Input validation:** Sanitise all user inputs; validate symbols, numbers, dates.
- **Database integrity:** Use constraints, transactions, parameterised queries.
- **Error handling:** Graceful failures with user-friendly messages; log details.
- **Logging:** Structured logs with levels; rotating file handlers.
- **Data freshness checks:** Track last-updated; flag stale data.
- **Duplicate prevention:** Upsert logic keyed on (symbol, period, source).
- **Source verification:** Store source for every record; verify before display.
- **No fabricated values:** N/A over invention; clearly disclose missing data.

---

## 12. Development Roadmap (20 Days)

### Day 1: Project architecture, folder structure, Python environment
- **Deliverables:** Project scaffold, venv, requirements, .env.example, .gitignore, README, health check, initial Streamlit dashboard (UI foundation).
- **Acceptance:** App launches; navigation works; tests pass.

### Day 2: Streamlit dashboard and professional UI
- **Deliverables:** Premium UI shell, theme, sidebar, layout components, loading/error states.
- **Acceptance:** Consistent design system applied; responsive layout.

### Day 3: NSE/BSE stock search and company profiles
- **Deliverables:** Stock search, company profile module, company master data.
- **Acceptance:** Search returns results; profile displays metadata.

### Day 4: Stock market API integration
- **Deliverables:** Data access layer, provider abstraction, caching, error handling.
- **Acceptance:** Price/fundamental fetch works with fallbacks.

### Day 5: Historical price data and charts
- **Deliverables:** OHLCV fetch, candlestick + volume charts, moving averages, intervals.
- **Acceptance:** Interactive charts render with zoom/pan/tooltips.

### Day 6: Revenue, profit and growth analysis
- **Deliverables:** Income statement module, growth metrics, trend charts.
- **Acceptance:** Revenue/profit trends and YoY/CAGR computed correctly.

### Day 7: Balance sheet and cash flow analysis
- **Deliverables:** Balance sheet module, cash flow module, derived metrics.
- **Acceptance:** Statements display with period alignment; FCF computed.

### Day 8: ROE, ROCE, margins, debt ratios
- **Deliverables:** Ratio engine, profitability/leverage/liquidity ratios.
- **Acceptance:** All ratios from Section 7 computed with validation.

### Day 9: P/E, P/B and valuation analysis
- **Deliverables:** Valuation module, multiples, historical/sector comparison.
- **Acceptance:** Valuation metrics computed; N/A handling.

### Day 10: Fundamental scoring engine
- **Deliverables:** Scoring model, sub-scores, grade bands, explanation.
- **Acceptance:** Score reproducible; methodology documented.

### Day 11: Company comparison engine
- **Deliverables:** Multi-company comparison module, aligned tables/charts.
- **Acceptance:** Side-by-side comparison works with consistent periods.

### Day 12: Stock screener
- **Deliverables:** Filter engine, screener UI, result export.
- **Acceptance:** Filters apply correctly; pagination works.

### Day 13: AI research agent
- **Deliverables:** LLM integration, retrieval, cited Q&A.
- **Acceptance:** Answers grounded in data with citations.

### Day 14: Quarterly results analysis
- **Deliverables:** Quarterly module, QoQ/YoY, margin trends.
- **Acceptance:** Quarterly data displays and computes correctly.

### Day 15: AI research report generation
- **Deliverables:** Report templates, generation pipeline, export (Markdown/PDF).
- **Acceptance:** Report generated with citations; labelled as AI interpretation.

### Day 16: Portfolio and watchlist
- **Deliverables:** Portfolio tracking, P&L, allocation; watchlist persistence.
- **Acceptance:** Holdings tracked; no broker integration.

### Day 17: Alerts and monitoring
- **Deliverables:** Alert rules, evaluation engine, notifications.
- **Acceptance:** Alerts trigger on thresholds; no auto-trading.

### Day 18: Database optimization and caching
- **Deliverables:** Schema optimization, indexes, caching layer, migrations.
- **Acceptance:** Improved performance; data integrity maintained.

### Day 19: Testing, error handling and validation
- **Deliverables:** Comprehensive tests, edge cases, validation, logging review.
- **Acceptance:** Test suite passes; robust error handling.

### Day 20: Final UI, documentation and GitHub deployment
- **Deliverables:** Final polish, docs update, deployment guide, GitHub release.
- **Acceptance:** Production-ready app; documentation complete.

---

## 13. Testing Strategy

- **Unit testing:** Financial formulas, data transformations, utilities.
- **API testing:** Data fetch functions, fallbacks, error handling.
- **Financial formula validation:** Cross-check computed ratios against known values.
- **Data quality testing:** Schema validation, duplicate detection, freshness checks.
- **UI testing:** Navigation, form validation, rendering (manual + automated where feasible).
- **Integration testing:** End-to-end flows (search → profile → financials → charts).
- **Performance testing:** Chart rendering, large dataset handling, caching effectiveness.

Tools: `pytest`, plus Streamlit's testing utilities where applicable.

---

## 14. Future Enhancements

- Advanced AI multi-agent research (LangGraph)
- RAG over annual reports and filings
- PDF financial statement extraction
- Industry benchmarking and peer comparison
- Financial anomaly detection
- Advanced portfolio analytics (risk, diversification)
- Automated research alerts and digests

---

## 15. Deployment

See `docs/deployment.md` for local and Streamlit Cloud deployment instructions.

## 16. Important Investment Disclaimer

This platform is a **research and educational tool**. It:

- Does **not** guarantee investment returns
- Does **not** present AI scores as guaranteed buy/sell signals
- Requires all financial data to be verified by the user
- Leaves all investment decisions to the user's responsibility

AI-generated content is an interpretation of data, not financial advice. Always consult a qualified financial advisor before making investment decisions.

---

*Document version: Day 1 foundation. Updated as development progresses.*
