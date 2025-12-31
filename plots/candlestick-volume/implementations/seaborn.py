"""pyplots.ai
candlestick-volume: Stock Candlestick Chart with Volume
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-12-31
"""

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import Patch


# Set seaborn style for consistent aesthetics
sns.set_style("whitegrid")
sns.set_context("talk", font_scale=1.2)

# Generate realistic stock data for 60 trading days
np.random.seed(42)
n_days = 60

# Start with a base price and generate realistic price movements
dates = pd.date_range("2024-01-02", periods=n_days, freq="B")  # Business days
base_price = 150.0

# Generate price series with trends and volatility
returns = np.random.normal(0.001, 0.02, n_days)  # Daily returns
prices = base_price * np.cumprod(1 + returns)

# Generate OHLC from the price series
opens = np.zeros(n_days)
highs = np.zeros(n_days)
lows = np.zeros(n_days)
closes = np.zeros(n_days)

opens[0] = base_price
for i in range(n_days):
    if i > 0:
        opens[i] = closes[i - 1] + np.random.normal(0, 0.5)
    closes[i] = prices[i]
    daily_range = abs(closes[i] - opens[i]) + np.random.uniform(0.5, 2.0)
    highs[i] = max(opens[i], closes[i]) + np.random.uniform(0.2, daily_range * 0.5)
    lows[i] = min(opens[i], closes[i]) - np.random.uniform(0.2, daily_range * 0.5)

# Generate volume with some correlation to price movements
base_volume = 5_000_000
volume = base_volume + np.random.normal(0, 1_000_000, n_days)
# Higher volume on bigger price moves
price_change = np.abs(closes - opens)
volume = volume + price_change * 500_000
volume = np.clip(volume, 1_000_000, 15_000_000).astype(int)

# Create DataFrame
df = pd.DataFrame({"date": dates, "open": opens, "high": highs, "low": lows, "close": closes, "volume": volume})

# Determine bullish (green) vs bearish (red) candles
df["bullish"] = df["close"] >= df["open"]
df["color"] = df["bullish"].map({True: "#306998", False: "#FFD43B"})  # Python Blue/Yellow
df["date_num"] = mdates.date2num(df["date"])

# Create figure with two subplots sharing x-axis (75% price, 25% volume)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 9), height_ratios=[3, 1], sharex=True, gridspec_kw={"hspace": 0.05})

# === Upper pane: Candlestick chart ===
# Draw wicks (high-low lines)
for _idx, row in df.iterrows():
    ax1.plot(
        [row["date_num"], row["date_num"]],
        [row["low"], row["high"]],
        color=row["color"],
        linewidth=1.5,
        solid_capstyle="round",
    )

# Draw candle bodies using seaborn-style bar approach
candle_width = 0.6
for _idx, row in df.iterrows():
    body_bottom = min(row["open"], row["close"])
    body_height = abs(row["close"] - row["open"])
    if body_height < 0.1:  # Doji handling - minimum visible height
        body_height = 0.1
    ax1.bar(
        row["date_num"],
        body_height,
        bottom=body_bottom,
        width=candle_width,
        color=row["color"],
        edgecolor=row["color"],
        linewidth=1,
    )

# Style the price axis
ax1.set_ylabel("Price ($)", fontsize=20)
ax1.tick_params(axis="both", labelsize=16)
ax1.grid(True, alpha=0.3, linestyle="--")
ax1.set_title("candlestick-volume · seaborn · pyplots.ai", fontsize=24, pad=15)

# Set y-axis range with padding
price_min = df["low"].min()
price_max = df["high"].max()
price_padding = (price_max - price_min) * 0.05
ax1.set_ylim(price_min - price_padding, price_max + price_padding)

# === Lower pane: Volume bars ===
# Create volume bar chart with colors matching candlesticks
for _idx, row in df.iterrows():
    ax2.bar(row["date_num"], row["volume"], width=candle_width, color=row["color"], edgecolor=row["color"], alpha=0.8)

# Style the volume axis
ax2.set_ylabel("Volume", fontsize=20)
ax2.set_xlabel("Date", fontsize=20)
ax2.tick_params(axis="both", labelsize=16)
ax2.grid(True, alpha=0.3, linestyle="--")

# Format y-axis for volume (millions)
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{x / 1e6:.1f}M"))

# Format x-axis dates
ax2.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO, interval=2))
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha="right")

# Add legend
legend_elements = [
    Patch(facecolor="#306998", label="Bullish (Close ≥ Open)"),
    Patch(facecolor="#FFD43B", label="Bearish (Close < Open)"),
]
ax1.legend(handles=legend_elements, loc="upper left", fontsize=14, framealpha=0.9)

# Adjust layout and save
fig.subplots_adjust(left=0.08, right=0.95, top=0.92, bottom=0.12, hspace=0.05)
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
