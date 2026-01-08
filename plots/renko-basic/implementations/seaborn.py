""" pyplots.ai
renko-basic: Basic Renko Chart
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 58/100 | Created: 2026-01-08
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Set seaborn style
sns.set_style("whitegrid")
sns.set_context("talk", font_scale=1.2)

# Generate synthetic stock price data
np.random.seed(42)
n_days = 250
dates = pd.date_range("2025-01-01", periods=n_days, freq="D")

# Simulate price movement with random walk
returns = np.random.normal(0.0005, 0.015, n_days)
prices = 100 * np.cumprod(1 + returns)

df = pd.DataFrame({"date": dates, "close": prices})

# Renko brick calculation
brick_size = 2.0  # $2 per brick
bricks = []

# Start from first price
current_price = df["close"].iloc[0]
brick_high = np.floor(current_price / brick_size) * brick_size
brick_low = brick_high

for price in df["close"]:
    # Check for upward bricks
    while price >= brick_high + brick_size:
        brick_high += brick_size
        brick_low = brick_high - brick_size
        bricks.append({"direction": "up", "open": brick_low, "close": brick_high})

    # Check for downward bricks
    while price <= brick_low - brick_size:
        brick_low -= brick_size
        brick_high = brick_low + brick_size
        bricks.append({"direction": "down", "open": brick_high, "close": brick_low})

renko_df = pd.DataFrame(bricks)
renko_df["brick_index"] = range(len(renko_df))
renko_df["bottom"] = renko_df[["open", "close"]].min(axis=1)

# Colorblind-accessible colors: blue for bullish, orange for bearish
bullish_color = "#1976D2"  # Blue for up bricks
bearish_color = "#E65100"  # Orange for down bricks

# Create expanded dataframe for seaborn barplot with gap between bricks
# Each brick will be represented as a bar from bottom to bottom+brick_size
bar_data = []
gap_size = 0.15  # Small gap between bricks as per spec

for idx, row in renko_df.iterrows():
    bar_data.append(
        {
            "brick_index": idx,
            "bottom": row["bottom"],
            "height": brick_size,
            "direction": "Bullish (Up)" if row["direction"] == "up" else "Bearish (Down)",
        }
    )

bar_df = pd.DataFrame(bar_data)

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Use seaborn barplot to draw the Renko bricks
# We plot bars with bottom offset using matplotlib's bar with seaborn styling
palette = {"Bullish (Up)": bullish_color, "Bearish (Down)": bearish_color}

# Draw bricks using seaborn's barplot function
# First create a grouped approach where each brick is a separate category
sns.barplot(
    data=bar_df,
    x="brick_index",
    y="height",
    hue="direction",
    palette=palette,
    dodge=False,
    ax=ax,
    width=1.0 - gap_size,
    edgecolor="white",
    linewidth=1.5,
)

# Adjust bar positions to correct y-position (barplot draws from 0)
# We need to offset each bar to its correct price level
for i, patch in enumerate(ax.patches):
    if i < len(bar_df):
        patch.set_y(bar_df.iloc[i]["bottom"])

# Set axis limits with padding
price_min = renko_df[["open", "close"]].min().min() - brick_size
price_max = renko_df[["open", "close"]].max().max() + brick_size
ax.set_ylim(price_min, price_max)
ax.set_xlim(-1, len(renko_df) + 1)

# Labels and styling
ax.set_xlabel("Brick Index", fontsize=20)
ax.set_ylabel("Price ($)", fontsize=20)
ax.set_title("renko-basic · seaborn · pyplots.ai", fontsize=24, fontweight="bold")
ax.tick_params(axis="both", labelsize=16)

# Adjust legend
ax.legend(fontsize=16, loc="upper left", title=None)

# Add subtle grid
ax.grid(True, alpha=0.3, linestyle="--", axis="y")
ax.set_axisbelow(True)

# Simplify x-axis ticks for cleaner look
tick_step = max(1, len(renko_df) // 10)
ax.set_xticks(range(0, len(renko_df), tick_step))

# Add annotation about brick size
ax.annotate(
    f"Brick Size: ${brick_size:.0f}",
    xy=(0.98, 0.02),
    xycoords="axes fraction",
    fontsize=14,
    ha="right",
    va="bottom",
    bbox={"boxstyle": "round,pad=0.5", "facecolor": "white", "edgecolor": "gray", "alpha": 0.8},
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
