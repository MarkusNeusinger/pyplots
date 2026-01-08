""" pyplots.ai
scatter-brush-zoom: Interactive Scatter Plot with Brush Selection and Zoom
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 91/100 | Created: 2026-01-08
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import RectangleSelector


# Data - Create clustered data for interactive exploration
np.random.seed(42)

# Generate 3 clusters of points
n_points = 200
cluster1_x = np.random.normal(3, 0.8, n_points // 3)
cluster1_y = np.random.normal(3, 0.8, n_points // 3)
cluster2_x = np.random.normal(7, 1.0, n_points // 3)
cluster2_y = np.random.normal(6, 0.8, n_points // 3)
cluster3_x = np.random.normal(5, 0.6, n_points - 2 * (n_points // 3))
cluster3_y = np.random.normal(8, 0.6, n_points - 2 * (n_points // 3))

x = np.concatenate([cluster1_x, cluster2_x, cluster3_x])
y = np.concatenate([cluster1_y, cluster2_y, cluster3_y])

# Category labels for color-coding
categories = np.array(
    ["Cluster A"] * (n_points // 3) + ["Cluster B"] * (n_points // 3) + ["Cluster C"] * (n_points - 2 * (n_points // 3))
)

# Color mapping
color_map = {"Cluster A": "#306998", "Cluster B": "#FFD43B", "Cluster C": "#4CAF50"}
colors = [color_map[cat] for cat in categories]

# Create figure with space for status text
fig, ax = plt.subplots(figsize=(16, 9))

# Store scatter reference and selection state
scatter = ax.scatter(x, y, c=colors, s=150, alpha=0.7, edgecolors="white", linewidth=1.5)
selected_indices = []

# Text annotation for selection count
status_text = ax.text(
    0.02,
    0.98,
    "Selected: 0 points",
    transform=ax.transAxes,
    fontsize=16,
    verticalalignment="top",
    bbox={"boxstyle": "round", "facecolor": "white", "alpha": 0.8, "edgecolor": "gray"},
)

# Store original colors for reset
original_colors = colors.copy()


def on_select(eclick, erelease):
    """Handle brush selection - highlight points in rectangle"""
    global selected_indices
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata

    # Find points within selection rectangle
    x_min, x_max = min(x1, x2), max(x1, x2)
    y_min, y_max = min(y1, y2), max(y1, y2)

    mask = (x >= x_min) & (x <= x_max) & (y >= y_min) & (y <= y_max)
    selected_indices = np.where(mask)[0]

    # Update colors - highlight selected points
    new_colors = []
    for i in range(len(x)):
        if i in selected_indices:
            # Darken selected points and add red tint
            new_colors.append("#E53935")
        else:
            new_colors.append(original_colors[i])

    scatter.set_facecolors(new_colors)

    # Update status text
    status_text.set_text(f"Selected: {len(selected_indices)} points")
    fig.canvas.draw_idle()


# Create rectangle selector for brush selection
rect_selector = RectangleSelector(
    ax,
    on_select,
    useblit=True,
    button=[1],  # Left mouse button
    minspanx=5,
    minspany=5,
    spancoords="pixels",
    interactive=True,
    props={"facecolor": "#306998", "alpha": 0.2, "edgecolor": "#306998", "linewidth": 2},
)

# Styling
ax.set_xlabel("X Value", fontsize=20)
ax.set_ylabel("Y Value", fontsize=20)
ax.set_title("scatter-brush-zoom · matplotlib · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, linestyle="--")

# Add legend for clusters
legend_elements = [
    plt.scatter([], [], c=color_map["Cluster A"], s=150, label="Cluster A", edgecolors="white"),
    plt.scatter([], [], c=color_map["Cluster B"], s=150, label="Cluster B", edgecolors="white"),
    plt.scatter([], [], c=color_map["Cluster C"], s=150, label="Cluster C", edgecolors="white"),
]
ax.legend(handles=legend_elements, fontsize=16, loc="lower right")

# Add instruction text
ax.text(
    0.98,
    0.98,
    "Drag to select • Scroll to zoom • Pan with toolbar",
    transform=ax.transAxes,
    fontsize=14,
    verticalalignment="top",
    horizontalalignment="right",
    style="italic",
    color="gray",
)

plt.tight_layout()

# Save static preview (shows initial state with brush selection visualization)
# Note: Interactive features (zoom, pan, brush) work when running the script
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
