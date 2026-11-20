# Project Architecture

## Overview
AI Share Market Research Agent is a modular Python platform for Indian stock market
research, fundamental analysis, screening, comparison and AI-generated reports.

## Day 1 Structure

```
AI-Share-Market-Agent/
├── app.py                  # Streamlit entry point
├── config/                 # Settings and logging configuration
│   ├── settings.py
│   └── logging_config.py
├── backend/                # Backend services and models (future)
│   ├── api/
│   └── models/
├── frontend/               # UI components and pages (future)
│   ├── components/
│   └── pages/
├── data/                   # Raw and processed data storage
│   ├── raw/
│   └── processed/
├── database/               # Local database files
├── agents/                 # AI agents (future)
├── analytics/              # Analytics modules (future)
├── services/               # Shared services (health, logging helpers)
├── reports/                # Generated reports (future)
├── tests/                  # Test suite
│   ├── unit/
│   └── integration/
├── docs/                   # Documentation
├── logs/                   # Application logs
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Design Principles
- Modular, clean, maintainable Python code.
- Configuration via environment variables (`.env`).
- Centralized logging with rotating file handler.
- Free and open-source technologies only.
- No hardcoded real market data; placeholders clearly labelled.
- Health checks exposed in the UI.

## Day 1 Scope
Only the UI foundation and project scaffolding. No real market data integration.
