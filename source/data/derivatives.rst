Dữ liệu phái sinh
================

``xnoapi.vn.data.derivatives``
-------------------------

Lấy dữ liệu lịch sử phái sinh
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. function:: get_hist(symbol, frequency)

   Lấy dữ liệu lịch sử của các sản phẩm phái sinh VN30F1M và VN30F2M.
   
   :param symbol: Mã phái sinh (VD: "VN30F1M", "VN30F2M")
   :type symbol: str
   :param frequency: Khung thời gian ('1m' cho phút, '5m' cho 5 phút)
   :type frequency: str
   :returns: DataFrame chứa dữ liệu lịch sử với thông tin thời gian, giá đóng cửa, khối lượng giao dịch
   :rtype: pandas.DataFrame

   **Ví dụ:**

   .. code-block:: python

      from xnoapi.vn.data import derivatives
      vn30f1m_data = derivatives.get_hist("VN30F1M", frequency='1m')
      print(vn30f1m_data.head())


   .. code-block:: python

      # Lấy dữ liệu theo 5 phút
      vn30f1m_5min = derivatives.get_hist("VN30F1M", frequency='5m')
      print(vn30f1m_5min.head())

