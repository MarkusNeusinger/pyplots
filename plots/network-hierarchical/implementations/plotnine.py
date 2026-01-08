"""pyplots.ai
network-hierarchical: Hierarchical Network Graph with Tree Layout
Library: plotnine | Python 3.13
Quality: pending | Created: 2026-01-08
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_rect,
    element_text,
    geom_point,
    geom_segment,
    geom_text,
    ggplot,
    labs,
    scale_color_manual,
    scale_size_identity,
    theme,
    xlim,
    ylim,
)


# Set seed for reproducibility
np.random.seed(42)

# Data: Software company organizational hierarchy (30 employees, 4 levels)
nodes = [
    # Level 0 - CEO
    {"id": 0, "label": "CEO", "level": 0},
    # Level 1 - VPs (3 people)
    {"id": 1, "label": "VP Engineering", "level": 1},
    {"id": 2, "label": "VP Product", "level": 1},
    {"id": 3, "label": "VP Operations", "level": 1},
    # Level 2 - Directors (8 people)
    {"id": 4, "label": "Frontend Dir", "level": 2},
    {"id": 5, "label": "Backend Dir", "level": 2},
    {"id": 6, "label": "QA Director", "level": 2},
    {"id": 7, "label": "PM Lead", "level": 2},
    {"id": 8, "label": "UX Lead", "level": 2},
    {"id": 9, "label": "IT Manager", "level": 2},
    {"id": 10, "label": "HR Manager", "level": 2},
    {"id": 11, "label": "Finance Mgr", "level": 2},
    # Level 3 - Team Members (18 people)
    {"id": 12, "label": "FE Dev 1", "level": 3},
    {"id": 13, "label": "FE Dev 2", "level": 3},
    {"id": 14, "label": "FE Dev 3", "level": 3},
    {"id": 15, "label": "BE Dev 1", "level": 3},
    {"id": 16, "label": "BE Dev 2", "level": 3},
    {"id": 17, "label": "QA Eng 1", "level": 3},
    {"id": 18, "label": "QA Eng 2", "level": 3},
    {"id": 19, "label": "PM 1", "level": 3},
    {"id": 20, "label": "PM 2", "level": 3},
    {"id": 21, "label": "Designer 1", "level": 3},
    {"id": 22, "label": "Designer 2", "level": 3},
    {"id": 23, "label": "IT Support", "level": 3},
    {"id": 24, "label": "SysAdmin", "level": 3},
    {"id": 25, "label": "HR Specialist", "level": 3},
    {"id": 26, "label": "Recruiter", "level": 3},
    {"id": 27, "label": "Accountant", "level": 3},
    {"id": 28, "label": "Analyst", "level": 3},
    {"id": 29, "label": "Intern", "level": 3},
]

edges = [
    # CEO to VPs
    (0, 1),
    (0, 2),
    (0, 3),
    # VP Engineering to Directors
    (1, 4),
    (1, 5),
    (1, 6),
    # VP Product to Leads
    (2, 7),
    (2, 8),
    # VP Operations to Managers
    (3, 9),
    (3, 10),
    (3, 11),
    # Directors to Team Members
    (4, 12),
    (4, 13),
    (4, 14),
    (5, 15),
    (5, 16),
    (6, 17),
    (6, 18),
    (7, 19),
    (7, 20),
    (8, 21),
    (8, 22),
    (9, 23),
    (9, 24),
    (10, 25),
    (10, 26),
    (11, 27),
    (11, 28),
    (11, 29),
]

# Compute hierarchical layout positions
# Group nodes by level
levels = {}
for node in nodes:
    lvl = node["level"]
    if lvl not in levels:
        levels[lvl] = []
    levels[lvl].append(node)

# Calculate positions: levels spread vertically, nodes at each level spread horizontally
positions = {}
y_spacing = 0.25  # Vertical spacing between levels
for lvl in sorted(levels.keys()):
    nodes_at_level = levels[lvl]
    n = len(nodes_at_level)
    # Spread nodes horizontally, wider spread for lower levels
    x_positions = np.linspace(0.05, 0.95, n) if n > 1 else [0.5]
    y_pos = 0.95 - lvl * y_spacing  # Root at top
    for i, node in enumerate(nodes_at_level):
        positions[node["id"]] = (x_positions[i], y_pos)

# Define colors by level - Python Blue for CEO, Yellow for VPs
level_colors = {
    "Level 0: CEO": "#306998",
    "Level 1: VPs": "#FFD43B",
    "Level 2: Directors": "#4ECDC4",
    "Level 3: Team": "#FF6B6B",
}
level_names = {0: "Level 0: CEO", 1: "Level 1: VPs", 2: "Level 2: Directors", 3: "Level 3: Team"}

# Node sizes by level (higher = larger)
size_map = {0: 16, 1: 12, 2: 9, 3: 6}

# Create node dataframe
node_df = pd.DataFrame(
    {
        "x": [positions[node["id"]][0] for node in nodes],
        "y": [positions[node["id"]][1] for node in nodes],
        "label": [node["label"] for node in nodes],
        "level": [level_names[node["level"]] for node in nodes],
        "size": [size_map[node["level"]] for node in nodes],
    }
)

# Create edge dataframe
edge_data = []
for parent, child in edges:
    edge_data.append(
        {"x": positions[parent][0], "y": positions[parent][1], "xend": positions[child][0], "yend": positions[child][1]}
    )
edge_df = pd.DataFrame(edge_data)

# Create the plot
plot = (
    ggplot()
    # Draw edges first (underneath nodes)
    + geom_segment(
        data=edge_df, mapping=aes(x="x", y="y", xend="xend", yend="yend"), color="#555555", size=1.2, alpha=0.7
    )
    # Draw nodes colored by level
    + geom_point(data=node_df, mapping=aes(x="x", y="y", color="level", size="size"), alpha=0.95, stroke=0.5)
    # Add node labels with offset above nodes
    + geom_text(
        data=node_df, mapping=aes(x="x", y="y", label="label"), size=8, va="bottom", nudge_y=0.025, color="#222222"
    )
    + scale_color_manual(values=level_colors)
    + scale_size_identity()
    + labs(title="network-hierarchical · plotnine · pyplots.ai", color="Hierarchy Level")
    + xlim(-0.02, 1.02)
    + ylim(0.1, 1.05)
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=24, ha="center"),
        legend_title=element_text(size=18),
        legend_text=element_text(size=16),
        legend_position="bottom",
        legend_background=element_rect(fill="white", alpha=0.95),
        legend_key=element_rect(fill="white"),
        # Remove axis elements for network graph
        axis_title=element_blank(),
        axis_text=element_blank(),
        axis_ticks=element_blank(),
        panel_grid=element_blank(),
        panel_background=element_rect(fill="white"),
        plot_background=element_rect(fill="white"),
    )
)

# Save the plot
plot.save("plot.png", dpi=300)
