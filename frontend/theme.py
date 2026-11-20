"""Application theme and styling helpers."""

from __future__ import annotations

import streamlit as st

PRIMARY_BG = "#0B1220"
SECONDARY_BG = "#111827"
CARD_BG = "#172033"
PRIMARY_ACCENT = "#14B8A6"
SECONDARY_ACCENT = "#3B82F6"
POSITIVE = "#22C55E"
NEGATIVE = "#EF4444"
TEXT_PRIMARY = "#F8FAFC"
TEXT_SECONDARY = "#94A3B8"


def get_css() -> str:
    """Return the global CSS for the premium financial UI."""
    return f"""
    <style>
    :root {{
        --asm-bg: {PRIMARY_BG};
        --asm-bg-2: {SECONDARY_BG};
        --asm-card: {CARD_BG};
        --asm-accent: {PRIMARY_ACCENT};
        --asm-accent-2: {SECONDARY_ACCENT};
        --asm-positive: {POSITIVE};
        --asm-negative: {NEGATIVE};
        --asm-text: {TEXT_PRIMARY};
        --asm-text-2: {TEXT_SECONDARY};
        --asm-radius: 12px;
        --asm-gap: 16px;
    }}

    .stApp {{
        background-color: var(--asm-bg);
        color: var(--asm-text);
    }}

    section[data-testid="stSidebar"] {{
        background-color: var(--asm-bg-2);
        border-right: 1px solid #1f2a44;
    }}

    section[data-testid="stSidebar"] * {{
        color: var(--asm-text);
    }}

    h1, h2, h3, h4 {{
        color: var(--asm-text);
        letter-spacing: -0.01em;
    }}

    .asm-page-header {{
        padding: 8px 0 16px 0;
        border-bottom: 1px solid #1f2a44;
        margin-bottom: 20px;
    }}

    .asm-page-title {{
        font-size: 1.9rem;
        font-weight: 700;
        color: var(--asm-text);
        margin: 0;
    }}

    .asm-page-subtitle {{
        font-size: 0.95rem;
        color: var(--asm-text-2);
        margin-top: 4px;
    }}

    .asm-card {{
        background-color: var(--asm-card);
        border: 1px solid #1f2a44;
        border-radius: var(--asm-radius);
        padding: 16px 18px;
        margin-bottom: var(--asm-gap);
        box-shadow: 0 4px 12px rgba(0,0,0,0.18);
    }}

    .asm-card-title {{
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--asm-text-2);
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 8px;
    }}

    .asm-metric-value {{
        font-size: 1.6rem;
        font-weight: 700;
        color: var(--asm-text);
        line-height: 1.1;
    }}

    .asm-metric-delta-positive {{
        color: var(--asm-positive);
        font-size: 0.85rem;
        font-weight: 600;
    }}

    .asm-metric-delta-negative {{
        color: var(--asm-negative);
        font-size: 0.85rem;
        font-weight: 600;
    }}

    .asm-sample-badge {{
        display: inline-block;
        font-size: 0.7rem;
        font-weight: 600;
        color: var(--asm-accent-2);
        background: rgba(59, 130, 246, 0.12);
        border: 1px solid rgba(59, 130, 246, 0.4);
        border-radius: 6px;
        padding: 2px 8px;
        margin-left: 8px;
        vertical-align: middle;
    }}

    .asm-section-header {{
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--asm-text);
        margin: 18px 0 8px 0;
        padding-bottom: 6px;
        border-bottom: 1px solid #1f2a44;
    }}

    .asm-alert {{
        border-radius: var(--asm-radius);
        padding: 12px 16px;
        margin-bottom: var(--asm-gap);
        border-left: 4px solid;
    }}

    .asm-alert-info {{
        background: rgba(20, 184, 166, 0.08);
        border-color: var(--asm-accent);
        color: var(--asm-text);
    }}

    .asm-alert-warning {{
        background: rgba(239, 68, 68, 0.08);
        border-color: var(--asm-negative);
        color: var(--asm-text);
    }}

    .asm-alert-success {{
        background: rgba(34, 197, 94, 0.08);
        border-color: var(--asm-positive);
        color: var(--asm-text);
    }}

    .asm-empty-state {{
        text-align: center;
        padding: 28px 16px;
        color: var(--asm-text-2);
        background: var(--asm-card);
        border: 1px dashed #2a3a5a;
        border-radius: var(--asm-radius);
    }}

    .asm-skeleton {{
        height: 14px;
        background: linear-gradient(90deg, #1f2a44 25%, #2a3a5a 50%, #1f2a44 75%);
        background-size: 200% 100%;
        animation: asm-shimmer 1.4s infinite;
        border-radius: 6px;
        margin: 6px 0;
    }}

    @keyframes asm-shimmer {{
        0% {{ background-position: 200% 0; }}
        100% {{ background-position: -200% 0; }}
    }}

    /* Streamlit tables */
    div[data-testid="stDataFrame"] {{
        border: 1px solid #1f2a44;
        border-radius: var(--asm-radius);
    }}

    /* Buttons */
    .stButton > button {{
        background-color: var(--asm-accent);
        color: #0B1220;
        border: none;
        border-radius: 8px;
        font-weight: 600;
    }}

    .stButton > button:hover {{
        background-color: #0ea5a5;
        color: #0B1220;
    }}

    /* Inputs */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {{
        background-color: var(--asm-card);
        color: var(--asm-text);
        border: 1px solid #2a3a5a;
        border-radius: 8px;
    }}

    @media (max-width: 768px) {{
        .asm-page-title {{ font-size: 1.5rem; }}
        .asm-metric-value {{ font-size: 1.3rem; }}
    }}
    </style>
    """


def apply_theme() -> None:
    """Inject global theme CSS into the Streamlit app."""
    st.markdown(get_css(), unsafe_allow_html=True)
