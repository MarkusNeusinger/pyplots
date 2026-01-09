"""pyplots.ai
network-transport-static: Static Transport Network Diagram
Library: lets-plot | Python 3.13
Quality: pending | Created: 2026-01-09
"""

import numpy as np
import pandas as pd
from lets_plot import *


LetsPlot.setup_html()

# Data: Regional rail network with stations and routes
np.random.seed(42)

# Station data with x, y coordinates (positioned like a simplified rail map)
# Adjusted to give more margin on edges for labels
stations = [
    {"id": "A", "label": "Central", "x": 0.5, "y": 0.5},
    {"id": "B", "label": "North", "x": 0.5, "y": 0.85},
    {"id": "C", "label": "East", "x": 0.78, "y": 0.5},
    {"id": "D", "label": "South", "x": 0.5, "y": 0.15},
    {"id": "E", "label": "West", "x": 0.22, "y": 0.5},
    {"id": "F", "label": "Airport", "x": 0.78, "y": 0.78},
    {"id": "G", "label": "University", "x": 0.22, "y": 0.78},
    {"id": "H", "label": "Harbor", "x": 0.78, "y": 0.22},
    {"id": "I", "label": "Tech Park", "x": 0.22, "y": 0.22},
    {"id": "J", "label": "Stadium", "x": 0.64, "y": 0.36},
]

# Route data: train connections with times
routes = [
    # Express routes (RE) - Central hub connections
    {"source": "A", "target": "B", "route_id": "RE1", "depart": "06:15", "arrive": "06:35", "type": "Express"},
    {"source": "A", "target": "C", "route_id": "RE2", "depart": "06:30", "arrive": "06:55", "type": "Express"},
    {"source": "A", "target": "D", "route_id": "RE3", "depart": "07:00", "arrive": "07:25", "type": "Express"},
    {"source": "A", "target": "E", "route_id": "RE4", "depart": "07:15", "arrive": "07:40", "type": "Express"},
    # Regional routes (RB) - Connecting outer stations
    {"source": "B", "target": "F", "route_id": "RB1", "depart": "07:00", "arrive": "07:20", "type": "Regional"},
    {"source": "B", "target": "G", "route_id": "RB2", "depart": "07:30", "arrive": "07:55", "type": "Regional"},
    {"source": "C", "target": "F", "route_id": "RB3", "depart": "08:00", "arrive": "08:25", "type": "Regional"},
    {"source": "C", "target": "H", "route_id": "RB4", "depart": "08:15", "arrive": "08:40", "type": "Regional"},
    {"source": "D", "target": "H", "route_id": "RB5", "depart": "08:30", "arrive": "08:55", "type": "Regional"},
    {"source": "D", "target": "I", "route_id": "RB6", "depart": "09:00", "arrive": "09:30", "type": "Regional"},
    {"source": "E", "target": "G", "route_id": "RB7", "depart": "09:15", "arrive": "09:40", "type": "Regional"},
    {"source": "E", "target": "I", "route_id": "RB8", "depart": "09:30", "arrive": "09:55", "type": "Regional"},
    # Local routes (S) - Short connections
    {"source": "C", "target": "J", "route_id": "S1", "depart": "10:00", "arrive": "10:12", "type": "Local"},
    {"source": "J", "target": "H", "route_id": "S2", "depart": "10:15", "arrive": "10:30", "type": "Local"},
    {"source": "A", "target": "J", "route_id": "S3", "depart": "10:30", "arrive": "10:50", "type": "Local"},
]

# Create DataFrames
stations_df = pd.DataFrame(stations)

# Build edge DataFrame with source/target coordinates
station_coords = {s["id"]: (s["x"], s["y"]) for s in stations}
edges_data = []
for r in routes:
    src_x, src_y = station_coords[r["source"]]
    tgt_x, tgt_y = station_coords[r["target"]]
    # Shorten edges slightly so arrows don't overlap nodes
    dx, dy = tgt_x - src_x, tgt_y - src_y
    length = np.sqrt(dx**2 + dy**2)
    offset = 0.04 / length if length > 0 else 0

    # Calculate perpendicular offset for label positioning
    perp_x = -dy / length if length > 0 else 0
    perp_y = dx / length if length > 0 else 0

    # Offset labels perpendicular to edge direction
    label_offset = 0.025

    edges_data.append(
        {
            "x": src_x + dx * offset,
            "y": src_y + dy * offset,
            "xend": tgt_x - dx * offset,
            "yend": tgt_y - dy * offset,
            "route_id": r["route_id"],
            "label": f"{r['route_id']} | {r['depart']} \u2192 {r['arrive']}",
            "type": r["type"],
            "mid_x": (src_x + tgt_x) / 2 + perp_x * label_offset,
            "mid_y": (src_y + tgt_y) / 2 + perp_y * label_offset,
        }
    )

edges_df = pd.DataFrame(edges_data)

# Color palette for route types (darker yellow for better label visibility)
route_colors = {"Express": "#306998", "Regional": "#B8860B", "Local": "#2E8B57"}

# Create the plot
plot = (
    ggplot()
    # Draw edges as segments with arrows
    + geom_segment(
        aes(x="x", y="y", xend="xend", yend="yend", color="type"),
        data=edges_df,
        size=1.8,
        alpha=0.85,
        arrow=arrow(angle=25, length=12, type="closed"),
    )
    # Draw edge labels (route and times)
    + geom_text(aes(x="mid_x", y="mid_y", label="label", color="type"), data=edges_df, size=5.5)
    # Draw station nodes
    + geom_point(aes(x="x", y="y"), data=stations_df, size=12, color="white", shape=21, fill="#303030", stroke=2.5)
    # Draw station labels
    + geom_text(
        aes(x="x", y="y", label="label"), data=stations_df, size=10, color="#202020", fontface="bold", nudge_y=-0.05
    )
    # Color scale for route types
    + scale_color_manual(values=route_colors, name="Route Type")
    # Styling
    + labs(title="network-transport-static \u00b7 letsplot \u00b7 pyplots.ai", x="", y="")
    + theme_void()
    + theme(
        plot_title=element_text(size=24, face="bold", hjust=0.5),
        legend_position="right",
        legend_title=element_text(size=16),
        legend_text=element_text(size=14),
    )
    + scale_x_continuous(limits=[0, 1])
    + scale_y_continuous(limits=[0, 1])
    + coord_fixed(ratio=1)
    + ggsize(1600, 900)
)

# Save as PNG (scale 3x for 4800x2700)
ggsave(plot, "plot.png", scale=3, path=".")

# Save as HTML for interactivity
ggsave(plot, "plot.html", path=".")
