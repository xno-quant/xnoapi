
TRADING_URL = "https://trading.vietcap.com.vn/api/"
GRAPHQL_URL = "https://trading.vietcap.com.vn/data-mt/graphql"
CHART_URL = "chart/OHLCChart/gap-chart"
INTRADAY_URL = "market-watch"

INTERVAL_MAP = {
    '1m':'ONE_MINUTE','5m':'ONE_MINUTE','15m':'ONE_MINUTE','30m':'ONE_MINUTE',
    '1H':'ONE_HOUR','1D':'ONE_DAY','1W':'ONE_DAY','1M':'ONE_DAY'
}

OHLC_COLUMNS = ["t","o","h","l","c","v"]
OHLC_RENAME = {"t":"time","o":"open","h":"high","l":"low","c":"close","v":"volume"}

INTRADAY_MAP = {'truncTime':'time','matchPrice':'price','matchVol':'volume','matchType':'match_type','id':'id'}

PRICE_DEPTH_URL = f"{TRADING_URL}{INTRADAY_URL}/AccumulatedPriceStepVol/getSymbolData"

PRICE_INFO_MAP = {
    'ev':'ev','ticker':'symbol',
    'open_price':'open','ceiling_price':'ceiling','floor_price':'floor','reference_price':'ref_price',
    'highest_price':'high','lowest_price':'low',
    'price_change':'price_change','percent_price_change':'price_change_pct',
    'foreign_total_volume':'foreign_volume','foreign_total_room':'foreign_room','foreign_holding_room':'foreign_holding_room',
    'average_match_volume2_week':'avg_match_volume_2w',
}
