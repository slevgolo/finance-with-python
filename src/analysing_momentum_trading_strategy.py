# test quantile based trading strategy, see https://www.youtube.com/watch?v=dnrJ4zwCADM
import pandas as pd
import datetime as dt
import yfinance as yf

tickers_yf_crypto = [
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

# get ticker symbols
tickers_dji = pd.read_html('https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average')[1].Symbol.to_list()
tickers_dax = pd.read_html('https://en.wikipedia.org/wiki/DAX')[3]['Ticker symbol'].to_list()

start = dt.datetime(2018, 1, 31)
end = dt.datetime(2020, 1, 31)

# get data from yahoo
df = yf.download(tickers_dji, start=start.strftime('%Y-%m-%d'), end=end.strftime('%Y-%m-%d'), period='1mo')['Adj Close']

print(df.head())
