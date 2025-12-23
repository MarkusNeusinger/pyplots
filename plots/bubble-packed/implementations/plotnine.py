""" pyplots.ai
bubble-packed: Basic Packed Bubble Chart
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 90/100 | Created: 2025-12-23
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

# Circle packing using force simulation (inline, KISS style)
n = len(df)
radii = df["radius"].values

# Sort by size (largest first) for better packing
idx = np.argsort(-radii)
sorted_radii = radii[idx]

# Initialize positions
x = np.zeros(n)
y = np.zeros(n)

# Place circles using greedy algorithm
for i in range(1, n):
    best_dist = float("inf")
    best_x, best_y = 0.0, 0.0

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
                center_dist = np.sqrt(test_x**2 + test_y**2)
                if center_dist < best_dist:
                    best_dist = center_dist
                    best_x, best_y = test_x, test_y

    x[i] = best_x
    y[i] = best_y

# Force simulation to tighten packing
for _ in range(1000):
    # Move toward center
    x -= x * 0.001
    y -= y * 0.001

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
for i, orig_idx in enumerate(idx):
    x_out[orig_idx] = x[i]
    y_out[orig_idx] = y[i]

df["x"] = x_out
df["y"] = y_out

# Create circle polygons for geom_polygon
circle_dfs = []
for i, row in df.iterrows():
    angles = np.linspace(0, 2 * np.pi, 64)
    cx = row["x"] + row["radius"] * np.cos(angles)
    cy = row["y"] + row["radius"] * np.sin(angles)
    circle_df = pd.DataFrame({"x": cx, "y": cy, "label": row["label"], "group": row["group"], "circle_id": i})
    circle_dfs.append(circle_df)

circles_df = pd.concat(circle_dfs, ignore_index=True)

# Color palette for groups - colorblind-safe (Okabe-Ito palette)
group_colors = {
    "Tech": "#0072B2",  # Blue
    "Business": "#E69F00",  # Orange
    "Operations": "#009E73",  # Bluish Green
    "Support": "#CC79A7",  # Reddish Purple
}

# Create label dataframe (centers) - show full labels for circles large enough
labels_df = df[["x", "y", "label", "radius"]].copy()

# Show full label for large circles, abbreviated for medium, none for small
labels_df["display_label"] = labels_df.apply(
    lambda row: (
        row["label"]
        if row["radius"] >= 0.85
        else (
            (row["label"][:8] if len(row["label"]) > 8 else row["label"])
            if row["radius"] >= 0.6
            else ((row["label"][:5] if len(row["label"]) > 5 else row["label"]) if row["radius"] >= 0.45 else "")
        )
    ),
    axis=1,
)

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
    + labs(title="bubble-packed · plotnine · pyplots.ai", fill="Department Group")
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
