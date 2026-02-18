"""pyplots.ai
radar-innovation-timeline: Innovation Radar with Time-Horizon Rings
Library: altair 6.0.0 | Python 3.13
Quality: pending | Created: 2026-02-18
"""

from collections import defaultdict

import altair as alt
import numpy as np
import pandas as pd


# Data - Technology radar with 4 rings and 4 sectors
np.random.seed(42)

rings = ["Adopt", "Trial", "Assess", "Hold"]
ring_radii = {"Adopt": 1, "Trial": 2, "Assess": 3, "Hold": 4}

sectors = ["AI & ML", "Cloud & Infra", "Data Engineering", "Security"]
n_sectors = len(sectors)

# Sector angular boundaries (270-degree layout, leaving 90 degrees at bottom-left for legend)
start_angle = -np.pi / 4
total_arc = 1.5 * np.pi
sector_arc = total_arc / n_sectors

sector_boundaries = {}
for i, sector in enumerate(sectors):
    sector_boundaries[sector] = (start_angle + i * sector_arc, start_angle + (i + 1) * sector_arc)

# Innovation items
items = [
    # AI & ML
    {"name": "LLM Agents", "ring": "Adopt", "sector": "AI & ML"},
    {"name": "RAG Pipelines", "ring": "Adopt", "sector": "AI & ML"},
    {"name": "Vision Models", "ring": "Trial", "sector": "AI & ML"},
    {"name": "AI Code Review", "ring": "Trial", "sector": "AI & ML"},
    {"name": "Neuro-symbolic AI", "ring": "Assess", "sector": "AI & ML"},
    {"name": "Autonomous ML Ops", "ring": "Assess", "sector": "AI & ML"},
    {"name": "AGI Frameworks", "ring": "Hold", "sector": "AI & ML"},
    # Cloud & Infra
    {"name": "Edge Computing", "ring": "Adopt", "sector": "Cloud & Infra"},
    {"name": "Platform Eng.", "ring": "Adopt", "sector": "Cloud & Infra"},
    {"name": "WASM Backends", "ring": "Trial", "sector": "Cloud & Infra"},
    {"name": "FinOps Tools", "ring": "Trial", "sector": "Cloud & Infra"},
    {"name": "Serverless GPUs", "ring": "Assess", "sector": "Cloud & Infra"},
    {"name": "Quantum Cloud", "ring": "Hold", "sector": "Cloud & Infra"},
    # Data Engineering
    {"name": "Data Contracts", "ring": "Adopt", "sector": "Data Engineering"},
    {"name": "Lakehouse Arch.", "ring": "Trial", "sector": "Data Engineering"},
    {"name": "Streaming SQL", "ring": "Trial", "sector": "Data Engineering"},
    {"name": "Data Mesh", "ring": "Assess", "sector": "Data Engineering"},
    {"name": "Graph Analytics", "ring": "Assess", "sector": "Data Engineering"},
    {"name": "Quantum DB", "ring": "Hold", "sector": "Data Engineering"},
    # Security
    {"name": "Zero Trust", "ring": "Adopt", "sector": "Security"},
    {"name": "SBOM Tooling", "ring": "Adopt", "sector": "Security"},
    {"name": "AI Threat Detection", "ring": "Trial", "sector": "Security"},
    {"name": "Passkeys", "ring": "Trial", "sector": "Security"},
    {"name": "Confidential Compute", "ring": "Assess", "sector": "Security"},
    {"name": "Post-Quantum Crypto", "ring": "Assess", "sector": "Security"},
    {"name": "Homomorphic Enc.", "ring": "Hold", "sector": "Security"},
]

# Position each item within its sector and ring
max_radius = 4.5
ring_inner = {"Adopt": 0.3, "Trial": 1.15, "Assess": 2.15, "Hold": 3.15}
ring_outer = {"Adopt": 1.05, "Trial": 2.05, "Assess": 3.05, "Hold": 4.05}

# Group items by (sector, ring) for even angular spacing
groups = defaultdict(list)
for item in items:
    groups[(item["sector"], item["ring"])].append(item)

records = []
for (sector, ring), group_items in groups.items():
    a_min, a_max = sector_boundaries[sector]
    padding = 0.12 * sector_arc
    n_items = len(group_items)
    r_in = ring_inner[ring]
    r_out = ring_outer[ring]
    r_mid = (r_in + r_out) / 2
    for idx, item in enumerate(group_items):
        # Spread items evenly across the sector arc
        frac = (idx + 0.5) / n_items
        angle = a_min + padding + frac * (a_max - a_min - 2 * padding)
        # Alternate radial position for items in same ring to reduce overlap
        r_offset = 0.15 * ((-1) ** idx) if n_items > 1 else 0
        radius = r_mid + r_offset

        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        records.append(
            {
                "name": item["name"],
                "ring": item["ring"],
                "sector": item["sector"],
                "x": x,
                "y": y,
                "radius": radius,
                "angle": angle,
            }
        )

df = pd.DataFrame(records)

# Color palette per sector
sector_colors = {"AI & ML": "#306998", "Cloud & Infra": "#E07A2F", "Data Engineering": "#2CA02C", "Security": "#9467BD"}
color_scale = alt.Scale(domain=list(sector_colors.keys()), range=list(sector_colors.values()))

# Shape per ring
ring_shapes = {"Adopt": "circle", "Trial": "diamond", "Assess": "triangle-up", "Hold": "square"}
shape_scale = alt.Scale(domain=rings, range=[ring_shapes[r] for r in rings])

# Ring boundary arcs (concentric rings from 0 to 270 degrees)
ring_boundary_radii = [1.1, 2.1, 3.1, 4.1]
arc_points = 100
arc_records = []
for rb in ring_boundary_radii:
    theta_vals = np.linspace(start_angle, start_angle + total_arc, arc_points)
    for i, theta in enumerate(theta_vals):
        arc_records.append({"x": rb * np.cos(theta), "y": rb * np.sin(theta), "ring_boundary": rb, "order": i})

df_arcs = pd.DataFrame(arc_records)

# Ring fill bands (subtle background)
ring_fill_records = []
ring_fill_colors = {"Adopt": "#306998", "Trial": "#4A8FBF", "Assess": "#7BB5D6", "Hold": "#B0D4E8"}
fill_points = 80
for ring_name in rings:
    r_in = ring_inner[ring_name]
    r_out = ring_outer[ring_name]
    theta_vals = np.linspace(start_angle, start_angle + total_arc, fill_points)
    # Inner arc forward
    for i, theta in enumerate(theta_vals):
        ring_fill_records.append({"x": r_in * np.cos(theta), "y": r_in * np.sin(theta), "ring": ring_name, "order": i})
    # Outer arc backward
    for i, theta in enumerate(reversed(theta_vals)):
        ring_fill_records.append(
            {"x": r_out * np.cos(theta), "y": r_out * np.sin(theta), "ring": ring_name, "order": fill_points + i}
        )
    # Close
    theta_first = theta_vals[0]
    ring_fill_records.append(
        {"x": r_in * np.cos(theta_first), "y": r_in * np.sin(theta_first), "ring": ring_name, "order": 2 * fill_points}
    )

df_ring_fills = pd.DataFrame(ring_fill_records)

# Sector divider lines (spokes at sector boundaries)
spoke_records = []
for i in range(n_sectors + 1):
    angle = start_angle + i * sector_arc
    spoke_records.append({"x": 0, "y": 0, "spoke_id": i, "order": 0})
    spoke_records.append(
        {"x": (max_radius - 0.3) * np.cos(angle), "y": (max_radius - 0.3) * np.sin(angle), "spoke_id": i, "order": 1}
    )

df_spokes = pd.DataFrame(spoke_records)

# Sector labels positioned at the midpoint angle of each sector, beyond outer ring
sector_label_records = []
label_radius = 4.65
for i, sector in enumerate(sectors):
    mid_angle = start_angle + (i + 0.5) * sector_arc
    sector_label_records.append(
        {
            "x": label_radius * np.cos(mid_angle),
            "y": label_radius * np.sin(mid_angle),
            "sector": sector,
            "angle_deg": np.degrees(mid_angle),
        }
    )

df_sector_labels = pd.DataFrame(sector_label_records)

# Ring labels at the top of each ring band
ring_label_records = []
for ring_name in rings:
    r_mid = (ring_inner[ring_name] + ring_outer[ring_name]) / 2
    label_angle = start_angle + total_arc + 0.08
    ring_label_records.append({"x": r_mid * np.cos(label_angle), "y": r_mid * np.sin(label_angle), "ring": ring_name})

df_ring_labels = pd.DataFrame(ring_label_records)

# Chart dimensions
chart_size = 1200
axis_domain = [-5.5, 5.5]
x_enc = alt.X("x:Q", scale=alt.Scale(domain=axis_domain), axis=None)
y_enc = alt.Y("y:Q", scale=alt.Scale(domain=axis_domain), axis=None)

# Ring fill bands
ring_fills = []
ring_fill_opacity = {"Adopt": 0.12, "Trial": 0.08, "Assess": 0.05, "Hold": 0.03}
for ring_name in rings:
    ring_df = df_ring_fills[df_ring_fills["ring"] == ring_name]
    fill_layer = (
        alt.Chart(ring_df)
        .mark_line(
            strokeWidth=0, filled=True, fill=ring_fill_colors[ring_name], fillOpacity=ring_fill_opacity[ring_name]
        )
        .encode(x=x_enc, y=y_enc, order="order:Q")
    )
    ring_fills.append(fill_layer)

# Ring boundary arcs
ring_arcs = (
    alt.Chart(df_arcs)
    .mark_line(strokeWidth=1.5, stroke="#aaaaaa", opacity=0.5)
    .encode(x=x_enc, y=y_enc, detail="ring_boundary:N", order="order:Q")
)

# Sector divider spokes
spokes = (
    alt.Chart(df_spokes)
    .mark_line(strokeWidth=1.5, stroke="#999999", opacity=0.5)
    .encode(x=x_enc, y=y_enc, detail="spoke_id:N", order="order:Q")
)

# Data points (items)
points = (
    alt.Chart(df)
    .mark_point(filled=True, size=350, strokeWidth=1.5, stroke="white", opacity=0.9)
    .encode(
        x=x_enc,
        y=y_enc,
        color=alt.Color(
            "sector:N",
            scale=color_scale,
            legend=alt.Legend(
                title="Sector",
                titleFontSize=20,
                labelFontSize=17,
                orient="bottom-left",
                offset=5,
                symbolSize=350,
                symbolStrokeWidth=0,
                direction="vertical",
                columns=1,
            ),
        ),
        shape=alt.Shape(
            "ring:N",
            scale=shape_scale,
            legend=alt.Legend(
                title="Ring",
                titleFontSize=20,
                labelFontSize=17,
                orient="bottom-left",
                offset=5,
                symbolSize=350,
                symbolStrokeWidth=0,
                direction="vertical",
                columns=1,
            ),
        ),
        tooltip=[
            alt.Tooltip("name:N", title="Technology"),
            alt.Tooltip("sector:N", title="Sector"),
            alt.Tooltip("ring:N", title="Ring"),
        ],
    )
)

# Item labels
item_labels = (
    alt.Chart(df)
    .mark_text(fontSize=12, dy=-14, color="#222222", fontWeight="normal")
    .encode(x=x_enc, y=y_enc, text="name:N")
)

# Sector labels
sector_labels = (
    alt.Chart(df_sector_labels)
    .mark_text(fontSize=22, fontWeight="bold", color="#333333")
    .encode(x="x:Q", y="y:Q", text="sector:N")
)

# Ring labels
ring_labels = (
    alt.Chart(df_ring_labels)
    .mark_text(fontSize=16, fontWeight="bold", color="#666666", align="left")
    .encode(x="x:Q", y="y:Q", text="ring:N")
)

# Combine all layers
chart = (
    alt.layer(*ring_fills, ring_arcs, spokes, points, item_labels, sector_labels, ring_labels)
    .properties(
        width=chart_size,
        height=chart_size,
        title=alt.Title("radar-innovation-timeline · altair · pyplots.ai", fontSize=28, anchor="middle", offset=20),
    )
    .configure_view(strokeWidth=0)
    .configure_legend(strokeColor="#cccccc", padding=15)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
