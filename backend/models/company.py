"""Company domain model."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Company:
    symbol: str
    name: str
    sector: str = ""
    industry: str = ""
    exchange: str = "NSE"
    listing_year: str = ""
    website: str = ""
    description: str = ""
    data_source: str = "Local seed (sample)"
    data_quality: str = "sample"

    def to_dict(self) -> dict:
        return {
            "symbol": self.symbol,
            "name": self.name,
            "sector": self.sector,
            "industry": self.industry,
            "exchange": self.exchange,
            "listing_year": self.listing_year,
            "website": self.website,
            "description": self.description,
            "data_source": self.data_source,
            "data_quality": self.data_quality,
        }
