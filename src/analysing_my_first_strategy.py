# First tests: implement and further develop source code from https://www.youtube.com/watch?v=r8pU-8l1KPU
import yfinance as yf
import numpy as np
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from classes.Indicators import Indicators
from classes.Strategies import Strategies

tickers = [
    'BTC-USD',
    'ETH-USD',
    'BNB-USD',
    'ADA-USD',
    'USDT-USD',
    'SOL1-USD',
    'XRP-USD',
    'HEX-USD',
    'DOT1-USD',
    'USDC-USD',
    'DOGE-USD',
    'LUNA1-USD',
    'UNI3-USD',
    'AVAX-USD',
    'LINK-USD',
    'LTC-USD',
    'BCH-USD',
    'ALGO-USD',
    'SHIB-USD',
    'MATIC-USD',
    'XLM-USD',
    'VET-USD',
    'ICP1-USD',
    'ATOM1-USD',
    'FTT1-USD'
]

LAGS = 4
WINDOW = 14
SMOOTH_WINDOW = 3
K_LINE_BOUNDS = [20, 80]
D_LINE_BOUNDS = [20, 80]
RSI_BOUND = 50
MACD_BOUND = 0


def foo(TICKER, LAGS, WINDOW, SMOOTH_WINDOW, K_LINE_BOUNDS, D_LINE_BOUNDS, RSI_BOUND, MACD_BOUND):
    start_date = (datetime.datetime.now() - datetime.timedelta(59)).strftime('%Y-%m-%d')
    df = yf.download(TICKER, start=start_date, interval='30m')
    df['%K'] = Indicators.get_k_line(df, window=WINDOW, smooth_window=SMOOTH_WINDOW)
    df['%D'] = Indicators.get_d_line(df, smooth_window=SMOOTH_WINDOW, name_k_line='%K')
    df['rsi'] = Indicators.get_rsi(df, window=WINDOW)
    df['macd'] = Indicators.get_macd(df)

    strategy = Strategies('stoch_rsi_macd')

    df['Buytrigger'] = strategy.get_triggers(df, LAGS, True)
    df['Selltrigger'] = strategy.get_triggers(df, LAGS, False)

    df['Buy'] = strategy.get_signals(df, True, K_LINE_BOUNDS, D_LINE_BOUNDS, RSI_BOUND, MACD_BOUND)
    df['Sell'] = strategy.get_signals(df, False, K_LINE_BOUNDS, D_LINE_BOUNDS, RSI_BOUND, MACD_BOUND)

    dates = strategy.get_dates(df)

    # sell after buy
    actuals = strategy.get_actual_dates(dates)

    profits = strategy.profit_calc(df, actuals)
    print(f'Mean profit per trade: {profits.mean()}')
    print(f'Overall profit: {(1 + profits).cumprod()[-1]}')
    return profits, profits.mean(), (1 + profits).cumprod()[-1]


# plt.figure(figsize=(15, 8))
# plt.plot(df.Close, color='k', alpha=0.7)
# plt.scatter(actuals.buy_dates, df.Open[actuals.buy_dates], marker='^', color='g', s=200)
# plt.scatter(actuals.sell_dates, df.Open[actuals.sell_dates], marker='v', color='r', s=200)
# plt.show()

profits, means, overalls = [], [], []
for ticker in tickers:
    profit, mean, overall = foo(ticker, LAGS, WINDOW, SMOOTH_WINDOW, K_LINE_BOUNDS, D_LINE_BOUNDS, RSI_BOUND, MACD_BOUND)
    profits.append(profit)
    means.append(mean)
    overalls.append(overall)

print(f'Mean profit over all ticker profit means: {np.array(means).mean()}')
print(f'Mean overall profit over all tickers: {np.array(overalls).mean()}')
