import numpy as np


class Metrics:
    """
    A class for calculating performance metrics from backtest results.

    Parameters
    ----------
    backtest : BacktestDerivatives
        An instance of BacktestDerivatives containing PNL data.
    """

    def __init__(self, backtest):
        """
        Initializes the Metrics class.

        Parameters
        ----------
        backtest : BacktestDerivates
            Instance of backtest results.
        """
        self.backtest = backtest
        self.daily_pnl = backtest.daily_PNL().diff().dropna()

    def avg_loss(self):
        """
        Compute the average loss from daily PNL.

        Returns
        -------
        float
            Average loss.
        """
        losses = self.daily_pnl[self.daily_pnl < 0]
        return losses.mean()

    def avg_return(self):
        """
        Compute the average return from daily PNL.

        Returns
        -------
        float
            Average return.
        """
        return self.daily_pnl.mean()

    def avg_win(self):
        """
        Compute the average win from daily PNL.

        Returns
        -------
        float
            Average win.
        """
        wins = self.daily_pnl[self.daily_pnl > 0]
        return wins.mean()

    def max_drawdown(self):
        """
        Compute the maximum drawdown.

        Returns
        -------
        float
            Maximum drawdown as a percentage of minimum capital.
        """
        cumulative = self.daily_pnl.cumsum()
        peak = cumulative.cummax()
        drawdown = cumulative - peak
        return drawdown.min() / self.backtest.estimate_minimum_capital()

    def win_rate(self):
        """
        Compute the win rate.

        Returns
        -------
        float
            Win rate.
        """
        wins = (self.daily_pnl > 0).sum()
        total = len(self.daily_pnl)
        return wins / total if total > 0 else 0

    def volatility(self):
        """
        Compute the standard deviation of daily PNL.

        Returns
        -------
        float
            Volatility.
        """
        return self.daily_pnl.std()

    def sharpe(self, risk_free_rate=0.0):
        """
        Compute the Sharpe ratio.

        Returns
        -------
        float
            Sharpe ratio.
        """
        return (self.avg_return() - risk_free_rate) / self.volatility() * np.sqrt(252)

    def sortino(self):
        """
        Compute the Sortino ratio.

        Returns
        -------
        float
            Sortino ratio.
        """
        downside_std = self.daily_pnl[self.daily_pnl < 0].std()
        return (
            np.sqrt(252) * self.avg_return() / downside_std
            if downside_std > 0
            else np.nan
        )

    def calmar(self):
        """
        Compute the Calmar ratio.

        Returns
        -------
        float
            Calmar ratio.
        """
        return (
            np.sqrt(252) * self.avg_return() / abs(self.max_drawdown())
            if self.max_drawdown() != 0
            else np.nan
        )

    def profit_factor(self):
        """
        Compute the profit factor.

        Returns
        -------
        float
            Profit factor.
        """
        total_gain = self.daily_pnl[self.daily_pnl > 0].sum()
        total_loss = abs(self.daily_pnl[self.daily_pnl < 0].sum())
        return total_gain / total_loss if total_loss != 0 else np.nan

    def risk_of_ruin(self):
        """
        Compute risk of ruin.

        Returns
        -------
        float
            Risk of ruin.
        """
        win_rate = self.win_rate()
        loss_rate = 1 - win_rate
        return (
            (loss_rate / win_rate) ** (1 / self.avg_loss())
            if self.avg_loss() != 0
            else np.nan
        )

    def value_at_risk(self, confidence_level=0.05):
        """
        Compute Value at Risk (VaR).

        Parameters
        ----------
        confidence_level : float, optional
            Confidence level for VaR, by default 0.05.

        Returns
        -------
        float
            Value at Risk (VaR).
        """
        return self.daily_pnl.quantile(confidence_level)
