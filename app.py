import datetime as dt

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

# --- Strategy descriptions (portfolio-friendly) ---
STRATEGY_INFO = {
    "All In": (
        "Fully invested in equities at all times. "
        "Useful as a benchmark to compare against more sophisticated strategies."
    ),
    "All Out": (
        "Always in cash (0% equity exposure). "
        "Acts as a lower-bound benchmark for risk and performance."
    ),
    "SMA Crossover": (
        "Trend-following strategy based on short/long simple moving average crossovers. "
        "All-in when SMA_short > SMA_long, otherwise in cash."
    ),
    "Volatility Breakout": (
        "Momentum strategy that enters when price breaks above a volatility-adjusted threshold "
        "(SMA + k·sigma) and exits when price falls below the SMA."
    ),
    "Volatility Scaling": (
        "Gradually adjusts equity exposure using volatility bands around the SMA. "
        "Exposure increases on upper breakouts and decreases on lower breakouts."
    ),
    "Personal Strategy": (
        "Combines trend filtering (price above SMA) with volatility-based position sizing. "
        "Lower volatility leads to higher exposure; higher volatility reduces risk."
    ),
}

# --- Header ---
st.title("Systematic Trading Strategies")
st.write("Interactive visualization of systematic investment strategies.")

today = dt.date.today()
default_end = today - dt.timedelta(days=1)  # safer than "today" (timezone / market close issues)

# --- Sidebar controls ---
with st.sidebar:
    st.header("Data")
    ticker = st.text_input("Ticker", "SPY").strip().upper()

    start_date = st.date_input("Start date", value=dt.date(2018, 1, 1))
    end_date = st.date_input("End date", value=default_end)

    # Clamp future end dates automatically
    if end_date > today:
        st.info("End date was in the future — adjusted to today.")
        end_date = today

    st.header("Strategy")
    strategy_name = st.selectbox(
        "Select strategy",
        list(STRATEGY_INFO.keys()),
        index=0
    )

    st.caption(STRATEGY_INFO[strategy_name])

    # Build strategy + parameters
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

# --- Date validation ---
if start_date >= end_date:
    st.error("Start date must be earlier than end date.")
    st.stop()

# --- Data download ---
data = yf.download(ticker, start=start_date, end=end_date, progress=False)

if data is None or data.empty:
    st.error(
        f"No data returned for **{ticker}** between **{start_date}** and **{end_date}**. "
        "Try a different ticker or a longer date range."
    )
    st.stop()

price_col = "Adj Close" if "Adj Close" in data.columns else ("Close" if "Close" in data.columns else None)
if price_col is None:
    st.error("Downloaded data does not contain 'Adj Close' or 'Close'.")
    st.stop()

prices = data[price_col].dropna()
if prices.empty:
    st.error("Price series is empty after dropping missing values.")
    st.stop()

# Show basic data info (pro touch)
st.caption(
    f"Loaded **{len(prices)}** daily observations for **{ticker}** "
    f"from **{prices.index.min().date()}** to **{prices.index.max().date()}** "
    f"(source: Yahoo Finance, column: {price_col})."
)

if len(prices) < 50:
    st.warning("Not enough data. Please choose a longer date range (at least 50 observations).")
    st.stop()

# --- Backtest ---
result, metrics = run_backtest(prices.values, strategy)

# --- Charts (cleaner layout) ---
tab1, tab2 = st.tabs(["Price", "Equity Curve"])

with tab1:
    fig_price = go.Figure()
    fig_price.add_trace(go.Scatter(x=prices.index, y=result["price"], name="Price"))
    fig_price.update_layout(
        title=f"Price ({price_col})",
        xaxis_title="Date",
        yaxis_title="Price"
    )
    st.plotly_chart(fig_price, use_container_width=True)

with tab2:
    fig_equity = go.Figure()
    fig_equity.add_trace(go.Scatter(x=prices.index, y=result["equity"], name="Equity"))
    fig_equity.update_layout(
        title="Equity Curve",
        xaxis_title="Date",
        yaxis_title="Portfolio Value"
    )
    st.plotly_chart(fig_equity, use_container_width=True)

# --- Metrics ---
c1, c2 = st.columns(2)
c1.metric("Total Return", f"{metrics['total_return']*100:.2f}%")
c2.metric("Max Drawdown", f"{metrics['max_drawdown']*100:.2f}%")


