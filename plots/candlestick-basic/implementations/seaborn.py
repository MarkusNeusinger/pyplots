""" pyplots.ai
candlestick-basic: Basic Candlestick Chart
Library: seaborn 0.13.2 | Python 3.14.3
Quality: /100 | Updated: 2026-02-24
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.collections import PatchCollection
from matplotlib.patches import Patch, Rectangle


# Seaborn theme and context
sns.set_theme(
    style="whitegrid",
    rc={
        "axes.facecolor": "#f8f9fa",
        "figure.facecolor": "white",
        "grid.color": "#dee2e6",
        "text.color": "#212529",
        "axes.labelcolor": "#495057",
        "xtick.color": "#495057",
        "ytick.color": "#495057",
    },
)
sns.set_context("talk", font_scale=1.2)
up_fill, up_edge = "#2978b5", "#1b5a8a"
down_fill, down_edge = "#e07a3a", "#b35a1f"

# Data - 30 trading days with rally then selloff pattern
np.random.seed(42)
n_days = 30
dates = pd.date_range("2024-01-02", periods=n_days, freq="B")

price = 145.0
drift = np.concatenate(
    [
        np.linspace(0.4, 0.8, 12),  # Uptrend phase
        np.linspace(-0.1, -0.6, 18),  # Reversal and selloff
    ]
)
opens, highs, lows, closes = [], [], [], []
for i in range(n_days):
    change = drift[i] + np.random.randn() * 2.5
    volatility = abs(np.random.randn()) * 1.5 + 0.8
    open_price = price
    close_price = price + change
    high_price = max(open_price, close_price) + abs(np.random.randn()) * volatility
    low_price = min(open_price, close_price) - abs(np.random.randn()) * volatility
    opens.append(open_price)
    highs.append(high_price)
    lows.append(low_price)
    closes.append(close_price)
    price = close_price

df = pd.DataFrame({"date": dates, "open": opens, "high": highs, "low": lows, "close": closes})
df["bullish"] = df["close"] >= df["open"]
df["x"] = range(n_days)

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

# Wicks
wick_colors = [up_edge if b else down_edge for b in df["bullish"]]
ax.vlines(df["x"], df["low"], df["high"], colors=wick_colors, linewidth=1.5)

# Candle bodies via PatchCollection
body_width = 0.6
rects, fcolors, ecolors = [], [], []
for _, row in df.iterrows():
    bottom = min(row["open"], row["close"])
    height = max(abs(row["close"] - row["open"]), 0.15)
    if abs(row["close"] - row["open"]) < 0.15:
        bottom = (row["open"] + row["close"]) / 2 - 0.075
    rects.append(Rectangle((row["x"] - body_width / 2, bottom), body_width, height))
    fcolors.append(up_fill if row["bullish"] else down_fill)
    ecolors.append(up_edge if row["bullish"] else down_edge)

bodies = PatchCollection(rects, facecolors=fcolors, edgecolors=ecolors, linewidths=0.8)
ax.add_collection(bodies)

# X-axis date labels
tick_idx = range(0, n_days, 5)
ax.set_xticks(list(tick_idx))
ax.set_xticklabels([dates[i].strftime("%b %d") for i in tick_idx])

# Style
ax.set_xlabel("Date", fontsize=20)
ax.set_ylabel("Price ($)", fontsize=20)
ax.set_title("candlestick-basic \u00b7 seaborn \u00b7 pyplots.ai", fontsize=24, fontweight="medium", pad=16)
ax.tick_params(axis="both", labelsize=16, length=0)
sns.despine(ax=ax)
ax.yaxis.grid(True, alpha=0.15, linewidth=0.8)
ax.xaxis.grid(False)
ax.set_axisbelow(True)

# Legend
legend_handles = [
    Patch(facecolor=up_fill, edgecolor=up_edge, label="Bullish"),
    Patch(facecolor=down_fill, edgecolor=down_edge, label="Bearish"),
]
ax.legend(handles=legend_handles, fontsize=14, loc="upper left", framealpha=0.9, edgecolor="#dee2e6")

# Axis limits
ax.set_xlim(-0.8, n_days - 0.2)
y_pad = (df["high"].max() - df["low"].min()) * 0.08
ax.set_ylim(df["low"].min() - y_pad, df["high"].max() + y_pad)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
