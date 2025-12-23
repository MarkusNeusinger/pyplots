""" pyplots.ai
candlestick-basic: Basic Candlestick Chart
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 90/100 | Created: 2025-12-23
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import Patch


# Set seaborn style
sns.set_theme(style="whitegrid")
sns.set_context("talk", font_scale=1.2)

# Data - 30 days of simulated stock OHLC data
np.random.seed(42)
n_days = 30
dates = pd.date_range("2024-01-02", periods=n_days, freq="B")  # Business days

# Generate realistic OHLC data
price = 150.0
opens, highs, lows, closes = [], [], [], []

for _ in range(n_days):
    # Daily volatility
    change = np.random.randn() * 3
    daily_range = abs(np.random.randn()) * 2 + 1

    open_price = price
    close_price = price + change

    # High and low include the open/close range plus some extra
    high_price = max(open_price, close_price) + abs(np.random.randn()) * daily_range
    low_price = min(open_price, close_price) - abs(np.random.randn()) * daily_range

    opens.append(open_price)
    highs.append(high_price)
    lows.append(low_price)
    closes.append(close_price)

    price = close_price

df = pd.DataFrame({"date": dates, "open": opens, "high": highs, "low": lows, "close": closes})

# Determine bullish (up) vs bearish (down) days - use colorblind-safe colors
df["bullish"] = df["close"] >= df["open"]
# Colorblind-safe: blue for up, orange for down
color_up = "#1f77b4"  # Blue for bullish
color_down = "#ff7f0e"  # Orange for bearish
df["color"] = df["bullish"].map({True: color_up, False: color_down})
df["x"] = range(len(df))

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))

# Draw candlesticks manually with seaborn styling applied
body_width = 0.6

for _, row in df.iterrows():
    x = row["x"]
    color = row["color"]

    # Draw wick (high-low line) using seaborn's lineplot via dataframe
    wick_data = pd.DataFrame({"x": [x, x], "price": [row["low"], row["high"]]})
    sns.lineplot(data=wick_data, x="x", y="price", ax=ax, color=color, linewidth=2, legend=False)

    # Draw candle body using matplotlib Rectangle for precise control
    body_bottom = min(row["open"], row["close"])
    body_height = abs(row["close"] - row["open"])
    # Ensure minimum body height for doji candles
    if body_height < 0.2:
        body_height = 0.2
        body_bottom = (row["open"] + row["close"]) / 2 - 0.1

    rect = plt.Rectangle(
        (x - body_width / 2, body_bottom), body_width, body_height, facecolor=color, edgecolor=color, linewidth=1
    )
    ax.add_patch(rect)

# Set x-axis to show dates
tick_positions = range(0, n_days, 5)  # Show every 5th date
tick_labels = [df["date"].iloc[i].strftime("%b %d") for i in tick_positions]
ax.set_xticks(tick_positions)
ax.set_xticklabels(tick_labels, rotation=0)

# Style the plot
ax.set_xlabel("Date", fontsize=20)
ax.set_ylabel("Price ($)", fontsize=20)
ax.set_title("candlestick-basic · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)

# Add legend with colorblind-safe colors - positioned outside data area
legend_elements = [Patch(facecolor=color_up, label="Bullish (Up)"), Patch(facecolor=color_down, label="Bearish (Down)")]
ax.legend(handles=legend_elements, fontsize=14, loc="upper right", bbox_to_anchor=(0.99, 0.99))

# Subtle grid
ax.grid(True, alpha=0.3, linestyle="--", axis="y")
ax.set_axisbelow(True)

# Set axis limits
ax.set_xlim(-0.5, n_days - 0.5)
y_min = df["low"].min()
y_max = df["high"].max()
y_padding = (y_max - y_min) * 0.1
ax.set_ylim(y_min - y_padding, y_max + y_padding)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
