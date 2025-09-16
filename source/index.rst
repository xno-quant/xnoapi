.. role:: raw-html-m2r(raw)
   :format: html


XNO API Library
===============

⚠️ **Ghi chú**\ : Tài liệu này bắt đầu bằng Tiếng Việt cho cộng đồng địa phương. 🌐 Phiên bản Tiếng Anh có sẵn bên dưới — cuộn xuống hoặc sử dụng mục lục để điều hướng.

Chào mừng bạn đến với **XNO API**\ , thư viện Python toàn diện cho phân tích định lượng và truy xuất dữ liệu tài chính, được tối ưu hóa đặc biệt cho thị trường tài chính Việt Nam.

Với sứ mệnh *"Đưa công cụ phân tích định lượng đến gần hơn với mọi nhà đầu tư Việt Nam"*\ , XNO API liên tục phát triển, tích hợp những công nghệ hiện đại để không chỉ đáp ứng nhu cầu cơ bản về dữ liệu, mà còn giúp bạn xây dựng các chiến lược giao dịch thông minh và hiệu quả.

✨ Tính năng nổi bật
--------------------

🆓 **Hoàn toàn miễn phí & mã nguồn mở**\ : Dễ dàng truy cập và sử dụng, phù hợp với nhà đầu tư cá nhân, nhà phân tích định lượng, và cộng đồng nghiên cứu.

🐍 **Giải pháp Python toàn diện**\ : Các hàm chức năng thân thiện, dễ dàng tích hợp để xây dựng các hệ thống giao dịch tự động.

📊 **Dữ liệu Việt Nam chuyên sâu**\ : Bao gồm cổ phiếu, chỉ số, phái sinh, quỹ mở, dữ liệu quốc tế với cấu trúc phí giao dịch chuẩn Việt Nam.

📈 **Công cụ phân tích mạnh mẽ**\ : Tích hợp sẵn các chỉ số hiệu suất, backtesting, và đánh giá rủi ro.

Bạn chính là một phần quan trọng trong hành trình chuyển đổi số thị trường tài chính Việt Nam. Hãy cùng XNO tạo nên những thay đổi tích cực và hiệu quả!

Tham gia ngay cộng đồng XNO để giao lưu, chia sẻ kinh nghiệm và cập nhật những tính năng mới nhất:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

🌐 **Website chính thức**\ : `xno.vn <https://xno.vn>`_\ :raw-html-m2r:`<br>`
👥 **Cộng đồng Quant Finance**\ : `xnoquant.vn <https://xnoquant.vn>`_

🚀 Tại sao chọn XNO API?
------------------------

XNO API giúp rút ngắn thời gian xử lý dữ liệu, hỗ trợ học tập, nghiên cứu và xây dựng hệ thống phân tích giao dịch định lượng một cách hiệu quả – không chỉ là một công cụ trích xuất dữ liệu, mà là nền tảng để phát triển giải pháp đầu tư thông minh cá nhân.

🔎 Truy xuất dữ liệu toàn diện
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


* **Cổ phiếu Việt Nam**\ : Dữ liệu lịch sử, realtime, thông tin doanh nghiệp
* **Phái sinh**\ : VN30F1M, VN30F2M với dữ liệu tần suất cao
* **Quỹ mở**\ : Thông tin quỹ, NAV, danh mục đầu tư
* **Thị trường quốc tế**\ : Chỉ số thế giới, forex, cryptocurrency
* **Dữ liệu định lượng**\ : OHLCV, order book, foreign trading

📊 Dữ liệu thị trường đa dạng
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Từ giá cổ phiếu thời gian thực đến dữ liệu báo cáo tài chính, từ phái sinh VN30 đến các chỉ số quốc tế như S&P 500, Nikkei 225.

📈 Công cụ phân tích hiệu suất
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Tích hợp sẵn các chỉ số Sharpe, Sortino, Max Drawdown, Win Rate, Value at Risk và nhiều metrics quan trọng khác.

🧪 Backtesting chuyên nghiệp
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Hỗ trợ backtest chiến lược với cấu trúc phí giao dịch chuẩn thị trường Việt Nam, tính toán PnL chính xác, hỗ trợ Take Profit/Stop Loss.

🖼️ Tích hợp visualization
^^^^^^^^^^^^^^^^^^^^^^^^^

Dễ dàng mở rộng để tạo các biểu đồ và báo cáo trực quan cho chiến lược giao dịch.

📦 Cài đặt
----------

Bạn có thể cài đặt thư viện bản phát hành ổn định qua PyPI với câu lệnh sau:

.. code-block:: bash

   pip install xnoapi

Hoặc cài đặt từ mã nguồn GitHub:

.. code-block:: bash

   git clone https://github.com/xnoproject/xnoapi.git
   pip install ./xnoapi

Bắt đầu sử dụng
---------------

Bạn cần nạp thư viện vào môi trường Python và khởi tạo API key:

.. code-block:: python

   from xnoapi import client
   from xnoapi.vn.data import stocks, derivatives
   from xnoapi.vn.metrics import Metrics, Backtest_Derivates

   # Khởi tạo client với API key
   client(apikey="your_api_key")

📚 Tài liệu hướng dẫn
---------------------

📖 **Tài liệu trực tuyến**\ : https://xnoapi.readthedocs.io\ :raw-html-m2r:`<br>`
📄 **Phiên bản PDF**\ : Tải xuống\ :raw-html-m2r:`<br>`
🎯 **Hướng dẫn chi tiết**\ : `xno.vn/docs <https://xno.vn/docs>`_\ :raw-html-m2r:`<br>`
💬 **Hỗ trợ cộng đồng**\ : `xnoquant.vn <https://xnoquant.vn>`_

🎯 Ví dụ sử dụng cơ bản
-----------------------

Truy xuất dữ liệu cổ phiếu và phái sinh Việt Nam
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from xnoapi.vn.data.utils import client
   from xnoapi.vn.data import stocks, derivatives
   from xnoapi.vn.data.quant_data import get_indices

   # Khởi tạo client
   client(apikey="your_api_key")

   # Danh sách cổ phiếu có tính thanh khoản cao
   liquid_stocks = stocks.list_liquid_asset()
   print("Cổ phiếu thanh khoản cao:", liquid_stocks)

   # Dữ liệu lịch sử cổ phiếu VIC (Vingroup)
   vic_data = stocks.get_hist("VIC")
   print("Dữ liệu VIC:")
   print(vic_data.head())

   # Dữ liệu phái sinh VN30F1M theo khung thời gian 1 phút
   vn30f1m_data = derivatives.get_hist("VN30F1M", "1m")
   print("Dữ liệu VN30F1M:")
   print(vn30f1m_data.head())

.. code-block:: output

   Cổ phiếu thanh khoản cao:        0             1
   0    SHS  3.885972e+10
   1    CEO  3.227357e+10
   2    PVS  1.849527e+10
   3    MBS  1.431323e+10
   4    IDC  7.032716e+09
   ..   ...           ...
   145  ITQ  7.207067e+07
   146  ANT  7.107417e+07
   147  PFL  6.960543e+07
   148  KCB  6.549169e+07
   149  VHE  6.431393e+07

   [150 rows x 2 columns]
   Dữ liệu VIC:
            Date      time  Open  High   Low  Close    volume
   0  2022-08-23  09:00:00  65.5  65.6  65.0   65.2  300000.0
   1  2022-08-23  10:00:00  65.2  65.2  65.0   65.0  216000.0
   2  2022-08-23  11:00:00  65.0  65.2  65.0   65.0  164700.0
   3  2022-08-23  13:00:00  65.0  65.1  64.8   64.8  328600.0
   4  2022-08-23  14:00:00  64.9  65.2  64.8   65.0  428500.0
   Dữ liệu VN30F1M:
            Date      time   Open   High    Low  Close  volume
   0  2018-08-13  09:01:00  943.0  943.1  942.9  943.1   220.0
   1  2018-08-13  09:02:00  943.0  943.6  943.0  943.5   121.0
   2  2018-08-13  09:03:00  943.3  943.4  943.3  943.4   135.0
   3  2018-08-13  09:04:00  943.2  943.2  943.0  943.1   361.0
   4  2018-08-13  09:05:00  943.1  943.1  942.9  943.0   343.0

🧠 Cấu trúc thư viện
--------------------

📊 Dữ liệu tài chính
^^^^^^^^^^^^^^^^^^^^

``xnoapi.vn.data.stocks``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


* ``list_liquid_asset()``\ : Danh sách cổ phiếu có tính thanh khoản cao trên thị trường Việt Nam
  .. code-block:: python

     liquid_stocks = stocks.list_liquid_asset()

* ``get_hist(asset)``\ : Dữ liệu OHLCV lịch sử của cổ phiếu
  .. code-block:: python

     vic_data = stocks.get_hist("VIC")
     print("Dữ liệu VIC:")
     print(vic_data.head())

``xnoapi.vn.data.derivatives``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


* 
  ``get_hist(asset, frequency)``\ : Dữ liệu thị trường phái sinh (VN30F1M, VN30F2M)

* 
  Hỗ trợ các frequency: "1m", "5m", "15m", "30m", "1H", "1D"

  .. code-block:: python

     # Dữ liệu phái sinh VN30F1M theo khung thời gian 1 phút
     vn30f1m_data = derivatives.get_hist("VN30F1M", "1m")
     print("Dữ liệu VN30F1M:")
     print(vn30f1m_data.head())

``xnoapi.vn.data.quant_data`` [MỚI]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Module dữ liệu định lượng chuyên sâu với API v2:


* ``ping()``\ : Kiểm tra kết nối đến dịch vụ
  .. code-block:: python

     print("\nPing quant-data:", xnoapi.vn.data.ping())

* ``get_indices()``\ : Danh sách các chỉ số thị trường
  .. code-block:: python

     print("\nDanh sách chỉ số thị trường:", xnoapi.vn.data.get_indices())

* ``get_market_index_snapshot(index_symbol)``\ : Snapshot chỉ số (VNI, HNX-Index, v.v.)
  .. code-block:: python

     print("\nget_market_index_snapshot('VNINDEX'):")
     xnoapi.vn.data.get_market_index_snapshot("VNINDEX")

* ``get_stock_info(symbol)``\ : Thông tin cổ phiếu realtime
  .. code-block:: python

     print("\nget_stock_info('HPG'):")
     xnoapi.vn.data.get_stock_info("HPG")

* ``get_stock_matches(symbol)``\ : Dữ liệu khớp lệnh gần nhất
  .. code-block:: python

     print("\nget_stock_matches('HPG'):")
     xnoapi.vn.data.get_stock_matches("HPG")

* ``get_stock_foreign_trading(symbol)``\ : Giao dịch khối ngoại
  .. code-block:: python

     print("\nget_stock_foreign_trading('HPG'):")
     xnoapi.vn.data.get_stock_foreign_trading("HPG")

* ``get_stock_top_price(symbol)``\ : Order book snapshot
  .. code-block::

     xnoapi.vn.data.get_stock_top_price('HPG')

``xnoapi.vn.data.quote_market``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


* ``Quote(symbol).history(start, end, interval)``\ : Dữ liệu lịch sử
  .. code-block:: python

     q = xnoapi.vn.data.Quote("ACB")
     q.history(start="2024-01-01", end="2024-03-31", interval="1D")

* ``Quote(symbol).intraday(page_size, last_time)``\ : Dữ liệu tick intraday
  .. code-block:: python

     q = xnoapi.vn.data.Quote("ACB")
     q.intraday(page_size = 200)

* ``Quote(symbol).price_depth()``\ : Độ sâu giá (accumulated volume)
  .. code-block:: python

     q = xnoapi.vn.data.Quote("ACB")
     q.price_depth()

``xnoapi.vn.data.company`` (Thông tin doanh nghiệp)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


* ``Company(symbol).overview()``\ : Tổng quan công ty
  .. code-block:: python

     c = xnoapi.vn.data.Company("ACB")
     print("\nACB.Company.overview:")
     c.overview()

* ``Company(symbol).profile()``\ : Thông tin chi tiết
  .. code-block:: python

     c = xnoapi.vn.data.Company("HPG")
     print("\HPG.Company.profile:")
     c.profile()

* ``Company(symbol).shareholders()``\ : Cổ đông
  .. code-block:: python

     c = xnoapi.vn.data.Company("VCI")
     print("\nVCI.Company.shareholders:")
     c.shareholders()

* ``Company(symbol).officers()``\ : Ban lãnh đạo
  .. code-block:: python

     c = xnoapi.vn.data.Company("VNM")
     print("\nVNM.Company.officers:")
     c.officers()

* ``Company(symbol).subsidiaries()``\ : Công ty con
  .. code-block:: python

     c = xnoapi.vn.data.Company("VIC")
     print("\nVIC.Company.subsidiaries:")
     c.subsidiaries()

* ``Company(symbol).events()``\ : Sự kiện quan trọng
  .. code-block:: python

     c = xnoapi.vn.data.Company("VCB")
     print("\nVCB.Company.events:")
     c.events()

* ``Company(symbol).news()``\ : Tin tức hoạt động
  .. code-block:: python

     c = xnoapi.vn.data.Company("FPT")
     print("\nFPT.Company.news:")
     c.news()

* ``Company(symbol).ratio_summary()``\ : Tỷ số tài chính
  .. code-block:: python

     c = xnoapi.vn.data.Company("TPB")
     print("\nTPB.Company.ratio_summary:")
     c.ratio_summary()

``xnoapi.vn.data.finance`` (Báo cáo tài chính)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


* ``Finance(symbol).income_statement(period='year')``\ : Báo cáo kết quả kinh doanh
  .. code-block:: python

     f = xnoapi.vn.data.Finance("ACB")
     print("\nACB.Finance.income_statement(year):")
     f.income_statement(period="year")

* ``Finance(symbol).balance_sheet(period='year')``\ : Bảng cân đối kế toán
  .. code-block:: python

     f = xnoapi.vn.data.Finance("HPG")
     print("\nACB.Finance.balance_sheet(year):")
     f.balance_sheet(period="year")

* ``Finance(symbol).cash_flow(period='year')``\ : Báo cáo lưu chuyển tiền tệ
  .. code-block:: python

     f = xnoapi.vn.data.Finance("VNM")
     print("\nACB.Finance.cash_flow(year):")
     f.cash_flow(period="year")

``xnoapi.vn.data.fund`` [MỚI] (Quỹ mở)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


* ``Fund().listing(fund_type="")``\ : Danh sách quỹ mở (BALANCED, BOND, STOCK)
  .. code-block:: python

     fund = xnoapi.vn.data.Fund()
     print("\nFmarket.Fund.listing(fund_type='STOCK'):")
     df_funds = fund.listing(fund_type="STOCK")
     df_funds

* ``Fund().filter(q)``\ : Tìm kiếm quỹ theo tên
  .. code-block:: python

     fund = xnoapi.vn.data.Fund()
     fund.filter('RVPIF')

``xnoapi.vn.data.quote_global``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


* ``Global().fx(symbol).quote.history(start, end)``\ : Tỷ giá ngoại tệ (USDVND, EURUSD)
  .. code-block:: python

     Global = xnoapi.vn.data.Global()
     print("\nGlobal.FX USDVND:")
     Global.fx("USDVND").quote.history(start="2024-01-01", end="2024-12-31")

* ``Global().crypto(symbol).quote.history(start, end)``\ : Cryptocurrency (BTC, ETH)
  .. code-block:: python

     Global = xnoapi.vn.data.Global()
     print("\nGlobal.BTCUSD:")
     Global.crypto("BTCUSD").quote.history(start="2024-01-01", end="2024-12-31")

* ``Global().world_index(symbol).quote.history(start, end)``\ : Chỉ số quốc tế (DJI, SPX, N225)
  .. code-block:: python

     Global = xnoapi.vn.data.Global()
     print("\nGlobal.BTCUSD:")
     Global.world_index("DJI").quote.history(start="2024-01-01", end="2024-12-31")

``xnoapi.vn.data.trading`` (Price Board)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


* ``Trading.price_board(symbols)``\ : Bảng giá realtime với thông tin foreign, ceiling/floor
  .. code-block:: python

     xnoapi.vn.data.Trading.price_board(["VCB","ACB","TCB"])

📈 Phân tích & đánh giá hiệu suất
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``xnoapi.vn.metrics.Metrics``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Bao gồm các chỉ số quan trọng:


* **Sharpe Ratio**\ : Đánh giá hiệu suất điều chỉnh theo rủi ro
* **Sortino Ratio**\ : Tập trung vào downside risk
* **Calmar Ratio**\ : Annual Return / Max Drawdown
* **Max Drawdown**\ : Mức thua lỗ tối đa
* **Average Gain/Loss**\ : Lãi/lỗ trung bình
* **Win Rate**\ : Tỷ lệ giao dịch thành công
* **Profit Factor**\ : Tổng lãi / Tổng lỗ
* **Value at Risk (VaR)**\ : Rủi ro tại mức tin cậy nhất định
* **Risk of Ruin**\ : Xác suất phá sản

``xnoapi.vn.metrics.Backtest_Derivates``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


* Logic backtesting cho chiến lược giao dịch phái sinh
* Hỗ trợ mô hình phí giao dịch chuẩn Việt Nam (transaction fee + overnight fee)
* Tính toán PnL thô và sau phí
* Ước tính vốn tối thiểu cần thiết

``xnoapi.metrics.TradingBacktest`` [NÂNG CẤP]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lớp backtesting đa năng với các tính năng mới:


* **Take Profit/Stop Loss**\ : ``apply_tp_sl(df, tp_percentage, sl_percentage)``
* **Trailing Stop Loss**\ : ``apply_tp_sl_trailing(df, tp_percentage, sl_percentage)``
* **Metrics tổng hợp**\ : Sharpe, Sortino, Calmar, Max Drawdown, Win Rate, Profit Factor, Risk of Ruin
* **Flexible PnL**\ : Hỗ trợ raw và after-fees PnL calculation

🧪 Ví dụ thực hành
------------------

1. Phân tích dữ liệu định lượng với API v2
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from xnoapi.vn.data.quant_data import *
   import datetime as dt

   # Kiểm tra kết nối
   if ping():
       print("✅ Kết nối thành công!")

   # Lấy danh sách chỉ số
   indices = get_indices()
   print("Các chỉ số có sẵn:", indices)

   # Snapshot VNINDEX
   vni_snapshot = get_market_index_snapshot("VNINDEX")
   print("VNINDEX hiện tại:", vni_snapshot)

   # Thông tin giao dịch khối ngoại
   foreign_data = get_stock_foreign_trading("VIC")
   print("Foreign trading VIC:", foreign_data)

.. code-block:: output

   ✅ Kết nối thành công!
   Các chỉ số có sẵn:            symbol           name
   0             HNX            HNX
   1           HNX30          HNX30
   2           HNX30          HNX30
   3        HNXIndex       HNXINDEX
   4   HNXUpcomIndex  HNXUPCOMINDEX
   5           UPCOM          UPCOM
   6           VN100          VN100
   7            VN30           VN30
   8            VN30           VN30
   9      VNALLSHARE     VNALLSHARE
   10         VNCOND         VNCOND
   11         VNCONS         VNCONS
   12      VNDIAMOND      VNDIAMOND
   13          VNENE          VNENE
   14          VNFIN          VNFIN
   15      VNFINLEAD      VNFINLEAD
   16    VNFINSELECT    VNFINSELECT
   17         VNHEAL         VNHEAL
   18          VNIND          VNIND
   19        VNINDEX        VNINDEX
   20        VNINDEX        VNINDEX
   21           VNIT           VNIT
   22          VNMAT          VNMAT
   23       VNMIDCAP       VNMIDCAP
   24         VNREAL         VNREAL
   25           VNSI           VNSI
   26     VNSMALLCAP     VNSMALLCAP
   27          VNUTI          VNUTI
   28          VNX50          VNX50
   29    VNXALLSHARE    VNXALLSHARE
   30    VNXALLSHARE    VNXALLSHARE
   VNINDEX hiện tại:                    time   symbol     name  prior        value   total_vol  \
   0  2025-08-22T14:45:15Z  VNINDEX  VNINDEX   1688  1645.469971  2234243072

         total_val  advance  decline  nochange  ceil  floor     change  \
   0  6.067808e+12       71      251        27     0      0 -42.529999

      change_pct
   0       -2.52
   Foreign trading VIC:                    time symbol  total_room  current_room  buy_vol  sell_vol  \
   0  2025-08-22T14:59:31Z    VIC   186240000     171226000    57880     76800

          buy_val     sell_val
   0  71619900000  95238300000

2. Đánh giá chiến lược giao dịch với Metrics nâng cao
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from xnoapi.vn.metrics import Metrics, Backtest_Derivates
   from xnoapi.vn.data import derivatives
   from xnoapi.metrics import TradingBacktest
   import numpy as np

   # Tạo tín hiệu giao dịch: chiến lược RSI đơn giản
   def gen_position_rsi(df, period=14, oversold=30, overbought=70):
       """
       Chiến lược RSI: Long khi RSI < oversold, Short khi RSI > overbought
       """
       delta = df["Close"].diff()
       gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
       loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
       rs = gain / loss
       rsi = 100 - (100 / (1 + rs))

       position = np.where(rsi < oversold, 1,  # Long signal
                          np.where(rsi > overbought, -1, 0))  # Short signal

       return df.assign(position=position, rsi=rsi)

   # Lấy dữ liệu và tạo tín hiệu
   print("📥 Đang tải dữ liệu VN30F1M...")
   df = derivatives.get_hist("VN30F1M", "5m")  # 5 phút cho phân tích chi tiết
   df_pos = gen_position_rsi(df)

   # Áp dụng Take Profit/Stop Loss
   backtester = TradingBacktest(df_pos)
   df_pos_with_tpsl = backtester.apply_tp_sl(df_pos, tp_percentage=2.0, sl_percentage=1.5)
   df_pos["position_tpsl"] = df_pos_with_tpsl

   for col in df_pos.columns:
       df_pos[col.lower()] = df_pos[col]
   df_pos["Date"] = df_pos["Date"].astype(str)
   df_pos["time"] = df_pos["time"].astype(str)

   df_pos['datetime'] = pd.to_datetime(df_pos['date'].astype(str + " " + df_pos['time']))
   df_pos = df_pos.set_index('datetime')

   # So sánh chiến lược gốc và có TP/SL
   backtest_original = Backtest_Derivates(df_pos, pnl_type="raw")
   backtest_tpsl = Backtest_Derivates(df_pos.assign(position=df_pos["position_tpsl"]), pnl_type="raw")

   metrics_original = Metrics(backtest_original)
   metrics_tpsl = Metrics(backtest_tpsl)

   # So sánh kết quả
   print("\n📊 SO SÁNH CHIẾN LƯỢC:")
   print("=" * 60)
   print(f"{'Metric':<20} {'Original':<15} {'With TP/SL':<15} {'Improvement':<15}")
   print("=" * 60)

   sharpe_orig = metrics_original.sharpe()
   sharpe_tpsl = metrics_tpsl.sharpe()
   print(f"{'Sharpe Ratio':<20} {sharpe_orig:<15.3f} {sharpe_tpsl:<15.3f} {((sharpe_tpsl/sharpe_orig-1)*100 if sharpe_orig != 0 else 0):<14.1f}%")

   win_rate_orig = metrics_original.win_rate()
   win_rate_tpsl = metrics_tpsl.win_rate()
   print(f"{'Win Rate':<20} {win_rate_orig*100:<15.1f}% {win_rate_tpsl*100:<15.1f}% {(win_rate_tpsl-win_rate_orig)*100:<14.1f}pp")

   max_dd_orig = metrics_original.max_drawdown()
   max_dd_tpsl = metrics_tpsl.max_drawdown()
   print(f"{'Max Drawdown':<20} {max_dd_orig*100:<15.1f}% {max_dd_tpsl*100:<15.1f}% {(max_dd_tpsl-max_dd_orig)*100:<14.1f}pp")

   profit_factor_orig = metrics_original.profit_factor()
   profit_factor_tpsl = metrics_tpsl.profit_factor()
   print(f"{'Profit Factor':<20} {profit_factor_orig:<15.3f} {profit_factor_tpsl:<15.3f} {((profit_factor_tpsl/profit_factor_orig-1)*100 if profit_factor_orig != 0 else 0):<14.1f}%")

.. code-block:: output


   📊 SO SÁNH CHIẾN LƯỢC:
   ============================================================
   Metric               Original        With TP/SL      Improvement
   ============================================================
   Sharpe Ratio         -2.076          -1.992          -4.0          %
   Win Rate             50.6           % 50.9           % 0.3           pp
   Max Drawdown         -54.4          % -52.1          % 2.3           pp
   Profit Factor        0.644           0.660           2.5           %

3. Phân tích quỹ mở và thị trường quốc tế
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from xnoapi.vn.data.fund import Fund
   from xnoapi.vn.data.quote_global import Global
   import datetime as dt

   # Phân tích quỹ mở
   fund = Fund()

   # Tìm quỹ cổ phiếu
   stock_funds = fund.listing(fund_type="STOCK")
   print("Top 5 quỹ cổ phiếu:")
   print(stock_funds[["name", "code", "nav", "productNavChange.navTo1Months"]].head())

   # Phân tích danh mục của một quỹ cụ thể
   if not stock_funds.empty:
       fund_code = stock_funds.iloc[0]["code"]
       holdings = Fund.details.top_holding(fund_code)
       print(f"\nDanh mục top holdings của {fund_code}:")
       print(holdings.head())

   # Dữ liệu thị trường quốc tế
   glb= Global()

   # So sánh VNINDEX với các chỉ số quốc tế
   start_date = "2024-01-01"
   end_date = "2024-12-31"

   vni_data = glb.world_index("VNI").quote.history(start_date, end_date)
   spy_data = glb.world_index("INX").quote.history(start_date, end_date)  # S&P 500
   nikkei_data = glb.world_index("N225").quote.history(start_date, end_date)

   print("\nSo sánh hiệu suất chỉ số 2024:")
   print("=" * 40)

   def calculate_return(df):
       if df.empty or df["close"].isna().all():
           return 0
       return (df["close"].iloc[-1] / df["close"].iloc[0] - 1) * 100

   vni_return = calculate_return(vni_data)
   spy_return = calculate_return(spy_data)
   nikkei_return = calculate_return(nikkei_data)

   print(f"VNINDEX: {vni_return:.2f}%")
   print(f"S&P 500: {spy_return:.2f}%")
   print(f"Nikkei 225: {nikkei_return:.2f}%")

   # Tỷ giá USD/VND
   usd_vnd = glb.fx("USDVND").quote.history(start_date, end_date)
   if not usd_vnd.empty:
       usd_change = calculate_return(usd_vnd)
       print(f"USD/VND: {usd_change:.2f}%")

.. code-block:: output

   Top 5 quỹ cổ phiếu:
                                                   name    code        nav  \
   0             QUỸ ĐẦU TƯ CỔ PHIẾU NĂNG ĐỘNG BẢO VIỆT   BVFED   31828.00
   1                QUỸ ĐẦU TƯ CHỨNG KHOÁN NĂNG ĐỘNG DC  VFMVF1  108787.18
   2  QUỸ ĐẦU TƯ CỔ PHIẾU TĂNG TRƯỞNG MIRAE ASSET VI...   MAGEF   21435.98
   3            QUỸ ĐẦU TƯ CỔ PHIẾU TẬP TRUNG CỔ TỨC DC  VFMVF4   34008.33
   4                  QUỸ ĐẦU TƯ TĂNG TRƯỞNG THÀNH CÔNG    TCGF   12862.16

      productNavChange.navTo1Months
   0                          17.14
   1                          13.97
   2                          13.38
   3                          12.34
   4                          12.38

   So sánh hiệu suất chỉ số 2024:
   ========================================
   VNINDEX: 0.00%
   S&P 500: 6.04%
   Nikkei 225: 4.41%
   USD/VND: 2.19%

4. Phân tích báo cáo tài chính và thông tin doanh nghiệp
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from xnoapi.vn.data.company import Company
   from xnoapi.vn.data.finance import Finance

   # Phân tích VIC - Vingroup
   symbol = "VIC"
   company = Company(symbol)
   finance = Finance(symbol)

   # Thông tin tổng quan
   overview = company.overview()
   print("Thông tin tổng quan VIC:")
   print(overview[["ticker", "exchange", "industry", "stockRating"]].iloc[0])

   # Cổ đông lớn
   shareholders = company.shareholders()
   print("\nTop 5 cổ đông lớn:")
   print(shareholders[["name", "ownPercent"]].head())

   # Báo cáo tài chính
   income_stmt = finance.income_statement(period='quarter')  # Báo cáo quý
   print("\nDoanh thu 4 quý gần nhất:")
   print(income_stmt[["quarter", "revenue", "investProfit"]].head())

   # Tỷ số tài chính
   ratios = company.ratio_summary()
   print("\nCác tỷ số tài chính chính:")
   if not ratios.empty:
       key_ratios = ["pe", "pb", "roe", "roa", "eps"]
       available_ratios = [col for col in key_ratios if col in ratios.columns]
       if available_ratios:
           print(ratios[available_ratios].iloc[0])

.. code-block:: output

   Thông tin tổng quan VIC:
   ticker                  VIC
   exchange               HOSE
   industry       Bất động sản
   stockRating             2.7
   Name: 0, dtype: object

   Top 5 cổ đông lớn:
                                                   name  ownPercent
   0           Công ty Cổ Phần Tập Đoàn Đầu Tư Việt Nam      0.3249
   1                                    Phạm Nhật Vượng      0.1160
   2  Công Ty Cổ Phần Quản Lý Và Đầu Tư Bất Động Sản...      0.0628
   3                                     Phạm Thu Hương      0.0440
   4                                     Phạm Thúy Hằng      0.0299

   Doanh thu 4 quý gần nhất:
      quarter  revenue investProfit
   0        5   189068         None
   1        5   161428         None
   2        5   101794         None
   3        5   125688         None
   4        5   110490         None

   Các tỷ số tài chính chính:
   roe    0.095
   roa    0.016
   Name: 0, dtype: float64

🆕 Tính năng mới
----------------

📊 Quant Data API v2
^^^^^^^^^^^^^^^^^^^^


* Dữ liệu OHLCV với timestamp chính xác đến giây
* Order book snapshot realtime
* Foreign trading data
* Market index snapshot

🏦 Quỹ mở & Tài sản quốc tế
^^^^^^^^^^^^^^^^^^^^^^^^^^^


* Thông tin quỹ mở đầy đủ (cổ phiếu, trái phiếu, cân bằng)
* Danh mục đầu tư và phân bổ tài sản của quỹ
* Dữ liệu forex, cryptocurrency, chỉ số quốc tế

🎯 Take Profit/Stop Loss nâng cao
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


* Fixed TP/SL với hold mechanism
* Trailing Stop Loss động
* Backtesting với risk management tự động

📈 Metrics mở rộng
^^^^^^^^^^^^^^^^^^


* Risk of Ruin calculation
* Value at Risk (VaR)
* Calmar Ratio
* Enhanced Sortino Ratio

🏢 Thông tin doanh nghiệp chi tiết
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


* Báo cáo tài chính theo quý/năm
* Thông tin cổ đông, ban lãnh đạo
* Tin tức và sự kiện quan trọng
* Tỷ số tài chính tổng hợp

🌟 Cộng đồng & Hỗ trợ
---------------------

XNO phát triển nhờ sự chung tay của cộng đồng những người yêu thích công nghệ và tài chính định lượng. Mỗi dòng code, mỗi bản sửa lỗi đều là minh chứng cho sự đóng góp quý giá của các bạn.

💬 Tham gia cộng đồng
^^^^^^^^^^^^^^^^^^^^^

🌐 **Website chính thức**\ : `xno.vn <https://xno.vn>`_ - Tin tức, blog, và tài nguyên\ :raw-html-m2r:`<br>`
👥 **Cộng đồng Quant**\ : `xnoquant.vn <https://xnoquant.vn>`_ - Thảo luận, chia sẻ chiến lược\ :raw-html-m2r:`<br>`
📧 **Hỗ trợ**\ : support@xno.vn\ :raw-html-m2r:`<br>`
🐛 **Báo lỗi**\ : GitHub Issues

🤝 Đóng góp
^^^^^^^^^^^

Chúng tôi hoan nghênh mọi đóng góp từ cộng đồng! Bạn có thể:


* 🌟 Star dự án trên GitHub
* 🐛 Báo cáo lỗi hoặc đề xuất tính năng
* 📖 Cải thiện tài liệu
* 💻 Đóng góp code

⚠️ Tuyên bố miễn trách nhiệm
----------------------------

XNO API được phát triển nhằm phục vụ mục đích nghiên cứu và sử dụng cá nhân. Dữ liệu cung cấp có thể không đầy đủ, không liên tục hoặc sai lệch so với thực tế, do đó không khuyến nghị sử dụng cho mục đích giao dịch thực tế, thuật toán đầu tư, hoặc ra quyết định tài chính khi bạn không hiểu rõ.

Các tác giả không chịu trách nhiệm đối với bất kỳ tổn thất hay thiệt hại nào phát sinh từ việc sử dụng dữ liệu hoặc mã nguồn này, bao gồm nhưng không giới hạn: sai lệch dữ liệu, mất mát tài chính, hoặc sử dụng sai mục đích.

XNO API không cung cấp tư vấn đầu tư hay tín hiệu giao dịch. Người dùng hoàn toàn tự chịu trách nhiệm khi sử dụng thư viện.

📄 Giấy phép
------------

XNO API được phát hành theo **Giấy phép MIT**. Xem chi tiết tại `LICENSE <https://github.com/xnoproject/xnoapi/blob/main/LICENSE>`_.
