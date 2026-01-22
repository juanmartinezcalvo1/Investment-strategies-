import numpy as np
import pandas as pd

def max_drawdown(equity):
    peak = equity.cummax()
    drawdown = equity / peak - 1.0
    return drawdown.min()

def run_backtest(prices, strategy, initial_cash=10_000):
    cash = initial_cash
    shares = 0.0

    equity_curve = []
    weights = []

    past_prices = []

    for i, price in enumerate(prices):
        portfolio_value = cash + shares * price
        equity_curve.append(portfolio_value)

        weight = (shares * price / portfolio_value) if portfolio_value > 0 else 0.0
        weights.append(weight)

        past_prices.append(price)

        if i == 0:
            continue

        target_weight = strategy.percentage_in_actions(past_prices, cash, shares)
        target_weight = max(0.0, min(1.0, target_weight))

        target_stock_value = target_weight * portfolio_value
        current_stock_value = shares * price
        trade_value = target_stock_value - current_stock_value

        if trade_value > 0:
            buy = min(cash, trade_value)
            shares += buy / price
            cash -= buy
        elif trade_value < 0:
            sell = min(current_stock_value, -trade_value)
            shares -= sell / price
            cash += sell

    result = pd.DataFrame({
        "price": prices,
        "equity": equity_curve,
        "weight": weights
    })

    metrics = {
        "total_return": equity_curve[-1] / equity_curve[0] - 1,
        "max_drawdown": max_drawdown(pd.Series(equity_curve))
    }

    return result, metrics
