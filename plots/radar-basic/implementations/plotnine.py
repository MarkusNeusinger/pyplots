"""
radar-basic: Basic Radar Chart
Library: plotnine
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    coord_fixed,
    element_text,
    geom_path,
    geom_point,
    geom_polygon,
    geom_segment,
    geom_text,
    ggplot,
    guide_legend,
    guides,
    labs,
    scale_color_manual,
    scale_fill_manual,
    theme,
    theme_void,
)


# Data - Performance metrics for two athletes
categories = ["Speed", "Power", "Accuracy", "Stamina", "Technique"]
athlete_a = [85, 70, 90, 65, 80]
athlete_b = [70, 85, 75, 80, 70]

n_vars = len(categories)

# Compute angles for each axis (evenly distributed)
angles = np.linspace(0, 2 * np.pi, n_vars, endpoint=False)


def polar_to_cartesian(values, angles):
    """Convert polar coordinates to cartesian for radar chart."""
    x = [v * np.cos(a) for v, a in zip(values, angles, strict=True)]
    y = [v * np.sin(a) for v, a in zip(values, angles, strict=True)]
    return x, y


# Close the polygons by repeating the first value
athlete_a_closed = athlete_a + [athlete_a[0]]
athlete_b_closed = athlete_b + [athlete_b[0]]
angles_closed = np.append(angles, angles[0])

# Convert to cartesian coordinates
x_a, y_a = polar_to_cartesian(athlete_a_closed, angles_closed)
x_b, y_b = polar_to_cartesian(athlete_b_closed, angles_closed)

# Create dataframe for polygon and path
df_a = pd.DataFrame({"x": x_a, "y": y_a, "entity": "Athlete A"})
df_b = pd.DataFrame({"x": x_b, "y": y_b, "entity": "Athlete B"})
df_data = pd.concat([df_a, df_b], ignore_index=True)

# Create points data (without the closing point)
x_a_pts, y_a_pts = polar_to_cartesian(athlete_a, angles)
x_b_pts, y_b_pts = polar_to_cartesian(athlete_b, angles)
df_points = pd.DataFrame(
    {"x": x_a_pts + x_b_pts, "y": y_a_pts + y_b_pts, "entity": ["Athlete A"] * n_vars + ["Athlete B"] * n_vars}
)

# Create grid circles at intervals of 20
grid_circles = []
for r in [20, 40, 60, 80, 100]:
    circle_angles = np.linspace(0, 2 * np.pi, 100)
    cx = r * np.cos(circle_angles)
    cy = r * np.sin(circle_angles)
    for i in range(len(cx)):
        grid_circles.append({"x": cx[i], "y": cy[i], "radius": r})
df_grid = pd.DataFrame(grid_circles)

# Create axis lines from center to edge
axis_lines = []
for a in angles:
    axis_lines.append({"x": 0, "y": 0, "xend": 100 * np.cos(a), "yend": 100 * np.sin(a)})
df_axes = pd.DataFrame(axis_lines)

# Create category labels positioned outside the chart
label_radius = 115
label_x = [label_radius * np.cos(a) for a in angles]
label_y = [label_radius * np.sin(a) for a in angles]
df_labels = pd.DataFrame({"x": label_x, "y": label_y, "label": categories})

# Create grid value labels
grid_label_angle = angles[0]  # Place along first axis
grid_labels = []
for r in [20, 40, 60, 80, 100]:
    grid_labels.append({"x": r * np.cos(grid_label_angle) + 5, "y": r * np.sin(grid_label_angle) + 5, "label": str(r)})
df_grid_labels = pd.DataFrame(grid_labels)

# Color palette from style guide
colors = {"Athlete A": "#306998", "Athlete B": "#DC2626"}

# Create the radar chart
plot = (
    ggplot()
    # Grid circles
    + geom_path(df_grid, aes(x="x", y="y", group="radius"), color="#cccccc", size=0.5, alpha=0.7)
    # Axis lines
    + geom_segment(df_axes, aes(x="x", y="y", xend="xend", yend="yend"), color="#cccccc", size=0.5, alpha=0.7)
    # Data polygons (filled areas)
    + geom_polygon(df_data, aes(x="x", y="y", fill="entity", group="entity"), alpha=0.25, color="none")
    # Data paths (outlines)
    + geom_path(df_data, aes(x="x", y="y", color="entity", group="entity"), size=1.5)
    # Data points
    + geom_point(df_points, aes(x="x", y="y", color="entity"), size=3)
    # Category labels
    + geom_text(df_labels, aes(x="x", y="y", label="label"), size=16, color="#333333")
    # Grid value labels
    + geom_text(df_grid_labels, aes(x="x", y="y", label="label"), size=10, color="#666666")
    # Colors
    + scale_color_manual(values=colors, name="Entity")
    + scale_fill_manual(values=colors, name="Entity")
    # Fixed aspect ratio for circular appearance
    + coord_fixed(xlim=(-130, 130), ylim=(-130, 130))
    + labs(title="Athlete Performance Comparison")
    + theme_void()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=20, ha="center", margin={"b": 20}),
        legend_position="right",
        legend_title=element_text(size=14),
        legend_text=element_text(size=14),
        legend_key_size=20,
    )
    + guides(color=guide_legend(override_aes={"size": 4}))
)

plot.save("plot.png", dpi=300, verbose=False)
