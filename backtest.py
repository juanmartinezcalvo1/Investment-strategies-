import numpy as np
import pandas as pd


def max_drawdown(equity: pd.Series) -> float:
    peak = equity.cummax()
    drawdown = equity / peak - 1.0
    return float(drawdown.min())


def run_backtest(prices, strategy, initial_cash: float = 10_000):
    # ✅ Ensure prices is a 1D float numpy array (handles (n,1), Series, lists, etc.)
    prices = np.asarray(prices, dtype=float).reshape(-1)

    cash = float(initial_cash)
    shares = 0.0

    equity_curve = []
    weights = []

    past_prices = []

    for i, price in enumerate(prices):
        price = float(price)

        portfolio_value = cash + shares * price
        equity_curve.append(portfolio_value)

        weight = (shares * price / portfolio_value) if portfolio_value > 0 else 0.0
        weights.append(weight)

        past_prices.append(price)

        if i == 0:
            continue

        target_weight = float(strategy.percentage_in_actions(past_prices, cash, shares))
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

    # ✅ Ensure columns are 1D arrays
    result = pd.DataFrame({
        "price": prices,
        "equity": np.asarray(equity_curve, dtype=float),
        "weight": np.asarray(weights, dtype=float),
    })

    metrics = {
        "total_return": float(equity_curve[-1] / equity_curve[0] - 1.0) if len(equity_curve) > 1 else 0.0,
        "max_drawdown": max_drawdown(pd.Series(equity_curve, dtype=float)),
    }

    return result, metrics
