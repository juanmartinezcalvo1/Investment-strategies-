import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

from backtest import run_backtest
from all_in import AllInStrategy
from all_out import AllOutStrategy
from sma_cross import SmaCrossStrategy
from vol_breakout import VolBreakoutStrategy
from Vol_scaling import VolScalingStrategy
from personal_strategy import PersonalStrategy

st.set_page_config(page_title="Quant Trading Strategies", layout="wide")

st.title("Systematic Trading Strategies")
st.write("Interactive visualization of systematic investment strategies.")

with st.sidebar:
    ticker = st.text_input("Ticker", "SPY")
    start_date = st.date_input("Start date", value=None)
    end_date = st.date_input("End date", value=None)

    strategy_name = st.selectbox(
        "Select strategy",
        [
            "All In",
            "All Out",
            "SMA Crossover",
            "Volatility Breakout",
            "Volatility Scaling",
            "Personal Strategy"
        ]
    )

    if strategy_name == "SMA Crossover":
        short = st.slider("Short SMA", 5, 100, 20)
        long = st.slider("Long SMA", 20, 300, 100)
        strategy = SmaCrossStrategy(short, long)

    elif strategy_name == "Volatility Breakout":
        size = st.slider("Window size", 10, 200, 50)
        mult = st.slider("Sigma multiplier", 0.5, 5.0, 2.0)
        strategy = VolBreakoutStrategy(size, mult)

    elif strategy_name == "Volatility Scaling":
        size = st.slider("Window size", 10, 200, 50)
        mult = st.slider("Sigma multiplier", 0.5, 5.0, 2.0)
        strategy = VolScalingStrategy(size, mult)

    elif strategy_name == "Personal Strategy":
        sma = st.slider("SMA window", 20, 300, 100)
        vol = st.slider("Vol window", 10, 100, 30)
        vlow = st.slider("Low vol", 0.1, 5.0, 1.0)
        vhigh = st.slider("High vol", 1.0, 10.0, 3.0)
        strategy = PersonalStrategy(sma, vol, vlow, vhigh)

    elif strategy_name == "All Out":
        strategy = AllOutStrategy()

    else:
        strategy = AllInStrategy()

prices = yf.download(ticker, start=start_date, end=end_date)["Adj Close"].dropna()

if len(prices) < 50:
    st.warning("Not enough data.")
    st.stop()

result, metrics = run_backtest(prices.values, strategy)

fig = go.Figure()
fig.add_trace(go.Scatter(y=result["price"], name="Price"))
fig.add_trace(go.Scatter(y=result["equity"], name="Equity"))

st.plotly_chart(fig, use_container_width=True)

st.metric("Total Return", f"{metrics['total_return']*100:.2f}%")
st.metric("Max Drawdown", f"{metrics['max_drawdown']*100:.2f}%")
