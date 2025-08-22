
import pandas as pd
from .core import send_request

BASE = "https://apipubaws.tcbs.com.vn"
ANALYSIS = "tcanalysis"

class Company:
    """Company information via TCBS tcanalysis endpoints."""
    def __init__(self, symbol):
        self.symbol = symbol

    def overview(self):
        url = f"{BASE}/{ANALYSIS}/v1/ticker/{self.symbol}/overview"
        data = send_request(url)
        return pd.DataFrame(data, index=[0])

    def profile(self):
        url = f"{BASE}/{ANALYSIS}/v1/company/{self.symbol}/overview"
        data = send_request(url)
        return pd.json_normalize(data)

    def shareholders(self, page_size=50, page=0):
        url = f"{BASE}/{ANALYSIS}/v1/company/{self.symbol}/large-share-holders"
        data = send_request(url, params={"page":page, "size":page_size})
        items = (data or {}).get("listShareHolder", [])
        return pd.json_normalize(items)

    def officers(self, page_size=50, page=0):
        url = f"{BASE}/{ANALYSIS}/v1/company/{self.symbol}/key-officers"
        data = send_request(url, params={"page":page, "size":page_size})
        items = (data or {}).get("listKeyOfficer", [])
        return pd.json_normalize(items)

    def subsidiaries(self, page_size=100, page=0):
        url = f"{BASE}/{ANALYSIS}/v1/company/{self.symbol}/sub-companies"
        data = send_request(url, params={"page":page, "size":page_size})
        items = (data or {}).get("listSubCompany", [])
        return pd.json_normalize(items)

    def events(self, page_size=15, page=0):
        url = f"{BASE}/{ANALYSIS}/v1/ticker/{self.symbol}/events-news"
        data = send_request(url, params={"page":page, "size":page_size})
        items = (data or {}).get("listEventNews", [])
        return pd.DataFrame(items)

    def news(self, page_size=15, page=0):
        url = f"{BASE}/{ANALYSIS}/v1/ticker/{self.symbol}/activity-news"
        data = send_request(url, params={"page":page, "size":page_size})
        items = (data or {}).get("listActivityNews", [])
        return pd.DataFrame(items)

    def ratio_summary(self):
        url = f"{BASE}/{ANALYSIS}/v1/ticker/{self.symbol}/ratios"
        try:
            data = send_request(url)
            return pd.DataFrame(data, index=[0]) if isinstance(data, dict) else pd.DataFrame(data)
        except Exception:
            url2 = f"{BASE}/{ANALYSIS}/v1/finance/{self.symbol}/financialratio"
            data = send_request(url2)
            return pd.DataFrame(data)
