"""pyplots.ai
gauge-realtime: Real-Time Updating Gauge
Library: lets-plot | Python 3.13
Quality: pending | Created: 2025-01-19
"""

import numpy as np
import pandas as pd
from lets_plot import *

LetsPlot.setup_html()

# Data - Simulated CPU usage with realtime effect
np.random.seed(42)
current_value = 67  # Current CPU usage percentage
min_value = 0
max_value = 100
thresholds = [50, 80]  # Green < 50, Yellow 50-80, Red > 80

# Ghost needle positions to show motion/realtime effect
previous_values = [58, 62, 65]  # Previous positions for motion blur effect

# Create gauge arc segments
n_segments = 100
inner_r = 0.6
outer_r = 1.0

# Create polygon data for gauge segments
polygon_segments = []
segment_id = 0
for i in range(n_segments):
    val = min_value + (max_value - min_value) * i / n_segments
    # Convert value to angle (pi to 0 for left-to-right gauge)
    normalized = (val - min_value) / (max_value - min_value)
    angle1 = np.pi - normalized * np.pi

    val2 = val + (max_value - min_value) / n_segments
    normalized2 = (val2 - min_value) / (max_value - min_value)
    angle2 = np.pi - normalized2 * np.pi

    # Determine color zone
    if val < thresholds[0]:
        zone = "Normal"
    elif val < thresholds[1]:
        zone = "Warning"
    else:
        zone = "Critical"

    # Four corners of segment polygon
    corners = [
        (np.cos(angle1) * inner_r, np.sin(angle1) * inner_r),
        (np.cos(angle1) * outer_r, np.sin(angle1) * outer_r),
        (np.cos(angle2) * outer_r, np.sin(angle2) * outer_r),
        (np.cos(angle2) * inner_r, np.sin(angle2) * inner_r),
    ]

    for x, y in corners:
        polygon_segments.append({"x": x, "y": y, "segment_id": segment_id, "zone": zone})
    segment_id += 1

polygon_df = pd.DataFrame(polygon_segments)

# Main needle
needle_length = 0.55
main_normalized = (current_value - min_value) / (max_value - min_value)
main_angle = np.pi - main_normalized * np.pi

needle_data = pd.DataFrame(
    {"x": [0], "y": [0], "xend": [np.cos(main_angle) * needle_length], "yend": [np.sin(main_angle) * needle_length]}
)

# Ghost needles for motion blur effect
ghost_data = []
for i, prev_val in enumerate(previous_values):
    normalized = (prev_val - min_value) / (max_value - min_value)
    angle = np.pi - normalized * np.pi
    ghost_data.append({"x": 0, "y": 0, "xend": np.cos(angle) * needle_length, "yend": np.sin(angle) * needle_length})
ghost_df = pd.DataFrame(ghost_data)

# Tick marks data
tick_data = []
tick_values = [0, 25, 50, 75, 100]
for val in tick_values:
    normalized = (val - min_value) / (max_value - min_value)
    angle = np.pi - normalized * np.pi
    tick_data.append(
        {
            "x": np.cos(angle) * 1.05,
            "y": np.sin(angle) * 1.05,
            "xend": np.cos(angle) * 1.15,
            "yend": np.sin(angle) * 1.15,
            "label_x": np.cos(angle) * 1.25,
            "label_y": np.sin(angle) * 1.25,
            "value": val,
        }
    )
tick_df = pd.DataFrame(tick_data)

# Label data for tick marks
label_df = pd.DataFrame(
    {
        "x": [t["label_x"] for t in tick_data],
        "y": [t["label_y"] for t in tick_data],
        "label": [str(int(t["value"])) for t in tick_data],
    }
)

# Create the plot
plot = (
    ggplot()
    # Gauge arc segments
    + geom_polygon(aes(x="x", y="y", group="segment_id", fill="zone"), data=polygon_df, color="white", size=0.2)
    # Color scale for zones
    + scale_fill_manual(values={"Normal": "#22C55E", "Warning": "#EAB308", "Critical": "#DC2626"}, name="Status")
    # Ghost needles (motion blur effect)
    + geom_segment(aes(x="x", y="y", xend="xend", yend="yend"), data=ghost_df, color="#64748B", size=3, alpha=0.25)
    # Main needle
    + geom_segment(aes(x="x", y="y", xend="xend", yend="yend"), data=needle_data, color="#1E293B", size=5)
    # Needle center hub
    + geom_point(aes(x="x", y="y"), data=pd.DataFrame({"x": [0], "y": [0]}), color="#1E293B", size=12)
    + geom_point(aes(x="x", y="y"), data=pd.DataFrame({"x": [0], "y": [0]}), color="#475569", size=6)
    # Tick marks
    + geom_segment(aes(x="x", y="y", xend="xend", yend="yend"), data=tick_df, color="#334155", size=1.5)
    # Tick labels
    + geom_text(aes(x="x", y="y", label="label"), data=label_df, size=14, color="#334155")
    # Current value display
    + geom_text(
        aes(x="x", y="y", label="label"),
        data=pd.DataFrame({"x": [0], "y": [-0.25], "label": [f"{current_value}%"]}),
        size=28,
        color="#1E293B",
        fontface="bold",
    )
    # Label below value
    + geom_text(
        aes(x="x", y="y", label="label"),
        data=pd.DataFrame({"x": [0], "y": [-0.45], "label": ["CPU Usage"]}),
        size=14,
        color="#64748B",
    )
    # Title
    + ggtitle("gauge-realtime · letsplot · pyplots.ai")
    # Theme and sizing
    + theme_void()
    + theme(
        plot_title=element_text(size=24, hjust=0.5, color="#1E293B"),
        legend_position="none",
        plot_background=element_rect(fill="white"),
        panel_background=element_rect(fill="white"),
    )
    + coord_fixed(ratio=1)
    + ggsize(1200, 900)
    + scale_x_continuous(limits=[-1.5, 1.5])
    + scale_y_continuous(limits=[-0.7, 1.5])
)

# Save outputs
ggsave(plot, "plot.png", scale=3)
ggsave(plot, "plot.html")
