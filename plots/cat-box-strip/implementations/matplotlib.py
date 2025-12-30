"""pyplots.ai
cat-box-strip: Box Plot with Strip Overlay
Library: matplotlib | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - Create groups with different distributions to show varied box plot features
np.random.seed(42)

# Group A: Normal distribution (medium spread)
group_a = np.random.normal(loc=65, scale=12, size=35)

# Group B: Skewed distribution with some high outliers
group_b = np.concatenate(
    [
        np.random.normal(loc=50, scale=8, size=30),
        np.array([85, 88, 92]),  # Outliers
    ]
)

# Group C: Tight distribution (low spread)
group_c = np.random.normal(loc=72, scale=5, size=40)

# Group D: Wide distribution with both low and high outliers
group_d = np.concatenate(
    [
        np.random.normal(loc=58, scale=15, size=28),
        np.array([15, 18, 95, 98]),  # Low and high outliers
    ]
)

data = [group_a, group_b, group_c, group_d]
categories = ["Region A", "Region B", "Region C", "Region D"]

# Create plot (16:9 landscape)
fig, ax = plt.subplots(figsize=(16, 9))

# Box plot - use Python Blue for boxes
box_color = "#306998"
boxprops = {"facecolor": box_color, "color": box_color, "alpha": 0.3}
whiskerprops = {"color": box_color, "linewidth": 2}
capprops = {"color": box_color, "linewidth": 2}
medianprops = {"color": "#1a3d5c", "linewidth": 3}
flierprops = {"marker": "", "markersize": 0}  # Hide default outliers, we'll show all points

bp = ax.boxplot(
    data,
    tick_labels=categories,
    patch_artist=True,
    boxprops=boxprops,
    whiskerprops=whiskerprops,
    capprops=capprops,
    medianprops=medianprops,
    flierprops=flierprops,
    widths=0.5,
)

# Strip plot overlay - use Python Yellow for points
strip_color = "#FFD43B"
for i, group_data in enumerate(data, start=1):
    # Add jitter to x positions
    x_jitter = np.random.uniform(-0.15, 0.15, size=len(group_data))
    x_positions = np.full(len(group_data), i) + x_jitter

    ax.scatter(
        x_positions, group_data, color=strip_color, s=120, alpha=0.7, edgecolors="#b39700", linewidth=1.5, zorder=3
    )

# Styling
ax.set_xlabel("Sales Region", fontsize=20)
ax.set_ylabel("Monthly Revenue ($K)", fontsize=20)
ax.set_title("cat-box-strip · matplotlib · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, linestyle="--", axis="y")

# Set y-axis limits with some padding
all_values = np.concatenate(data)
y_min, y_max = all_values.min(), all_values.max()
y_padding = (y_max - y_min) * 0.1
ax.set_ylim(y_min - y_padding, y_max + y_padding)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
