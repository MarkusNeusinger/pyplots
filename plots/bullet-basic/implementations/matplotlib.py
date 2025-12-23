""" pyplots.ai
bullet-basic: Basic Bullet Chart
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-23
"""

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch


# Data - Multiple KPIs with actual values, targets, and qualitative ranges
metrics = [
    {"label": "Revenue", "actual": 275, "target": 250, "ranges": [150, 200, 300], "unit": "$K"},
    {"label": "Profit", "actual": 45, "target": 50, "ranges": [20, 40, 60], "unit": "%"},
    {"label": "New Customers", "actual": 85, "target": 100, "ranges": [50, 75, 120], "unit": ""},
    {"label": "Satisfaction", "actual": 4.2, "target": 4.5, "ranges": [3.0, 4.0, 5.0], "unit": "/5"},
]

# Qualitative band colors (grayscale: poor -> satisfactory -> good)
band_colors = ["#d9d9d9", "#bfbfbf", "#a6a6a6"]

# Create plot (4800x2700 px)
fig, ax = plt.subplots(figsize=(16, 9))

bar_height = 0.4
spacing = 1.5
y_positions = [i * spacing for i in range(len(metrics))]

for i, metric in enumerate(metrics):
    y = y_positions[i]
    ranges = metric["ranges"]
    max_range = ranges[-1]

    # Draw qualitative range bands (background bands from low to high)
    band_starts = [0] + ranges[:-1]
    band_ends = ranges

    for j, (start, end) in enumerate(zip(band_starts, band_ends, strict=True)):
        width = end - start
        ax.barh(y, width, left=start, height=bar_height * 2.2, color=band_colors[j], edgecolor="none", zorder=1)

    # Draw actual value bar (the main measure)
    ax.barh(y, metric["actual"], height=bar_height, color="#306998", edgecolor="none", zorder=2)

    # Draw target marker (vertical line)
    ax.plot(
        [metric["target"], metric["target"]],
        [y - bar_height * 0.7, y + bar_height * 0.7],
        color="#1a1a1a",
        linewidth=4,
        solid_capstyle="butt",
        zorder=3,
    )

    # Add actual value as text label (positioned after the max range for consistency)
    label_x = max_range + max_range * 0.03
    ax.text(
        label_x,
        y,
        f"{metric['actual']}{metric['unit']}",
        va="center",
        ha="left",
        fontsize=16,
        fontweight="bold",
        color="#306998",
        zorder=4,
    )

# Y-axis labels (metric names)
ax.set_yticks(y_positions)
ax.set_yticklabels([m["label"] for m in metrics], fontsize=18)

# X-axis styling - no label since metrics have different units
ax.tick_params(axis="x", labelsize=16)
ax.tick_params(axis="y", labelsize=18)

# Title
ax.set_title("bullet-basic · matplotlib · pyplots.ai", fontsize=24, pad=20)

# Grid on x-axis only, subtle
ax.xaxis.grid(True, alpha=0.3, linestyle="--", zorder=0)
ax.set_axisbelow(True)

# Remove spines for cleaner look
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

# Set x-axis to start at 0
ax.set_xlim(left=0)

# Adjust y-axis limits for padding
ax.set_ylim(-spacing * 0.4, y_positions[-1] + spacing * 0.4)

# Invert y-axis so first metric is at top
ax.invert_yaxis()

# Add legend
legend_elements = [
    Patch(facecolor="#306998", edgecolor="none", label="Actual"),
    Line2D([0], [0], color="#1a1a1a", linewidth=4, label="Target"),
    Patch(facecolor="#a6a6a6", edgecolor="none", label="Good"),
    Patch(facecolor="#bfbfbf", edgecolor="none", label="Satisfactory"),
    Patch(facecolor="#d9d9d9", edgecolor="none", label="Poor"),
]
ax.legend(handles=legend_elements, loc="lower right", fontsize=14, framealpha=0.9)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
