import datetime
import pandas as pd
from .const import (
    TRADING_URL, CHART_URL, INTRADAY_URL,
    INTERVAL_MAP, INTRADAY_MAP, OHLC_COLUMNS, OHLC_RENAME,
    PRICE_DEPTH_URL
)
from .core import send_request


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
            # 1M: xấp xỉ theo số tháng
            return max(1, (end_dt.year - start_dt.year) * 12 + (end_dt.month - start_dt.month) + 1)
        if interval == "1H":
            return max(1, int((end_dt - start_dt).total_seconds() // 3600) + 1)
        step = {"1m": 1, "5m": 5, "15m": 15, "30m": 30}[interval]
        return max(1, int((end_dt - start_dt).total_seconds() // 60) // step + 1)

    def history(self, start, end=None, interval="1D"):
        assert interval in INTERVAL_MAP, f"Unsupported interval: {interval}"
        start_dt = datetime.datetime.strptime(start, "%Y-%m-%d")
        end_dt = (
            datetime.datetime.utcnow() + pd.Timedelta(days=1)
            if end is None else
            (datetime.datetime.strptime(end, "%Y-%m-%d") + pd.Timedelta(days=1))
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
        # 🔧 Fix FutureWarning: ép numeric trước khi to_datetime(unit='s')
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

        # 🔧 Chuẩn hoá time: ưu tiên epoch (ms/s), fallback ISO string
        vals = pd.to_numeric(df["time"], errors="coerce")
        if vals.notna().any():
            # nếu có giá trị > 1e12 → epoch milliseconds, ngược lại seconds
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
