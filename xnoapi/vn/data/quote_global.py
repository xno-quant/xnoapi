import time
import pandas as pd
from .core import send_request

BASE = "https://assets.msn.com/service/Finance"

# Headers giống trình duyệt để MSN bớt trả 401
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

# Map MSN symbol_id
CURRENCY_ID = {
    "USDVND": "avyufr",
    "JPYVND": "ave8sm",
    "EURUSD": "av932w",
    "USDCNY": "avym77",
    "USDKRW": "avyoyc",
}
CRYPTO_ID = {"BTC": "c2111", "ETH": "c2112", "USDT": "c2115", "BNB": "c2113", "ADA": "c2114", "SOL": "c2116"}
INDICES_ID = {"DJI": "a6qja2", "INX": "a33k6h", "COMP": "a3oxnm", "N225": "a9j7bh", "VNI": "aqk2nm"}

# Yahoo fallback map (chủ yếu để chắc ăn tên chỉ số/crypto)
Y_INDICES = {"DJI": "^DJI", "INX": "^GSPC", "COMP": "^IXIC", "N225": "^N225", "VNI": "^VNINDEX"}
Y_CRYPTO = {"BTC": "BTC-USD", "ETH": "ETH-USD", "BNB": "BNB-USD", "ADA": "ADA-USD", "SOL": "SOL-USD"}

def _normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    # Trả về đúng cột chuẩn
    for col in ["time", "open", "high", "low", "close", "volume"]:
        if col not in df.columns:
            df[col] = None
    return df[["time", "open", "high", "low", "close", "volume"]].reset_index(drop=True)

# ---------- MSN primary ----------
def _chart_msn(symbol_id, start=None, end=None, interval="1D") -> pd.DataFrame:
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

    # series có thể là list các điểm hoặc dict các mảng
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

    # explode nếu cột là mảng
    for col in ["time", "open", "high", "low", "close", "volume"]:
        if col in df.columns and df[col].apply(lambda x: isinstance(x, (list, tuple))).any():
            df = df.explode(col)

    # chuẩn hoá time (epoch seconds)
    df["time"] = pd.to_numeric(df.get("time"), errors="coerce")
    df["time"] = pd.to_datetime(df["time"], unit="s", errors="coerce")

    return _normalize_df(df)

# ---------- Yahoo fallback ----------
def _yahoo_symbol(kind: str, symbol: str) -> list[str]:
    if kind == "fx":
        # Thử 'USDVND=X' dạng chuẩn YF
        return [f"{symbol}=X", f"{symbol[:3]}{symbol[3:]}=X"]
    if kind == "crypto":
        return [Y_CRYPTO.get(symbol, f"{symbol}-USD")]
    if kind == "index":
        return [Y_INDICES.get(symbol, symbol)]
    return [symbol]

def _interval_map_yahoo(interval: str) -> tuple[str, str]:
    # map interval đơn giản cho YF
    if interval in ("1m", "5m", "15m", "30m", "60m", "1H"):
        return ("1mo", "1m")  # range, interval
    if interval in ("1W",):
        return ("6mo", "1d")
    if interval in ("1M",):
        return ("2y", "1d")
    # mặc định ngày
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
            # Lọc theo start/end nếu có
            if start:
                df = df[df["time"] >= pd.to_datetime(start)]
            if end:
                df = df[df["time"] <= pd.to_datetime(end)]
            if not df.empty:
                return _normalize_df(df)
        except Exception:
            continue
    return pd.DataFrame(columns=["time", "open", "high", "low", "close", "volume"])

# ---------- Public API ----------
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
            # Thử MSN trước, nếu lỗi/không có thì fallback Yahoo
            try:
                df = _chart_msn(self.sid, start, end, interval)
                if df is not None and not df.empty:
                    return df
            except Exception:
                pass
            # Fallback Yahoo
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
