"""pyplots.ai
bullet-basic: Basic Bullet Chart
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data - Multiple KPIs with actual values, targets, and qualitative ranges
np.random.seed(42)

metrics = ["Revenue", "Customer\nSatisfaction", "Efficiency", "Quality\nScore"]
actuals = [78, 85, 62, 91]
targets = [90, 80, 75, 85]
# Ranges define thresholds for qualitative bands (poor/satisfactory/good)
ranges_list = [
    [50, 75, 100],  # Revenue
    [60, 80, 100],  # Customer Satisfaction
    [40, 60, 100],  # Efficiency
    [70, 85, 100],  # Quality Score
]

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))
sns.set_style("whitegrid")

# Qualitative range colors (grayscale as per specification - dark to light for poor to good)
range_colors = ["#e0e0e0", "#bdbdbd", "#8c8c8c"]

# Bar dimensions
range_height = 0.7
actual_height = 0.35
n_metrics = len(metrics)
y_positions = np.arange(n_metrics)

# Draw qualitative ranges as background bands for each metric
for y_pos, ranges in zip(y_positions, ranges_list, strict=True):
    prev = 0
    for end, color in zip(ranges, range_colors, strict=True):
        width = end - prev
        ax.barh(y_pos, width, left=prev, height=range_height, color=color, edgecolor="none", zorder=1)
        prev = end

# Create DataFrame for seaborn barplot
df = pd.DataFrame({"Metric": metrics, "Actual": actuals})

# Draw actual value bars using seaborn
sns.barplot(
    data=df,
    x="Actual",
    y="Metric",
    color="#306998",  # Python Blue
    width=actual_height,
    ax=ax,
    zorder=3,
    edgecolor="#1e4d6b",
    linewidth=1.5,
)

# Draw target markers as vertical lines
for i, target in enumerate(targets):
    ax.plot(
        [target, target],
        [i - range_height / 2 + 0.02, i + range_height / 2 - 0.02],
        color="#1a1a1a",
        linewidth=5,
        zorder=4,
        solid_capstyle="butt",
    )

# Add actual value labels at end of bars
for i, (actual, target) in enumerate(zip(actuals, targets, strict=True)):
    label_x = max(actual, target) + 2
    ax.text(label_x, i, f"{actual}%", va="center", ha="left", fontsize=18, fontweight="bold", color="#306998")

# Styling
ax.set_xlim(0, 115)
ax.set_xlabel("Performance (%)", fontsize=20)
ax.set_ylabel("")
ax.set_title("bullet-basic · seaborn · pyplots.ai", fontsize=24, fontweight="bold", pad=20)
ax.tick_params(axis="both", labelsize=16)
ax.tick_params(axis="y", length=0)

# Customize grid - subtle vertical lines only
ax.xaxis.grid(True, alpha=0.3, linestyle="--", zorder=0)
ax.yaxis.grid(False)

# Create legend
legend_elements = [
    mpatches.Patch(facecolor=range_colors[0], label="Poor"),
    mpatches.Patch(facecolor=range_colors[1], label="Satisfactory"),
    mpatches.Patch(facecolor=range_colors[2], label="Good"),
    mpatches.Patch(facecolor="#306998", edgecolor="#1e4d6b", linewidth=1.5, label="Actual"),
    plt.Line2D([0], [0], color="#1a1a1a", linewidth=5, label="Target"),
]
ax.legend(handles=legend_elements, loc="upper right", fontsize=14, framealpha=0.95)

# Remove spines for cleaner look
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
