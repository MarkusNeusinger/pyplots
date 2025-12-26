""" pyplots.ai
pie-exploded: Exploded Pie Chart
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-26
"""

import sys


sys.path = [p for p in sys.path if not p.endswith("implementations")]

import math  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from plotnine import (  # noqa: E402
    aes,
    coord_fixed,
    element_blank,
    element_text,
    geom_polygon,
    geom_text,
    ggplot,
    labs,
    scale_fill_identity,
    scale_x_continuous,
    scale_y_continuous,
    theme,
)


# Data - Market share by company with explode values
categories = ["TechCorp", "DataSoft", "CloudInc", "NetWorks", "DevHub", "Others"]
values = [32, 24, 18, 12, 8, 6]
explode = [0.1, 0, 0, 0, 0, 0]  # Explode the market leader

# Colors - Python Blue first, then colorblind-safe palette
colors = ["#306998", "#FFD43B", "#2ECC71", "#E74C3C", "#9B59B6", "#1ABC9C"]

# Pie chart dimensions
radius = 120
center_x = 0
center_y = 0


def create_pie_segment(start_angle, end_angle, radius, center_x, center_y, n_points=50):
    """Create polygon points for a pie segment."""
    # Add small gap between segments
    gap = 0.02
    start_angle += gap
    end_angle -= gap

    points = [(center_x, center_y)]  # Start at center

    # Arc from start to end
    angles = np.linspace(start_angle, end_angle, n_points)
    for angle in angles:
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        points.append((x, y))

    # Close the polygon back to center
    points.append((center_x, center_y))
    return points


# Build polygon data for pie slices
rows = []
label_rows = []
total = sum(values)
current_angle = math.pi / 2  # Start at top (12 o'clock)

for cat, val, exp, color in zip(categories, values, explode, colors, strict=True):
    # Calculate sweep angle
    sweep = (val / total) * 2 * math.pi
    end_angle = current_angle - sweep  # Clockwise

    # Calculate explode offset (radial displacement)
    mid_angle = (current_angle + end_angle) / 2
    offset_x = exp * radius * math.cos(mid_angle) * 0.8
    offset_y = exp * radius * math.sin(mid_angle) * 0.8

    # Create segment polygon with offset center
    points = create_pie_segment(end_angle, current_angle, radius, center_x + offset_x, center_y + offset_y)

    for order, (x, y) in enumerate(points):
        rows.append({"x": x, "y": y, "segment": cat, "order": order, "fill": color})

    # Calculate percentage label position (inside the slice)
    percentage = val / total * 100
    label_radius = radius * 0.65
    label_x = center_x + offset_x + label_radius * math.cos(mid_angle)
    label_y = center_y + offset_y + label_radius * math.sin(mid_angle)
    label_rows.append({"x": label_x, "y": label_y, "label": f"{percentage:.1f}%", "category": cat})

    current_angle = end_angle

df = pd.DataFrame(rows)
label_df = pd.DataFrame(label_rows)

# Create legend data (positioned to the right)
legend_rows = []
legend_x = 180
legend_y_start = 80
legend_spacing = 35

for idx, (cat, val, color) in enumerate(zip(categories, values, colors, strict=True)):
    percentage = val / total * 100
    legend_rows.append(
        {
            "x": legend_x,
            "y": legend_y_start - idx * legend_spacing,
            "label": f"{cat} ({percentage:.1f}%)",
            "fill": color,
        }
    )

legend_df = pd.DataFrame(legend_rows)

# Create legend color boxes
legend_box_rows = []
box_size = 12

for idx, (cat, color) in enumerate(zip(categories, colors, strict=True)):
    y_pos = legend_y_start - idx * legend_spacing
    # Create a small square
    box_points = [
        (legend_x - 25, y_pos - box_size / 2),
        (legend_x - 25 + box_size, y_pos - box_size / 2),
        (legend_x - 25 + box_size, y_pos + box_size / 2),
        (legend_x - 25, y_pos + box_size / 2),
        (legend_x - 25, y_pos - box_size / 2),
    ]
    for order, (x, y) in enumerate(box_points):
        legend_box_rows.append({"x": x, "y": y, "segment": f"legend_{cat}", "order": order, "fill": color})

legend_box_df = pd.DataFrame(legend_box_rows)

# Plot
plot = (
    ggplot()
    # Pie slices
    + geom_polygon(aes(x="x", y="y", group="segment", fill="fill"), data=df, color="#FFFFFF", size=1, alpha=0.95)
    # Percentage labels on slices
    + geom_text(aes(x="x", y="y", label="label"), data=label_df, size=14, fontweight="bold", color="#FFFFFF")
    # Legend color boxes
    + geom_polygon(aes(x="x", y="y", group="segment", fill="fill"), data=legend_box_df, color="#333333", size=0.5)
    # Legend text
    + geom_text(aes(x="x", y="y", label="label"), data=legend_df, size=12, ha="left", color="#333333")
    # Use fill colors directly
    + scale_fill_identity()
    # Fixed aspect ratio for proper circle
    + coord_fixed(ratio=1)
    # Axis limits with padding for legend
    + scale_x_continuous(limits=(-180, 350))
    + scale_y_continuous(limits=(-180, 180))
    # Title
    + labs(title="Market Share by Company · pie-exploded · plotnine · pyplots.ai")
    # Clean theme
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=24, ha="center"),
        axis_title=element_blank(),
        axis_text=element_blank(),
        axis_ticks=element_blank(),
        axis_line=element_blank(),
        panel_grid_major=element_blank(),
        panel_grid_minor=element_blank(),
        panel_background=element_blank(),
        legend_position="none",
    )
)

# Save
plot.save("plot.png", dpi=300)
