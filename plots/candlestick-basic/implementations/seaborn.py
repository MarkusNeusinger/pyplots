"""
candlestick-basic: Basic Candlestick Chart
Library: seaborn
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Data - simulated 30 trading days of stock prices
np.random.seed(42)
n_days = 30

# Generate realistic OHLC data
dates = pd.date_range(start="2024-01-02", periods=n_days, freq="B")  # Business days
base_price = 150.0
returns = np.random.randn(n_days) * 0.02  # Daily returns ~2% std

# Build price series
close_prices = [base_price]
for r in returns[:-1]:
    close_prices.append(close_prices[-1] * (1 + r))
close_prices = np.array(close_prices)

# Generate OHLC from close prices
opens = np.roll(close_prices, 1)
opens[0] = base_price * 0.998

# High is max of open/close plus some random wick
highs = np.maximum(opens, close_prices) + np.abs(np.random.randn(n_days)) * 1.5

# Low is min of open/close minus some random wick
lows = np.minimum(opens, close_prices) - np.abs(np.random.randn(n_days)) * 1.5

df = pd.DataFrame({"date": dates, "open": opens, "high": highs, "low": lows, "close": close_prices})

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Candlestick colors
up_color = "#22c55e"  # Green for bullish
down_color = "#ef4444"  # Red for bearish

# Width for candle bodies
body_width = 0.6
wick_width = 2

# Draw each candlestick
for i, (_idx, row) in enumerate(df.iterrows()):
    is_up = row["close"] >= row["open"]
    color = up_color if is_up else down_color

    # Draw wick (high-low line)
    ax.plot([i, i], [row["low"], row["high"]], color=color, linewidth=wick_width, solid_capstyle="round")

    # Draw body (open-close rectangle)
    body_bottom = min(row["open"], row["close"])
    body_height = abs(row["close"] - row["open"])

    # Use a minimum height for doji candles
    if body_height < 0.1:
        body_height = 0.1
        body_bottom = (row["open"] + row["close"]) / 2 - 0.05

    rect = plt.Rectangle(
        (i - body_width / 2, body_bottom), body_width, body_height, facecolor=color, edgecolor=color, linewidth=1
    )
    ax.add_patch(rect)

# Format x-axis with dates
tick_positions = np.arange(0, len(df), 5)  # Every 5 days
ax.set_xticks(tick_positions)
ax.set_xticklabels([df["date"].iloc[i].strftime("%b %d") for i in tick_positions], fontsize=16)

# Set axis limits with padding
ax.set_xlim(-1, len(df))
ax.set_ylim(df["low"].min() - 2, df["high"].max() + 2)

# Labels and title
ax.set_xlabel("Date", fontsize=20)
ax.set_ylabel("Price ($)", fontsize=20)
ax.set_title("candlestick-basic · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="y", labelsize=16)

# Subtle grid for price levels
ax.grid(True, alpha=0.3, linestyle="--", axis="y")
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
