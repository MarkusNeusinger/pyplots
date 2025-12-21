""" pyplots.ai
waterfall-basic: Basic Waterfall Chart
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-14
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.patches import Patch


# Set seaborn style
sns.set_style("whitegrid")

# Data - Quarterly financial breakdown
categories = [
    "Revenue",
    "Cost of Goods",
    "Gross Profit",
    "Operating Exp",
    "Marketing",
    "R&D",
    "Operating Income",
    "Taxes",
    "Net Income",
]
# Values: positive = increase, negative = decrease, None = total (including starting value)
values = [None, -200, None, -80, -40, -30, None, -45, None]
starting_value = 500  # Revenue as starting total

# Calculate cumulative values and bar positions
cumulative = []
bar_values = []
current = starting_value  # Start with revenue

for v in values:
    if v is None:
        # This is a total bar - use current cumulative value
        cumulative.append(0)  # Start from 0
        bar_values.append(current)
    else:
        cumulative.append(current)
        bar_values.append(v)
        current += v

# Determine bar types and colors
colors = []
bar_types = []  # 'positive', 'negative', 'total'
for v in values:
    if v is None:
        colors.append("#306998")  # Python Blue for totals
        bar_types.append("total")
    elif v >= 0:
        colors.append("#2ecc71")  # Green for positive
        bar_types.append("positive")
    else:
        colors.append("#e74c3c")  # Red for negative
        bar_types.append("negative")

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

x = np.arange(len(categories))
bar_width = 0.6

# Draw bars
bars = ax.bar(x, bar_values, bar_width, bottom=cumulative, color=colors, edgecolor="white", linewidth=2)

# Draw connecting lines between bars
for i in range(len(categories) - 1):
    if bar_types[i] == "total":
        y_end = bar_values[i]
    else:
        y_end = cumulative[i] + bar_values[i]

    if bar_types[i + 1] == "total":
        y_start_next = 0
    else:
        y_start_next = cumulative[i + 1]

    # Draw line from end of current bar to start of next bar
    ax.plot(
        [x[i] + bar_width / 2, x[i + 1] - bar_width / 2],
        [y_end, y_start_next],
        color="#555555",
        linestyle="--",
        linewidth=1.5,
        alpha=0.7,
    )

# Add value labels on bars
for i, bar in enumerate(bars):
    height = bar.get_height()
    bottom = bar.get_y()

    if bar_types[i] == "total":
        label = f"${int(height):,}"
        y_pos = height / 2
    else:
        if height >= 0:
            label = f"+${int(height):,}"
            y_pos = bottom + height / 2
        else:
            label = f"-${int(abs(height)):,}"
            y_pos = bottom + height / 2

    ax.text(
        bar.get_x() + bar.get_width() / 2,
        y_pos,
        label,
        ha="center",
        va="center",
        fontsize=14,
        fontweight="bold",
        color="white",
    )

# Styling
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=16, rotation=30, ha="right")
ax.tick_params(axis="y", labelsize=16)
ax.set_ylabel("Amount ($K)", fontsize=20)
ax.set_xlabel("Category", fontsize=20)
ax.set_title("waterfall-basic · seaborn · pyplots.ai", fontsize=24, fontweight="bold")

# Add legend
legend_elements = [
    Patch(facecolor="#306998", edgecolor="white", label="Total"),
    Patch(facecolor="#2ecc71", edgecolor="white", label="Increase"),
    Patch(facecolor="#e74c3c", edgecolor="white", label="Decrease"),
]
ax.legend(handles=legend_elements, loc="upper right", fontsize=14)

# Adjust grid
ax.yaxis.grid(True, alpha=0.3, linestyle="--")
ax.xaxis.grid(False)

# Set y-axis to start at 0
ax.set_ylim(bottom=0)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
