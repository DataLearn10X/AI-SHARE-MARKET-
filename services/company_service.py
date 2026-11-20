"""Company search and profile service."""

from __future__ import annotations

import csv
from functools import lru_cache
from pathlib import Path
from typing import List, Optional

from backend.models.company import Company
from config.settings import PROJECT_ROOT

MASTER_PATH = PROJECT_ROOT / "data" / "company_master.csv"


@lru_cache(maxsize=1)
def load_company_master() -> List[Company]:
    """Load the local company master seed (sample data)."""
    companies: List[Company] = []
    if not MASTER_PATH.exists():
        return companies
    with MASTER_PATH.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            companies.append(
                Company(
                    symbol=(row.get("symbol") or "").strip().upper(),
                    name=(row.get("name") or "").strip(),
                    sector=(row.get("sector") or "").strip(),
                    industry=(row.get("industry") or "").strip(),
                    exchange=(row.get("exchange") or "").strip(),
                    listing_year=(row.get("listing_year") or "").strip(),
                    website=(row.get("website") or "").strip(),
                    description=(row.get("description") or "").strip(),
                )
            )
    return companies


def search_companies(query: str, limit: int = 25) -> List[Company]:
    """Search companies by symbol, name, sector or industry."""
    companies = load_company_master()
    q = (query or "").strip().lower()
    if not q:
        return companies[:limit]
    results = []
    for c in companies:
        haystack = " ".join([c.symbol, c.name, c.sector, c.industry]).lower()
        if q in haystack:
            results.append(c)
            if len(results) >= limit:
                break
    return results


def get_company(symbol: str) -> Optional[Company]:
    """Fetch a single company by symbol (case-insensitive)."""
    if not symbol:
        return None
    target = symbol.strip().upper()
    for c in load_company_master():
        if c.symbol == target:
            return c
    return None


def all_symbols() -> List[str]:
    return [c.symbol for c in load_company_master()]
