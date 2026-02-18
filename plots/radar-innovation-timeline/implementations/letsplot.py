""" pyplots.ai
radar-innovation-timeline: Innovation Radar with Time-Horizon Rings
Library: letsplot 4.8.2 | Python 3.14.3
Quality: 78/100 | Created: 2026-02-18
"""

import math

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    coord_fixed,
    element_blank,
    element_rect,
    element_text,
    geom_path,
    geom_point,
    geom_polygon,
    geom_segment,
    geom_text,
    ggplot,
    ggsave,
    ggsize,
    labs,
    scale_color_manual,
    scale_x_continuous,
    scale_y_continuous,
    theme,
)


LetsPlot.setup_html()

np.random.seed(42)

# Data - Innovation items across 4 sectors and 4 time-horizon rings
rings = ["Adopt", "Trial", "Assess", "Hold"]
sectors = ["AI & ML", "Sustainability", "Biotech", "Infrastructure"]
sector_colors = {"AI & ML": "#306998", "Biotech": "#9F5AC1", "Infrastructure": "#E56910", "Sustainability": "#22A06B"}

# 270-degree layout (gap at top-center for ring labels)
arc_start = math.pi * 3 / 4  # 135 degrees (upper-left)
arc_end = arc_start + math.pi * 3 / 2  # +270 degrees to 45 degrees (upper-right)
arc_span = arc_end - arc_start

sector_span = arc_span / len(sectors)

ring_inner = {"Adopt": 0.5, "Trial": 1.5, "Assess": 2.5, "Hold": 3.5}
ring_outer = {"Adopt": 1.5, "Trial": 2.5, "Assess": 3.5, "Hold": 4.5}

innovations = [
    {"name": "LLM Agents", "ring": "Adopt", "sector": "AI & ML"},
    {"name": "RAG Pipelines", "ring": "Adopt", "sector": "AI & ML"},
    {"name": "Vision Models", "ring": "Trial", "sector": "AI & ML"},
    {"name": "AI Code Review", "ring": "Trial", "sector": "AI & ML"},
    {"name": "Neuro-symbolic AI", "ring": "Assess", "sector": "AI & ML"},
    {"name": "Quantum ML", "ring": "Hold", "sector": "AI & ML"},
    {"name": "Carbon Tracking", "ring": "Adopt", "sector": "Sustainability"},
    {"name": "Green Cloud", "ring": "Trial", "sector": "Sustainability"},
    {"name": "Circular Design", "ring": "Trial", "sector": "Sustainability"},
    {"name": "Biodegradable PCBs", "ring": "Assess", "sector": "Sustainability"},
    {"name": "Fusion Energy", "ring": "Hold", "sector": "Sustainability"},
    {"name": "Ocean Cleanup AI", "ring": "Assess", "sector": "Sustainability"},
    {"name": "mRNA Platforms", "ring": "Adopt", "sector": "Biotech"},
    {"name": "Gene Editing", "ring": "Trial", "sector": "Biotech"},
    {"name": "Digital Twins (Bio)", "ring": "Assess", "sector": "Biotech"},
    {"name": "Organ-on-Chip", "ring": "Assess", "sector": "Biotech"},
    {"name": "Synthetic Biology", "ring": "Trial", "sector": "Biotech"},
    {"name": "Nanomedicine", "ring": "Hold", "sector": "Biotech"},
    {"name": "Edge Computing", "ring": "Adopt", "sector": "Infrastructure"},
    {"name": "WebAssembly", "ring": "Adopt", "sector": "Infrastructure"},
    {"name": "Service Mesh", "ring": "Trial", "sector": "Infrastructure"},
    {"name": "Confidential Compute", "ring": "Assess", "sector": "Infrastructure"},
    {"name": "6G Research", "ring": "Hold", "sector": "Infrastructure"},
    {"name": "Satellite Internet", "ring": "Trial", "sector": "Infrastructure"},
]

# Ring-dependent angular micro-offsets to stagger labels across adjacent rings
ring_micro_offsets = {"Adopt": -0.08, "Trial": 0.08, "Assess": -0.06, "Hold": -0.15}
# Larger radial label offsets for inner rings where items converge near center
ring_label_offsets = {"Adopt": 0.60, "Trial": 0.50, "Assess": 0.45, "Hold": 0.40}

# Compute positions for each innovation item
item_rows = []
for item in innovations:
    sector_idx = sectors.index(item["sector"])
    ring_name = item["ring"]

    sector_start_angle = arc_start + sector_idx * sector_span
    sector_center = sector_start_angle + sector_span / 2

    same_items = [inn for inn in innovations if inn["sector"] == item["sector"] and inn["ring"] == ring_name]
    item_idx = same_items.index(item)
    n_same = len(same_items)

    # Wider angular spread within sectors to reduce crowding
    usable_span = sector_span * 0.80
    if n_same > 1:
        angle_offset = -usable_span / 2 + item_idx * usable_span / (n_same - 1)
    else:
        angle_offset = 0

    # Add ring micro-offset to prevent cross-ring label alignment
    angle = sector_center + angle_offset + ring_micro_offsets[ring_name]

    ring_mid = (ring_inner[ring_name] + ring_outer[ring_name]) / 2
    radius = ring_mid + np.random.uniform(-0.15, 0.15)

    x = radius * math.cos(angle)
    y = radius * math.sin(angle)

    # Label offset: push label radially outward (more for inner rings to reduce center crowding)
    label_r = radius + ring_label_offsets[ring_name]
    lx = label_r * math.cos(angle)
    ly = label_r * math.sin(angle)

    # Determine horizontal alignment based on which side of the chart
    norm_angle = angle % (2 * math.pi)
    if norm_angle > math.pi / 2 and norm_angle < 3 * math.pi / 2:
        side = "left"
    else:
        side = "right"

    item_rows.append(
        {
            "name": item["name"],
            "ring": ring_name,
            "sector": item["sector"],
            "x": x,
            "y": y,
            "lx": lx,
            "ly": ly,
            "side": side,
        }
    )

items_df = pd.DataFrame(item_rows)
items_left = items_df[items_df["side"] == "left"]
items_right = items_df[items_df["side"] == "right"]

# Ring background arcs (subtle fills per time horizon)
ring_bg_rows = []
ring_fill_colors = ["#DCEDC8", "#FFF9C4", "#FFE0B2", "#FFCDD2"]
n_arc = 100

for ring_name in rings:
    r_in = ring_inner[ring_name]
    r_out = ring_outer[ring_name]
    arc_angles = np.linspace(arc_start, arc_end, n_arc)

    xs = []
    ys = []
    for a in arc_angles:
        xs.append(r_out * math.cos(a))
        ys.append(r_out * math.sin(a))
    for a in reversed(arc_angles):
        xs.append(r_in * math.cos(a))
        ys.append(r_in * math.sin(a))
    xs.append(xs[0])
    ys.append(ys[0])

    for px, py in zip(xs, ys, strict=True):
        ring_bg_rows.append({"x": px, "y": py, "ring": ring_name})

ring_bg_df = pd.DataFrame(ring_bg_rows)

# Concentric ring boundary arcs using geom_path with explicit ordering
ring_boundary_rows = []
boundary_radii = [0.5, 1.5, 2.5, 3.5, 4.5]
for radius in boundary_radii:
    arc_angles = np.linspace(arc_start, arc_end, n_arc)
    for idx, a in enumerate(arc_angles):
        ring_boundary_rows.append(
            {"x": radius * math.cos(a), "y": radius * math.sin(a), "group": f"r{radius}", "order": idx}
        )

ring_boundary_df = pd.DataFrame(ring_boundary_rows).sort_values(["group", "order"])

# Sector divider spokes
spoke_rows = []
for i in range(len(sectors) + 1):
    angle = arc_start + i * sector_span
    spoke_rows.append(
        {
            "x": 0.5 * math.cos(angle),
            "y": 0.5 * math.sin(angle),
            "xend": 4.5 * math.cos(angle),
            "yend": 4.5 * math.sin(angle),
        }
    )

spoke_df = pd.DataFrame(spoke_rows)

# Sector header labels along outer edge
sector_label_rows = []
for i, sector in enumerate(sectors):
    angle = arc_start + (i + 0.5) * sector_span
    r = 5.8
    sector_label_rows.append({"label": sector, "x": r * math.cos(angle), "y": r * math.sin(angle)})

sector_label_df = pd.DataFrame(sector_label_rows)

# Ring name labels placed in the arc gap (top center at 90 degrees)
# This avoids overlap with data points which only exist within the 270-degree arc
ring_label_rows = []
gap_center = math.pi / 2  # 90 degrees = center of the 90-degree gap at top
for ring_name in rings:
    r = (ring_inner[ring_name] + ring_outer[ring_name]) / 2
    ring_label_rows.append({"label": ring_name, "x": r * math.cos(gap_center), "y": r * math.sin(gap_center)})

ring_label_df = pd.DataFrame(ring_label_rows)

# Plot
plot = ggplot()

# Ring background fills
for ring_name, fill_color in zip(rings, ring_fill_colors, strict=True):
    ring_data = ring_bg_df[ring_bg_df["ring"] == ring_name].copy()
    plot = plot + geom_polygon(aes(x="x", y="y"), data=ring_data, fill=fill_color, alpha=0.45)

# Ring boundary arcs
plot = plot + geom_path(aes(x="x", y="y", group="group"), data=ring_boundary_df, color="#BBBBBB", size=0.4, alpha=0.8)

# Sector divider spokes
plot = plot + geom_segment(
    aes(x="x", y="y", xend="xend", yend="yend"), data=spoke_df, color="#BBBBBB", size=0.4, alpha=0.8
)

# Sector header labels (drawn before data so data labels render on top)
plot = plot + geom_text(
    aes(x="x", y="y", label="label"), data=sector_label_df, size=14, color="#222222", fontface="bold"
)

# Ring name labels (in the arc gap at top center)
plot = plot + geom_text(aes(x="x", y="y", label="label"), data=ring_label_df, size=13, color="#444444", fontface="bold")

# Innovation points (color by sector)
plot = plot + geom_point(aes(x="x", y="y", color="sector"), data=items_df, size=6, alpha=0.9)

# Innovation labels - split by chart side for outward-extending horizontal alignment
plot = plot + geom_text(
    aes(x="lx", y="ly", label="name", color="sector"),
    data=items_left,
    size=8,
    hjust=1,  # right-align: text extends leftward (away from center)
)
plot = plot + geom_text(
    aes(x="lx", y="ly", label="name", color="sector"),
    data=items_right,
    size=8,
    hjust=0,  # left-align: text extends rightward (away from center)
)

# Style
plot = (
    plot
    + scale_color_manual(values=sector_colors)  # Dict mapping ensures correct color-sector pairing
    + scale_x_continuous(limits=(-7.0, 7.5))
    + scale_y_continuous(limits=(-6.2, 5.8))
    + coord_fixed()
    + labs(title="radar-innovation-timeline · letsplot · pyplots.ai", color="Sector")
    + ggsize(1200, 1200)
    + theme(
        plot_title=element_text(size=24, face="bold"),
        legend_title=element_text(size=18),
        legend_text=element_text(size=16),
        legend_position="bottom",
        axis_title=element_blank(),
        axis_text=element_blank(),
        axis_ticks=element_blank(),
        axis_line=element_blank(),
        panel_grid=element_blank(),
        plot_background=element_rect(fill="white", color="white"),
        panel_background=element_rect(fill="white", color="white"),
    )
)

# Save
ggsave(plot, "plot.png", path=".", scale=3)
ggsave(plot, "plot.html", path=".")
