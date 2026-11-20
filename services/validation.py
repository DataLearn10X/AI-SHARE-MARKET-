"""Input validation helpers."""

from __future__ import annotations

import re
from datetime import datetime
from typing import Optional


def is_valid_symbol(symbol: Optional[str]) -> bool:
    if not symbol:
        return False
    s = symbol.strip().upper()
    return bool(re.fullmatch(r"[A-Z0-9&\-\.]{1,20}", s))


def is_positive_number(value) -> bool:
    try:
        return float(value) > 0
    except (TypeError, ValueError):
        return False


def is_non_negative_number(value) -> bool:
    try:
        return float(value) >= 0
    except (TypeError, ValueError):
        return False


def is_valid_date(value: Optional[str]) -> bool:
    if not value:
        return True  # optional
    try:
        datetime.strptime(value.strip(), "%Y-%m-%d")
        return True
    except (ValueError, AttributeError):
        return False


def sanitize_symbol(symbol: Optional[str]) -> str:
    if not symbol:
        return ""
    return symbol.strip().upper()
