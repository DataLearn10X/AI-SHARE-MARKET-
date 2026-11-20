"""NSE India provider (placeholder).

NSE does not provide an official public API. Automated scraping or undocumented
endpoints are intentionally not implemented to respect NSE's terms of service.
This provider reports as unavailable so the fallback chain can move on.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

import pandas as pd

logger = logging.getLogger(__name__)


class NSEProvider:
    name = "nse_india"

    def is_available(self) -> bool:
        return False

    def get_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        logger.info("NSE provider unavailable; skipping %s", symbol)
        return None

    def get_price_history(self, symbol: str, period: str = "1y",
                          interval: str = "1d") -> Optional[pd.DataFrame]:
        return None

    def get_company_info(self, symbol: str) -> Optional[Dict[str, Any]]:
        return None
