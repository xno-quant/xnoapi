import pandas as pd
import numpy as np


class Backtest_Derivates:
    """
    A class for backtesting derivatives trading strategies.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing historical data with columns ['Date', 'time', 'Close', 'position'].
    pnl_type : str, optional
        Type of PNL calculation ('raw' or 'after_fees'), by default 'after_fees'.

    Raises
    ------
    ValueError
        If pnl_type is not 'raw' or 'after_fees'.
    """

    def __init__(self, df, pnl_type="after_fees"):
        """
        Initializes the BacktestDerivates class.

        Parameters
        ----------
        df : pd.DataFrame
            Data containing trade details.
        pnl_type : str, optional
            Type of PNL calculation ('raw' or 'after_fees'), by default "after_fees".
        """
        if pnl_type not in ["raw", "after_fees"]:
            raise ValueError("Invalid pnl_type. Choose 'raw' or 'after_fees'.")

        self.df = df.copy()
        self.pnl_type = pnl_type
        self.df["datetime"] = pd.to_datetime(self.df["Date"] + " " + self.df["time"])
        self.df.set_index("datetime", inplace=True)
        self.df.sort_index(inplace=True)

        # Calculate raw PNL
        self.df["pnl_raw"] = self.df["Close"].diff().shift(-1) * self.df["position"]
        self.df["pnl_raw"].fillna(0, inplace=True)

        # Calculate PNL after fees
        transaction_fee = 2700 / 100000  # VND per contract
        overnight_fee = 2550 / 100000  # VND per contract per day if held overnight

        self.df["transaction_fee"] = self.df["position"].diff().abs() * transaction_fee

        # Identify overnight holdings
        self.df["date"] = self.df.index.date
        self.df["overnight"] = (self.df["position"] > 0) & (
            self.df["date"] != self.df["date"].shift()
        )
        self.df["overnight_fee"] = self.df["overnight"] * overnight_fee

        self.df["total_fee"] = self.df["transaction_fee"].fillna(0) + self.df[
            "overnight_fee"
        ].fillna(0)
        self.df["pnl_after_fees"] = self.df["pnl_raw"] - self.df["total_fee"]

    def PNL(self):
        """
        Calculate cumulative PNL based on selected pnl_type.

        Returns
        -------
        pandas.Series
            Cumulative PNL.
        """
        return self.df[f"pnl_{self.pnl_type}"].cumsum()

    def daily_PNL(self):
        """
        Calculate daily PNL based on selected pnl_type.

        Returns
        -------
        pandas.Series
            Daily cumulative PNL.
        """
        daily_pnl = (
            self.df.groupby(self.df.index.date)[f"pnl_{self.pnl_type}"].sum().cumsum()
        )
        return daily_pnl

    def estimate_minimum_capital(self):
        """
        Estimate the minimum capital required to run the strategy.

        Returns
        -------
        float
            Minimum capital required.
        """
        self.df["cumulative_pnl"] = (
            self.df[f"pnl_{self.pnl_type}"].cumsum().shift().fillna(0)
        )
        self.df["capital_required"] = (
            self.df["position"].abs() * self.df["Close"]
        ) - self.df["cumulative_pnl"]

        return max(self.df["capital_required"].max(), 0)

    def PNL_percentage(self):
        """
        Calculate PNL percentage relative to minimum required capital.

        Returns
        -------
        float
            PNL percentage.
        """
        min_capital = self.estimate_minimum_capital()
        if min_capital == 0:
            return np.nan  # Avoid division by zero
        return self.daily_PNL() / min_capital
