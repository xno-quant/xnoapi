#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
stocks.py — Lấy OHLCV từ XNO API v2, bỏ giới hạn ~500 dòng.

Public:
- list_liquid_asset()
- get_hist(asset_name, resolution="m")  # resolution: "m" | "h"

Đặc điểm:
- Parser "chịu lỗi": JSON 1 khối, nhiều khối JSON ghép nối, NDJSON, dict-of-arrays (t/o/h/l/c/v),
  list-of-dicts, CSV fallback.
- Tự động phân trang theo thời gian: gọi nhiều request với from=last_ts+step cho tới khi hết dữ liệu.
- Output: DataFrame ["Date","time","Open","High","Low","Close","volume"]
  (KHÔNG đổi timezone; format từ datetime hiện có).
"""

from __future__ import annotations

import io
import json
import itertools
from typing import Any, Dict, List, Union, Optional

import pandas as pd
import requests
from .utils import Config
from .core import send_request
from .const import (
    TRADING_URL, CHART_URL, INTRADAY_URL,
    INTERVAL_MAP, INTRADAY_MAP, OHLC_COLUMNS, OHLC_RENAME,
    PRICE_DEPTH_URL, GRAPHQL_URL, PRICE_INFO_MAP
)
import datetime as dt
import requests

__all__ = ["list_liquid_asset", "get_hist"]

# ===== Cấu hình nguồn XNO API v2 =====
_STOCKS_API_BASE = "https://api-v2.xno.vn/quant-data/v1/stocks"
_TIMEOUT = 30  # giây
_MAX_REQUESTS = 2000  # giới hạn an toàn số lần phân trang

# Giữ cho API cũ list_liquid_asset (nếu bạn dùng ở nơi khác)
LAMBDA_URL = Config.get_link()


def list_liquid_asset() -> pd.DataFrame:
    """Retrieve a list of highly liquid assets (qua Lambda cũ)."""
    api_key = Config.get_api_key()
    r = requests.get(f"{LAMBDA_URL}/list-liquid-asset", headers={"x-api-key": api_key}, timeout=_TIMEOUT)
    r.raise_for_status()
    return pd.DataFrame(r.json())


# ===================== Helpers: Parse & Chuẩn hóa =====================

def _json_relaxed(text: str) -> Optional[Union[dict, list]]:
    """
    Thử parse JSON "chịu lỗi" theo 3 bước:
      1) json.loads toàn bộ
      2) Cắt substring giữa ký tự JSON đầu/cuối (lọc rác log) rồi loads
      3) NDJSON: mỗi dòng 1 JSON
    Trả về dict/list nếu parse được, ngược lại None.
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    starts = [i for i in [text.find("{"), text.find("[")] if i != -1]
    ends   = [i for i in [text.rfind("}"), text.rfind("]")] if i != -1]
    if starts and ends and max(ends) > min(starts):
        s, e = min(starts), max(ends) + 1
        try:
            return json.loads(text[s:e])
        except json.JSONDecodeError:
            pass

    items = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        try:
            items.append(json.loads(s))
        except json.JSONDecodeError:
            continue
    if items:
        if isinstance(items[0], list):
            out = []
            for it in items:
                if isinstance(it, list):
                    out.extend(it)
            return out
        return items

    return None


def _scan_all_json_blocks(text: str) -> List[Any]:
    """
    Quét *tất cả* khối JSON (object/array) nối tiếp trong text (fix lỗi 'Extra data').
    Trả về danh sách các object đã parse (dict/list). Bỏ qua block lỗi.
    """
    s = text.lstrip()
    i, n = 0, len(s)
    blocks: List[Any] = []

    while i < n:
        while i < n and s[i] not in "{[":
            i += 1
        if i >= n:
            break

        opening = s[i]
        closing = "}" if opening == "{" else "]"
        depth = 0
        in_str = False
        esc = False
        j = i

        while j < n:
            ch = s[j]
            if in_str:
                if esc:
                    esc = False
                elif ch == "\\":
                    esc = True
                elif ch == '"':
                    in_str = False
            else:
                if ch == '"':
                    in_str = True
                elif ch == opening:
                    depth += 1
                elif ch == closing:
                    depth -= 1
                    if depth == 0:
                        j += 1
                        break
            j += 1

        if depth != 0:
            break

        block = s[i:j]
        try:
            obj = json.loads(block)
            blocks.append(obj)
        except Exception:
            pass
        i = j

    return blocks


def _merge_ohlcv_dict_blocks(blocks: List[dict]) -> dict:
    """Gộp nhiều dict kiểu {t,o,h,l,c,(v)} thành một dict duy nhất (append theo chiều dọc)."""
    keys = set().union(*[set(b.keys()) for b in blocks])
    merged: Dict[str, List[Any]] = {}
    for k in keys:
        buf: List[Any] = []
        for b in blocks:
            v = b.get(k, None)
            if isinstance(v, list):
                buf.extend(v)
            else:
                if k == "v":
                    buf.extend([None] * len(b.get("t", [])))
        if buf:
            merged[k] = buf
    return merged


def _as_dataframe(parsed: Any, raw_text: str) -> pd.DataFrame:
    """
    Đưa bất kỳ cấu trúc phổ biến nào về DataFrame:
    - dict-of-arrays {t,o,h,l,c,(v)}
    - list-of-dicts
    - list-of-lists (để pandas đoán)
    - CSV fallback
    """
    if parsed is not None:
        if isinstance(parsed, list) and parsed and all(isinstance(b, dict) and {"t","o","h","l","c"}.issubset(b.keys()) for b in parsed):
            parsed = _merge_ohlcv_dict_blocks(parsed)

        if isinstance(parsed, dict):
            if "data" in parsed:
                parsed = parsed["data"]
            if isinstance(parsed, dict) and {"t","o","h","l","c"}.issubset(parsed.keys()):
                n = len(parsed["t"])
                vol = parsed.get("v", [None]*n)
                return pd.DataFrame({
                    "t": parsed["t"], "o": parsed["o"], "h": parsed["h"],
                    "l": parsed["l"], "c": parsed["c"], "v": vol
                })
            try:
                return pd.DataFrame(parsed)
            except Exception:
                return pd.DataFrame([parsed])

        if isinstance(parsed, list):
            if not parsed:
                return pd.DataFrame()
            if isinstance(parsed[0], dict):
                return pd.DataFrame(parsed)
            return pd.DataFrame(parsed)

    try:
        return pd.read_csv(io.StringIO(raw_text))
    except Exception:
        return pd.DataFrame()


def _flatten_if_cell_is_list(df: pd.DataFrame) -> pd.DataFrame:
    """Nếu mỗi ô chứa list (ví dụ cột 't' là list epoch), flatten thành từng dòng."""
    if df.empty:
        return df
    cols = set(df.columns)
    tcol = _pick(cols, "t","time","timestamp","ts","date","dt")
    if tcol is None:
        return df

    first = df.iloc[0][tcol]
    if not isinstance(first, (list, tuple)):
        return df  # đã phẳng

    def chain(series):
        seqs = [x for x in series.dropna().tolist() if isinstance(x, (list, tuple))]
        return list(itertools.chain.from_iterable(seqs)) if seqs else []

    t = chain(df[tcol])
    n = len(t)

    def vals(name_candidates):
        c = _pick(set(df.columns), *name_candidates)
        if c is None:
            return [None]*n
        v = chain(df[c])
        return (v[:n] + [None]*max(0, n - len(v))) if v else [None]*n

    out = pd.DataFrame({
        "t": t,
        "o": vals(("o","open","Open")),
        "h": vals(("h","high","High")),
        "l": vals(("l","low","Low")),
        "c": vals(("c","close","Close")),
        "v": vals(("v","vol","volume","Volume")),
    })
    return out


def _pick(cols, *cands):
    for c in cands:
        if c in cols:
            return c
    return None


def _normalize_ohlcv_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Chuẩn hóa về cột: Date (datetime), Open, High, Low, Close, Volume
    - Tự nhận epoch giây/ms
    - KHÔNG đổi timezone
    """
    if df.empty:
        return pd.DataFrame(columns=["Date","Open","High","Low","Close","Volume"])

    ren = {}
    if "t" in df.columns: ren["t"] = "Date"
    if "time" in df.columns: ren["time"] = "Date"
    for a,b in [("o","Open"),("open","Open"),("h","High"),("high","High"),
                ("l","Low"),("low","Low"),("c","Close"),("close","Close"),
                ("v","Volume"),("vol","Volume"),("Volume","Volume")]:
        if a in df.columns:
            ren[a] = b
    df = df.rename(columns=ren)

    for col in ["Date","Open","High","Low","Close","Volume"]:
        if col not in df.columns:
            df[col] = pd.NA

    s = df["Date"]
    if pd.api.types.is_numeric_dtype(s):
        unit = "ms" if (s.dropna().astype("int64") > 1_000_000_000_000).any() else "s"
        # Kết quả là timezone-naive (không đổi UTC)
        df["Date"] = pd.to_datetime(s, unit=unit)
    else:
        df["Date"] = pd.to_datetime(s, errors="coerce")

    for col in ["Open","High","Low","Close","Volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["Date"]).sort_values("Date").reset_index(drop=True)
    return df[["Date","Open","High","Low","Close","Volume"]]


def _format_date_time_output(df: pd.DataFrame) -> pd.DataFrame:
    """
    Input: df có cột Date (datetime), Open/High/Low/Close/Volume
    Output: Date (YYYY-MM-DD), time (HH:MM:SS), Open.., volume (lowercase)
    KHÔNG đổi timezone; chỉ format từ datetime hiện có.
    """
    if df.empty:
        return pd.DataFrame(columns=["Date","time","Open","High","Low","Close","volume"])

    out = df.copy()
    out["Date"] = pd.to_datetime(out["Date"]).dt.strftime("%Y-%m-%d")
    out["time"] = pd.to_datetime(out["Date"] + " " + pd.to_datetime(df["Date"]).dt.strftime("%H:%M:%S")).dt.strftime("%H:%M:%S")
    # Cách trên đảm bảo "time" lấy từ phần giờ gốc; không chuyển TZ.

    if "Volume" in out.columns:
        out = out.rename(columns={"Volume": "volume"})

    for col in ["Open","High","Low","Close","volume"]:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")

    out = out[["Date","time","Open","High","Low","Close","volume"]]
    out = out.sort_values(["Date","time"], kind="mergesort").reset_index(drop=True)
    return out


def _extract_last_epoch(df_seg: pd.DataFrame) -> Optional[int]:
    """Lấy epoch giây cuối cùng của đoạn df_seg (sau normalize)."""
    if df_seg.empty:
        return None
    ns = pd.to_datetime(df_seg["Date"]).astype("int64").max()
    return int(ns // 1_000_000_000)


# ===================== Fetch từng trang thời gian =====================

def _fetch_segment(symbol: str, resolution: str, start_from: int, api_token: str) -> pd.DataFrame:
    """
    Gọi 1 request từ start_from -> 9999999999, trả về DataFrame đã normalize (có thể <=500 dòng).
    Parser chịu lỗi & flatten đầy đủ.
    """
    url = f"{_STOCKS_API_BASE}/{symbol}/ohlcv/{resolution}"
    params = {"from": start_from, "to": 9999999999}
    headers = {"accept": "application/json", "Authorization": api_token}

    r = requests.get(url, params=params, headers=headers, timeout=_TIMEOUT)
    r.raise_for_status()
    if not r.encoding:
        r.encoding = r.apparent_encoding

    try:
        parsed = r.json()
    except Exception:
        blocks = _scan_all_json_blocks(r.text)
        if blocks:
            if all(isinstance(b, dict) and {"t","o","h","l","c"}.issubset(b.keys()) for b in blocks):
                parsed = _merge_ohlcv_dict_blocks(blocks)
            else:
                parsed = blocks
        else:
            parsed = _json_relaxed(r.text)

    df = _as_dataframe(parsed, r.text)
    df = _flatten_if_cell_is_list(df)
    df = _normalize_ohlcv_df(df)
    return df


# ===================== Reorganized: Company & Finance =====================

class Company:
    """Company information via TCBS tcanalysis endpoints."""
    def __init__(self, symbol):
        self.symbol = symbol

    def overview(self):
        BASE = "https://apipubaws.tcbs.com.vn"; ANALYSIS = "tcanalysis"
        url = f"{BASE}/{ANALYSIS}/v1/ticker/{self.symbol}/overview"
        data = send_request(url)
        return pd.DataFrame(data, index=[0])

    def profile(self):
        BASE = "https://apipubaws.tcbs.com.vn"; ANALYSIS = "tcanalysis"
        url = f"{BASE}/{ANALYSIS}/v1/company/{self.symbol}/overview"
        data = send_request(url)
        return pd.json_normalize(data)

    def shareholders(self, page_size=50, page=0):
        BASE = "https://apipubaws.tcbs.com.vn"; ANALYSIS = "tcanalysis"
        url = f"{BASE}/{ANALYSIS}/v1/company/{self.symbol}/large-share-holders"
        data = send_request(url, params={"page":page, "size":page_size})
        items = (data or {}).get("listShareHolder", [])
        return pd.json_normalize(items)

    def officers(self, page_size=50, page=0):
        BASE = "https://apipubaws.tcbs.com.vn"; ANALYSIS = "tcanalysis"
        url = f"{BASE}/{ANALYSIS}/v1/company/{self.symbol}/key-officers"
        data = send_request(url, params={"page":page, "size":page_size})
        items = (data or {}).get("listKeyOfficer", [])
        return pd.json_normalize(items)

    def subsidiaries(self, page_size=100, page=0):
        BASE = "https://apipubaws.tcbs.com.vn"; ANALYSIS = "tcanalysis"
        url = f"{BASE}/{ANALYSIS}/v1/company/{self.symbol}/sub-companies"
        data = send_request(url, params={"page":page, "size":page_size})
        items = (data or {}).get("listSubCompany", [])
        return pd.json_normalize(items)

    def events(self, page_size=15, page=0):
        BASE = "https://apipubaws.tcbs.com.vn"; ANALYSIS = "tcanalysis"
        url = f"{BASE}/{ANALYSIS}/v1/ticker/{self.symbol}/events-news"
        data = send_request(url, params={"page":page, "size":page_size})
        items = (data or {}).get("listEventNews", [])
        return pd.DataFrame(items)

    def news(self, page_size=15, page=0):
        BASE = "https://apipubaws.tcbs.com.vn"; ANALYSIS = "tcanalysis"
        url = f"{BASE}/{ANALYSIS}/v1/ticker/{self.symbol}/activity-news"
        data = send_request(url, params={"page":page, "size":page_size})
        items = (data or {}).get("listActivityNews", [])
        return pd.DataFrame(items)

    def ratio_summary(self):
        BASE = "https://apipubaws.tcbs.com.vn"; ANALYSIS = "tcanalysis"
        url = f"{BASE}/{ANALYSIS}/v1/ticker/{self.symbol}/ratios"
        try:
            data = send_request(url)
            return pd.DataFrame(data, index=[0]) if isinstance(data, dict) else pd.DataFrame(data)
        except Exception:
            url2 = f"{BASE}/{ANALYSIS}/v1/finance/{self.symbol}/financialratio"
            data = send_request(url2)
            return pd.DataFrame(data)


FIN_MAP = {'income_statement':'incomestatement','balance_sheet':'balancesheet','cash_flow':'cashflow'}
PERIOD_MAP = {'year':1, 'quarter':0}

class Finance:
    """Financial statements via TCBS."""
    def __init__(self, symbol):
        self.symbol = symbol

    def _fetch(self, report, period='year', lang='vi', dropna=False):
        BASE = "https://apipubaws.tcbs.com.vn"; ANALYSIS = "tcanalysis"
        assert report in FIN_MAP, f"Invalid report: {report}"
        url = f"{BASE}/{ANALYSIS}/v1/finance/{self.symbol}/{FIN_MAP[report]}"
        params = {"period": PERIOD_MAP.get(period, 1), "size": 1000}
        data = send_request(url, params=params)
        df = pd.DataFrame(data)
        if dropna:
            df = df.dropna(axis=1, how="all")
        return df

    def income_statement(self, period='year', lang='vi', dropna=False):
        return self._fetch('income_statement', period, lang, dropna)

    def balance_sheet(self, period='year', lang='vi', dropna=False):
        return self._fetch('balance_sheet', period, lang, dropna)

    def cash_flow(self, period='year', lang='vi', dropna=False):
        return self._fetch('cash_flow', period, lang, dropna)


# ===================== Reorganized: Fund =====================

class Fund:
    """Mutual funds via Fmarket."""

    def __init__(self):
        pass

    def listing(self, fund_type: str = "") -> pd.DataFrame:
        BASE = "https://api.fmarket.vn/res/products"
        url = f"{BASE}/filter"
        payload = {
            "types": ["NEW_FUND", "TRADING_FUND"],
            "issuerIds": [],
            "sortOrder": "DESC",
            "sortField": "navTo6Months",
            "page": 1,
            "pageSize": 500,
            "isIpo": False,
            "fundAssetTypes": [] if not fund_type else [fund_type],
            "bondRemainPeriods": [],
            "searchField": "",
            "isBuyByReward": False,
            "thirdAppIds": [],
        }
        try:
            data = send_request(url, method="POST", payload=payload)
            rows = (data or {}).get("data", {}).get("rows", [])
            df = pd.json_normalize(rows)
            return df
        except Exception:
            data = send_request(f"{BASE}/public", params={"page": 1, "size": 500})
            df = pd.json_normalize((data or {}).get("data", []))
            if fund_type and "dataFundAssetType.name" in df.columns:
                df = df[df["dataFundAssetType.name"].eq(fund_type)]
            return df

    def filter(self, q: str) -> pd.DataFrame:
        df = self.listing()
        if df.empty:
            return df
        mask = False
        for col in [c for c in ["name", "shortName"] if c in df.columns]:
            mask = mask | df[col].astype(str).str.contains(q, case=False, na=False)
        return df[mask]

    @staticmethod
    def _resolve_candidates(code_or_id: str) -> list[str]:
        cands = []
        key = str(code_or_id).strip()
        if key:
            cands.append(key)
        try:
            _df = Fund().listing()
            if not _df.empty:
                cols = _df.columns
                def _add(val):
                    if val is None:
                        return
                    s = str(val).strip()
                    if s and s not in cands:
                        cands.append(s)
                if "code" in cols and _df["code"].notna().any():
                    m = _df["code"].astype(str).str.upper().eq(key.upper())
                    if m.any():
                        r = _df[m].iloc[0]
                        for k in ["code", "id", "vsdFeeId"]:
                            if k in cols:
                                _add(r.get(k))
                if "id" in cols and _df["id"].notna().any():
                    m = _df["id"].astype(str).eq(key)
                    if m.any():
                        r = _df[m].iloc[0]
                        for k in ["code", "id", "vsdFeeId"]:
                            if k in cols:
                                _add(r.get(k))
                if "vsdFeeId" in cols and _df["vsdFeeId"].notna().any():
                    m = _df["vsdFeeId"].astype(str).eq(key)
                    if m.any():
                        r = _df[m].iloc[0]
                        for k in ["code", "id", "vsdFeeId"]:
                            if k in cols:
                                _add(r.get(k))
        except Exception:
            pass
        return cands

    @staticmethod
    def _try_paths(paths: list[str]) -> pd.DataFrame:
        for url in paths:
            try:
                data = send_request(url)
                if isinstance(data, list):
                    return pd.DataFrame(data)
                return pd.json_normalize(data)
            except Exception:
                continue
        return pd.DataFrame()

    class details:
        @staticmethod
        def nav_report(code_or_id: str) -> pd.DataFrame:
            BASE = "https://api.fmarket.vn/res/products"
            cands = Fund._resolve_candidates(code_or_id)
            paths = (
                [f"{BASE}/public/{c}/nav-report" for c in cands]
                + [f"{BASE}/{c}/nav-report" for c in cands]
            )
            return Fund._try_paths(paths)

        @staticmethod
        def top_holding(code_or_id: str) -> pd.DataFrame:
            BASE = "https://api.fmarket.vn/res/products"
            cands = Fund._resolve_candidates(code_or_id)
            paths = (
                [f"{BASE}/public/{c}/top-holding" for c in cands]
                + [f"{BASE}/{c}/top-holding" for c in cands]
            )
            return Fund._try_paths(paths)

        @staticmethod
        def industry_holding(code_or_id: str) -> pd.DataFrame:
            BASE = "https://api.fmarket.vn/res/products"
            cands = Fund._resolve_candidates(code_or_id)
            paths = (
                [f"{BASE}/public/{c}/industry-holding" for c in cands]
                + [f"{BASE}/{c}/industry-holding" for c in cands]
            )
            return Fund._try_paths(paths)

        @staticmethod
        def asset_holding(code_or_id: str) -> pd.DataFrame:
            BASE = "https://api.fmarket.vn/res/products"
            cands = Fund._resolve_candidates(code_or_id)
            paths = (
                [f"{BASE}/public/{c}/asset-holding" for c in cands]
                + [f"{BASE}/{c}/asset-holding" for c in cands]
            )
            return Fund._try_paths(paths)


# ===================== Reorganized: Listing =====================

class Listing:
    def __init__(self, source='VCI'):
        self.source = source

    def all_symbols(self):
        # Try to use liquid asset list if available
        try:
            df = list_liquid_asset()
            if not df.empty:
                cols = set(df.columns)
                sym_col = "symbol" if "symbol" in cols else ("ticker" if "ticker" in cols else None)
                ex_col = "exchange" if "exchange" in cols else None
                if sym_col:
                    out = pd.DataFrame({
                        "symbol": df[sym_col].astype(str),
                        "short_name": df.get("short_name", pd.Series([None]*len(df))),
                        "exchange": df[ex_col] if ex_col in df.columns else pd.Series([None]*len(df)),
                    })
                    return out.dropna(subset=["symbol"]).reset_index(drop=True)
        except Exception:
            pass
        # Fallback minimal known set
        return pd.DataFrame([
            {"symbol": "HPG", "short_name": "HoaPhat", "exchange": "HOSE"},
            {"symbol": "VIC", "short_name": "Vingroup", "exchange": "HOSE"},
            {"symbol": "VNM", "short_name": "Vinamilk", "exchange": "HOSE"},
        ])

    def symbols_by_exchange(self):
        df = self.all_symbols()
        if not df.empty and "exchange" in df.columns:
            out: dict[str, list[str]] = {"HOSE": [], "HNX": [], "UPCOM": []}
            for ex, g in df.groupby(df["exchange"].fillna("HOSE")):
                if ex in out:
                    out[ex] = g["symbol"].astype(str).dropna().unique().tolist()
            return out
        return {"HOSE": ["HPG", "VIC", "VNM"], "HNX": [], "UPCOM": []}

    def symbols_by_group(self, group='VN30'):
        return []

    def symbols_by_industries(self):
        return pd.DataFrame(columns=["symbol","icb_industry"])

    def industries_icb(self):
        return pd.DataFrame(columns=["icb_code","icb_name"])


# ===================== Reorganized: Market Quote (VCI) =====================

class Quote:
    """Market data via VCI: OHLCV history, intraday tick, price depth."""

    def __init__(self, symbol, source="VCI"):
        self.symbol = symbol
        self.source = source

    def _estimate_countback(self, start_dt, end_dt, interval):
        if interval in ["1D", "1W", "1M"]:
            if interval == "1D":
                return max(1, (end_dt.date() - start_dt.date()).days + 1)
            if interval == "1W":
                return max(1, ((end_dt.date() - start_dt.date()).days // 7) + 1)
            return max(1, (end_dt.year - start_dt.year) * 12 + (end_dt.month - start_dt.month) + 1)
        if interval == "1H":
            return max(1, int((end_dt - start_dt).total_seconds() // 3600) + 1)
        step = {"1m": 1, "5m": 5, "15m": 15, "30m": 30}[interval]
        return max(1, int((end_dt - start_dt).total_seconds() // 60) // step + 1)

    def history(self, start, end=None, interval="1D"):
        assert interval in INTERVAL_MAP, f"Unsupported interval: {interval}"
        start_dt = dt.datetime.strptime(start, "%Y-%m-%d")
        end_dt = (
            dt.datetime.utcnow() + pd.Timedelta(days=1)
            if end is None else
            (dt.datetime.strptime(end, "%Y-%m-%d") + pd.Timedelta(days=1))
        )
        count_back = self._estimate_countback(start_dt, end_dt, interval)
        payload = {
            "timeFrame": INTERVAL_MAP[interval],
            "symbols": [self.symbol],
            "to": int(end_dt.timestamp()),
            "countBack": count_back
        }
        data = send_request(TRADING_URL + CHART_URL, method="POST", payload=payload)
        arr = data[0] if isinstance(data, list) and data else []
        if not arr:
            return pd.DataFrame(columns=["time", "open", "high", "low", "close", "volume"])

        df = pd.DataFrame(arr)[OHLC_COLUMNS].rename(columns=OHLC_RENAME)
        ts = pd.to_numeric(df["time"], errors="coerce")
        df["time"] = pd.to_datetime(ts, unit="s")
        df = df[df["time"] >= start_dt].reset_index(drop=True)
        return df

    def intraday(self, page_size=100, last_time=None):
        url = f"{TRADING_URL}{INTRADAY_URL}/LEData/getAll"
        payload = {"symbol": self.symbol, "limit": int(page_size), "truncTime": last_time}
        data = send_request(url, method="POST", payload=payload)
        if not data:
            return pd.DataFrame(columns=list(INTRADAY_MAP.values()))

        df = pd.DataFrame(data)
        cols = list(INTRADAY_MAP.keys())
        df = df[cols].rename(columns=INTRADAY_MAP)

        vals = pd.to_numeric(df["time"], errors="coerce")
        if vals.notna().any():
            unit = "ms" if vals.dropna().astype("int64").gt(10**12).any() else "s"
            df["time"] = pd.to_datetime(vals, unit=unit)
        else:
            df["time"] = pd.to_datetime(df["time"], errors="coerce")

        return df

    def price_depth(self):
        data = send_request(PRICE_DEPTH_URL, method="POST", payload={"symbol": self.symbol})
        if not data:
            return pd.DataFrame(columns=["price", "acc_volume", "acc_buy_volume", "acc_sell_volume", "acc_undefined_volume"])
        df = pd.DataFrame(data)
        df = df[[
            "priceStep",
            "accumulatedVolume",
            "accumulatedBuyVolume",
            "accumulatedSellVolume",
            "accumulatedUndefinedVolume"
        ]]
        return df.rename(columns={
            "priceStep": "price",
            "accumulatedVolume": "acc_volume",
            "accumulatedBuyVolume": "acc_buy_volume",
            "accumulatedSellVolume": "acc_sell_volume",
            "accumulatedUndefinedVolume": "acc_undefined_volume"
        })


# ===================== Reorganized: Global quotes (MSN/Yahoo) =====================

MSN_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "https://www.msn.com",
    "Referer": "https://www.msn.com/en-us/money",
}

CURRENCY_ID = {
    "USDVND": "avyufr",
    "JPYVND": "ave8sm",
    "EURUSD": "av932w",
    "USDCNY": "avym77",
    "USDKRW": "avyoyc",
}
CRYPTO_ID = {"BTC": "c2111", "ETH": "c2112", "USDT": "c2115", "BNB": "c2113", "ADA": "c2114", "SOL": "c2116"}
INDICES_ID = {"DJI": "a6qja2", "INX": "a33k6h", "COMP": "a3oxnm", "N225": "a9j7bh", "VNI": "aqk2nm"}
Y_INDICES = {"DJI": "^DJI", "INX": "^GSPC", "COMP": "^IXIC", "N225": "^N225", "VNI": "^VNINDEX"}
Y_CRYPTO = {"BTC": "BTC-USD", "ETH": "ETH-USD", "BNB": "BNB-USD", "ADA": "ADA-USD", "SOL": "SOL-USD"}

def _normalize_df_global(df: pd.DataFrame) -> pd.DataFrame:
    for col in ["time", "open", "high", "low", "close", "volume"]:
        if col not in df.columns:
            df[col] = None
    return df[["time", "open", "high", "low", "close", "volume"]].reset_index(drop=True)

def _chart_msn(symbol_id, start=None, end=None, interval="1D") -> pd.DataFrame:
    BASE = "https://assets.msn.com/service/Finance"
    url = f"{BASE}/Charts/TimeRange"
    params = {
        "ids": symbol_id,
        "type": "All",
        "timeframe": 1,
        "wrapodata": "false",
        "ocid": "finance-utils-peregrine",
        "cm": "en-us",
        "it": "web",
        "scn": "ANON",
    }
    data = send_request(url, params=params, headers=MSN_HEADERS)
    series = None
    if isinstance(data, list) and data and isinstance(data[0], dict):
        series = data[0].get("series") or (data[0].get("charts", [{}])[0].get("series") if data[0].get("charts") else None)
    elif isinstance(data, dict):
        series = data.get("series") or (data.get("charts", [{}])[0].get("series") if data.get("charts") else None)
    if not series:
        return pd.DataFrame(columns=["time", "open", "high", "low", "close", "volume"])
    if isinstance(series, list):
        df = pd.DataFrame(series)
    else:
        df = pd.DataFrame([series])
    rename = {
        "timeStamps": "time",
        "openPrices": "open",
        "pricesHigh": "high",
        "pricesLow": "low",
        "prices": "close",
        "volumes": "volume",
    }
    df.rename(columns={k: v for k, v in rename.items() if k in df.columns}, inplace=True)
    for col in ["time", "open", "high", "low", "close", "volume"]:
        if col in df.columns and df[col].apply(lambda x: isinstance(x, (list, tuple))).any():
            df = df.explode(col)
    df["time"] = pd.to_numeric(df.get("time"), errors="coerce")
    df["time"] = pd.to_datetime(df["time"], unit="s", errors="coerce")
    return _normalize_df_global(df)

def _yahoo_symbol(kind: str, symbol: str) -> list[str]:
    if kind == "fx":
        return [f"{symbol}=X", f"{symbol[:3]}{symbol[3:]}=X"]
    if kind == "crypto":
        return [Y_CRYPTO.get(symbol, f"{symbol}-USD")]
    if kind == "index":
        return [Y_INDICES.get(symbol, symbol)]
    return [symbol]

def _interval_map_yahoo(interval: str) -> tuple[str, str]:
    if interval in ("1m", "5m", "15m", "30m", "60m", "1H"):
        return ("1mo", "1m")
    if interval in ("1W",):
        return ("6mo", "1d")
    if interval in ("1M",):
        return ("2y", "1d")
    return ("1y", "1d")

def _chart_yahoo(kind: str, symbol: str, start=None, end=None, interval="1D") -> pd.DataFrame:
    rng, itv = _interval_map_yahoo(interval)
    for ysym in _yahoo_symbol(kind, symbol):
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ysym}"
            params = {"range": rng, "interval": itv, "includePrePost": "false", "events": "div,splits"}
            data = send_request(url, params=params, headers={
                "User-Agent": MSN_HEADERS["User-Agent"],
                "Accept": "application/json, text/plain, */*",
            })
            res = (data or {}).get("chart", {}).get("result", [])
            if not res:
                continue
            r0 = res[0]
            ts = r0.get("timestamp", []) or r0.get("meta", {}).get("regularTradingPeriod", [])
            ind = r0.get("indicators", {})
            q = (ind.get("quote") or [{}])[0]
            df = pd.DataFrame({
                "time": pd.to_datetime(ts, unit="s", errors="coerce"),
                "open": q.get("open"),
                "high": q.get("high"),
                "low": q.get("low"),
                "close": q.get("close"),
                "volume": q.get("volume"),
            })
            if start:
                df = df[df["time"] >= pd.to_datetime(start)]
            if end:
                df = df[df["time"] <= pd.to_datetime(end)]
            if not df.empty:
                return _normalize_df_global(df)
        except Exception:
            continue
    return pd.DataFrame(columns=["time", "open", "high", "low", "close", "volume"])

class _Wrap:
    def __init__(self, id_map, kind: str):
        self.id_map = id_map
        self.kind = kind

    class _Quote:
        def __init__(self, sid, kind, raw_symbol):
            self.sid = sid
            self.kind = kind
            self.raw_symbol = raw_symbol

        def history(self, start, end, interval="1D"):
            try:
                df = _chart_msn(self.sid, start, end, interval)
                if df is not None and not df.empty:
                    return df
            except Exception:
                pass
            return _chart_yahoo(self.kind, self.raw_symbol, start, end, interval)

    def __call__(self, symbol):
        sid = self.id_map.get(symbol)
        return type("Obj", (), {"quote": self._Quote(sid, self.kind, symbol)})()

class FX:
    def __init__(self):
        self._wrap = _Wrap(CURRENCY_ID, "fx")
    def __call__(self, symbol):
        return self._wrap(symbol)

class Crypto:
    def __init__(self):
        self._wrap = _Wrap(CRYPTO_ID, "crypto")
    def __call__(self, symbol):
        return self._wrap(symbol)

class WorldIndex:
    def __init__(self):
        self._wrap = _Wrap(INDICES_ID, "index")
    def __call__(self, symbol):
        return self._wrap(symbol)

class Global:
    def fx(self, symbol):
        return FX()(symbol)
    def crypto(self, symbol):
        return Crypto()(symbol)
    def world_index(self, symbol):
        return WorldIndex()(symbol)

class MSN(Global):
    pass


# ===================== Reorganized: quant-data (indices, stocks) =====================

class APIError(Exception):
    pass

QUANT_BASE_URL = "https://api-v2.xno.vn/quant-data"

def _get_auth_header() -> Dict[str, str]:
    try:
        api_key = Config.get_api_key()
        return {"Authorization": api_key}
    except Exception as e:
        raise APIError("API key not configured. Use client(apikey='xd_...') first.") from e

def _to_unix_timestamp(timestamp: Union[int, float, str, dt.datetime]) -> int:
    if isinstance(timestamp, (int, float)):
        return int(timestamp)
    if isinstance(timestamp, str):
        dt_obj = dt.datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return int(dt_obj.timestamp())
    if isinstance(timestamp, dt.datetime):
        if timestamp.tzinfo is None:
            return int(timestamp.replace(tzinfo=dt.timezone.utc).timestamp())
        return int(timestamp.astimezone(dt.timezone.utc).timestamp())
    raise TypeError(f"Unsupported timestamp type: {type(timestamp)}")

def _make_request(url: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
    headers = _get_auth_header()
    try:
        response = requests.get(url, headers=headers, params=params, timeout=_TIMEOUT)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        raise APIError(f"Request failed: {e}") from e

def _parse_json_response(response: requests.Response) -> Any:
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
    if not data:
        return pd.DataFrame(columns=columns)
    if isinstance(data, dict) and all(isinstance(v, list) for v in data.values()):
        df_data = {col: data.get(col, []) for col in columns}
        return pd.DataFrame(df_data)
    if isinstance(data, dict):
        return pd.DataFrame([data])
    if isinstance(data, list):
        return pd.DataFrame(data)
    return pd.DataFrame()

def _chunk_time_range(start_ts: int, end_ts: int, chunk_seconds: int):
    current = start_ts
    while current < end_ts:
        next_ts = min(current + chunk_seconds, end_ts)
        yield current, next_ts
        current = next_ts

def ping() -> bool:
    try:
        url = f"{QUANT_BASE_URL}/v1/ping"
        response = requests.get(url, timeout=5)
        return response.ok
    except requests.RequestException:
        return False

def get_indices() -> pd.DataFrame:
    url = f"{QUANT_BASE_URL}/v1/indices"
    response = _make_request(url)
    data = _parse_json_response(response)
    return _create_dataframe_with_columns(data, columns=['symbol', 'name'])

def get_market_index_snapshot(index_symbol: str) -> pd.DataFrame:
    index_symbol = (index_symbol or "").strip().upper()
    url = f"{QUANT_BASE_URL}/v1/indices/{index_symbol}/market-index"
    response = _make_request(url)
    data = _parse_json_response(response)
    return pd.DataFrame([data])

def get_stock_foreign_trading(symbol: str) -> pd.DataFrame:
    symbol = (symbol or "").strip().upper()
    url = f"{QUANT_BASE_URL}/v1/stocks/{symbol}/foreign-trading"
    response = _make_request(url)
    data = _parse_json_response(response)
    return pd.DataFrame([data])

def get_stock_matches(symbol: str) -> pd.DataFrame:
    symbol = (symbol or "").strip().upper()
    url = f"{QUANT_BASE_URL}/v1/stocks/{symbol}/matches"
    response = _make_request(url)
    data = _parse_json_response(response)
    return _create_dataframe_with_columns(data, columns=['time', 'symbol', 'price', 'volume', 'side'])

# get_stock_ohlcv removed — use get_hist for intraday/hourly or chart sources directly

def get_stock_info(symbol: str) -> pd.DataFrame:
    symbol = (symbol or "").strip().upper()
    url = f"{QUANT_BASE_URL}/v1/stocks/{symbol}/stock-info"
    response = _make_request(url)
    data = _parse_json_response(response)
    return pd.DataFrame([data])

def get_stock_top_price(symbol: str) -> pd.DataFrame:
    symbol = (symbol or "").strip().upper()
    url = f"{QUANT_BASE_URL}/v1/stocks/{symbol}/top-price"
    try:
        response = _make_request(url)
        data = _parse_json_response(response)
        return pd.DataFrame([data])
    except APIError:
        return pd.DataFrame()


# ===================== Reorganized: Trading =====================

_PRICEBOARD_QUERY = """
query PriceBoard($tickers:[String!]){
  priceBoard(tickers:$tickers){
    ticker open_price ceiling_price floor_price reference_price
    highest_price lowest_price price_change percent_price_change
    foreign_total_volume foreign_total_room foreign_holding_room
    average_match_volume2_week
  }
}
"""

class Trading:
    @staticmethod
    def _fallback(symbols):
        rows = []
        now = pd.Timestamp.utcnow()
        start = (now - pd.Timedelta(days=10)).strftime("%Y-%m-%d")
        end = now.strftime("%Y-%m-%d")
        for sym in symbols:
            try:
                q = Quote(sym)
                tick = q.intraday(page_size=1)
                price = float(tick["price"].iloc[0]) if not tick.empty else None
                hist = q.history(start=start, end=end, interval="1D")
                if len(hist) >= 2:
                    ref = float(hist["close"].iloc[-2])
                elif len(hist) == 1:
                    ref = float(hist["close"].iloc[-1])
                else:
                    ref = None
                change = (
                    (price - ref) if (price is not None and ref is not None) else None
                )
                pct = (
                    (change / ref * 100.0)
                    if (change is not None and ref not in (None, 0))
                    else None
                )
                rows.append(
                    {
                        "symbol": sym,
                        "open": None,
                        "ceiling": None,
                        "floor": None,
                        "ref_price": ref,
                        "high": None,
                        "low": None,
                        "price_change": change,
                        "price_change_pct": pct,
                        "foreign_volume": None,
                        "foreign_room": None,
                        "foreign_holding_room": None,
                        "avg_match_volume_2w": None,
                    }
                )
            except Exception:
                rows.append(
                    {
                        "symbol": sym,
                        "open": None,
                        "ceiling": None,
                        "floor": None,
                        "ref_price": None,
                        "high": None,
                        "low": None,
                        "price_change": None,
                        "price_change_pct": None,
                        "foreign_volume": None,
                        "foreign_room": None,
                        "foreign_holding_room": None,
                        "avg_match_volume_2w": None,
                    }
                )
        return pd.DataFrame(rows)

    @staticmethod
    def price_board(symbols):
        payload = {
            "operationName": "PriceBoard",
            "query": _PRICEBOARD_QUERY,
            "variables": {"tickers": list(symbols)},
        }
        try:
            data = send_request(
                GRAPHQL_URL,
                method="POST",
                headers={"Content-Type": "application/json"},
                payload=payload,
            )
            rows = (data or {}).get("data", {}).get("priceBoard", [])
            if rows:
                df = pd.DataFrame(rows).rename(columns=PRICE_INFO_MAP)
                return df
        except Exception:
            pass
        return Trading._fallback(symbols)


# ===================== Public: get_hist =====================

def get_hist(asset_name: str, resolution: str = "m") -> pd.DataFrame:
    """
    Lấy toàn bộ OHLCV theo khung thời gian 'm' hoặc 'h', KHÔNG còn giới hạn ~500 dòng.
    - Input:
        asset_name: ví dụ "HPG"
        resolution: "m" (phút) hoặc "h" (giờ)  [mặc định: "m"]
    - Output:
        DataFrame ["Date","time","Open","High","Low","Close","volume"]
        (Date/time là string format từ datetime hiện có; KHÔNG đổi timezone)
    """
    if not isinstance(asset_name, str) or not asset_name.strip():
        raise ValueError("asset_name phải là chuỗi hợp lệ (ví dụ: 'HPG').")
    res = (resolution or "m").lower()
    if res not in {"m", "h"}:
        raise ValueError("resolution chỉ được phép 'm' hoặc 'h'.")

    token = Config.get_api_key()
    symbol = asset_name.strip().upper()

    step = 60 if res == "m" else 3600  # giây
    frames: List[pd.DataFrame] = []

    current_from = 0
    last_epoch_seen = -1
    requests_made = 0

    while requests_made < _MAX_REQUESTS:
        seg = _fetch_segment(symbol, res, current_from, token)
        requests_made += 1

        if seg.empty:
            break

        frames.append(seg)

        seg_last = _extract_last_epoch(seg)
        if seg_last is None:
            break

        if seg_last <= last_epoch_seen:
            break

        last_epoch_seen = seg_last
        current_from = seg_last + step

        # Nếu segment nhỏ hơn 500 thì có thể đã gần cuối; vẫn cho vòng lặp tự kết thúc khi hết dữ liệu

    if not frames:
        return pd.DataFrame(columns=["Date","time","Open","High","Low","Close","volume"])

    df = pd.concat(frames, ignore_index=True)
    df = df.drop_duplicates(subset=["Date"], keep="last")
    df = df.sort_values("Date").reset_index(drop=True)

    # Xuất theo định dạng yêu cầu (KHÔNG đổi timezone)
    df = _format_date_time_output(df)
    return df
