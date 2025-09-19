Phân tích quỹ mở và thị trường quốc tế
=====================================

1. Phân tích quỹ mở và thị trường quốc tế
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from xnoapi.vn.data.stocks import Fund, Global
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

**Kết quả:**

.. code-block:: text

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

2. So sánh hiệu suất chỉ số quốc tế
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Dữ liệu thị trường quốc tế
   glb = Global()

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

**Kết quả:**

.. code-block:: text

   So sánh hiệu suất chỉ số 2024:
   ========================================
   VNINDEX: 0.00%
   S&P 500: 6.04%
   Nikkei 225: 4.41%
   USD/VND: 2.19%

3. Phân tích quỹ nâng cao
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Tìm kiếm quỹ theo tên
   fund = Fund()
   search_result = fund.filter('RVPIF')
   print("Kết quả tìm kiếm quỹ RVPIF:")
   print(search_result)

   # Lọc quỹ trái phiếu
   bond_funds = fund.listing(fund_type="BOND")
   print(f"\nSố lượng quỹ trái phiếu: {len(bond_funds)}")
   print("Top 3 quỹ trái phiếu theo NAV:")
   print(bond_funds.nlargest(3, 'nav')[['name', 'code', 'nav']])

   # Lọc quỹ cân bằng
   balanced_funds = fund.listing(fund_type="BALANCED")
   print(f"\nSố lượng quỹ cân bằng: {len(balanced_funds)}")

**Ứng dụng thực tế:**

1. **Đánh giá hiệu suất quỹ**: So sánh NAV growth của các quỹ cùng loại
2. **Phân tích danh mục**: Xem top holdings để hiểu chiến lược đầu tư
3. **Benchmark so sánh**: So sánh hiệu suất quỹ với chỉ số tham chiếu
4. **Risk assessment**: Đánh giá volatility và drawdown của quỹ