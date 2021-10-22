from pandas import DataFrame
from numpy import where, ndarray
from typing import Tuple


class Strategies:

    def __init__(self, strategy: str):
        self.strategy = strategy

    def get_triggers(self, df: DataFrame, lags: int, buy: bool) -> ndarray:

        if self.strategy == 'stoch_rsi_macd':
            triggers = DataFrame()
            for i in range(1, lags + 1):
                if buy:
                    mask = (df['%K'].shift(i) < 20) & (df['%D'].shift(i) < 20)
                else:
                    mask = (df['%K'].shift(i) > 80) & (df['%D'].shift(i) > 80)
                triggers = triggers.append(mask, ignore_index=True)
            return where(triggers.sum(axis=0), 1, 0)

        else:
            raise NameError(f'Strategy {self.strategy} is not defined')

    def get_signals(
            self,
            df: DataFrame,
            buy: bool,
            k_line_bounds: list,
            d_line_bounds: list,
            rsi_bound: int,
            macd_bound: int
    ) -> ndarray:
        if self.strategy == 'stoch_rsi_macd':
            if buy:
                return where(
                    df.Buytrigger &
                    (df['%K'].between(k_line_bounds[0], k_line_bounds[1])) &
                    (df['%D'].between(d_line_bounds[0], d_line_bounds[1])) &
                    (df.rsi > rsi_bound) &
                    (df.macd > macd_bound),
                    1, 0)
            else:
                return where(
                    df.Selltrigger &
                    (df['%K'].between(k_line_bounds[0], k_line_bounds[1])) &
                    (df['%D'].between(d_line_bounds[0], d_line_bounds[1])) &
                    (df.rsi < rsi_bound) &
                    (df.macd < macd_bound),
                    1, 0)
        else:
            raise NameError(f'Strategy {self.strategy} is not defined')

    def get_dates(self, df: DataFrame) -> DataFrame:
        if self.strategy == 'stoch_rsi_macd':
            buy_dates, sell_dates = [], []
            for i in range(len(df) - 1):
                if df.Buy.iloc[i]:
                    buy_dates.append(df.iloc[i + 1].name)
                    for num, j in enumerate(df.Sell[i:]):
                        if j:
                            sell_dates.append(df.iloc[i + num + 1].name)
                            break
        else:
            raise NameError(f'Strategy {self.strategy} is not defined')

        cut_off = len(buy_dates) - len(sell_dates)
        if cut_off != 0:
            buy_dates = buy_dates[:-cut_off]

        return DataFrame({'buy_dates': buy_dates, 'sell_dates': sell_dates})

    @staticmethod
    def get_actual_dates(dates: DataFrame) -> DataFrame:
        return dates[dates.buy_dates > dates.sell_dates.shift(1)]

    @staticmethod
    def profit_calc(df: DataFrame, dates: DataFrame) -> ndarray:
        buy_prices = df.loc[dates.buy_dates].Open
        sell_prices = df.loc[dates.sell_dates].Open
        return (sell_prices.values - buy_prices.values) / buy_prices.values




