.. xnoapi documentation master file, created by
   sphinx-quickstart on Mon Mar 31 16:42:27 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

xnoapi documentation
====================

XNO API is a Python package for retrieving financial data from multiple sources with a simple and intuitive interface. To sign up for API Key access, register free account at xbot.xno.vn

Author: XNO API Team

License: MIT License

----

Installation
------------

You can install the XNO API package using pip:

.. code:: none

   pip install xnoapi

Alternatively, you can clone this repository and install the package manually:

.. code:: none

   $ git clone https://github.com/xnoproject/xnoapi.git
   $ pip install ./xnoapi

After installation, you can import and start using XNO API:

.. code:: python

   from xnoapi import client
   from xnoapi.vn.data import stocks, derivatives
   from xnoapi.vn.metrics import Metrics, Backtest_Derivates

   client(apikey="your_api_key")

----

Usage
-----

XNO API provides a structured interface for retrieving financial data and modules for efficient PNL calculation and performance tracking in the Vietnamese Financial Market:

.. code:: python

   from xnoapi import client
   from xnoapi.vn.data import stocks, derivatives

   client(apikey="your_api_key")

   # List of liquid stocks
   stocks.list_liquid_asset()

   # Historical data for VIC (Vingroup)
   vic = stocks.get_hist("VIC")

   # Historical data for VN30F1M derivative
   vn30f1m = derivatives.get_hist("VN30F1M", "1m")

----

Available Modules
-----------------

**Stocks**   
 - `list_liquid_asset()` : List of high-liquidity Vietnamese stocks.
 - `get_hist(asset)` : Retrieve historical OHLCV data for a given stock.

**Derivatives**
 - `get_hist(asset, frequency)` : Retrieve derivative market data (e.g., VN30F1M futures) with specified frequency.

**Metrics**
 - `avg_loss()`: Average loss per trade.
 - `avg_return()`: Average return per trade.
 - `avg_win()`: Average win per trade.
 - `max_drawdown()`: Maximum drawdown observed.
 - `win_rate()`: Percentage of winning trades.
 - `volatility()`: Measure of price fluctuations.
 - `sharpe()`: Sharpe ratio for risk-adjusted return.
 - `sortino()`: Sortino ratio for downside risk adjustment.
 - `calmar()`: Calmar ratio for risk-adjusted return over drawdown.
 - `profit_factor()`: Ratio of gross profit to gross loss.
 - `risk_of_ruin()`: Probability of losing all capital.
 - `value_at_risk()`: Measure of potential loss in value of an asset.

**Backtesting**
 - `PNL()`: Calculate cumulative profit and loss.
 - `daily_PNL()`: Calculate daily cumulative profit and loss.
 - `estimate_minimum_capital()`: Estimate minimum capital required for trading.
 - `PNL_percentage()`: Calculate PNL as a percentage of capital.

----

Examples
--------

**Retrieving Stock Data**

.. code:: python

   from xnoapi import client
   from xnoapi.vn.data import stocks

   client(apikey="your_api_key")

   # Get list of liquid assets
   liquid_assets = stocks.list_liquid_asset()

   # Get historical data for VIC stock
   vic_history = stocks.get_hist("VIC")

----

**Retrieving Derivatives Data**

.. code:: python

   from xnoapi import client
   from xnoapi.vn.data import derivatives

   client(apikey="your_api_key")

   # Get historical data for VN30F1M derivative
   vn30f1m_history = derivatives.get_hist("VN30F1M", "1m")

----

**Using Metrics**

.. code:: python

   from xnoapi.vn.metrics import Metrics, Backtest_Derivates
   from xnoapi.vn.data import derivatives
   import numpy as np

   # Generate signal: simple strategy based on 20-period median
   def gen_position(df):
      return df.assign(
         position=np.sign(df["Close"] - df["Close"].rolling(20).median())
      )

   # Fetch 1-minute historical data
   df = derivatives.get_hist("VN30F1M", "1m")
   df_pos = gen_position(df)

   # Backtest the strategy
   backtest = Backtest_Derivates(df_pos, pnl_type="raw")

   # Initialize metrics
   metrics = Metrics(backtest)

   # === Backtest_Derivates Methods ===

   # Cumulative PNL
   cumulative_pnl = backtest.PNL()

   # Daily cumulative PNL
   daily_cumulative_pnl = backtest.daily_PNL()

   # Estimate Minimum Capital Required
   min_capital = backtest.estimate_minimum_capital()

   # PNL Percentage
   pnl_percentage = backtest.PNL_percentage()

   # === Metrics Methods ===

   # Average Loss
   metrics.avg_loss()

   # Average Return
   metrics.avg_return()

   # Average Win
   metrics.avg_win()

   # Max Drawdown
   metrics.max_drawdown()

   # Win Rate
   metrics.win_rate()

   # Volatility
   metrics.volatility()

   # Sharpe Ratio
   metrics.sharpe()

   # Sortino Ratio
   metrics.sortino()

   # Calmar Ratio
   metrics.calmar()

   # Profit Factor
   metrics.profit_factor()

   # Risk of Ruin
   metrics.risk_of_ruin()

   # Value at Risk
   metrics.value_at_risk()

----

Uploading Strategy and Getting API Key
--------------------------------------

Before using the XNO API services for automated strategy backtesting and deployment, you need to prepare two things:

1. A valid **Python strategy file** containing a `gen_position(df)` function.
2. Your personal **API Key** from `https://xbot.xno.vn`.

**Prepare the Strategy Python File**

Your Python script must define a function named **`gen_position(df)`**.  
This function takes a **DataFrame** (historical data) as input, and returns a **DataFrame** with a mandatory `position` column.

- **Input**: `df` with at least 'Open', 'High', 'Low', 'Close' columns.
- **Output**: `df` with a new `position` column:

  - `1` for long (buy signal)
  - `-1` for short (sell signal)
  - `0` for no action

Example structure of your script (`strategy.py`):

.. code:: python

   import numpy as np

   def gen_position(df):
       """
       Generate trading signals based on a simple moving median strategy.
       
       Args:
           df (pd.DataFrame): Historical OHLCV data.

       Returns:
           pd.DataFrame: Same DataFrame with an additional 'position' column.
       """
       df["position"] = np.sign(df["Close"] - df["Close"].rolling(20).median())
       return df

**Important Requirements**

- The file **must contain** a function named `gen_position`.
- The function **must return** a DataFrame with a `position` column.
- No additional external API calls or infinite loops inside your function.


**Get Your API Key**

You need an API Key to interact with the XNO API services. Follow these steps:

1. Go to the XNO API Portal:  
   `https://xbot.xno.vn`
2. Register a new account (if you don't have one) or log in.
3. Navigate to "Xbot Hub" -> Cài đặt -> Mã API.
4. Click "Tạo mã API" or Copy your API Key existed.

You will need to initialize the XNO API client in your scripts using:

.. code:: python

   from xnoapi import client

   client(apikey="your_generated_api_key")

**Next Steps**

- Upload your `.py` file via the XNO bot upload interface.
- Monitor strategy performance, backtesting results, and live trading simulations via your dashboard.

----

Credits
-------

This library is developed and maintained by the XNO API team. Special thanks to contributors and financial data providers for their support.

----

License
-------

This library is licensed under the MIT License. See the LICENSE file for more details.



