""" pyplots.ai
gauge-realtime: Real-Time Updating Gauge
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 91/100 | Created: 2026-01-19
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    coord_fixed,
    element_blank,
    geom_point,
    geom_polygon,
    geom_segment,
    geom_text,
    ggplot,
    labs,
    scale_alpha_identity,
    scale_fill_manual,
    theme,
    theme_void,
)


# Data - simulated CPU usage fluctuating (realtime snapshot)
current_value = 67
min_value = 0
max_value = 100
thresholds = [50, 80]  # Green < 50, Yellow 50-80, Red > 80

# Previous values to show motion trail (simulating recent updates)
# Values show a realistic gradual change pattern
previous_values = [58, 62, 65]  # Gradual increase to current value

# Gauge parameters
inner_radius = 0.5
outer_radius = 1.0
start_angle = np.pi  # 180 degrees (left)
end_angle = 0  # 0 degrees (right)

# Create color zones based on thresholds (green/yellow/red for CPU)
zones = []
zone_colors = ["#27AE60", "#F1C40F", "#E74C3C"]  # Green, Yellow, Red
zone_bounds = [min_value] + thresholds + [max_value]

for i in range(len(zone_bounds) - 1):
    start_pct = (zone_bounds[i] - min_value) / (max_value - min_value)
    end_pct = (zone_bounds[i + 1] - min_value) / (max_value - min_value)

    # Create arc segment as polygon
    start_ang = start_angle - start_pct * (start_angle - end_angle)
    end_ang = start_angle - end_pct * (start_angle - end_angle)
    n_points = 50

    angles_outer = np.linspace(start_ang, end_ang, n_points)
    angles_inner = np.linspace(end_ang, start_ang, n_points)

    x = np.concatenate([outer_radius * np.cos(angles_outer), inner_radius * np.cos(angles_inner)])
    y = np.concatenate([outer_radius * np.sin(angles_outer), inner_radius * np.sin(angles_inner)])

    for j in range(len(x)):
        zones.append({"x": x[j], "y": y[j], "zone": i, "color": zone_colors[i]})

df_zones = pd.DataFrame(zones)

# Create motion trail - ghost needles showing previous positions
ghost_needles = []
alphas = [0.15, 0.25, 0.4]  # Increasing opacity for more recent positions

for idx, prev_val in enumerate(previous_values):
    prev_pct = (prev_val - min_value) / (max_value - min_value)
    prev_angle = start_angle - prev_pct * (start_angle - end_angle)
    ghost_length = outer_radius * 0.85
    ghost_needles.append(
        {
            "x": 0,
            "y": 0,
            "xend": ghost_length * np.cos(prev_angle),
            "yend": ghost_length * np.sin(prev_angle),
            "alpha": alphas[idx],
        }
    )

df_ghost = pd.DataFrame(ghost_needles)

# Create current needle pointing to value
value_pct = (current_value - min_value) / (max_value - min_value)
needle_angle = start_angle - value_pct * (start_angle - end_angle)
needle_length = outer_radius * 0.85

df_needle = pd.DataFrame(
    {"x": [0], "y": [0], "xend": [needle_length * np.cos(needle_angle)], "yend": [needle_length * np.sin(needle_angle)]}
)

# Create tick marks and labels
tick_values = [0, 25, 50, 75, 100]
tick_data = []
label_data = []
tick_inner = outer_radius * 1.02
tick_outer = outer_radius * 1.08
label_radius = outer_radius * 1.18

for tv in tick_values:
    pct = (tv - min_value) / (max_value - min_value)
    ang = start_angle - pct * (start_angle - end_angle)
    tick_data.append(
        {
            "x": tick_inner * np.cos(ang),
            "y": tick_inner * np.sin(ang),
            "xend": tick_outer * np.cos(ang),
            "yend": tick_outer * np.sin(ang),
        }
    )
    label_data.append({"x": label_radius * np.cos(ang), "y": label_radius * np.sin(ang), "label": str(tv)})

df_ticks = pd.DataFrame(tick_data)
df_labels = pd.DataFrame(label_data)

# Value display label with percentage
df_value = pd.DataFrame({"x": [0], "y": [-0.15], "label": [f"{current_value}%"]})

# Metric name label
df_metric = pd.DataFrame({"x": [0], "y": [-0.35], "label": ["CPU Usage"]})

# Title label
df_title = pd.DataFrame({"x": [0], "y": [1.45], "label": ["gauge-realtime · plotnine · pyplots.ai"]})

# Real-time indicator label
df_indicator = pd.DataFrame({"x": [0], "y": [-0.52], "label": ["● LIVE"]})

# Build the plot
plot = (
    ggplot()
    # Draw zone arcs as polygons grouped by zone
    + geom_polygon(aes(x="x", y="y", fill="factor(zone)", group="zone"), data=df_zones, color="white", size=0.5)
    # Draw tick marks
    + geom_segment(aes(x="x", y="y", xend="xend", yend="yend"), data=df_ticks, color="#2C3E50", size=1.5)
    # Draw tick labels
    + geom_text(aes(x="x", y="y", label="label"), data=df_labels, color="#2C3E50", size=16)
    # Draw ghost needles (motion trail) with varying alpha
    + geom_segment(aes(x="x", y="y", xend="xend", yend="yend", alpha="alpha"), data=df_ghost, color="#2C3E50", size=2)
    + scale_alpha_identity()
    # Draw current needle (solid)
    + geom_segment(aes(x="x", y="y", xend="xend", yend="yend"), data=df_needle, color="#2C3E50", size=3)
    # Draw needle center circle
    + geom_point(aes(x="x", y="y"), data=pd.DataFrame({"x": [0], "y": [0]}), color="#2C3E50", size=8)
    # Draw value label
    + geom_text(aes(x="x", y="y", label="label"), data=df_value, color="#2C3E50", size=28, fontweight="bold")
    # Draw metric name
    + geom_text(aes(x="x", y="y", label="label"), data=df_metric, color="#7F8C8D", size=14)
    # Draw live indicator
    + geom_text(aes(x="x", y="y", label="label"), data=df_indicator, color="#E74C3C", size=12, fontweight="bold")
    # Draw title
    + geom_text(aes(x="x", y="y", label="label"), data=df_title, color="#2C3E50", size=14)
    + coord_fixed(ratio=1, xlim=(-1.5, 1.5), ylim=(-0.7, 1.6))
    + labs(x="", y="")
    + theme_void()
    + theme(figure_size=(16, 9), legend_position="none", plot_background=element_blank())
    # Manual fill colors for zones
    + scale_fill_manual(values=zone_colors)
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
