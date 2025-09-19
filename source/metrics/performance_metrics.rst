Chỉ số hiệu suất
================

``xnoapi.vn.metrics.Metrics``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lớp Metrics cung cấp các chỉ số quan trọng để đánh giá hiệu suất giao dịch:

Các chỉ số chính
~~~~~~~~~~~~~~~

- **Sharpe Ratio**: Tỷ lệ giữa lợi nhuận vượt trội và độ lệch chuẩn
- **Sortino Ratio**: Tương tự Sharpe nhưng chỉ tính downside deviation  
- **Calmar Ratio**: Tỷ lệ giữa lợi nhuận hàng năm và Max Drawdown
- **Max Drawdown**: Mức sụt giảm lớn nhất từ đỉnh đến đáy
- **Average Gain/Loss**: Lợi nhuận/thua lỗ trung bình
- **Win Rate**: Tỷ lệ giao dịch thắng
- **Profit Factor**: Tỷ lệ tổng lời/tổng lỗ
- **Value at Risk (VaR)**: Giá trị rủi ro
- **Risk of Ruin**: Nguy cơ phá sản

Ví dụ sử dụng
~~~~~~~~~~~~~

.. code-block:: python

   from xnoapi.vn.metrics import Metrics
   
   # Giả sử bạn có DataFrame với kết quả backtest
   metrics = Metrics(backtest_result)
   
   # Tính các chỉ số
   sharpe = metrics.sharpe()
   sortino = metrics.sortino()
   max_dd = metrics.max_drawdown()
   win_rate = metrics.win_rate()
   profit_factor = metrics.profit_factor()
   
   print(f"Sharpe Ratio: {sharpe:.3f}")
   print(f"Sortino Ratio: {sortino:.3f}")
   print(f"Max Drawdown: {max_dd:.3f}")
   print(f"Win Rate: {win_rate:.3f}")
   print(f"Profit Factor: {profit_factor:.3f}")

``xnoapi.metrics.TradingBacktest`` [NÂNG CẤP]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lớp TradingBacktest cung cấp các tính năng nâng cao:

Take Profit/Stop Loss
~~~~~~~~~~~~~~~~~~~~

.. method:: apply_tp_sl(df, tp_percentage, sl_percentage)

   Áp dụng Take Profit và Stop Loss cho chiến lược.
   
   :param df: DataFrame chứa tín hiệu giao dịch
   :type df: pandas.DataFrame
   :param tp_percentage: % Take Profit
   :type tp_percentage: float
   :param sl_percentage: % Stop Loss  
   :type sl_percentage: float

.. method:: apply_tp_sl_trailing(df, tp_percentage, sl_percentage)

   Áp dụng Trailing Stop Loss động.
   
   :param df: DataFrame chứa tín hiệu giao dịch
   :type df: pandas.DataFrame
   :param tp_percentage: % Take Profit
   :type tp_percentage: float
   :param sl_percentage: % Trailing Stop Loss
   :type sl_percentage: float

Ví dụ sử dụng TP/SL
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from xnoapi.metrics import TradingBacktest
   import pandas as pd
   
   # Giả sử bạn có DataFrame với position signals
   backtester = TradingBacktest(df_with_positions)
   
   # Áp dụng Take Profit 2% và Stop Loss 1.5%
   df_with_tpsl = backtester.apply_tp_sl(
       df_positions, 
       tp_percentage=2.0, 
       sl_percentage=1.5
   )
   
   # Áp dụng Trailing Stop Loss
   df_with_trailing = backtester.apply_tp_sl_trailing(
       df_positions,
       tp_percentage=2.0,
       sl_percentage=1.0
   )