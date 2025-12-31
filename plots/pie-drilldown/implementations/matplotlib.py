"""pyplots.ai
pie-drilldown: Drilldown Pie Chart with Click Navigation
Library: matplotlib | Python 3.13
Quality: pending | Created: 2025-12-31
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch


# Hierarchical data: Sales by Region -> Country
# Root level: Sales by Region
regions = ["North America", "Europe", "Asia Pacific", "Latin America"]
region_values = [4500, 3200, 2800, 1500]
region_colors = ["#306998", "#4A90D9", "#7AB8F5", "#A8D4FF"]

# Drilldown level: North America breakdown (showing expanded view)
na_countries = ["USA", "Canada", "Mexico"]
na_values = [3200, 800, 500]
na_colors = ["#306998", "#3D7AB3", "#5A8FC4"]

# Create figure with GridSpec for better layout control
fig = plt.figure(figsize=(16, 9))
fig.patch.set_facecolor("white")

# Create axes with more space between them
ax_main = fig.add_axes([0.05, 0.12, 0.38, 0.70])
ax_drill = fig.add_axes([0.57, 0.12, 0.38, 0.70])

# Main pie chart (all regions) - use startangle to position labels better
wedges_main, texts_main, autotexts_main = ax_main.pie(
    region_values,
    labels=None,
    autopct=lambda pct: f"{pct:.1f}%",
    colors=region_colors,
    startangle=45,
    explode=[0.08, 0, 0, 0],  # Explode first slice to show it's selected
    wedgeprops={"linewidth": 3, "edgecolor": "white"},
    textprops={"fontsize": 16, "fontweight": "bold", "color": "white"},
    pctdistance=0.6,
)

# Add value labels outside the main pie
for wedge, value, name in zip(wedges_main, region_values, regions, strict=True):
    ang = (wedge.theta2 + wedge.theta1) / 2
    x = 1.35 * np.cos(np.deg2rad(ang))
    y = 1.35 * np.sin(np.deg2rad(ang))
    ax_main.annotate(
        f"{name}\n${value:,}M",
        xy=(0.9 * np.cos(np.deg2rad(ang)), 0.9 * np.sin(np.deg2rad(ang))),
        xytext=(x, y),
        fontsize=13,
        ha="center",
        va="center",
        arrowprops={"arrowstyle": "-", "color": "#666666", "lw": 1.5},
    )

ax_main.set_title("Sales by Region", fontsize=20, fontweight="bold", pad=20)

# Drilldown pie chart (North America breakdown) - adjust startangle
wedges_drill, texts_drill, autotexts_drill = ax_drill.pie(
    na_values,
    labels=None,
    autopct=lambda pct: f"{pct:.1f}%",
    colors=na_colors,
    startangle=45,
    wedgeprops={"linewidth": 3, "edgecolor": "white"},
    textprops={"fontsize": 16, "fontweight": "bold", "color": "white"},
    pctdistance=0.6,
)

# Add value labels outside the drilldown pie
for wedge, value, name in zip(wedges_drill, na_values, na_countries, strict=True):
    ang = (wedge.theta2 + wedge.theta1) / 2
    x = 1.35 * np.cos(np.deg2rad(ang))
    y = 1.35 * np.sin(np.deg2rad(ang))
    ax_drill.annotate(
        f"{name}\n${value:,}M",
        xy=(0.9 * np.cos(np.deg2rad(ang)), 0.9 * np.sin(np.deg2rad(ang))),
        xytext=(x, y),
        fontsize=13,
        ha="center",
        va="center",
        arrowprops={"arrowstyle": "-", "color": "#666666", "lw": 1.5},
    )

ax_drill.set_title("North America Breakdown", fontsize=20, fontweight="bold", pad=20)

# Add breadcrumb navigation indicator
fig.text(
    0.76,
    0.88,
    "All  >  North America",
    fontsize=14,
    ha="center",
    va="center",
    fontweight="bold",
    bbox={"boxstyle": "round,pad=0.4", "facecolor": "#FFD43B", "edgecolor": "#306998", "linewidth": 2},
)

# Add arrow between charts to show drill-down relationship
arrow = FancyArrowPatch(
    (0.45, 0.47),
    (0.55, 0.47),
    transform=fig.transFigure,
    color="#306998",
    linewidth=4,
    arrowstyle="-|>",
    mutation_scale=30,
    connectionstyle="arc3,rad=0",
)
fig.add_artist(arrow)

# Add drill indicator text above the arrow
fig.text(0.5, 0.55, "Drill Down", fontsize=16, ha="center", va="center", color="#306998", fontweight="bold")

# Add "Click slice" indicator text below the arrow
fig.text(0.5, 0.39, "(click slice)", fontsize=11, ha="center", va="center", color="#666666", style="italic")

# Add title
fig.suptitle("pie-drilldown · matplotlib · pyplots.ai", fontsize=24, fontweight="bold", y=0.98)

# Add subtitle at bottom
fig.text(
    0.5,
    0.03,
    "Static representation: Main view (left) with drilldown into selected slice (right)",
    fontsize=12,
    ha="center",
    va="center",
    color="#666666",
    style="italic",
)

plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
