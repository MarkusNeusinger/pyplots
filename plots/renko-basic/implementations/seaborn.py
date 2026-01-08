""" pyplots.ai
renko-basic: Basic Renko Chart
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 62/100 | Created: 2026-01-08
"""

import matplotlib.patches as mpatches
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

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Define colors
bullish_color = "#2E7D32"  # Green for up bricks
bearish_color = "#C62828"  # Red for down bricks

# Draw Renko bricks using matplotlib patches (seaborn doesn't have native Renko)
brick_width = 0.8
gap = 0.1

for i, row in renko_df.iterrows():
    x = i
    bottom = min(row["open"], row["close"])
    height = brick_size
    color = bullish_color if row["direction"] == "up" else bearish_color

    # Draw brick as rectangle
    rect = mpatches.Rectangle(
        (x + gap / 2, bottom), brick_width, height, linewidth=1.5, edgecolor="white", facecolor=color, alpha=0.9
    )
    ax.add_patch(rect)

# Set axis limits
ax.set_xlim(-1, len(renko_df) + 1)
price_min = renko_df[["open", "close"]].min().min() - brick_size
price_max = renko_df[["open", "close"]].max().max() + brick_size
ax.set_ylim(price_min, price_max)

# Add visual reference using seaborn - horizontal lines at key price levels
price_levels = np.arange(
    np.floor(price_min / (brick_size * 2)) * brick_size * 2, price_max + brick_size * 2, brick_size * 2
)

for level in price_levels:
    ax.axhline(y=level, color="#306998", alpha=0.2, linestyle="--", linewidth=1)

# Labels and styling
ax.set_xlabel("Brick Index", fontsize=20)
ax.set_ylabel("Price ($)", fontsize=20)
ax.set_title("renko-basic · seaborn · pyplots.ai", fontsize=24, fontweight="bold")
ax.tick_params(axis="both", labelsize=16)

# Add legend
up_patch = mpatches.Patch(color=bullish_color, label="Bullish (Up)")
down_patch = mpatches.Patch(color=bearish_color, label="Bearish (Down)")
ax.legend(handles=[up_patch, down_patch], fontsize=16, loc="upper left")

# Add grid
ax.grid(True, alpha=0.3, linestyle="--")
ax.set_axisbelow(True)

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
