Thị trường quốc tế
==================

1. Global quotes (MSN/Yahoo)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from xnoapi.vn.data.stocks import Global

   g = Global()
   
   print('FX EURUSD:')
   df_fx = g.fx('EURUSD').quote.history('2024-01-01', '2024-03-01', '1h')
   print(df_fx.head())
   
   print('Crypto BTCUSD:')
   df_btc = g.crypto('BTCUSD').quote.history('2024-01-01', '2024-03-01', '1D')
   print(df_btc.head())
   
   print('World Index S&P 500:')
   df_spx = g.world_index('INX').quote.history('2024-01-01', '2024-03-01', '1D')
   print(df_spx.head())

**Kết quả mẫu:**

.. code-block:: text

   FX EURUSD:
            time   open   high    low  close  volume
   0 2024-01-01   1.105  1.108  1.103  1.106   45678
   1 2024-01-02   1.106  1.109  1.104  1.107   52341
   2 2024-01-03   1.107  1.110  1.105  1.108   48923
   
   Crypto BTCUSD:
            time     open     high      low    close    volume
   0 2024-01-01  42150.5  42800.2  41900.1  42650.8  15678.45
   1 2024-01-02  42650.8  43200.4  42300.7  42950.3  18234.67
   2 2024-01-03  42950.3  43500.1  42600.9  43180.7  19876.32

2. Phân tích correlation giữa các thị trường
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pandas as pd
   import numpy as np
   from xnoapi.vn.data.stocks import Global

   def analyze_market_correlation():
       """Phân tích tương quan giữa các thị trường"""
       
       g = Global()
       start_date = "2024-01-01"
       end_date = "2024-12-31"
       
       # Lấy dữ liệu các chỉ số chính
       markets = {
           'VN Index': g.world_index("VNI").quote.history(start_date, end_date),
           'S&P 500': g.world_index("INX").quote.history(start_date, end_date),
           'Nikkei 225': g.world_index("N225").quote.history(start_date, end_date),
           'FTSE 100': g.world_index("UKX").quote.history(start_date, end_date),
           'DAX': g.world_index("DAX").quote.history(start_date, end_date)
       }
       
       # Tính toán daily returns
       returns_data = {}
       for market_name, data in markets.items():
           if not data.empty:
               data['returns'] = data['close'].pct_change()
               returns_data[market_name] = data.set_index('time')['returns']
       
       # Tạo DataFrame chung
       returns_df = pd.DataFrame(returns_data)
       returns_df = returns_df.dropna()
       
       # Tính correlation matrix
       correlation_matrix = returns_df.corr()
       print("Correlation Matrix:")
       print(correlation_matrix.round(3))
       
       # Tính volatility
       volatility = returns_df.std() * np.sqrt(252) * 100  # Annualized volatility
       print(f"\nAnnualized Volatility (%):")
       for market, vol in volatility.items():
           print(f"{market}: {vol:.2f}%")
       
       return correlation_matrix, volatility

   # Chạy phân tích
   corr_matrix, vol_data = analyze_market_correlation()

**Kết quả mẫu:**

.. code-block:: text

   Correlation Matrix:
                VN Index  S&P 500  Nikkei 225  FTSE 100    DAX
   VN Index        1.000    0.245       0.312     0.198  0.234
   S&P 500         0.245    1.000       0.678     0.756  0.812
   Nikkei 225      0.312    0.678       1.000     0.587  0.623
   FTSE 100        0.198    0.756       0.587     1.000  0.834
   DAX             0.234    0.812       0.623     0.834  1.000

   Annualized Volatility (%):
   VN Index: 18.45%
   S&P 500: 16.23%
   Nikkei 225: 19.87%
   FTSE 100: 15.67%
   DAX: 17.91%

3. Theo dõi tỷ giá và commodities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def track_currencies_commodities():
       """Theo dõi tỷ giá và hàng hóa ảnh hưởng đến VN"""
       
       g = Global()
       start_date = "2024-01-01"
       end_date = "2024-12-31"
       
       # Các cặp tiền tệ quan trọng với VN
       currencies = {
           'USD/VND': g.fx("USDVND").quote.history(start_date, end_date),
           'EUR/USD': g.fx("EURUSD").quote.history(start_date, end_date),
           'JPY/USD': g.fx("USDJPY").quote.history(start_date, end_date),
           'CNY/USD': g.fx("USDCNY").quote.history(start_date, end_date)
       }
       
       # Cryptocurrencies
       cryptos = {
           'Bitcoin': g.crypto("BTCUSD").quote.history(start_date, end_date),
           'Ethereum': g.crypto("ETHUSD").quote.history(start_date, end_date)
       }
       
       # Tính performance YTD
       print("Year-to-Date Performance:")
       print("=" * 40)
       
       def calc_ytd_performance(data, name):
           if not data.empty:
               start_price = data['close'].iloc[0]
               end_price = data['close'].iloc[-1]
               performance = ((end_price / start_price) - 1) * 100
               print(f"{name}: {performance:+.2f}%")
               return performance
           return 0
       
       print("\nCurrencies:")
       for name, data in currencies.items():
           calc_ytd_performance(data, name)
       
       print("\nCryptocurrencies:")
       for name, data in cryptos.items():
           calc_ytd_performance(data, name)
       
       # Tìm volatility cao nhất
       print(f"\nHighest Volatility Analysis:")
       all_assets = {**currencies, **cryptos}
       volatilities = {}
       
       for name, data in all_assets.items():
           if not data.empty:
               returns = data['close'].pct_change()
               vol = returns.std() * np.sqrt(252) * 100
               volatilities[name] = vol
       
       # Sắp xếp theo volatility
       sorted_vol = sorted(volatilities.items(), key=lambda x: x[1], reverse=True)
       for name, vol in sorted_vol:
           print(f"{name}: {vol:.2f}%")

   track_currencies_commodities()

**Kết quả mẫu:**

.. code-block:: text

   Year-to-Date Performance:
   ========================================

   Currencies:
   USD/VND: +2.19%
   EUR/USD: -3.45%
   JPY/USD: +8.76%
   CNY/USD: +1.23%

   Cryptocurrencies:
   Bitcoin: +156.78%
   Ethereum: +102.34%

   Highest Volatility Analysis:
   Bitcoin: 67.89%
   Ethereum: 58.43%
   JPY/USD: 12.34%
   USD/VND: 8.76%
   EUR/USD: 7.23%
   CNY/USD: 5.67%

4. Cross-market arbitrage opportunities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def find_arbitrage_signals():
       """Tìm kiếm cơ hội arbitrage giữa các thị trường"""
       
       from xnoapi.vn.data import get_stock_hist
       from xnoapi.vn.data.stocks import Global
       
       # So sánh VN-Index với regional indices
       g = Global()
       
       # Lấy dữ liệu intraday nếu có
       vni_data = get_stock_hist("VNI", resolution='h')  # VN-Index hourly
       
       # Asian indices  
       nikkei_data = g.world_index("N225").quote.history("2024-12-01", "2024-12-31", "1H")
       hang_seng = g.world_index("HSI").quote.history("2024-12-01", "2024-12-31", "1H")
       
       # Tính Z-score để tìm divergence
       def calculate_zscore(data, window=20):
           if data.empty:
               return pd.Series()
           
           returns = data['close'].pct_change()
           rolling_mean = returns.rolling(window).mean()
           rolling_std = returns.rolling(window).std()
           zscore = (returns - rolling_mean) / rolling_std
           return zscore
       
       print("Cross-market Divergence Analysis:")
       print("=" * 50)
       
       if not vni_data.empty:
           vni_zscore = calculate_zscore(vni_data)
           extreme_moves = vni_zscore[abs(vni_zscore) > 2]  # Movements > 2 std dev
           
           if not extreme_moves.empty:
               print(f"VN-Index extreme moves detected:")
               for date, score in extreme_moves.tail().items():
                   direction = "Oversold" if score < -2 else "Overbought"
                   print(f"  {date}: Z-score {score:.2f} ({direction})")
           else:
               print("No extreme divergences detected in VN-Index")
       
       # Sector rotation analysis
       print(f"\nSector Rotation Signals:")
       print("-" * 30)
       
       # Giả sử tracking major VN sectors vs global peers
       sectors_performance = {
           'VN Banks': 2.5,      # % performance last week
           'VN Steel': -1.8,
           'VN Real Estate': 0.7,
           'Global Banks': 1.9,
           'Global Steel': -0.9,
           'Global REIT': 1.2
       }
       
       # Tìm sectors outperform/underperform
       vn_sectors = {k: v for k, v in sectors_performance.items() if k.startswith('VN')}
       global_sectors = {k: v for k, v in sectors_performance.items() if k.startswith('Global')}
       
       for vn_sector, vn_perf in vn_sectors.items():
           sector_name = vn_sector.replace('VN ', '')
           global_sector = f'Global {sector_name}' if sector_name != 'Real Estate' else 'Global REIT'
           
           if global_sector in global_sectors:
               global_perf = global_sectors[global_sector]
               relative_perf = vn_perf - global_perf
               
               if abs(relative_perf) > 1.0:  # Significant divergence
                   status = "Outperforming" if relative_perf > 0 else "Underperforming"
                   print(f"  {sector_name}: {status} by {relative_perf:+.1f}%")

   find_arbitrage_signals()

**Trading Applications:**

1. **Market Timing**: Sử dụng correlation để predict VN market direction
2. **Currency Hedging**: Hedge USD exposure dựa trên USD/VND trends  
3. **Sector Rotation**: Rotate between sectors dựa trên global trends
4. **Risk Management**: Diversify portfolio across uncorrelated markets
5. **Arbitrage**: Exploit temporary pricing differences

**Risk Considerations:**

- Time zone differences affect correlation calculations
- Liquidity differences between markets
- Currency conversion impacts
- Regulatory restrictions on cross-border investments