from __future__ import annotations

# Public constants/helpers
from .const import *  # noqa: F401,F403

# Core helpers (do NOT import merge_fund_into_price here to avoid hard dependency)
from .core import (
    send_request,
    add_all_ta_features,
    add_all_fund_features,
    fund_feature,
)

# Other helpers
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

# ========== Dynamic single-feature API (module-level) ==========
# ========== Dynamic single-feature API (module-level) ==========
def __getattr__(name: str):
    # Fallback: danh sách feature hợp lệ nếu core không export _FUND_CANONICAL_NAMES
    _fallback = {
        "earningPerShare","bookValuePerShare","roe","roa","priceToEarning","priceToBook",
        "interestMargin","nonInterestOnToi","badDebtPercentage","provisionOnBadDebt",
        "costOfFinancing","equityOnTotalAsset","equityOnLoan","costToIncome","equityOnLiability",
        "assetOnEquity","preProvisionOnToi","postTaxOnToi","loanOnEarnAsset","loanOnAsset","loanOnDeposit",
        "depositOnEarnAsset","badDebtOnAsset","liquidityOnLiability","payableOnEquity","cancelDebt","creditGrowth",
        "earningPerShare_yoy","earningPerShare_yoy_abs","roe_yoy","roe_yoy_abs","roa_yoy","roa_yoy_abs",
        "bookValuePerShare_yoy","bookValuePerShare_yoy_abs",
        "eps_yoy_up","eps_up_4p","cash_on_equity_yoy_up","capex_pos",
        "curr_gt1_5_yoy_up","quick_gt1_yoy_up","int_cov_gt3","bvps_yoy_up","wc_pos_yoy_up",
        "roe_gt15_yoy_up","roa_gt8_yoy_up","asset_turnover_yoy_up",
        "days_inv_yoy_down","days_rec_yoy_down","days_pay_yoy_down","gpa_yoy_up","charter_cap_yoy_up",
    }
    try:
        from .core import _FUND_CANONICAL_NAMES as _names
    except Exception:
        _names = _fallback

    if name in _names:
        from .core import fund_feature as _fund_feature
        def _fn(symbol: str, **kwargs):
            return _fund_feature(name, symbol, **kwargs)
        _fn.__name__ = name
        _fn.__doc__ = (
            f"Return DataFrame: date,time,open,high,low,close,volume,{name} "
            f"for the given symbol. Example: {name}('VCB')."
        )
        return _fn

    raise AttributeError(name)


__all__ = [
    # helpers
    "send_request",
    # core bulk adders
    "add_all_ta_features", "add_all_fund_features", "fund_feature",
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
