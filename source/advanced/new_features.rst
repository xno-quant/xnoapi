Tính năng mới
=============

🆕 Các tính năng được bổ sung gần đây
------------------------------------

📊 Quant Data API v2
~~~~~~~~~~~~~~~~~~~~

- **Dữ liệu OHLCV** với timestamp chính xác đến giây
- **Order book snapshot** realtime  
- **Foreign trading data** - dữ liệu giao dịch khối ngoại
- **Market index snapshot** - snapshot các chỉ số thị trường

**Ví dụ sử dụng:**

.. code-block:: python

   from xnoapi.vn.data import (
       get_indices, get_market_index_snapshot,
       get_stock_foreign_trading, get_stock_info, 
       get_stock_top_price
   )
   
   # Snapshot VNINDEX realtime
   vnindex_data = get_market_index_snapshot("VNINDEX")
   
   # Giao dịch khối ngoại của VIC
   foreign_data = get_stock_foreign_trading("VIC")
   
   # Order book snapshot của HPG
   orderbook = get_stock_top_price("HPG")

🏦 Quỹ mở & Tài sản quốc tế
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Thông tin quỹ mở đầy đủ** (cổ phiếu, trái phiếu, cân bằng)
- **Danh mục đầu tư và phân bổ tài sản** của quỹ
- **Dữ liệu forex, cryptocurrency, chỉ số quốc tế**

**Ví dụ sử dụng:**

.. code-block:: python

   from xnoapi.vn.data.stocks import Fund, Global
   
   # Quỹ mở
   fund = Fund()
   stock_funds = fund.listing(fund_type="STOCK")
   
   # Thị trường quốc tế
   global_data = Global()
   usd_vnd = global_data.fx("USDVND").quote.history("2024-01-01", "2024-12-31")
   btc_data = global_data.crypto("BTCUSD").quote.history("2024-01-01", "2024-12-31")

🎯 Take Profit/Stop Loss nâng cao
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Fixed TP/SL** với hold mechanism
- **Trailing Stop Loss** động
- **Backtesting với risk management** tự động

**Ví dụ sử dụng:**

.. code-block:: python

   from xnoapi.metrics import TradingBacktest
   
   backtester = TradingBacktest(df_positions)
   
   # Fixed TP/SL
   df_with_tpsl = backtester.apply_tp_sl(
       df_positions,
       tp_percentage=2.0,
       sl_percentage=1.5
   )
   
   # Trailing Stop Loss
   df_with_trailing = backtester.apply_tp_sl_trailing(
       df_positions,
       tp_percentage=2.0, 
       sl_percentage=1.0
   )

📈 Metrics mở rộng
~~~~~~~~~~~~~~~~~~

- **Risk of Ruin calculation** - tính toán nguy cơ phá sản
- **Value at Risk (VaR)** - đo lường rủi ro
- **Calmar Ratio** - tỷ lệ return/max drawdown
- **Enhanced Sortino Ratio** - Sortino ratio cải tiến

**Ví dụ sử dụng:**

.. code-block:: python

   from xnoapi.vn.metrics import Metrics
   
   metrics = Metrics(backtest_result)
   
   # Các metrics mới
   calmar = metrics.calmar_ratio()
   var_95 = metrics.value_at_risk(confidence=0.95)
   risk_of_ruin = metrics.risk_of_ruin(ruin_threshold=0.2)
   
   print(f"Calmar Ratio: {calmar:.3f}")
   print(f"VaR (95%): {var_95:.3f}")
   print(f"Risk of Ruin: {risk_of_ruin:.3f}")

🏢 Thông tin doanh nghiệp chi tiết  
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Báo cáo tài chính theo quý/năm** - thu thập dữ liệu tài chính chi tiết
- **Thông tin cổ đông, ban lãnh đạo** - corporate governance data
- **Tin tức và sự kiện quan trọng** - event-driven analysis
- **Tỷ số tài chính tổng hợp** - comprehensive ratio analysis

**Ví dụ sử dụng:**

.. code-block:: python

   from xnoapi.vn.data.stocks import Company, Finance
   
   # Thông tin công ty
   company = Company("VIC")
   shareholders = company.shareholders()
   officers = company.officers()
   events = company.events()
   news = company.news()
   
   # Báo cáo tài chính
   finance = Finance("VIC")
   income_stmt = finance.income_statement(period='quarter')
   balance_sheet = finance.balance_sheet(period='year')
   cash_flow = finance.cash_flow(period='year')

🔄 Cải tiến hiệu suất
~~~~~~~~~~~~~~~~~~~~

- **Caching mechanism** để tăng tốc độ truy xuất
- **Batch processing** cho việc xử lý nhiều symbol cùng lúc
- **Error handling** được cải thiện
- **Data validation** tự động

🛠️ Developer Experience
~~~~~~~~~~~~~~~~~~~~~~~

- **Type hints** đầy đủ cho IDE support
- **Docstring** chi tiết cho tất cả functions
- **Example code** trong documentation
- **Unit tests** coverage cao hơn

📱 Tương thích và tích hợp
~~~~~~~~~~~~~~~~~~~~~~~~~

- **Jupyter Notebook** optimized display
- **Pandas integration** seamless
- **Matplotlib/Plotly** visualization ready
- **REST API** endpoints