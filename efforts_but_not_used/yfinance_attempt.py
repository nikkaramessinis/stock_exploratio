import numpy as np
import yfinance as yf
from helpers import retrieve_sp500_tickers
from datetime import date
import pandas_ta

def garman_klass_volatility(df):
    df["garman_klass_vol"] = ((np.log(df['high'] - np.log(df['low']))**2)/2-(2*np.log(2)-1)*((np.log(df['adj close']) - np.log(df['open']))**2))

def rsi(df):
    df['rsi'] = df.groupby(level=1)['adj close'].transform(lambda x: pandas_ta.rsi(close=x, length=20))

def bbands(df):
    df['bb_hign'] = df.groupby(level=1)['adj close'].transform(lambda x: pandas_ta.bbands(close=np.log1p(x), length=20).iloc[:, 0])
    df['bb_mid'] = df.groupby(level=1)['adj close'].transform(lambda x: pandas_ta.bbands(close=np.log1p(x), length=20).iloc[:, 1])
    df['bb_low'] = df.groupby(level=1)['adj close'].transform(lambda x: pandas_ta.bbands(close=np.log1p(x), length=20).iloc[:, 2])

def main():
    msft = yf.Ticker("MSFT")

    # get all stock info
    print(msft.info)

    # get historical market data
    hist = msft.history(period="1d")

    # show meta information about the history (requires history() to be called first)
    print(msft.history_metadata)

    # show actions (dividends, splits, capital gains)
    msft.actions
    msft.dividends
    msft.splits
    msft.capital_gains  # only for mutual funds & etfs

    # show share count
    msft.get_shares_full(start="2022-01-01", end=None)

    # show financials:
    # - income statement
    msft.income_stmt
    msft.quarterly_income_stmt
    # - balance sheet
    msft.balance_sheet
    msft.quarterly_balance_sheet
    # - cash flow statement
    msft.cashflow
    msft.quarterly_cashflow
    # see `Ticker.get_income_stmt()` for more options

    # show holders
    msft.major_holders
    msft.institutional_holders
    msft.mutualfund_holders
    msft.insider_transactions
    msft.insider_purchases
    msft.insider_roster_holders

    # show recommendations
    msft.recommendations
    msft.recommendations_summary
    msft.upgrades_downgrades

    # Show future and historic earnings dates, returns at most next 4 quarters and last 8 quarters by default.
    # Note: If more are needed use msft.get_earnings_dates(limit=XX) with increased limit argument.
    #msft.earnings_dates

    # show ISIN code - *experimental*
    # ISIN = International Securities Identification Number
    msft.isin

    # show options expirations
    msft.options

    # show news
    #msft.news

    # get option chain for specific expiration
    # opt = msft.option_chain('2024-05-18')
    # data available via: opt.calls, opt.puts

    symbols_list = retrieve_sp500_tickers()
    print(symbols_list)
    start_date = '2023-09-27'
    end_date = date.today()
    print(end_date)
    symbols_str = " ".join(symbols_list)
    try:
        df = yf.download(tickers=symbols_list, start=start_date, end=str(end_date), auto_adjust=True)
        #df = yf.download(tickers=symbols_list, period="max", auto_adjust=True)

    except KeyError:
        pass
    print(df.head())
    df = df.stack()
    df.index.names = ['date', 'ticker']
    df.columns = df.columns.str.lower()
    print(df)
    print(len(df))
    garman_klass_volatility(df)
    rsi(df)
    bbands(df)
    rv_dataframe = df.to_csv("yfinance.csv", index=False)

if __name__=="__main__":
    main()
