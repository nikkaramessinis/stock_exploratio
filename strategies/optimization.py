from utils.helpers import fetch_latest_data, fill_with_ta
from backtesting import Backtest


def optimize(strategy, symbols_list):
    upper_bounds, lower_bounds, rsi_window = 0, 0, 0

    for symbol in symbols_list:
        print("Calling fetching data")
        df = fetch_latest_data(symbol)
        df = fill_with_ta(df)

        bt = Backtest(df, strategy, cash=1000, commission=0.002, exclusive_orders=True)
        stats, optiheatmap = bt.optimize(upper_bound=range(10, 85, 5),
                            lower_bound=range(10, 45, 5),
                            rsi_window=range(10, 30, 2),
                            maximize="Equity Final [$]",
                            constraint= lambda param: param.upper_bound > param.lower_bound,
                            return_heatmap = True
                            )
        best_params = optiheatmap.idxmax()
        upper_bound = best_params[0]
        lower_bound = best_params[1]
        rsi_window = best_params[2]
        upper_bounds += upper_bound
        lower_bound +=lower_bounds
        rsi_window += rsi_window
        stats['Name'] = symbol
    upper_bound = upper_bounds/len(symbols_list)
    lower_bound = lower_bounds/len(symbols_list)
    rsi_window = rsi_window/len(symbols_list)