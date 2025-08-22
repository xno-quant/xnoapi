import pandas as pd

from .const import GRAPHQL_URL, PRICE_INFO_MAP
from .core import send_request
from .quote_market import Quote

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
        # Lấy nhanh snapshot: last tick + tham chiếu từ lịch sử gần nhất
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
        # Thử GraphQL trước
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
            pass  # rơi xuống fallback

        # Fallback an toàn nếu GraphQL bị 400 / đổi schema / cần cookie
        return Trading._fallback(symbols)
