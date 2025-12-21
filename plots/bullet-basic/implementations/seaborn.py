""" pyplots.ai
bullet-basic: Basic Bullet Chart
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 95/100 | Created: 2025-12-16
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Set seaborn style for clean aesthetics
sns.set_style("whitegrid")

# Data - Q3 Sales KPIs with actuals, targets, and qualitative ranges (normalized 0-100)
# Each metric shows performance against goals with poor/satisfactory/good bands
metrics = [
    {"label": "Revenue", "actual": 92, "target": 100, "ranges": [50, 75, 100]},
    {"label": "Profit Margin", "actual": 68, "target": 80, "ranges": [50, 75, 100]},
    {"label": "Customer Acquisition", "actual": 85, "target": 90, "ranges": [50, 75, 100]},
    {"label": "Satisfaction Score", "actual": 78, "target": 85, "ranges": [50, 75, 100]},
    {"label": "Order Fulfillment", "actual": 95, "target": 90, "ranges": [50, 75, 100]},
]

# Colors for qualitative ranges (grayscale from dark to light)
range_colors = ["#c0c0c0", "#d9d9d9", "#ececec"]

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Bar heights and spacing
bar_height = 0.5
gap = 1.2
y_positions = np.arange(len(metrics)) * gap

for i, metric in enumerate(metrics):
    y = y_positions[i]
    ranges = metric["ranges"]
    actual = metric["actual"]
    target = metric["target"]

    # Draw qualitative range bands (from largest to smallest so they layer correctly)
    for end, color in zip(reversed(ranges), range_colors, strict=False):
        ax.barh(y, end, height=bar_height * 1.6, color=color, edgecolor="none", zorder=1)

    # Draw actual value bar (primary measure)
    ax.barh(y, actual, height=bar_height * 0.6, color="#306998", edgecolor="none", zorder=2)

    # Draw target marker (vertical line)
    ax.plot([target, target], [y - bar_height * 0.5, y + bar_height * 0.5], color="#1a1a1a", linewidth=4, zorder=3)

    # Add actual value as text label
    ax.text(
        actual + 2, y, f"{actual}%", va="center", ha="left", fontsize=16, fontweight="bold", color="#306998", zorder=4
    )

# Set y-axis labels (metric names)
ax.set_yticks(y_positions)
ax.set_yticklabels([m["label"] for m in metrics], fontsize=18)

# Configure axes
ax.set_xlabel("Performance (% of Goal)", fontsize=20)
ax.set_ylabel("")
ax.tick_params(axis="x", labelsize=16)
ax.set_xlim(0, 110)

# Invert y-axis so first metric appears at top
ax.invert_yaxis()

# Title
ax.set_title("Q3 Sales KPIs · bullet-basic · seaborn · pyplots.ai", fontsize=24, fontweight="bold", pad=20)

# Create legend
legend_elements = [
    mpatches.Patch(facecolor="#306998", label="Actual"),
    mpatches.Patch(facecolor="none", edgecolor="#1a1a1a", linewidth=3, label="Target"),
    mpatches.Patch(facecolor="#ececec", label="Good (75-100%)"),
    mpatches.Patch(facecolor="#d9d9d9", label="Satisfactory (50-75%)"),
    mpatches.Patch(facecolor="#c0c0c0", label="Poor (0-50%)"),
]
ax.legend(handles=legend_elements, loc="lower right", fontsize=14, framealpha=0.9, edgecolor="none")

# Subtle grid (only x-axis)
ax.grid(axis="x", alpha=0.3, linestyle="--")
ax.grid(axis="y", visible=False)

# Remove spines for cleaner look
sns.despine(left=True, bottom=False)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
