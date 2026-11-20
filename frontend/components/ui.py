"""Reusable UI components for the premium financial interface."""

from __future__ import annotations

from typing import Optional

import streamlit as st


def page_header(title: str, subtitle: Optional[str] = None) -> None:
    """Render a consistent page header."""
    sub = f'<div class="asm-page-subtitle">{subtitle}</div>' if subtitle else ""
    st.markdown(
        f'<div class="asm-page-header"><h1 class="asm-page-title">{title}</h1>{sub}</div>',
        unsafe_allow_html=True,
    )


def section_header(title: str) -> None:
    """Render a section divider header."""
    st.markdown(f'<div class="asm-section-header">{title}</div>', unsafe_allow_html=True)


def sample_badge(text: str = "Sample data") -> None:
    """Inline badge indicating placeholder/sample content."""
    st.markdown(f'<span class="asm-sample-badge">{text}</span>', unsafe_allow_html=True)


def card(title: Optional[str] = None) -> None:
    """Open a styled card container (use with st.container)."""
    if title:
        st.markdown(f'<div class="asm-card"><div class="asm-card-title">{title}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="asm-card">', unsafe_allow_html=True)


def card_end() -> None:
    """Close a styled card container."""
    st.markdown("</div>", unsafe_allow_html=True)


def metric_card(label: str, value: str, delta: Optional[str] = None, sample: bool = False,
                delta_positive: bool = True) -> None:
    """Render a metric card with optional delta and sample badge."""
    badge = '<span class="asm-sample-badge">Sample</span>' if sample else ""
    delta_html = ""
    if delta:
        cls = "asm-metric-delta-positive" if delta_positive else "asm-metric-delta-negative"
        delta_html = f'<div class="{cls}">{delta}</div>'
    st.markdown(
        f"""
        <div class="asm-card">
            <div class="asm-card-title">{label}{badge}</div>
            <div class="asm-metric-value">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def alert(message: str, kind: str = "info") -> None:
    """Render an alert box. kind: info | warning | success."""
    cls = {"info": "asm-alert-info", "warning": "asm-alert-warning", "success": "asm-alert-success"}.get(kind, "asm-alert-info")
    st.markdown(f'<div class="asm-alert {cls}">{message}</div>', unsafe_allow_html=True)


def empty_state(message: str) -> None:
    """Render an empty-state placeholder."""
    st.markdown(f'<div class="asm-empty-state">{message}</div>', unsafe_allow_html=True)


def loading_state(message: str = "Loading...") -> None:
    """Render a loading placeholder with skeleton bars."""
    st.markdown(
        f"""
        <div class="asm-card">
            <div class="asm-card-title">{message}</div>
            <div class="asm-skeleton"></div>
            <div class="asm-skeleton"></div>
            <div class="asm-skeleton" style="width:70%"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def sample_note(text: str = "All values shown are illustrative samples, not real market data.") -> None:
    """Render a standard sample-data disclosure note."""
    st.caption(f"⚠️ {text}")


def profile_card(profile: dict) -> None:
    """Render a company profile card from a dict."""
    rows = []
    field_labels = [
        ("symbol", "Symbol"),
        ("name", "Company Name"),
        ("sector", "Sector"),
        ("industry", "Industry"),
        ("exchange", "Exchange"),
        ("listing_year", "Listing Year"),
        ("website", "Website"),
        ("description", "Description"),
    ]
    for key, label in field_labels:
        val = profile.get(key)
        if val:
            rows.append((label, val))
    body = "".join(
        f'<div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #1f2a44;">'
        f'<span style="color:#94A3B8;font-weight:600;">{lbl}</span>'
        f'<span style="color:#F8FAFC;text-align:right;max-width:60%;word-break:break-word;">{val}</span></div>'
        for lbl, val in rows
    )
    source = profile.get("data_source", "Local seed (sample)")
    st.markdown(
        f'<div class="asm-card"><div class="asm-card-title">Company Profile</div>{body}'
        f'<div style="margin-top:8px;font-size:0.75rem;color:#94A3B8;">Source: {source} (sample seed)</div></div>',
        unsafe_allow_html=True,
    )
