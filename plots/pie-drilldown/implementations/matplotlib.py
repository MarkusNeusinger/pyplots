""" pyplots.ai
pie-drilldown: Drilldown Pie Chart with Click Navigation
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-31
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch


# Hierarchical data: Sales by Region -> Country -> State (3 levels)
# Level 1: Sales by Region
regions = ["North America", "Europe", "Asia Pacific", "Latin America"]
region_values = [4500, 3200, 2800, 1500]
region_colors = ["#306998", "#4A90D9", "#7AB8F5", "#A8D4FF"]

# Level 2: North America breakdown
na_countries = ["USA", "Canada", "Mexico"]
na_values = [3200, 800, 500]
na_colors = ["#306998", "#3D7AB3", "#5A8FC4"]

# Level 3: USA breakdown (demonstrating 3rd hierarchy level)
usa_states = ["California", "Texas", "New York", "Florida", "Others"]
usa_values = [850, 720, 680, 550, 400]
usa_colors = ["#1A3A5C", "#24517A", "#306998", "#4A90D9", "#7AB8F5"]

# Create figure with 3 pie charts showing hierarchy progression
fig = plt.figure(figsize=(16, 9))
fig.patch.set_facecolor("white")

# Three axes for 3 hierarchy levels
ax1 = fig.add_axes([0.02, 0.15, 0.30, 0.60])
ax2 = fig.add_axes([0.35, 0.15, 0.30, 0.60])
ax3 = fig.add_axes([0.68, 0.15, 0.30, 0.60])

# Level 1: Main pie chart (all regions)
wedges1, texts1, autotexts1 = ax1.pie(
    region_values,
    labels=None,
    autopct=lambda pct: f"{pct:.0f}%",
    colors=region_colors,
    startangle=90,
    explode=[0.08, 0, 0, 0],
    wedgeprops={"linewidth": 2, "edgecolor": "white"},
    textprops={"fontsize": 18, "fontweight": "bold", "color": "white"},
    pctdistance=0.55,
)

# Add click indicator icons on main chart slices (using "+" symbol)
for wedge in wedges1:
    ang = (wedge.theta2 + wedge.theta1) / 2
    x = 0.78 * np.cos(np.deg2rad(ang))
    y = 0.78 * np.sin(np.deg2rad(ang))
    ax1.annotate(
        "+",
        xy=(x, y),
        fontsize=20,
        fontweight="bold",
        ha="center",
        va="center",
        color="white",
        alpha=0.85,
        bbox={"boxstyle": "circle,pad=0.15", "fc": "#306998", "ec": "white", "lw": 1.5},
    )

# Add value labels outside level 1 pie
for wedge, value, name in zip(wedges1, region_values, regions, strict=True):
    ang = (wedge.theta2 + wedge.theta1) / 2
    x = 1.30 * np.cos(np.deg2rad(ang))
    y = 1.30 * np.sin(np.deg2rad(ang))
    ax1.annotate(
        f"{name}\n${value:,}M",
        xy=(0.95 * np.cos(np.deg2rad(ang)), 0.95 * np.sin(np.deg2rad(ang))),
        xytext=(x, y),
        fontsize=11,
        ha="center",
        va="center",
        arrowprops={"arrowstyle": "-", "color": "#666666", "lw": 1},
    )

ax1.set_title("Level 1: All Regions", fontsize=18, fontweight="bold", pad=15)

# Level 2: North America drilldown
wedges2, texts2, autotexts2 = ax2.pie(
    na_values,
    labels=None,
    autopct=lambda pct: f"{pct:.0f}%",
    colors=na_colors,
    startangle=90,
    explode=[0.08, 0, 0],
    wedgeprops={"linewidth": 2, "edgecolor": "white"},
    textprops={"fontsize": 18, "fontweight": "bold", "color": "white"},
    pctdistance=0.55,
)

# Add click indicator icons on level 2 slices (using "+" symbol)
for wedge in wedges2:
    ang = (wedge.theta2 + wedge.theta1) / 2
    x = 0.78 * np.cos(np.deg2rad(ang))
    y = 0.78 * np.sin(np.deg2rad(ang))
    ax2.annotate(
        "+",
        xy=(x, y),
        fontsize=20,
        fontweight="bold",
        ha="center",
        va="center",
        color="white",
        alpha=0.85,
        bbox={"boxstyle": "circle,pad=0.15", "fc": "#306998", "ec": "white", "lw": 1.5},
    )

# Add value labels outside level 2 pie
for wedge, value, name in zip(wedges2, na_values, na_countries, strict=True):
    ang = (wedge.theta2 + wedge.theta1) / 2
    x = 1.30 * np.cos(np.deg2rad(ang))
    y = 1.30 * np.sin(np.deg2rad(ang))
    ax2.annotate(
        f"{name}\n${value:,}M",
        xy=(0.95 * np.cos(np.deg2rad(ang)), 0.95 * np.sin(np.deg2rad(ang))),
        xytext=(x, y),
        fontsize=11,
        ha="center",
        va="center",
        arrowprops={"arrowstyle": "-", "color": "#666666", "lw": 1},
    )

ax2.set_title("Level 2: North America", fontsize=18, fontweight="bold", pad=15)

# Level 3: USA drilldown
wedges3, texts3, autotexts3 = ax3.pie(
    usa_values,
    labels=None,
    autopct=lambda pct: f"{pct:.0f}%",
    colors=usa_colors,
    startangle=90,
    wedgeprops={"linewidth": 2, "edgecolor": "white"},
    textprops={"fontsize": 18, "fontweight": "bold", "color": "white"},
    pctdistance=0.55,
)

# Add value labels outside level 3 pie
for wedge, value, name in zip(wedges3, usa_values, usa_states, strict=True):
    ang = (wedge.theta2 + wedge.theta1) / 2
    x = 1.30 * np.cos(np.deg2rad(ang))
    y = 1.30 * np.sin(np.deg2rad(ang))
    ax3.annotate(
        f"{name}\n${value:,}M",
        xy=(0.95 * np.cos(np.deg2rad(ang)), 0.95 * np.sin(np.deg2rad(ang))),
        xytext=(x, y),
        fontsize=11,
        ha="center",
        va="center",
        arrowprops={"arrowstyle": "-", "color": "#666666", "lw": 1},
    )

ax3.set_title("Level 3: USA", fontsize=18, fontweight="bold", pad=15)

# Add drill-down arrows between charts
arrow1 = FancyArrowPatch(
    (0.325, 0.45),
    (0.365, 0.45),
    transform=fig.transFigure,
    color="#306998",
    linewidth=3,
    arrowstyle="-|>",
    mutation_scale=25,
)
fig.add_artist(arrow1)

arrow2 = FancyArrowPatch(
    (0.655, 0.45),
    (0.695, 0.45),
    transform=fig.transFigure,
    color="#306998",
    linewidth=3,
    arrowstyle="-|>",
    mutation_scale=25,
)
fig.add_artist(arrow2)

# Add breadcrumb navigation showing full path
breadcrumb_box = fig.text(
    0.5,
    0.88,
    "All  >  North America  >  USA",
    fontsize=16,
    ha="center",
    va="center",
    fontweight="bold",
    bbox={"boxstyle": "round,pad=0.5", "facecolor": "#FFD43B", "edgecolor": "#306998", "linewidth": 2},
)

# Add interactive hint
fig.text(
    0.5,
    0.06,
    "Click any slice to drill down  |  Click breadcrumb to navigate up",
    fontsize=13,
    ha="center",
    va="center",
    color="#555555",
    style="italic",
)

# Add title
fig.suptitle("pie-drilldown · matplotlib · pyplots.ai", fontsize=24, fontweight="bold", y=0.97)

plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
