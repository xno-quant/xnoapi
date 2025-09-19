Ví dụ sử dụng cơ bản
===================

1. Phân tích dữ liệu định lượng với API v2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from xnoapi.vn.data import *
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

**Kết quả:**

.. code-block:: text

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

2. Thông tin cổ phiếu HPG
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   symbol = 'HPG'
   
   print("Stock info HPG:")
   stock_info = get_stock_info(symbol)
   print(stock_info.head(1))

   print("Stock matches HPG:")
   matches = get_stock_matches(symbol)
   print(matches.head(1))

   print("Stock top price HPG:")
   top_price = get_stock_top_price(symbol)
   print(top_price.head(1))

   print("Foreign trading:")
   foreign = get_stock_foreign_trading(symbol)
   print(foreign.head(1))

**Kết quả:**

.. code-block:: text

   Stock info HPG:
     symbol                  time   open   high   low  close     avg  ceil  floor  prior
   0    HPG  2025-09-15T15:33:13Z  30.25  30.85  30.1  30.35  30.451  32.1   27.9     30

   Stock matches HPG:
                      time symbol  price  volume side
   0  2025-09-15T14:45:04Z    HPG  30.35      50    S

   Stock top price HPG:
     symbol source                  time    bp    bq    ap    aq  total_bid  total_ask
   0    HPG         2025-09-15T14:45:04Z  None  None  None  None          0          0

   Foreign trading:
                      time symbol  total_room  current_room  buy_vol  sell_vol       buy_val      sell_val
   0  2025-09-15T15:33:13Z    HPG   376098000     229122000   356690    942100  108758000000  286886000000

3. Listing symbols theo sàn
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from xnoapi.vn.data.stocks import Listing

   lst = Listing()
   print('Listing symbols_by_exchange:')
   symbols = lst.symbols_by_exchange()
   print(symbols)

**Kết quả:**

.. code-block:: text

   Listing symbols_by_exchange:
   {'HOSE': ['HPG', 'VIC', 'VNM'], 'HNX': [], 'UPCOM': []}