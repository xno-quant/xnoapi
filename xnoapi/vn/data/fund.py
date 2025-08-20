import pandas as pd
from .core import send_request

BASE = "https://api.fmarket.vn/res/products"


class Fund:
    """Mutual funds via Fmarket."""

    def __init__(self):
        pass

    def listing(self, fund_type: str = "") -> pd.DataFrame:
        """
        Liệt kê quỹ mở. Ưu tiên POST /filter (chuẩn Fmarket), fallback GET /public.
        fund_type: 'BALANCED' | 'BOND' | 'STOCK' | '' (tất cả)
        """
        # Thử API filter (chuẩn, nhiều trường hơn)
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
            # Fallback: public listing
            data = send_request(f"{BASE}/public", params={"page": 1, "size": 500})
            df = pd.json_normalize((data or {}).get("data", []))
            if fund_type and "dataFundAssetType.name" in df.columns:
                df = df[df["dataFundAssetType.name"].eq(fund_type)]
            return df

    def filter(self, q: str) -> pd.DataFrame:
        """
        Lọc quỹ theo chuỗi q trong name/shortName.
        """
        df = self.listing()
        if df.empty:
            return df
        mask = False
        for col in [c for c in ["name", "shortName"] if c in df.columns]:
            mask = mask | df[col].astype(str).str.contains(q, case=False, na=False)
        return df[mask]

    # ---------------- details helpers ----------------

    @staticmethod
    def _resolve_candidates(code_or_id: str) -> list[str]:
        """
        Tạo danh sách candidate id cho endpoint details:
        [input, code, id, vsdFeeId] (không trùng lặp).
        """
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

                # match by code (string, case-insensitive)
                if "code" in cols and _df["code"].notna().any():
                    m = _df["code"].astype(str).str.upper().eq(key.upper())
                    if m.any():
                        r = _df[m].iloc[0]
                        for k in ["code", "id", "vsdFeeId"]:
                            if k in cols:
                                _add(r.get(k))

                # match by id (exact)
                if "id" in cols and _df["id"].notna().any():
                    m = _df["id"].astype(str).eq(key)
                    if m.any():
                        r = _df[m].iloc[0]
                        for k in ["code", "id", "vsdFeeId"]:
                            if k in cols:
                                _add(r.get(k))

                # match by vsdFeeId (exact)
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
                # data có thể là list/dict; chuẩn hoá DataFrame
                if isinstance(data, list):
                    return pd.DataFrame(data)
                return pd.json_normalize(data)
            except Exception:
                continue
        return pd.DataFrame()

    class details:
        @staticmethod
        def nav_report(code_or_id: str) -> pd.DataFrame:
            cands = Fund._resolve_candidates(code_or_id)
            paths = (
                [f"{BASE}/public/{c}/nav-report" for c in cands]
                + [f"{BASE}/{c}/nav-report" for c in cands]
            )
            return Fund._try_paths(paths)

        @staticmethod
        def top_holding(code_or_id: str) -> pd.DataFrame:
            cands = Fund._resolve_candidates(code_or_id)
            paths = (
                [f"{BASE}/public/{c}/top-holding" for c in cands]
                + [f"{BASE}/{c}/top-holding" for c in cands]
            )
            return Fund._try_paths(paths)

        @staticmethod
        def industry_holding(code_or_id: str) -> pd.DataFrame:
            cands = Fund._resolve_candidates(code_or_id)
            paths = (
                [f"{BASE}/public/{c}/industry-holding" for c in cands]
                + [f"{BASE}/{c}/industry-holding" for c in cands]
            )
            return Fund._try_paths(paths)

        @staticmethod
        def asset_holding(code_or_id: str) -> pd.DataFrame:
            cands = Fund._resolve_candidates(code_or_id)
            paths = (
                [f"{BASE}/public/{c}/asset-holding" for c in cands]
                + [f"{BASE}/{c}/asset-holding" for c in cands]
            )
            return Fund._try_paths(paths)
