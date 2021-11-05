# test quantile based trading strategy, see https://www.youtube.com/watch?v=dnrJ4zwCADM
import datetime as dt

import numpy as np
import pandas as pd
import yfinance as yf

# get ticker symbols
# tickers = pd.read_html('https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average')[1].Symbol.to_list()
tickers = pd.read_html('https://en.wikipedia.org/wiki/DAX')[3]['Ticker symbol'].to_list()

start = dt.datetime(2018, 1, 31)
end = dt.datetime(2020, 2, 1)

# index_data = yf.download('^DJI', start=start, end=end, interval='1d')['Adj Close']
index_data = yf.download('DAX', start=start, end=end, interval='1d')['Adj Close']

# get data from yahoo
df = yf.download(tickers, start=start.strftime('%Y-%m-%d'), end=end.strftime('%Y-%m-%d'), interval='1d')[
    'Adj Close']

# calculate monthly returns by cumulating daily returns
monthly_returns = df.pct_change().resample('M').agg(lambda x: (x + 1).prod() - 1)

# calculate returns over the past 11 months
past_11_months = (monthly_returns + 1).rolling(11).apply(np.prod) - 1
past_11_months.dropna(inplace=True)

formation_date = dt.datetime(2019, 12, 31)
end_measurement = dt.datetime(2019, 11, 30)

# calculate 12 month returns
returns_12_month = past_11_months.loc[end_measurement].reset_index()

# get 'winner' and 'loser' assets by quantiles
returns_12_month['quintile'] = pd.qcut(returns_12_month.iloc[:, 1], 5, labels=False)
winners = returns_12_month[returns_12_month['quintile'] == 4]
losers = returns_12_month[returns_12_month['quintile'] == 0]

# strategy: buy winners and hold for one month, shortsell losers and hold for one month
winner_return = monthly_returns.loc[dt.datetime(2020, 1, 31), df.columns.isin(winners['index'])]
loser_return = monthly_returns.loc[dt.datetime(2020, 1, 31), df.columns.isin(losers['index'])]

# assume we weight every asset the same. We can subtract loser return mean because we shortsell losers
momentumprofit = winner_return.mean() - loser_return.mean()
print(f'Momentumprofit: {momentumprofit}')

# do benchmark vs whole index
index_profit = index_data.pct_change().resample('M').agg(lambda x: (x + 1).prod() - 1)[-1]
print(f'Indexperformance: {index_profit}')
