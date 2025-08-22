
import pandas as pd
from .core import send_request

BASE = "https://apipubaws.tcbs.com.vn"
ANALYSIS = "tcanalysis"
FIN_MAP = {'income_statement':'incomestatement','balance_sheet':'balancesheet','cash_flow':'cashflow'}
PERIOD_MAP = {'year':1, 'quarter':0}

class Finance:
    """Financial statements via TCBS."""
    def __init__(self, symbol):
        self.symbol = symbol

    def _fetch(self, report, period='year', lang='vi', dropna=False):
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
