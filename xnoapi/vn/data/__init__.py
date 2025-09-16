from __future__ import annotations

# Public constants/helpers
from .const import *  # noqa: F401,F403
from .core import send_request
from .utils import *  # noqa: F401,F403

# Stocks theme (consolidated)
from .stocks import (
    Company,
    Finance,
    Fund,
    Listing,
    Quote,
    Global,
    MSN,
    FX,
    Crypto,
    WorldIndex,
    list_liquid_asset,
    get_hist as get_stock_hist,
    ping,
    get_indices,
    get_market_index_snapshot,
    get_stock_foreign_trading,
    get_stock_matches,
    get_stock_info,
    get_stock_top_price,
    Trading,
)

# Derivatives theme
from .derivatives import get_hist as get_derivatives_hist

# Backward-compatibility: default get_hist refers to stocks
get_hist = get_stock_hist

__all__ = [
    # helpers
    "send_request",
    # stocks theme
    "Company", "Finance", "Fund", "Listing", "Quote",
    "Global", "MSN", "FX", "Crypto", "WorldIndex",
    "list_liquid_asset", "get_stock_hist", "get_hist",
    "ping", "get_indices", "get_market_index_snapshot",
    "get_stock_foreign_trading", "get_stock_matches",
    "get_stock_info", "get_stock_top_price", "Trading",
    # derivatives
    "get_derivatives_hist",
]
