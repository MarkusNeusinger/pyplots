""" pyplots.ai
area-stock-range: Stock Area Chart with Range Selector
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 91/100 | Created: 2026-01-11
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data - Generate realistic stock price data
np.random.seed(42)
dates = pd.date_range("2022-01-01", periods=750, freq="B")  # ~3 years of business days
returns = np.random.normal(0.0005, 0.018, len(dates))  # Daily returns
price = 100 * np.cumprod(1 + returns)  # Starting price $100

df = pd.DataFrame({"date": dates, "price": price})

# Define selected range (simulating range selector - last 6 months)
range_start = dates[-130]  # ~6 months of trading days
range_end = dates[-1]
df_selected = df[(df["date"] >= range_start) & (df["date"] <= range_end)]

# Create figure with two subplots (main chart + range selector)
fig, (ax_main, ax_range) = plt.subplots(2, 1, figsize=(16, 9), height_ratios=[4, 1], sharex=False)
fig.subplots_adjust(hspace=0.15)

# Main chart - selected range with gradient fill effect
sns.lineplot(data=df_selected, x="date", y="price", ax=ax_main, color="#306998", linewidth=2.5)

# Set y-axis range to focus on data (not starting at 0)
price_min, price_max = df_selected["price"].min(), df_selected["price"].max()
y_padding = (price_max - price_min) * 0.1
ax_main.set_ylim(price_min - y_padding, price_max + y_padding)

# Fill with gradient effect (layered fills from bottom)
fill_bottom = price_min - y_padding
ax_main.fill_between(df_selected["date"], df_selected["price"], fill_bottom, alpha=0.4, color="#306998")

ax_main.set_title("area-stock-range · seaborn · pyplots.ai", fontsize=24, fontweight="bold", pad=15)
ax_main.set_xlabel("")
ax_main.set_ylabel("Price (USD)", fontsize=20)
ax_main.tick_params(axis="both", labelsize=16)
ax_main.grid(True, alpha=0.3, linestyle="--")

# Format main chart y-axis
ax_main.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:.0f}"))

# Range selector (mini chart showing full history)
sns.lineplot(data=df, x="date", y="price", ax=ax_range, color="#306998", linewidth=1.5)
ax_range.fill_between(df["date"], df["price"], alpha=0.25, color="#306998")

# Highlight selected range with shading
ax_range.axvspan(range_start, range_end, alpha=0.3, color="#FFD43B", zorder=2)

# Add range handles (vertical lines)
ax_range.axvline(range_start, color="#FFD43B", linewidth=3, zorder=3)
ax_range.axvline(range_end, color="#FFD43B", linewidth=3, zorder=3)

ax_range.set_xlabel("Date", fontsize=20)
ax_range.set_ylabel("", fontsize=16)
ax_range.tick_params(axis="both", labelsize=14)
ax_range.set_yticks([])
ax_range.grid(True, alpha=0.2, linestyle="--")

# Add range labels
ax_range.text(
    0.02,
    0.85,
    "Range Selector (drag to zoom)",
    transform=ax_range.transAxes,
    fontsize=14,
    color="#555555",
    style="italic",
)

# Add preset range buttons (visual only - static representation)
button_y = 0.96
button_labels = ["1M", "3M", "6M", "1Y", "YTD", "ALL"]
for i, label in enumerate(button_labels):
    x_pos = 0.72 + i * 0.045
    is_selected = label == "6M"  # Highlight the selected range
    bbox_props = {
        "boxstyle": "round,pad=0.3",
        "facecolor": "#FFD43B" if is_selected else "#E8E8E8",
        "edgecolor": "#306998" if is_selected else "#CCCCCC",
        "linewidth": 2 if is_selected else 1,
    }
    ax_main.text(
        x_pos,
        button_y,
        label,
        transform=ax_main.transAxes,
        fontsize=13,
        fontweight="bold" if is_selected else "normal",
        ha="center",
        va="center",
        bbox=bbox_props,
    )

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
