# Deployment Guide

## Local Deployment

1. Create and activate a virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Copy environment template:
   ```powershell
   copy .env.example .env
   ```
   Fill in any optional API keys.
4. Run the app:
   ```powershell
   streamlit run app.py
   ```
   Open http://localhost:8501

## Streamlit Community Cloud

1. Push the repository to GitHub.
2. Go to https://share.streamlit.io and create a new app.
3. Set the main file path to `app.py`.
4. Add secrets in the Streamlit Cloud dashboard (equivalent to `.env`):
   - `OPENAI_API_KEY`, `GROQ_API_KEY`, etc. (optional)
5. Deploy.

## Notes
- The app uses SQLite (`database/app.db`) for local persistence. On Streamlit Cloud, the filesystem is ephemeral; data resets on redeploy.
- No paid APIs are required. yfinance is unofficial and may be rate-limited.
- All market data is labelled as unofficial/sample where applicable.
