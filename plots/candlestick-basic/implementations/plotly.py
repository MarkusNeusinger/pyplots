""" pyplots.ai
candlestick-basic: Basic Candlestick Chart
Library: plotly 6.5.0 | Python 3.13.11
Quality: 100/100 | Created: 2025-12-14
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go


# Data - 30 trading days of simulated stock prices
np.random.seed(42)
dates = pd.date_range(start="2024-01-02", periods=30, freq="B")  # Business days

# Generate realistic price movement starting at $100
price = 100.0
opens, highs, lows, closes = [], [], [], []

for _ in range(30):
    open_price = price
    # Random daily change with slight upward bias
    change = np.random.randn() * 2 + 0.1
    close_price = open_price + change

    # High is above both open and close, low is below both
    high_price = max(open_price, close_price) + abs(np.random.randn()) * 1.5
    low_price = min(open_price, close_price) - abs(np.random.randn()) * 1.5

    opens.append(open_price)
    highs.append(high_price)
    lows.append(low_price)
    closes.append(close_price)

    price = close_price

df = pd.DataFrame({"date": dates, "open": opens, "high": highs, "low": lows, "close": closes})

# Create candlestick chart
fig = go.Figure(
    data=[
        go.Candlestick(
            x=df["date"],
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            increasing={"line": {"color": "#26A69A", "width": 2}, "fillcolor": "#26A69A"},
            decreasing={"line": {"color": "#EF5350", "width": 2}, "fillcolor": "#EF5350"},
        )
    ]
)

# Layout with proper sizing for 4800x2700
fig.update_layout(
    title={"text": "candlestick-basic · plotly · pyplots.ai", "font": {"size": 28}, "x": 0.5, "xanchor": "center"},
    xaxis={
        "title": {"text": "Date", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "rangeslider": {"visible": False},
        "gridcolor": "rgba(128, 128, 128, 0.3)",
        "gridwidth": 1,
    },
    yaxis={
        "title": {"text": "Price ($)", "font": {"size": 22}},
        "tickfont": {"size": 18},
        "gridcolor": "rgba(128, 128, 128, 0.3)",
        "gridwidth": 1,
    },
    template="plotly_white",
    plot_bgcolor="white",
    margin={"l": 80, "r": 40, "t": 80, "b": 80},
)

# Save as PNG (4800x2700)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save interactive HTML
fig.write_html("plot.html", include_plotlyjs=True, full_html=True)
