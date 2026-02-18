""" pyplots.ai
radar-innovation-timeline: Innovation Radar with Time-Horizon Rings
Library: plotnine 0.15.3 | Python 3.14.3
Quality: 81/100 | Created: 2026-02-18
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
    geom_polygon,
    geom_segment,
    geom_text,
    ggplot,
    guide_legend,
    guides,
    labs,
    scale_alpha_manual,
    scale_color_manual,
    scale_fill_identity,
    scale_size_manual,
    scale_x_continuous,
    scale_y_continuous,
    theme,
)


np.random.seed(42)

# === Three-quarter circle layout (270 deg), open at bottom ===
rings = ["Adopt", "Trial", "Assess", "Hold"]
ring_inner = [0.75, 2.25, 3.75, 5.25]
ring_outer = [2.25, 3.75, 5.25, 6.75]
ring_mid = [1.5, 3.0, 4.5, 6.0]
ring_fills_c = ["#C8E6C9", "#FFF9C4", "#FFE0B2", "#FFCDD2"]
ring_sizes = {"Adopt": 7, "Trial": 5.5, "Assess": 4.5, "Hold": 3.5}
ring_alphas = {"Adopt": 1.0, "Trial": 0.85, "Assess": 0.7, "Hold": 0.55}

sectors = ["AI & ML", "Cloud & Infra", "Data Engineering", "Security"]
sector_colors = {"AI & ML": "#306998", "Cloud & Infra": "#27833A", "Data Engineering": "#D2691E", "Security": "#7B4DAA"}

total_arc = 1.5 * math.pi  # 270 degrees
arc_start = -math.pi / 4  # Start at -45 deg (lower-right)
sector_span = total_arc / len(sectors)  # 67.5 deg each
sector_starts = {s: arc_start + i * sector_span for i, s in enumerate(sectors)}

# === Innovation data ===
innovations = [
    ("LLM Agents", "AI & ML", "Adopt", 0.25),
    ("RAG Pipelines", "AI & ML", "Adopt", 0.85),
    ("Vision Transformers", "AI & ML", "Trial", 0.15),
    ("Federated Learning", "AI & ML", "Trial", 0.6),
    ("Neural Arch. Search", "AI & ML", "Assess", 0.55),
    ("Neuromorphic Comp.", "AI & ML", "Hold", 0.25),
    ("Quantum ML", "AI & ML", "Hold", 0.8),
    ("Kubernetes", "Cloud & Infra", "Adopt", 0.5),
    ("WebAssembly", "Cloud & Infra", "Trial", 0.65),
    ("FinOps Platforms", "Cloud & Infra", "Trial", 0.2),
    ("Edge Computing", "Cloud & Infra", "Assess", 0.55),
    ("Serverless Cont.", "Cloud & Infra", "Assess", 0.2),
    ("Confidential Comp.", "Cloud & Infra", "Hold", 0.5),
    ("dbt", "Data Engineering", "Adopt", 0.3),
    ("Apache Iceberg", "Data Engineering", "Adopt", 0.8),
    ("RT Feature Stores", "Data Engineering", "Trial", 0.25),
    ("Data Mesh", "Data Engineering", "Trial", 0.7),
    ("Lakehouse Arch.", "Data Engineering", "Assess", 0.3),
    ("Data Contracts", "Data Engineering", "Assess", 0.75),
    ("Semantic Layer", "Data Engineering", "Hold", 0.5),
    ("Zero Trust", "Security", "Adopt", 0.5),
    ("SBOM Tooling", "Security", "Trial", 0.25),
    ("AI Threat Detection", "Security", "Trial", 0.75),
    ("Post-Quantum Crypto", "Security", "Assess", 0.45),
    ("Homomorphic Enc.", "Security", "Hold", 0.3),
    ("Deception Tech.", "Security", "Hold", 0.75),
]

# === Compute positions ===
ring_idx = {r: i for i, r in enumerate(rings)}
rows = []
for name, sector, ring, frac in innovations:
    ri = ring_idx[ring]
    base = sector_starts[sector]
    pad = sector_span * 0.15
    angle = base + pad + frac * (sector_span - 2 * pad)
    jitter = np.random.uniform(-0.2, 0.2)
    r = ring_mid[ri] + jitter
    rows.append(
        {
            "name": name,
            "sector": sector,
            "ring": ring,
            "angle": angle,
            "radius": r,
            "x": r * math.cos(angle),
            "y": r * math.sin(angle),
        }
    )

df = pd.DataFrame(rows)
df["ring"] = pd.Categorical(df["ring"], categories=rings, ordered=True)

# === Ring fill polygons (annular wedges) ===
n_arc = 150
arc_angles = np.linspace(arc_start, arc_start + total_arc, n_arc)
fill_rows = []
for i, rname in enumerate(rings):
    r_in, r_out = ring_inner[i], ring_outer[i]
    for a in arc_angles:
        fill_rows.append({"x": r_out * math.cos(a), "y": r_out * math.sin(a), "ring_g": rname, "fc": ring_fills_c[i]})
    for a in reversed(arc_angles):
        fill_rows.append({"x": r_in * math.cos(a), "y": r_in * math.sin(a), "ring_g": rname, "fc": ring_fills_c[i]})

fill_df = pd.DataFrame(fill_rows)

# === Ring boundary arcs ===
boundaries = [0.75, 2.25, 3.75, 5.25, 6.75]
circ_rows = []
for rb in boundaries:
    for a in arc_angles:
        circ_rows.append({"x": rb * math.cos(a), "y": rb * math.sin(a), "r": rb})

circ_df = pd.DataFrame(circ_rows)

# === Sector spokes ===
spoke_rows = []
for i in range(len(sectors) + 1):
    a = arc_start + i * sector_span
    spoke_rows.append(
        {"x1": 0.75 * math.cos(a), "y1": 0.75 * math.sin(a), "x2": 6.75 * math.cos(a), "y2": 6.75 * math.sin(a)}
    )

spoke_df = pd.DataFrame(spoke_rows)

# === Sector header labels ===
slbl_rows = []
for s in sectors:
    mid = sector_starts[s] + sector_span / 2
    r = 7.5
    slbl_rows.append({"label": s, "x": r * math.cos(mid), "y": r * math.sin(mid)})

slbl_df = pd.DataFrame(slbl_rows)

# === Ring name labels (centered in gap, at 270 deg = straight down) ===
rlbl_rows = []
rlbl_angle = 3 * math.pi / 2  # 270 deg, center of the open gap
for i, rname in enumerate(rings):
    r = ring_mid[i]
    rlbl_rows.append({"label": rname, "x": r * math.cos(rlbl_angle), "y": r * math.sin(rlbl_angle)})

rlbl_df = pd.DataFrame(rlbl_rows)

# === Innovation labels (split by x position for alignment) ===
lbl_l, lbl_r = [], []
for _, row in df.iterrows():
    off = 0.55
    lx = (row["radius"] + off) * math.cos(row["angle"])
    ly = (row["radius"] + off) * math.sin(row["angle"])
    entry = {"name": row["name"], "x": lx, "y": ly, "sector": row["sector"]}
    (lbl_l if lx >= 0 else lbl_r).append(entry)

lbl_l_df = pd.DataFrame(lbl_l)
lbl_r_df = pd.DataFrame(lbl_r)


# === Build plot ===
plot = (
    ggplot()
    # Ring background fills
    + geom_polygon(aes(x="x", y="y", group="ring_g", fill="fc"), data=fill_df, size=0, alpha=0.6)
    + scale_fill_identity()
    # Ring boundary arcs
    + geom_path(aes(x="x", y="y", group="r"), data=circ_df, color="#B0B0B0", size=0.5)
    # Sector divider spokes
    + geom_segment(aes(x="x1", y="y1", xend="x2", yend="y2"), data=spoke_df, color="#B0B0B0", size=0.5)
    # Innovation points with size + alpha by ring (visual hierarchy)
    + geom_point(aes(x="x", y="y", color="sector", size="ring", alpha="ring"), data=df)
    + scale_size_manual(values=ring_sizes)
    + scale_alpha_manual(values=ring_alphas)
    # Innovation labels (left-aligned for right side)
    + geom_text(
        aes(x="x", y="y", label="name", color="sector"),
        data=lbl_l_df,
        size=8,
        ha="left",
        va="center",
        show_legend=False,
    )
    # Innovation labels (right-aligned for left side)
    + geom_text(
        aes(x="x", y="y", label="name", color="sector"),
        data=lbl_r_df,
        size=8,
        ha="right",
        va="center",
        show_legend=False,
    )
    # Sector headers
    + geom_text(aes(x="x", y="y", label="label"), data=slbl_df, size=13, fontweight="bold", color="#222222")
    # Ring labels (prominent, along gap edge)
    + geom_text(
        aes(x="x", y="y", label="label"), data=rlbl_df, size=10, fontweight="bold", color="#555555", ha="center"
    )
    # Scales
    + scale_color_manual(values=sector_colors, name="Category")
    + guides(color=guide_legend(override_aes={"size": 5}), size=False, alpha=False)
    + coord_fixed(ratio=1)
    + scale_x_continuous(limits=(-10.5, 10.5))
    + scale_y_continuous(limits=(-8, 8.5))
    + labs(
        title="radar-innovation-timeline \u00b7 plotnine \u00b7 pyplots.ai",
        subtitle="Inner rings \u2192 near-term adoption  \u00b7  Outer rings \u2192 future exploration",
    )
    + theme(
        figure_size=(12, 12),
        plot_title=element_text(size=24, ha="center", weight="bold"),
        plot_subtitle=element_text(size=13, ha="center", color="#666666", style="italic"),
        legend_title=element_text(size=16),
        legend_text=element_text(size=14),
        legend_position=(0.78, 0.08),
        legend_background=element_rect(fill="white", color="#CCCCCC"),
        legend_key=element_rect(fill="white"),
        axis_title=element_blank(),
        axis_text=element_blank(),
        axis_ticks=element_blank(),
        axis_line=element_blank(),
        panel_grid_major=element_blank(),
        panel_grid_minor=element_blank(),
        panel_background=element_rect(fill="white", color="white"),
        plot_background=element_rect(fill="white", color="white"),
    )
)

# Save
plot.save("plot.png", dpi=300)
