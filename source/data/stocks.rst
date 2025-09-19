Dữ liệu cổ phiếu
================

``xnoapi.vn.data.stocks``
-------------------------

Danh sách cổ phiếu thanh khoản
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. function:: list_liquid_asset()

   Trả về danh sách cổ phiếu có tính thanh khoản cao trên thị trường Việt Nam.
   
   :returns: DataFrame chứa symbol và volume giao dịch
   :rtype: pandas.DataFrame

   **Ví dụ:**

   .. code-block:: python

      from xnoapi.vn.data import stocks
      liquid_stocks = stocks.list_liquid_asset()
      print(liquid_stocks.head())

Lấy dữ liệu lịch sử
~~~~~~~~~~~~~~~~~~~

.. function:: get_stock_hist(symbol, resolution='h')

   Lấy dữ liệu OHLCV lịch sử của cổ phiếu.
   
   :param symbol: Mã cổ phiếu (VD: "VIC", "HPG")
   :type symbol: str
   :param resolution: Khung thời gian ('h' cho giờ, 'D' cho ngày)
   :type resolution: str
   :returns: DataFrame chứa dữ liệu OHLCV
   :rtype: pandas.DataFrame

   **Ví dụ:**

   .. code-block:: python

      from xnoapi.vn.data import get_stock_hist
      vic_data = get_stock_hist("VIC", resolution='h')
      print(vic_data.head())

Quote Class
~~~~~~~~~~~

.. class:: Quote(symbol)

   Lớp để truy xuất dữ liệu quote của cổ phiếu.
   
   :param symbol: Mã cổ phiếu
   :type symbol: str

   .. method:: history(start, end, interval)
   
      Lấy dữ liệu lịch sử trong khoảng thời gian.
      
      :param start: Ngày bắt đầu (format: "YYYY-MM-DD")
      :type start: str
      :param end: Ngày kết thúc (format: "YYYY-MM-DD")
      :type end: str
      :param interval: Khung thời gian ("1D", "1H", "1m")
      :type interval: str

      **Ví dụ:**

      .. code-block:: python

         from xnoapi.vn.data.stocks import Quote
         q = Quote("ACB")
         data = q.history(start="2024-01-01", end="2024-03-31", interval="1D")

   .. method:: intraday(page_size, last_time=None)
   
      Lấy dữ liệu tick intraday.
      
      :param page_size: Số lượng record muốn lấy
      :type page_size: int
      :param last_time: Thời gian cuối (optional)
      :type last_time: str, optional

      **Ví dụ:**

      .. code-block:: python

         q = Quote("ACB")
         intraday_data = q.intraday(page_size=200)

   .. method:: price_depth()
   
      Lấy độ sâu giá (accumulated volume).

      **Ví dụ:**

      .. code-block:: python

         q = Quote("ACB")
         depth_data = q.price_depth()

Trading Class
~~~~~~~~~~~~~

.. class:: Trading

   Lớp chứa các phương thức liên quan đến giao dịch.

   .. staticmethod:: price_board(symbols)
   
      Lấy bảng giá realtime với thông tin foreign, ceiling/floor.
      
      :param symbols: Danh sách mã cổ phiếu
      :type symbols: list

      **Ví dụ:**

      .. code-block:: python

         from xnoapi.vn.data.stocks import Trading
         price_board = Trading.price_board(["VCB","ACB","TCB"])