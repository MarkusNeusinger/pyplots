"""
candlestick-basic: Basic Candlestick Chart
Library: matplotlib
"""

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Data - Generate realistic stock price data for 30 trading days
np.random.seed(42)
n_days = 30

# Start date and generate business days
dates = pd.bdate_range(start="2024-01-02", periods=n_days)

# Generate random walk for prices starting at $150
returns = np.random.randn(n_days) * 0.02  # 2% daily volatility
price_series = 150 * np.exp(np.cumsum(returns))

# Generate OHLC data
open_prices = []
high_prices = []
low_prices = []
close_prices = []

for base_price in price_series:
    # Random intraday movement
    intraday_range = base_price * np.random.uniform(0.01, 0.03)

    # Open near previous close or base
    open_price = base_price * (1 + np.random.uniform(-0.005, 0.005))

    # Close with some drift
    close_price = base_price * (1 + np.random.uniform(-0.015, 0.015))

    # High and low contain both open and close
    low_price = min(open_price, close_price) - np.random.uniform(0, intraday_range * 0.5)
    high_price = max(open_price, close_price) + np.random.uniform(0, intraday_range * 0.5)

    open_prices.append(open_price)
    high_prices.append(high_price)
    low_prices.append(low_price)
    close_prices.append(close_price)

df = pd.DataFrame({"date": dates, "open": open_prices, "high": high_prices, "low": low_prices, "close": close_prices})

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

# Width for candlesticks (in days)
width = 0.6

# Colors for up/down days
color_up = "#26a69a"  # Green for bullish
color_down = "#ef5350"  # Red for bearish

# Draw candlesticks
for _i, row in df.iterrows():
    date_num = mdates.date2num(row["date"])

    # Determine if bullish or bearish
    if row["close"] >= row["open"]:
        color = color_up
        body_bottom = row["open"]
        body_height = row["close"] - row["open"]
    else:
        color = color_down
        body_bottom = row["close"]
        body_height = row["open"] - row["close"]

    # Draw wick (high-low line)
    ax.plot([date_num, date_num], [row["low"], row["high"]], color=color, linewidth=2, solid_capstyle="round")

    # Draw body (open-close rectangle)
    rect = plt.Rectangle(
        (date_num - width / 2, body_bottom),
        width,
        body_height if body_height > 0 else 0.01,  # Minimum height for doji
        facecolor=color,
        edgecolor=color,
        linewidth=1.5,
    )
    ax.add_patch(rect)

# Format x-axis with dates
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
ax.xaxis.set_minor_locator(mdates.DayLocator())

# Style
ax.set_xlabel("Date", fontsize=20)
ax.set_ylabel("Price ($)", fontsize=20)
ax.set_title("candlestick-basic · matplotlib · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.tick_params(axis="x", rotation=45)

# Grid for reading price levels
ax.grid(True, alpha=0.3, linestyle="--", axis="y")
ax.grid(True, alpha=0.15, linestyle="--", axis="x")

# Set y-axis limits with padding
y_min = df["low"].min()
y_max = df["high"].max()
y_padding = (y_max - y_min) * 0.1
ax.set_ylim(y_min - y_padding, y_max + y_padding)

# Set x-axis limits with padding
x_min = mdates.date2num(df["date"].min())
x_max = mdates.date2num(df["date"].max())
ax.set_xlim(x_min - 1, x_max + 1)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
