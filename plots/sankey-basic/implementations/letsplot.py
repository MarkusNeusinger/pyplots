""" pyplots.ai
sankey-basic: Basic Sankey Diagram
Library: letsplot 4.8.1 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-14
"""

import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_blank,
    element_text,
    geom_polygon,
    geom_rect,
    geom_text,
    ggplot,
    ggsize,
    labs,
    scale_fill_manual,
    scale_x_continuous,
    theme,
    theme_minimal,
)
from lets_plot.export import ggsave


LetsPlot.setup_html()

# Energy flow data: sources -> sectors
flows = [
    ("Coal", "Industrial", 25),
    ("Coal", "Residential", 10),
    ("Natural Gas", "Industrial", 20),
    ("Natural Gas", "Residential", 30),
    ("Natural Gas", "Commercial", 15),
    ("Nuclear", "Industrial", 15),
    ("Nuclear", "Commercial", 10),
    ("Renewable", "Residential", 12),
    ("Renewable", "Commercial", 8),
]

# Build node positions
sources = ["Coal", "Natural Gas", "Nuclear", "Renewable"]
targets = ["Industrial", "Residential", "Commercial"]

# Calculate totals for node heights
source_totals = {}
for src, _, val in flows:
    source_totals[src] = source_totals.get(src, 0) + val

target_totals = {}
for _, tgt, val in flows:
    target_totals[tgt] = target_totals.get(tgt, 0) + val

# Normalize and position nodes
total_flow = sum(v for _, _, v in flows)
node_gap = 0.03
x_left = 0.15
x_right = 0.85

# Source node positions (left side)
source_positions = {}
y_offset = 0
for src in sources:
    height = source_totals.get(src, 0) / total_flow
    source_positions[src] = {"y0": y_offset, "y1": y_offset + height, "x": x_left}
    y_offset += height + node_gap

# Target node positions (right side)
target_positions = {}
y_offset = 0
for tgt in targets:
    height = target_totals.get(tgt, 0) / total_flow
    target_positions[tgt] = {"y0": y_offset, "y1": y_offset + height, "x": x_right}
    y_offset += height + node_gap

# Track flow offsets within each node
source_offsets = dict.fromkeys(sources, 0)
target_offsets = dict.fromkeys(targets, 0)

# Build flow polygons using bezier curves approximated as polygons
flow_data = []

for src, tgt, val in flows:
    flow_height = val / total_flow

    # Source connection points
    src_y0 = source_positions[src]["y0"] + source_offsets[src]
    src_y1 = src_y0 + flow_height
    source_offsets[src] += flow_height

    # Target connection points
    tgt_y0 = target_positions[tgt]["y0"] + target_offsets[tgt]
    tgt_y1 = tgt_y0 + flow_height
    target_offsets[tgt] += flow_height

    # Create bezier-like polygon for the flow
    n_points = 30
    x_vals_top = []
    y_vals_top = []
    x_vals_bottom = []
    y_vals_bottom = []

    for i in range(n_points + 1):
        t = i / n_points
        # Bezier curve for smooth flow
        x = x_left + t * (x_right - x_left)
        # Cubic bezier interpolation
        ease = t * t * (3 - 2 * t)
        y_top = src_y1 + ease * (tgt_y1 - src_y1)
        y_bottom = src_y0 + ease * (tgt_y0 - src_y0)

        x_vals_top.append(x)
        y_vals_top.append(y_top)
        x_vals_bottom.append(x)
        y_vals_bottom.append(y_bottom)

    # Combine into polygon (top forward, bottom backward)
    x_polygon = x_vals_top + x_vals_bottom[::-1]
    y_polygon = y_vals_top + y_vals_bottom[::-1]

    for x, y in zip(x_polygon, y_polygon, strict=False):
        flow_data.append({"x": x, "y": y, "flow_id": f"{src}->{tgt}", "source": src, "value": val})

df_flows = pd.DataFrame(flow_data)

# Build node rectangles
node_rects = []
node_width = 0.03

for src in sources:
    pos = source_positions[src]
    node_rects.append(
        {
            "xmin": pos["x"] - node_width / 2,
            "xmax": pos["x"] + node_width / 2,
            "ymin": pos["y0"],
            "ymax": pos["y1"],
            "label": src,
            "side": "source",
        }
    )

for tgt in targets:
    pos = target_positions[tgt]
    node_rects.append(
        {
            "xmin": pos["x"] - node_width / 2,
            "xmax": pos["x"] + node_width / 2,
            "ymin": pos["y0"],
            "ymax": pos["y1"],
            "label": tgt,
            "side": "target",
        }
    )

df_nodes = pd.DataFrame(node_rects)

# Node labels
labels = []
for src in sources:
    pos = source_positions[src]
    labels.append(
        {
            "x": pos["x"] - node_width - 0.01,
            "y": (pos["y0"] + pos["y1"]) / 2,
            "label": f"{src} ({source_totals[src]})",
            "side": "left",
        }
    )

for tgt in targets:
    pos = target_positions[tgt]
    labels.append(
        {
            "x": pos["x"] + node_width + 0.01,
            "y": (pos["y0"] + pos["y1"]) / 2,
            "label": f"{tgt} ({target_totals[tgt]})",
            "side": "right",
        }
    )

df_labels = pd.DataFrame(labels)

# Create the plot
plot = (
    ggplot()
    + geom_polygon(aes(x="x", y="y", group="flow_id", fill="source"), data=df_flows, alpha=0.6, color="white", size=0.1)
    + geom_rect(
        aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax"), data=df_nodes, fill="#2C3E50", color="#1A252F", size=1
    )
    + geom_text(aes(x="x", y="y", label="label"), data=df_labels[df_labels["side"] == "left"], size=12, hjust=1)
    + geom_text(aes(x="x", y="y", label="label"), data=df_labels[df_labels["side"] == "right"], size=12, hjust=0)
    + scale_fill_manual(values=["#4A4A4A", "#306998", "#9B59B6", "#27AE60"], name="Energy Source")
    + labs(title="Energy Flow · sankey-basic · letsplot · pyplots.ai")
    + theme_minimal()
    + theme(
        plot_title=element_text(size=28, face="bold"),
        axis_title=element_blank(),
        axis_text=element_blank(),
        axis_ticks=element_blank(),
        panel_grid=element_blank(),
        legend_text=element_text(size=16),
        legend_title=element_text(size=18),
        legend_position="bottom",
    )
    + scale_x_continuous(limits=[-0.05, 1.05])
    + ggsize(1600, 900)
)

# Save as PNG (path='.' saves to current directory)
ggsave(plot, "plot.png", path=".", scale=3)

# Save as HTML
ggsave(plot, "plot.html", path=".")
