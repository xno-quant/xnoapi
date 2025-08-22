from __future__ import annotations

import datetime as dt
import json
import os
from typing import Any, Dict, Iterable, List, Optional, Union

import pandas as pd
import requests

from .utils import Config

__all__ = [
    "get_indices",
    "get_market_index_snapshot", 
    "get_stock_foreign_trading",
    "get_stock_matches",
    "get_stock_ohlcv",
    "get_stock_info", 
    "get_stock_top_price",
    "ping",
]

# Configuration
QUANT_BASE_URL = "https://api-v2.xno.vn/quant-data"
REQUEST_TIMEOUT = 30

# Resolution mapping for time series data
RESOLUTION_MAP: Dict[str, str] = {
    "1M": "1", "1": "1",
    "5M": "5", "5": "5", 
    "15M": "15", "15": "15",
    "30M": "30", "30": "30",
    "1H": "60", "60": "60",
    "D": "D", "1D": "D", "DAY": "D",
    "W": "W", "1W": "W", "WEEK": "W",
}


class APIError(Exception):
    """Custom exception for API-related errors."""
    pass


def _get_auth_header() -> Dict[str, str]:
    """
    Build Authorization header from globally-set API key.
    
    Raises:
        APIError: If API key is not configured.
    """
    try:
        api_key = Config.get_api_key()
        return {"Authorization": api_key}
    except Exception as e:
        raise APIError("API key not configured. Use client(apikey='xd_...') first.") from e


def _normalize_symbol(symbol: str) -> str:
    """Normalize stock symbol to uppercase format."""
    return (symbol or "").strip().upper()


def _to_unix_timestamp(timestamp: Union[int, float, str, dt.datetime]) -> int:
    """
    Convert various timestamp formats to Unix seconds (UTC).
    
    Args:
        timestamp: Unix seconds, ISO8601 string, or datetime object.
        
    Returns:
        Unix timestamp as integer.
    """
    if isinstance(timestamp, (int, float)):
        return int(timestamp)
        
    if isinstance(timestamp, str):
        try:
            dt_obj = dt.datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            return int(dt_obj.timestamp())
        except ValueError as e:
            raise ValueError(f"Invalid timestamp format: {timestamp}") from e
            
    if isinstance(timestamp, dt.datetime):
        if timestamp.tzinfo is None:
            # Assume naive datetime is UTC as per standard practice
            return int(timestamp.replace(tzinfo=dt.timezone.utc).timestamp())
        return int(timestamp.astimezone(dt.timezone.utc).timestamp())
        
    raise TypeError(f"Unsupported timestamp type: {type(timestamp)}")


def _make_request(url: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
    """
    Make an authenticated GET request with standard error handling.
    """
    headers = _get_auth_header()
    
    try:
        response = requests.get(
            url, 
            headers=headers, 
            params=params, 
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response
    except requests.RequestException as e:
        raise APIError(f"Request failed: {e}") from e


def _parse_json_response(response: requests.Response) -> Any:
    """
    Parse JSON response and handle potential errors.
    
    Returns:
        Parsed JSON data, typically a dictionary.
    """
    try:
        data = response.json()
        if "data" not in data:
            raise APIError(f"API response missing 'data' field: {response.text[:200]}")
        return data["data"]
    except ValueError as e:
        raise APIError(f"Invalid JSON response: {response.text[:200]}") from e


def _create_dataframe_with_columns(
    data: Union[Dict, List], 
    columns: List[str]
) -> pd.DataFrame:
    """
    Create a DataFrame with specified columns, handling both dict and list inputs.
    """
    if not data:
        return pd.DataFrame(columns=columns)

    if isinstance(data, dict) and all(isinstance(v, list) for v in data.values()):
        # Handle format {'t': [...], 'o': [...]}
        df_data = {col: data.get(col, []) for col in columns}
        return pd.DataFrame(df_data)
    
    if isinstance(data, dict):
        # Handle single record
        return pd.DataFrame([data])
        
    if isinstance(data, list):
        # Handle list of records
        return pd.DataFrame(data)

    return pd.DataFrame()


def _normalize_resolution(resolution: str) -> str:
    """Normalize resolution string to backend format."""
    key = (resolution or "").strip().upper()
    if key not in RESOLUTION_MAP:
        raise ValueError(f"Unsupported resolution. Use one of {list(RESOLUTION_MAP.keys())}")
    return RESOLUTION_MAP[key]


def _chunk_time_range(start_ts: int, end_ts: int, chunk_seconds: int):
    """
    Generator that yields time range chunks.
    """
    current = start_ts
    while current < end_ts:
        next_ts = min(current + chunk_seconds, end_ts)
        yield current, next_ts
        current = next_ts


# --- Public API Functions ---

def ping() -> bool:
    """
    Check connectivity to the quant-data service.
    
    Returns:
        True if the service is reachable, False otherwise.
    """
    try:
        url = f"{QUANT_BASE_URL}/v1/ping"
        response = requests.get(url, timeout=5)
        return response.ok
    except requests.RequestException:
        return False


def get_indices() -> pd.DataFrame:
    """
    Retrieve a list of available market indices.
    
    Returns:
        DataFrame with columns: ['symbol', 'name'].
    """
    url = f"{QUANT_BASE_URL}/v1/indices"
    response = _make_request(url)
    data = _parse_json_response(response)
    return _create_dataframe_with_columns(data, columns=['symbol', 'name'])


def get_market_index_snapshot(index_symbol: str) -> pd.DataFrame:
    """
    Retrieve the current snapshot for a market index.
    
    Args:
        index_symbol: Index symbol (e.g., 'VNINDEX').
        
    Returns:
        A single-row DataFrame with index data.
    """
    index_symbol = _normalize_symbol(index_symbol)
    url = f"{QUANT_BASE_URL}/v1/indices/{index_symbol}/market-index"
    response = _make_request(url)
    data = _parse_json_response(response)
    return pd.DataFrame([data])


def get_stock_foreign_trading(symbol: str) -> pd.DataFrame:
    """
    Get foreign trading data for a specific stock.
    
    Args:
        symbol: Stock symbol.
        
    Returns:
        A DataFrame with foreign trading information.
    """
    symbol = _normalize_symbol(symbol)
    url = f"{QUANT_BASE_URL}/v1/stocks/{symbol}/foreign-trading"
    response = _make_request(url)
    data = _parse_json_response(response)
    return pd.DataFrame([data])


def get_stock_matches(symbol: str) -> pd.DataFrame:
    """
    Retrieve recent match ticks for a stock.
    
    Returns:
        DataFrame with columns: ['time', 'symbol', 'price', 'volume', 'side'].
    """
    symbol = _normalize_symbol(symbol)
    url = f"{QUANT_BASE_URL}/v1/stocks/{symbol}/matches"
    response = _make_request(url)
    data = _parse_json_response(response)
    return _create_dataframe_with_columns(data, columns=['time', 'symbol', 'price', 'volume', 'side'])


def get_stock_ohlcv(
    symbol: str,
    resolution: str,
    start: Union[int, str, dt.datetime],
    end: Union[int, str, dt.datetime],
) -> pd.DataFrame:
    """
    Retrieve OHLCV data for a stock [BETA].
    
    Args:
        symbol: Stock symbol.
        resolution: Time resolution ('1M', '5M', '1H', 'D', 'W', etc.).
        start: Start time (Unix timestamp, ISO string, or datetime object).
        end: End time (Unix timestamp, ISO string, or datetime object).
        
    Returns:
        DataFrame with columns: ['t', 'o', 'h', 'l', 'c', 'v'].
    """
    symbol = _normalize_symbol(symbol)
    start_ts = _to_unix_timestamp(start)
    end_ts = _to_unix_timestamp(end)
    resolution_norm = _normalize_resolution(resolution)

    # Determine chunk size based on resolution to avoid request timeouts
    if resolution_norm in {"1", "5", "15", "30", "60"}:  # Intraday
        chunk_size = 3 * 24 * 3600  # 3 days per chunk
    else:  # Daily, Weekly
        chunk_size = 365 * 24 * 3600  # 1 year per chunk

    url_template = f"{QUANT_BASE_URL}/v1/stocks/{symbol}/ohlcv/{resolution_norm}"
    all_chunks: List[pd.DataFrame] = []

    for chunk_start, chunk_end in _chunk_time_range(start_ts, end_ts, chunk_size):
        params = {"from": chunk_start, "to": chunk_end}
        try:
            response = _make_request(url_template, params=params)
            data = _parse_json_response(response)
            chunk_df = _create_dataframe_with_columns(data, columns=["t", "o", "h", "l", "c", "v"])
            if not chunk_df.empty:
                all_chunks.append(chunk_df)
        except APIError:
            # Skip failed chunks but continue with others
            continue
    
    if not all_chunks:
        return pd.DataFrame(columns=["t", "o", "h", "l", "c", "v"])

    # Concatenate all dataframes and ensure uniqueness and order
    result_df = pd.concat(all_chunks, ignore_index=True)
    result_df = result_df.drop_duplicates(subset=['t']).sort_values(by='t').reset_index(drop=True)
    return result_df


def get_stock_info(symbol: str) -> pd.DataFrame:
    """
    Get the current stock information snapshot.
    
    Args:
        symbol: Stock symbol.
        
    Returns:
        A DataFrame with stock information (open, high, low, close, etc.).
    """
    symbol = _normalize_symbol(symbol)
    url = f"{QUANT_BASE_URL}/v1/stocks/{symbol}/stock-info"
    response = _make_request(url)
    data = _parse_json_response(response)
    return pd.DataFrame([data])


def get_stock_top_price(symbol: str) -> pd.DataFrame:
    """
    Get the top price (order book snapshot) for a stock [BETA].
    
    Note:
        Returns an empty DataFrame on server errors to maintain pipeline stability.
    """
    symbol = _normalize_symbol(symbol)
    url = f"{QUANT_BASE_URL}/v1/stocks/{symbol}/top-price"
    try:
        response = _make_request(url)
        data = _parse_json_response(response)
        return pd.DataFrame([data])
    except APIError:
        return pd.DataFrame()