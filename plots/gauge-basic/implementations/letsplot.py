""" pyplots.ai
gauge-basic: Basic Gauge Chart
Library: letsplot 4.8.1 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-14
"""

import math

import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_blank,
    element_text,
    geom_polygon,
    geom_segment,
    geom_text,
    ggplot,
    ggsave,
    ggsize,
    labs,
    scale_fill_manual,
    theme,
    xlim,
    ylim,
)


LetsPlot.setup_html()

# Data
value = 72
min_value = 0
max_value = 100
thresholds = [30, 70]

# Build arc segments for the gauge background (semi-circle)
# The gauge spans from 180° (left) to 0° (right)


def arc_polygon(start_deg, end_deg, inner_r, outer_r, n_points=50):
    """Generate polygon coordinates for an arc segment."""
    angles = [math.radians(a) for a in [start_deg + (end_deg - start_deg) * i / n_points for i in range(n_points + 1)]]
    # Outer arc (clockwise)
    x_outer = [outer_r * math.cos(a) for a in angles]
    y_outer = [outer_r * math.sin(a) for a in angles]
    # Inner arc (counter-clockwise)
    x_inner = [inner_r * math.cos(a) for a in reversed(angles)]
    y_inner = [inner_r * math.sin(a) for a in reversed(angles)]

    return x_outer + x_inner, y_outer + y_inner


# Create gauge zones based on thresholds
# Map value range to angle range (180° to 0°)
def value_to_angle(val):
    """Convert value to angle in degrees (180° at min, 0° at max)."""
    ratio = (val - min_value) / (max_value - min_value)
    return 180 - ratio * 180


inner_radius = 0.5
outer_radius = 1.0

# Zone boundaries in value space
zone_boundaries = [min_value] + thresholds + [max_value]
zone_colors = ["#DC2626", "#FFD43B", "#22C55E"]  # Red, Yellow, Green
zone_names = ["Low", "Medium", "High"]

# Build polygon data for each zone
polygons_data = []
for i in range(len(zone_boundaries) - 1):
    start_val = zone_boundaries[i]
    end_val = zone_boundaries[i + 1]
    start_angle = value_to_angle(start_val)
    end_angle = value_to_angle(end_val)

    x_coords, y_coords = arc_polygon(end_angle, start_angle, inner_radius, outer_radius)

    for j, (x, y) in enumerate(zip(x_coords, y_coords, strict=True)):
        polygons_data.append({"x": x, "y": y, "zone": zone_names[i], "order": j})

df_polygons = pd.DataFrame(polygons_data)

# Calculate needle position
needle_angle = math.radians(value_to_angle(value))
needle_length = 0.85
needle_x_end = needle_length * math.cos(needle_angle)
needle_y_end = needle_length * math.sin(needle_angle)

df_needle = pd.DataFrame({"x": [0], "y": [0], "xend": [needle_x_end], "yend": [needle_y_end]})

# Center circle for needle pivot
circle_points = 30
circle_angles = [2 * math.pi * i / circle_points for i in range(circle_points + 1)]
circle_r = 0.08
df_circle = pd.DataFrame(
    {"x": [circle_r * math.cos(a) for a in circle_angles], "y": [circle_r * math.sin(a) for a in circle_angles]}
)

# Value label
df_label = pd.DataFrame({"x": [0], "y": [-0.25], "label": [str(value)]})

# Create plot
plot = (
    ggplot()
    + geom_polygon(aes(x="x", y="y", fill="zone", group="zone"), data=df_polygons, color="#FFFFFF", size=1, alpha=0.9)
    + scale_fill_manual(values={"Low": "#DC2626", "Medium": "#FFD43B", "High": "#22C55E"})
    + geom_segment(aes(x="x", y="y", xend="xend", yend="yend"), data=df_needle, color="#1F2937", size=4)
    + geom_polygon(aes(x="x", y="y"), data=df_circle, fill="#1F2937", color="#1F2937")
    + geom_text(aes(x="x", y="y", label="label"), data=df_label, size=24, color="#1F2937", fontface="bold")
    + labs(title="gauge-basic · letsplot · pyplots.ai")
    + xlim(-1.3, 1.3)
    + ylim(-0.5, 1.2)
    + theme(
        axis_title=element_blank(),
        axis_text=element_blank(),
        axis_ticks=element_blank(),
        axis_line=element_blank(),
        panel_grid=element_blank(),
        panel_background=element_blank(),
        plot_background=element_blank(),
        legend_position="none",
        plot_title=element_text(size=24, face="bold"),
    )
    + ggsize(1600, 900)
)

# Save outputs
ggsave(plot, "plot.png", scale=3, path=".")
ggsave(plot, "plot.html", path=".")
