""" pyplots.ai
bar-basic: Basic Bar Chart
Library: matplotlib 3.10.8 | Python 3.14
Quality: 88/100 | Created: 2025-12-23
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# Data - Product sales by category (mixed order for natural variation)
categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys"]
values = [45200, 32800, 28500, 38700, 18900, 24100]


# Shared dollar formatter (eliminates duplication)
def dollar_fmt(v, *_):
    return f"${v:,.0f}"


# Identify top and bottom performers for storytelling
max_idx = values.index(max(values))
min_idx = values.index(min(values))

# Create plot (4800x2700 px)
fig, ax = plt.subplots(figsize=(16, 9))
fig.set_facecolor("#FAFAFA")
ax.set_facecolor("#FAFAFA")

# Color bars: highlight top performer in darker shade, bottom in muted tone
bar_colors = ["#306998"] * len(values)
bar_colors[max_idx] = "#1A4971"  # Darker blue for leader
bar_colors[min_idx] = "#7BA7C9"  # Lighter blue for lowest

# Bar chart with wider bars for better canvas fill
bars = ax.bar(categories, values, color=bar_colors, width=0.7, edgecolor="white", linewidth=1.5, zorder=3)

# Value labels using bar_label with shared formatter
ax.bar_label(bars, fmt=dollar_fmt, padding=8, fontsize=16, fontweight="medium")

# Y-axis dollar formatting via shared formatter
ax.yaxis.set_major_formatter(ticker.FuncFormatter(dollar_fmt))

# Labels and title
ax.set_xlabel("Product Category", fontsize=20, labelpad=12)
ax.set_ylabel("Sales (USD)", fontsize=20, labelpad=12)
ax.set_title("bar-basic \u00b7 matplotlib \u00b7 pyplots.ai", fontsize=24, fontweight="medium", pad=20)

# Style tick labels
ax.tick_params(axis="both", labelsize=16)
ax.tick_params(axis="x", length=0)  # Remove x tick marks for cleaner look

# Subtle grid on y-axis only
ax.yaxis.grid(True, alpha=0.15, linewidth=0.8, color="#888888", zorder=0)
ax.set_axisbelow(True)

# Spine styling: remove top/right, style bottom with weight
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_linewidth(1.2)
ax.spines["bottom"].set_color("#333333")

# Set y-axis range for better canvas utilization
ax.set_ylim(bottom=0, top=max(values) * 1.12)

# Storytelling annotation: highlight top performer
ax.annotate(
    f"Top seller\n{categories[max_idx]}",
    xy=(max_idx, values[max_idx]),
    xytext=(max_idx + 0.8, values[max_idx] * 0.92),
    fontsize=14,
    fontweight="bold",
    color="#1A4971",
    ha="left",
    arrowprops={"arrowstyle": "-|>", "color": "#1A4971", "lw": 1.5},
)

# Margin adjustments for better canvas fill
plt.subplots_adjust(left=0.09, right=0.95, top=0.90, bottom=0.10)
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
