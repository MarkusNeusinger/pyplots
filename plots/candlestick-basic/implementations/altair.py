""" pyplots.ai
candlestick-basic: Basic Candlestick Chart
Library: altair 6.0.0 | Python 3.13.11
Quality: 90/100 | Created: 2025-12-14
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Simulated 30 days of stock price data
np.random.seed(42)
n_days = 30
start_date = pd.Timestamp("2024-01-01")
dates = pd.date_range(start=start_date, periods=n_days, freq="B")  # Business days

# Generate realistic OHLC data with random walk
prices = [100.0]
for _ in range(n_days - 1):
    change = np.random.randn() * 2
    prices.append(prices[-1] + change)

data = []
for i, date in enumerate(dates):
    base = prices[i]
    volatility = np.random.uniform(1, 3)

    open_price = base + np.random.uniform(-volatility, volatility)
    close_price = base + np.random.uniform(-volatility, volatility)
    high_price = max(open_price, close_price) + np.random.uniform(0.5, volatility)
    low_price = min(open_price, close_price) - np.random.uniform(0.5, volatility)

    data.append(
        {
            "date": date,
            "open": round(open_price, 2),
            "high": round(high_price, 2),
            "low": round(low_price, 2),
            "close": round(close_price, 2),
        }
    )

df = pd.DataFrame(data)

# Add direction column for color encoding
df["direction"] = df.apply(lambda row: "up" if row["close"] >= row["open"] else "down", axis=1)

# Color scale: green for up, red for down
color_scale = alt.Scale(domain=["up", "down"], range=["#26A69A", "#EF5350"])

# Candlestick wicks (high-low lines)
wicks = (
    alt.Chart(df)
    .mark_rule(strokeWidth=2)
    .encode(
        x=alt.X("date:T", title="Date", axis=alt.Axis(labelFontSize=16, titleFontSize=20, format="%b %d")),
        y=alt.Y(
            "low:Q", title="Price ($)", scale=alt.Scale(zero=False), axis=alt.Axis(labelFontSize=16, titleFontSize=20)
        ),
        y2="high:Q",
        color=alt.Color("direction:N", scale=color_scale, legend=None),
    )
)

# Candlestick bodies (open-close bars)
bodies = (
    alt.Chart(df)
    .mark_bar(size=20)
    .encode(
        x="date:T",
        y="open:Q",
        y2="close:Q",
        color=alt.Color(
            "direction:N", scale=color_scale, legend=alt.Legend(title="Direction", labelFontSize=14, titleFontSize=16)
        ),
    )
)

# Layer wicks and bodies
chart = (
    alt.layer(wicks, bodies)
    .properties(
        width=1600, height=900, title=alt.Title("candlestick-basic · altair · pyplots.ai", fontSize=28, anchor="middle")
    )
    .configure_axis(labelFontSize=16, titleFontSize=20, gridOpacity=0.3)
    .configure_view(strokeWidth=0)
)

# Save as PNG and HTML
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
