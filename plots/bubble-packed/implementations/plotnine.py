"""
bubble-packed: Basic Packed Bubble Chart
Library: plotnine
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    coord_fixed,
    element_blank,
    element_text,
    geom_polygon,
    geom_text,
    ggplot,
    labs,
    scale_fill_manual,
    theme,
    theme_void,
)


# Data - department budgets (in millions)
np.random.seed(42)
data = {
    "label": [
        "Engineering",
        "Marketing",
        "Sales",
        "Operations",
        "HR",
        "Finance",
        "R&D",
        "IT Support",
        "Legal",
        "Customer Service",
        "Design",
        "Logistics",
        "Quality",
        "Training",
        "Admin",
    ],
    "value": [45, 32, 28, 22, 15, 18, 38, 12, 10, 20, 14, 16, 8, 6, 5],
    "group": [
        "Tech",
        "Business",
        "Business",
        "Operations",
        "Support",
        "Business",
        "Tech",
        "Tech",
        "Support",
        "Operations",
        "Tech",
        "Operations",
        "Operations",
        "Support",
        "Support",
    ],
}

df = pd.DataFrame(data)

# Scale values to radii (area-based scaling for accurate perception)
max_radius = 1.0
min_radius = 0.3
df["radius"] = min_radius + (max_radius - min_radius) * np.sqrt(df["value"] / df["value"].max())


# Circle packing algorithm using force simulation
def pack_circles(radii, iterations=1000):
    """Pack circles using force-directed placement with collision resolution."""
    n = len(radii)
    # Sort by size (largest first) for better packing
    idx = np.argsort(-radii)
    sorted_radii = radii[idx]

    # Initialize positions
    x = np.zeros(n)
    y = np.zeros(n)

    # Place first circle at center
    x[0] = 0
    y[0] = 0

    # Place remaining circles
    for i in range(1, n):
        # Try to place close to existing circles
        best_dist = float("inf")
        best_x, best_y = 0, 0

        for angle in np.linspace(0, 2 * np.pi, 36):
            for ref in range(i):
                # Try placing next to reference circle
                test_x = x[ref] + (sorted_radii[ref] + sorted_radii[i] + 0.05) * np.cos(angle)
                test_y = y[ref] + (sorted_radii[ref] + sorted_radii[i] + 0.05) * np.sin(angle)

                # Check for collisions
                valid = True
                for j in range(i):
                    dist = np.sqrt((test_x - x[j]) ** 2 + (test_y - y[j]) ** 2)
                    if dist < sorted_radii[i] + sorted_radii[j] + 0.03:
                        valid = False
                        break

                if valid:
                    # Prefer positions closer to center
                    center_dist = np.sqrt(test_x**2 + test_y**2)
                    if center_dist < best_dist:
                        best_dist = center_dist
                        best_x, best_y = test_x, test_y

        x[i] = best_x
        y[i] = best_y

    # Run force simulation to tighten packing
    for _ in range(iterations):
        # Move toward center
        for i in range(n):
            cx, cy = x[i] * 0.001, y[i] * 0.001
            x[i] -= cx
            y[i] -= cy

        # Separate overlapping circles
        for i in range(n):
            for j in range(i + 1, n):
                dx = x[j] - x[i]
                dy = y[j] - y[i]
                dist = np.sqrt(dx * dx + dy * dy)
                min_dist = sorted_radii[i] + sorted_radii[j] + 0.03

                if dist < min_dist and dist > 0.001:
                    overlap = (min_dist - dist) / 2
                    dx_norm = dx / dist
                    dy_norm = dy / dist
                    x[i] -= overlap * dx_norm * 0.5
                    y[i] -= overlap * dy_norm * 0.5
                    x[j] += overlap * dx_norm * 0.5
                    y[j] += overlap * dy_norm * 0.5

    # Restore original order
    x_out = np.zeros(n)
    y_out = np.zeros(n)
    r_out = np.zeros(n)
    for i, orig_idx in enumerate(idx):
        x_out[orig_idx] = x[i]
        y_out[orig_idx] = y[i]
        r_out[orig_idx] = sorted_radii[i]

    return x_out, y_out


# Pack circles
x_pos, y_pos = pack_circles(df["radius"].values)
df["x"] = x_pos
df["y"] = y_pos


# Create circle polygons for geom_polygon
def make_circle(cx, cy, r, n_points=64):
    """Generate polygon approximation of circle."""
    angles = np.linspace(0, 2 * np.pi, n_points)
    return cx + r * np.cos(angles), cy + r * np.sin(angles)


# Build polygon dataframe
circle_dfs = []
for i, row in df.iterrows():
    cx, cy = make_circle(row["x"], row["y"], row["radius"])
    circle_df = pd.DataFrame({"x": cx, "y": cy, "label": row["label"], "group": row["group"], "circle_id": i})
    circle_dfs.append(circle_df)

circles_df = pd.concat(circle_dfs, ignore_index=True)

# Color palette for groups
group_colors = {
    "Tech": "#306998",  # Python Blue
    "Business": "#FFD43B",  # Python Yellow
    "Operations": "#4CAF50",  # Green
    "Support": "#9C27B0",  # Purple
}

# Create label dataframe (centers)
labels_df = df[["x", "y", "label", "radius"]].copy()
# Only show labels for larger circles
labels_df["show_label"] = labels_df["radius"] > 0.5
labels_df.loc[labels_df["show_label"], "display_label"] = labels_df.loc[labels_df["show_label"], "label"].apply(
    lambda s: s[:10] if len(s) > 10 else s
)
labels_df.loc[~labels_df["show_label"], "display_label"] = ""

# Create plot
plot = (
    ggplot()
    + geom_polygon(
        data=circles_df, mapping=aes(x="x", y="y", fill="group", group="circle_id"), color="white", size=0.5, alpha=0.85
    )
    + geom_text(
        data=labels_df, mapping=aes(x="x", y="y", label="display_label"), size=9, color="white", fontweight="bold"
    )
    + scale_fill_manual(values=group_colors)
    + coord_fixed()
    + labs(title="bubble-packed \u00b7 plotnine \u00b7 pyplots.ai", fill="Department Group")
    + theme_void()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=24, ha="center", weight="bold"),
        legend_title=element_text(size=18),
        legend_text=element_text(size=14),
        legend_position="right",
        plot_background=element_blank(),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
