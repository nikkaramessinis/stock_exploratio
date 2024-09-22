import pandas as pd
from backtesting import Backtest

from cli.weightcalculation import calculate_weights
from config.feqos import merge_reference_with_test
from optimizers.optimizer import Optimizer
from optimizers.strategy_params import get_params_defaults, get_params_ranges
from utils.helpers import check_crossover, fetch_latest_data, fill_with_ta


def analyze(
    strategy, symbols_list, display_dashboard, save_as_reference, weights, param_ranges
):

    print(weights.columns)
    results_dataframe = pd.DataFrame()
    symbol_data = {}

    for index, symbol in enumerate(symbols_list):
        print(f"Fetching data for {symbol}")
        df = fetch_latest_data(symbol)
        df = fill_with_ta(df)

        check_crossover(df)
        stock_weight = weights.iloc[index, 0]
        print(f"stock_weight {stock_weight}")

        bt = Backtest(
            df,
            strategy,
            cash=1000 * stock_weight,
            commission=0.002,
            exclusive_orders=True,
        )

        if param_ranges:
            stats = bt.optimize(
                **param_ranges,
                maximize="Equity Final [$]",
                constraint=lambda param: param.upper_bound > param.lower_bound,
            )
        else:
            stats = bt.run()

        bt.plot(filename=f"csvs/{symbol}")
        # print(f"type(stats {type(stats)}")
        stats["Name"] = symbol
        stats["Cash"] = 1000 * stock_weight
        results_dataframe = results_dataframe._append(stats, ignore_index=True)

        # Store the DataFrame for each symbol
        symbol_data[symbol] = df

    results_dataframe.to_csv("csvs/stats.csv", index=False)

    if display_dashboard:
        merge_reference_with_test(results_dataframe, symbol_data)

    if save_as_reference:
        results_dataframe.to_csv("csvs/reference.csv", index=False)
    return results_dataframe, symbol_data


def run_prediction(
    strategy,
    strategy_name,
    stocks_list,
    display_dashboard,
    save_reference,
    enable_optimizing,
    enable_opt_portfolio,
):
    args = get_params_defaults(strategy_name)
    weights = pd.DataFrame({"weights": [1] * len(stocks_list)})
    if enable_opt_portfolio:
        weights = calculate_weights(stocks_list)

    current_optimizer = Optimizer(strategy, stocks_list, args)
    if enable_optimizing:
        optimized_args = current_optimizer.optimize(
            weights, get_params_ranges(strategy_name)
        )
        args = {
            key: (range(value, value + 1, 5)) for key, value in optimized_args.items()
        }
    return analyze(
        strategy, stocks_list, display_dashboard, save_reference, weights, args
    )
