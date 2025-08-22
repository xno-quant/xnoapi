
import pandas as pd

class Listing:
    """Listing facade for VCI.
    NOTE: VCI không public đầy đủ endpoint listing ổn định; bạn có thể thay thế
    các hàm dưới đây bằng các truy vấn GraphQL thực tế của VCI (nếu có).
    Tạm thời trả về cấu trúc rỗng để giữ API shape ổn định.
    """
    def __init__(self, source='VCI'):
        self.source = source

    def all_symbols(self):
        return pd.DataFrame(columns=["symbol","short_name","exchange"])

    def symbols_by_exchange(self):
        return {"HOSE":[], "HNX":[], "UPCOM":[]}

    def symbols_by_group(self, group='VN30'):
        return []

    def symbols_by_industries(self):
        return pd.DataFrame(columns=["symbol","icb_industry"])

    def industries_icb(self):
        return pd.DataFrame(columns=["icb_code","icb_name"])
