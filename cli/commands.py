import json
import os

import pandas as pd

from core.email_alert import schedule_email_alert
from core.prediction_strategy import run_prediction
from strategies.backtesting_bollinger_bands import BBandsCross
from strategies.backtesting_ema import EmaCross
from strategies.backtesting_grip import GridCross
from strategies.backtesting_mix import MixCross
from strategies.backtesting_ml import LogisticRegressionCross
from strategies.backtesting_rsi import RSIOscillatorCross
from strategies.backtesting_sma import SmaCross
from strategies.live_strategy_reminder import live_strategy

strategies = {
    "SMA": SmaCross,
    "EMA": EmaCross,
    "RSI": RSIOscillatorCross,
    "BBands": BBandsCross,
    "Mix": MixCross,
    "Logistic": LogisticRegressionCross,
    # Add other strategies here
}


def run_strategy(args):
    flow_name = args.flow_name
    strategy_name = args.strategy
    stocks_list = args.stocks_list
    display_dashboard = args.display_dashboard
    save_reference = args.save_reference
    enable_optimizing = args.enable_optimizing
    enable_opt_portfolio = args.enable_opt_portfolio

    if not strategy_name:
        print("Strategy name is required.")
        return

    if strategy_name in strategies:
        strategy = strategies[strategy_name]

        print(f"Running strategy: {strategy_name} with flow {flow_name}")

        if flow_name == "optimization":
            run_prediction(
                strategy,
                strategy_name,
                stocks_list,
                display_dashboard,
                save_reference,
                enable_optimizing,
                enable_opt_portfolio,
            )
        elif flow_name == "live":
            live_strategy(strategy, stocks_list)
    else:
        assert False, f"Unknown strategy: {strategy_name} add it in strategies"
        return


def email_alerts(args):
    try:
        email_config = json.loads(args.email) if args.email else {}
        schedule_email_alert(email_config)
    except json.JSONDecodeError:
        print("Invalid JSON format for email configuration.")
