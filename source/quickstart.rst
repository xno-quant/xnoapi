Bắt đầu nhanh
=============

🎯 Ví dụ sử dụng cơ bản
-----------------------

Truy xuất dữ liệu cổ phiếu và phái sinh Việt Nam
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from xnoapi.vn.data.utils import client
   from xnoapi.vn.data import stocks, derivatives

   # Khởi tạo client
   client(apikey="your_api_key")

   # Danh sách cổ phiếu có tính thanh khoản cao
   liquid_stocks = stocks.list_liquid_asset()
   print("Cổ phiếu thanh khoản cao:", liquid_stocks)

   # Dữ liệu lịch sử cổ phiếu VIC (Vingroup)
   from xnoapi.vn.data import get_stock_hist
   vic_data = get_stock_hist("VIC", resolution='h')
   print("Dữ liệu VIC:")
   print(vic_data.head())

   # Dữ liệu phái sinh VN30F1M theo khung thời gian 1 phút
   from xnoapi.vn.data import get_derivatives_hist
   vn30f1m_data = get_derivatives_hist("VN30F1M", "1m")
   print("Dữ liệu VN30F1M:")
   print(vn30f1m_data.head())

**Kết quả mẫu:**

.. code-block:: text

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

🧠 Import chính
---------------

Để bắt đầu sử dụng XNO API, bạn thường sẽ cần import các module sau:

.. code-block:: python

   # Client và authentication
   from xnoapi import client
   
   # Dữ liệu cổ phiếu và phái sinh
   from xnoapi.vn.data import stocks, derivatives
   from xnoapi.vn.data import get_stock_hist, get_derivatives_hist
   
   # Phân tích và metrics
   from xnoapi.vn.metrics import Metrics, Backtest_Derivates
   from xnoapi.metrics import TradingBacktest

📚 Tài liệu hướng dẫn
---------------------

- **Tài liệu trực tuyến**: https://xnoapi.readthedocs.io
- **Hỗ trợ cộng đồng**: `xnoquant.vn <https://xnoquant.vn>`_