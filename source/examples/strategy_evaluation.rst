Đánh giá chiến lược giao dịch
============================

1. Đánh giá chiến lược giao dịch với Metrics nâng cao
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from xnoapi.vn.metrics import Metrics, Backtest_Derivates
   from xnoapi.vn.data import derivatives
   from xnoapi.metrics import TradingBacktest
   import numpy as np
   import pandas as pd

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
   from xnoapi.vn.data import get_derivatives_hist
   df = get_derivatives_hist("VN30F1M", "5m")  # 5 phút cho phân tích chi tiết
   df_pos = gen_position_rsi(df)

   # Áp dụng Take Profit/Stop Loss
   backtester = TradingBacktest(df_pos)
   df_pos_with_tpsl = backtester.apply_tp_sl(df_pos, tp_percentage=2.0, sl_percentage=1.5)
   df_pos["position_tpsl"] = df_pos_with_tpsl

   # Chuẩn bị dữ liệu cho backtest
   for col in df_pos.columns:
       df_pos[col.lower()] = df_pos[col]
   df_pos["Date"] = df_pos["Date"].astype(str)
   df_pos["time"] = df_pos["time"].astype(str)

   df_pos['datetime'] = pd.to_datetime(df_pos['date'].astype(str) + " " + df_pos['time'])
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

**Kết quả mẫu:**

.. code-block:: text

   📊 SO SÁNH CHIẾN LƯỢC:
   ============================================================
   Metric               Original        With TP/SL      Improvement
   ============================================================
   Sharpe Ratio         -2.076          -1.992          -4.0          %
   Win Rate             50.6           % 50.9           % 0.3           pp
   Max Drawdown         -54.4          % -52.1          % 2.3           pp
   Profit Factor        0.644           0.660           2.5           %

2. Demo backtest MA(20/50) đơn giản
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from xnoapi.vn.metrics.backtest import Backtest_Stock
   from xnoapi.vn.data import get_stock_hist
   import pandas as pd

   # Lấy dữ liệu VIC
   df = get_stock_hist('VIC', resolution='h')
   df = df[['Date', 'time', 'Close']].dropna().copy()

   # Tính toán Moving Average
   close = pd.to_numeric(df['Close'], errors='coerce')
   ma20  = close.rolling(20, min_periods=20).mean()
   ma50  = close.rolling(50, min_periods=50).mean()
   
   # Tạo tín hiệu: Long khi MA20 > MA50
   signal = (ma20 > ma50).astype(int).shift(1).fillna(0)

   # Chuẩn bị dữ liệu cho backtest
   df['position'] = signal * 100
   bt_input = df[['Date', 'time', 'Close', 'position']]
   
   # Chạy backtest
   bt = Backtest_Stock(bt_input, pnl_type='after_fees')
   bt.plot_PNL("VIC – MA(20/50) long-only")  # hiển thị biểu đồ PnL

**Các chỉ số quan trọng:**

- **Sharpe Ratio > 1.0**: Chiến lược có risk-adjusted return tốt
- **Max Drawdown < 20%**: Rủi ro có thể chấp nhận được  
- **Win Rate > 50%**: Tỷ lệ thắng cao hơn thua
- **Profit Factor > 1.5**: Lời nhiều hơn lỗ đáng kể