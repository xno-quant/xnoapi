Phân tích báo cáo tài chính
===========================

1. Phân tích báo cáo tài chính và thông tin doanh nghiệp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from xnoapi.vn.data.stocks import Company, Finance

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

**Kết quả mẫu:**

.. code-block:: text

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

2. Phân tích chi tiết Company và Finance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Phân tích HPG - Hòa Phát Group
   comp = Company('HPG')
   fin = Finance('HPG')

   print('Company overview HPG:')
   overview_hpg = comp.overview()
   print(overview_hpg[['exchange', 'industry', 'stockRating', 'noEmployees']].iloc[0])

   print('\nCompany profile HPG:')
   profile_hpg = comp.profile()
   # Profile thường chứa HTML, chỉ hiển thị thông tin cơ bản
   if not profile_hpg.empty:
       print(f"Company name: {profile_hpg['companyName'].iloc[0]}")

   print('\nBáo cáo kết quả kinh doanh (năm):')
   income_annual = fin.income_statement(period='year')
   if not income_annual.empty:
       recent_data = income_annual.head(1)
       print(recent_data[['year', 'revenue', 'grossProfit', 'postTaxProfit']].iloc[0])

   print('\nBảng cân đối kế toán (năm):')
   balance_sheet = fin.balance_sheet(period='year')
   if not balance_sheet.empty:
       print("✅ Dữ liệu bảng cân đối kế toán có sẵn")

   print('\nBáo cáo lưu chuyển tiền tệ (năm):')
   cash_flow = fin.cash_flow(period='year')
   if not cash_flow.empty:
       print("✅ Dữ liệu lưu chuyển tiền tệ có sẵn")

**Kết quả mẫu:**

.. code-block:: text

   Company overview HPG:
   exchange               HOSE
   industry       Tài nguyên Cơ bản
   stockRating                3.1
   noEmployees              32780
   Name: 0, dtype: object

   Company profile HPG:
   Company name: Công ty Cổ phần Tập đoàn Hòa Phát

   Báo cáo kết quả kinh doanh (năm):
   year            2024
   revenue       138855
   grossProfit    18498
   postTaxProfit  12020
   Name: 0, dtype: object

   ✅ Dữ liệu bảng cân đối kế toán có sẵn
   ✅ Dữ liệu lưu chuyển tiền tệ có sẵn

3. Các thông tin doanh nghiệp khác
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Thông tin về ban lãnh đạo
   officers = comp.officers()
   if not officers.empty:
       print("Ban lãnh đạo:")
       print(officers[['name', 'position']].head())

   # Công ty con
   subsidiaries = comp.subsidiaries()
   if not subsidiaries.empty:
       print("\nCông ty con:")
       print(subsidiaries.head())

   # Sự kiện quan trọng
   events = comp.events()
   if not events.empty:
       print("\nSự kiện gần đây:")
       print(events.head())

   # Tin tức
   news = comp.news()
   if not news.empty:
       print("\nTin tức mới:")
       print(news[['title', 'publishDate']].head())

**Ứng dụng thực tế:**

1. **Fundamental Analysis**: Đánh giá định giá dựa trên P/E, P/B, ROE
2. **Growth Analysis**: Theo dõi tăng trưởng doanh thu, lợi nhuận qua các quý/năm
3. **Financial Health**: Phân tích cấu trúc tài chính, thanh khoản, đòn bẩy
4. **Corporate Governance**: Theo dõi thay đổi ban lãnh đạo, cổ đông lớn
5. **Event-driven Trading**: Theo dõi sự kiện quan trọng, tin tức ảnh hưởng đến giá