""" pyplots.ai
candlestick-basic: Basic Candlestick Chart
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 85/100 | Created: 2025-12-23
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
df["day_type"] = df.apply(lambda row: "Bullish (Up)" if row["close"] >= row["open"] else "Bearish (Down)", axis=1)
# Colorblind-safe: blue for up, orange for down
color_map = {"Bullish (Up)": "#1f77b4", "Bearish (Down)": "#ff7f0e"}
df["x"] = range(len(df))

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))

# Use seaborn lineplot for wicks by plotting high-low connections
for _, row in df.iterrows():
    color = color_map[row["day_type"]]
    # Use seaborn lineplot for each wick
    wick_segment = pd.DataFrame({"x": [row["x"], row["x"]], "y": [row["low"], row["high"]]})
    sns.lineplot(data=wick_segment, x="x", y="y", ax=ax, color=color, linewidth=2, legend=False)

# Prepare body data for seaborn barplot
body_data = []
for _, row in df.iterrows():
    body_bottom = min(row["open"], row["close"])
    body_height = abs(row["close"] - row["open"])
    # Ensure minimum body height for doji candles
    if body_height < 0.2:
        body_height = 0.2
        body_bottom = (row["open"] + row["close"]) / 2 - 0.1
    body_data.append({"x": row["x"], "bottom": body_bottom, "height": body_height, "day_type": row["day_type"]})
body_df = pd.DataFrame(body_data)

# Use seaborn barplot for candle bodies
sns.barplot(data=body_df, x="x", y="height", hue="day_type", palette=color_map, ax=ax, width=0.6, legend=False)

# Adjust bar positions to correct bottom values
for bar, (_, row) in zip(ax.patches, body_df.iterrows(), strict=False):
    bar.set_y(row["bottom"])

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

# Add legend - positioned outside data area to avoid overlap
legend_elements = [Patch(facecolor="#1f77b4", label="Bullish (Up)"), Patch(facecolor="#ff7f0e", label="Bearish (Down)")]
ax.legend(handles=legend_elements, fontsize=14, loc="upper right", bbox_to_anchor=(0.99, 0.99))

# Subtle grid
ax.grid(True, alpha=0.3, linestyle="--", axis="y")
ax.set_axisbelow(True)

# Set reasonable y-axis margins
ax.margins(x=0.02)
y_min = df["low"].min()
y_max = df["high"].max()
y_padding = (y_max - y_min) * 0.1
ax.set_ylim(y_min - y_padding, y_max + y_padding)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
