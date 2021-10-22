import ta
from pandas import DataFrame


class Indicators:

    @staticmethod
    def get_k_line(df: DataFrame, window: int, smooth_window: int):
        """

        :param df:
        :param window:
        :param smooth_window:
        :return:
        """
        return ta.momentum.stoch(
            df.High,
            df.Low,
            df.Close,
            window=window,
            smooth_window=smooth_window
        )

    @staticmethod
    def get_d_line(df: DataFrame, smooth_window: int, name_k_line: str):
        """

        :param df:
        :param smooth_window:
        :param name_k_line:
        :return:
        """
        return df[name_k_line].rolling(smooth_window).mean()

    @staticmethod
    def get_rsi(df: DataFrame, window: int):
        """

        :param df:
        :param window:
        :return:
        """
        return ta.momentum.rsi(df.Close, window=window)

    @staticmethod
    def get_macd(df: DataFrame):
        """

        :param df:
        :return:
        """
        return ta.trend.macd_diff(df.Close)
