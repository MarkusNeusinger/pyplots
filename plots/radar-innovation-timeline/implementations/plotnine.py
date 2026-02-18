""" pyplots.ai
radar-innovation-timeline: Innovation Radar with Time-Horizon Rings
Library: plotnine 0.15.3 | Python 3.14.3
Quality: 69/100 | Created: 2026-02-18
"""

import math

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    coord_fixed,
    element_blank,
    element_rect,
    element_text,
    geom_path,
    geom_point,
    geom_segment,
    geom_text,
    ggplot,
    labs,
    scale_color_manual,
    scale_x_continuous,
    scale_y_continuous,
    theme,
)


# Data - Technology innovation radar with 4 rings and 4 sectors
np.random.seed(42)

rings = ["Adopt", "Trial", "Assess", "Hold"]
ring_radii = {"Adopt": 1.5, "Trial": 3.0, "Assess": 4.5, "Hold": 6.0}

sectors = ["AI & ML", "Cloud & Infra", "Data Engineering", "Security"]
n_sectors = len(sectors)
sector_span = 2 * math.pi / n_sectors
sector_starts = {s: i * sector_span for i, s in enumerate(sectors)}

sector_colors = {"AI & ML": "#306998", "Cloud & Infra": "#2CA02C", "Data Engineering": "#E77C2A", "Security": "#9467BD"}

innovations = [
    # AI & ML
    ("LLM Agents", "AI & ML", "Adopt", 0.15),
    ("RAG Pipelines", "AI & ML", "Adopt", 0.65),
    ("Vision Transformers", "AI & ML", "Trial", 0.25),
    ("Federated Learning", "AI & ML", "Trial", 0.75),
    ("Neural Arch. Search", "AI & ML", "Assess", 0.4),
    ("Neuromorphic Comp.", "AI & ML", "Hold", 0.25),
    ("Quantum ML", "AI & ML", "Hold", 0.75),
    # Cloud & Infra
    ("Kubernetes", "Cloud & Infra", "Adopt", 0.35),
    ("WebAssembly", "Cloud & Infra", "Trial", 0.55),
    ("FinOps Platforms", "Cloud & Infra", "Trial", 0.2),
    ("Edge Computing", "Cloud & Infra", "Assess", 0.55),
    ("Serverless Cont.", "Cloud & Infra", "Assess", 0.2),
    ("Confidential Comp.", "Cloud & Infra", "Hold", 0.5),
    # Data Engineering
    ("dbt", "Data Engineering", "Adopt", 0.35),
    ("Apache Iceberg", "Data Engineering", "Adopt", 0.7),
    ("RT Feature Stores", "Data Engineering", "Trial", 0.35),
    ("Data Mesh", "Data Engineering", "Trial", 0.75),
    ("Lakehouse Arch.", "Data Engineering", "Assess", 0.3),
    ("Data Contracts", "Data Engineering", "Assess", 0.7),
    ("Semantic Layer", "Data Engineering", "Hold", 0.45),
    # Security
    ("Zero Trust", "Security", "Adopt", 0.5),
    ("SBOM Tooling", "Security", "Trial", 0.3),
    ("AI Threat Detection", "Security", "Trial", 0.7),
    ("Post-Quantum Crypto", "Security", "Assess", 0.5),
    ("Homomorphic Enc.", "Security", "Hold", 0.3),
    ("Deception Tech.", "Security", "Hold", 0.7),
]

# Build dataframe with angular + radial positions
rows = []
for name, sector, ring, frac in innovations:
    base_angle = sector_starts[sector]
    padding = sector_span * 0.1
    angle = base_angle + padding + frac * (sector_span - 2 * padding)
    jitter = np.random.uniform(-0.25, 0.25)
    radius = ring_radii[ring] + jitter
    x = radius * math.cos(angle - math.pi / 2)
    y = radius * math.sin(angle - math.pi / 2)
    rows.append({"name": name, "sector": sector, "ring": ring, "angle": angle, "radius": radius, "x": x, "y": y})

df = pd.DataFrame(rows)

# Ring boundary circles
ring_boundaries = [0.75, 2.25, 3.75, 5.25, 6.75]
circle_angles = np.linspace(0, 2 * math.pi, 201)
circle_rows = []
for rb in ring_boundaries:
    for ca in circle_angles:
        circle_rows.append({"x": rb * math.cos(ca - math.pi / 2), "y": rb * math.sin(ca - math.pi / 2), "radius": rb})

circle_df = pd.DataFrame(circle_rows)

# Sector divider spokes
spoke_rows = []
max_r = 6.9
for i in range(n_sectors):
    angle = i * sector_span
    spoke_rows.append(
        {
            "x1": 0.75 * math.cos(angle - math.pi / 2),
            "y1": 0.75 * math.sin(angle - math.pi / 2),
            "x2": max_r * math.cos(angle - math.pi / 2),
            "y2": max_r * math.sin(angle - math.pi / 2),
        }
    )

spoke_df = pd.DataFrame(spoke_rows)

# Sector header labels at outer edge
sector_label_rows = []
label_r = 7.5
for sector_name in sectors:
    mid_angle = sector_starts[sector_name] + sector_span / 2
    sector_label_rows.append(
        {
            "label": sector_name,
            "x": label_r * math.cos(mid_angle - math.pi / 2),
            "y": label_r * math.sin(mid_angle - math.pi / 2),
        }
    )

sector_label_df = pd.DataFrame(sector_label_rows)

# Ring name labels (positioned between Security and AI & ML sectors)
ring_label_rows = []
label_angle = sector_starts["Security"] + sector_span * 0.95
for ring_name in rings:
    r = ring_radii[ring_name]
    ring_label_rows.append(
        {"label": ring_name, "x": r * math.cos(label_angle - math.pi / 2), "y": r * math.sin(label_angle - math.pi / 2)}
    )

ring_label_df = pd.DataFrame(ring_label_rows)

# Innovation labels - split into left/right aligned groups
label_left_rows = []
label_right_rows = []
for _, row in df.iterrows():
    offset_r = 0.45
    lx = (row["radius"] + offset_r) * math.cos(row["angle"] - math.pi / 2)
    ly = (row["radius"] + offset_r) * math.sin(row["angle"] - math.pi / 2)
    entry = {"name": row["name"], "x": lx, "y": ly, "sector": row["sector"]}
    if lx >= 0:
        label_left_rows.append(entry)
    else:
        label_right_rows.append(entry)

label_left_df = pd.DataFrame(label_left_rows)
label_right_df = pd.DataFrame(label_right_rows)

# Plot
plot = (
    ggplot()
    # Ring boundary circles
    + geom_path(aes(x="x", y="y", group="radius"), data=circle_df, color="#CCCCCC", size=0.3, alpha=0.6)
    # Sector dividers
    + geom_segment(aes(x="x1", y="y1", xend="x2", yend="y2"), data=spoke_df, color="#CCCCCC", size=0.3, alpha=0.6)
    # Innovation points colored by sector
    + geom_point(aes(x="x", y="y", color="sector"), data=df, size=4.5, alpha=0.9)
    # Innovation labels (left-aligned for right side)
    + geom_text(
        aes(x="x", y="y", label="name", color="sector"), data=label_left_df, size=6.5, ha="left", show_legend=False
    )
    # Innovation labels (right-aligned for left side)
    + geom_text(
        aes(x="x", y="y", label="name", color="sector"), data=label_right_df, size=6.5, ha="right", show_legend=False
    )
    # Sector header labels
    + geom_text(aes(x="x", y="y", label="label"), data=sector_label_df, size=11, fontweight="bold", color="#333333")
    # Ring name labels
    + geom_text(
        aes(x="x", y="y", label="label"), data=ring_label_df, size=8, color="#888888", fontstyle="italic", ha="left"
    )
    # Colors by sector
    + scale_color_manual(values=sector_colors, name="Category")
    + coord_fixed(ratio=1)
    + scale_x_continuous(limits=(-9.5, 9.5))
    + scale_y_continuous(limits=(-9.5, 9.5))
    + labs(title="radar-innovation-timeline \u00b7 plotnine \u00b7 pyplots.ai")
    + theme(
        figure_size=(12, 12),
        plot_title=element_text(size=24, ha="center"),
        legend_title=element_text(size=16),
        legend_text=element_text(size=14),
        legend_position="right",
        axis_title=element_blank(),
        axis_text=element_blank(),
        axis_ticks=element_blank(),
        axis_line=element_blank(),
        panel_grid_major=element_blank(),
        panel_grid_minor=element_blank(),
        panel_background=element_rect(fill="white"),
        plot_background=element_rect(fill="white"),
    )
)

# Save
plot.save("plot.png", dpi=300)
