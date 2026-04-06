"""pyplots.ai
chord-basic: Basic Chord Diagram
Library: altair 6.0.0 | Python 3.14
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Migration flows between continents (thousands of people, bidirectional)
flows_data = [
    {"source": "Europe", "target": "North America", "value": 45},
    {"source": "North America", "target": "Europe", "value": 30},
    {"source": "Europe", "target": "Asia", "value": 25},
    {"source": "Asia", "target": "Europe", "value": 35},
    {"source": "Asia", "target": "North America", "value": 40},
    {"source": "North America", "target": "Asia", "value": 20},
    {"source": "Africa", "target": "Europe", "value": 55},
    {"source": "Europe", "target": "Africa", "value": 15},
    {"source": "Africa", "target": "North America", "value": 25},
    {"source": "South America", "target": "North America", "value": 50},
    {"source": "North America", "target": "South America", "value": 18},
    {"source": "South America", "target": "Europe", "value": 22},
    {"source": "Oceania", "target": "Asia", "value": 30},
    {"source": "Asia", "target": "Oceania", "value": 25},
    {"source": "Oceania", "target": "Europe", "value": 12},
]

df = pd.DataFrame(flows_data)

# Canvas dimensions (1600x900 internal, 4800x2700 at scale_factor=3)
W, H = 1600, 900
CX, CY = W / 2, H / 2
R_OUTER, R_INNER, R_CHORD = 350, 320, 310

# Entity ordering and color palette (colorblind-safe, distinct hues)
entities = ["Europe", "North America", "Asia", "Africa", "South America", "Oceania"]
colors = ["#306998", "#FFD43B", "#E76F51", "#FF6B6B", "#2A9D8F", "#A86EDB"]
color_scale = alt.Scale(domain=entities, range=colors)

# Compute entity totals and arc positions
entity_totals = {e: df[df["source"] == e]["value"].sum() + df[df["target"] == e]["value"].sum() for e in entities}
total_flow = sum(entity_totals.values())
gap = 0.04
available_angle = 2 * np.pi - gap * len(entities)

entity_arcs = {}
angle = -np.pi / 2
for e in entities:
    arc_len = (entity_totals[e] / total_flow) * available_angle
    entity_arcs[e] = (angle, angle + arc_len, arc_len)
    angle += arc_len + gap

# Build outer arc polygons
N_ARC = 50
arcs_rows = []
for e in entities:
    start, end, _ = entity_arcs[e]
    angles = np.linspace(start, end, N_ARC)
    xs_outer = CX + R_OUTER * np.cos(angles)
    ys_outer = CY + R_OUTER * np.sin(angles)
    xs_inner = CX + R_INNER * np.cos(angles[::-1])
    ys_inner = CY + R_INNER * np.sin(angles[::-1])
    for i, (x, y) in enumerate(
        zip(np.concatenate([xs_outer, xs_inner]), np.concatenate([ys_outer, ys_inner]), strict=True)
    ):
        arcs_rows.append({"entity": e, "x": x, "y": y, "order": i})

arcs_df = pd.DataFrame(arcs_rows)

# Compute chord offsets within each entity arc
source_off = {}
target_off = {}
for e in entities:
    start, _, arc_len = entity_arcs[e]
    src_total = df[df["source"] == e]["value"].sum()
    frac = src_total / entity_totals[e] if entity_totals[e] > 0 else 0.5
    source_off[e] = start
    target_off[e] = start + frac * arc_len

# Identify top flows for visual emphasis (storytelling)
value_threshold = df["value"].quantile(0.7)

# Build chord polygons with bezier curves
N_BEZ = 40
chords_rows = []
for _idx, row in df.iterrows():
    src, tgt, val = row["source"], row["target"], row["value"]
    s_start, s_end, s_len = entity_arcs[src]
    t_start, t_end, t_len = entity_arcs[tgt]

    sw = (val / entity_totals[src]) * s_len if entity_totals[src] > 0 else 0
    tw = (val / entity_totals[tgt]) * t_len if entity_totals[tgt] > 0 else 0

    sa = source_off[src]
    source_off[src] = sa + sw
    ta = target_off[tgt]
    target_off[tgt] = ta + tw

    pts = []
    # Source arc
    for a in np.linspace(sa, sa + sw, 10):
        pts.append((CX + R_CHORD * np.cos(a), CY + R_CHORD * np.sin(a)))
    # Bezier: source end -> target start
    p0 = np.array([CX + R_CHORD * np.cos(sa + sw), CY + R_CHORD * np.sin(sa + sw)])
    p2 = np.array([CX + R_CHORD * np.cos(ta), CY + R_CHORD * np.sin(ta)])
    center = np.array([CX, CY])
    for i in range(N_BEZ):
        t = i / (N_BEZ - 1)
        p = (1 - t) ** 2 * p0 + 2 * (1 - t) * t * center + t**2 * p2
        pts.append((p[0], p[1]))
    # Target arc
    for a in np.linspace(ta, ta + tw, 10):
        pts.append((CX + R_CHORD * np.cos(a), CY + R_CHORD * np.sin(a)))
    # Bezier: target end -> source start
    p0 = np.array([CX + R_CHORD * np.cos(ta + tw), CY + R_CHORD * np.sin(ta + tw)])
    p2 = np.array([CX + R_CHORD * np.cos(sa), CY + R_CHORD * np.sin(sa)])
    for i in range(N_BEZ):
        t = i / (N_BEZ - 1)
        p = (1 - t) ** 2 * p0 + 2 * (1 - t) * t * center + t**2 * p2
        pts.append((p[0], p[1]))

    is_major = val >= value_threshold
    chord_id = f"{src}->{tgt}"
    for pi, (x, y) in enumerate(pts):
        chords_rows.append(
            {
                "chord_id": chord_id,
                "source": src,
                "target": tgt,
                "value": val,
                "x": x,
                "y": y,
                "order": pi,
                "major": is_major,
            }
        )

chords_df = pd.DataFrame(chords_rows)

# Labels positioned outside arcs
labels_rows = []
for e in entities:
    start, end, _ = entity_arcs[e]
    mid = (start + end) / 2
    r_label = R_OUTER + 35
    deg = np.degrees(mid)
    align = "left" if (-90 < deg < 90 or deg > 270 or deg < -270) else "right"
    labels_rows.append({"entity": e, "x": CX + r_label * np.cos(mid), "y": CY + r_label * np.sin(mid), "align": align})

labels_df = pd.DataFrame(labels_rows)

# Shared axis scales (no axes shown)
x_scale = alt.Scale(domain=[0, W])
y_scale = alt.Scale(domain=[0, H])

# Outer arc ring layer
arcs_layer = (
    alt.Chart(arcs_df)
    .mark_line(filled=True, strokeWidth=0)
    .encode(
        x=alt.X("x:Q", scale=x_scale, axis=None),
        y=alt.Y("y:Q", scale=y_scale, axis=None),
        color=alt.Color(
            "entity:N",
            scale=color_scale,
            legend=alt.Legend(
                title="Region", titleFontSize=20, labelFontSize=18, orient="right", symbolSize=250, titlePadding=8
            ),
        ),
        detail="entity:N",
        order="order:Q",
    )
)

# Major chords (dominant flows) - higher opacity for visual hierarchy
major_chords = (
    alt.Chart(chords_df[chords_df["major"]])
    .mark_line(filled=True, opacity=0.7, strokeWidth=0)
    .encode(
        x=alt.X("x:Q", scale=x_scale, axis=None),
        y=alt.Y("y:Q", scale=y_scale, axis=None),
        color=alt.Color("source:N", scale=color_scale, legend=None),
        detail="chord_id:N",
        order="order:Q",
        tooltip=[
            alt.Tooltip("source:N", title="From"),
            alt.Tooltip("target:N", title="To"),
            alt.Tooltip("value:Q", title="Flow (thousands)"),
        ],
    )
)

# Minor chords - subtle, recede into background
minor_chords = (
    alt.Chart(chords_df[~chords_df["major"]])
    .mark_line(filled=True, opacity=0.3, strokeWidth=0)
    .encode(
        x=alt.X("x:Q", scale=x_scale, axis=None),
        y=alt.Y("y:Q", scale=y_scale, axis=None),
        color=alt.Color("source:N", scale=color_scale, legend=None),
        detail="chord_id:N",
        order="order:Q",
        tooltip=[
            alt.Tooltip("source:N", title="From"),
            alt.Tooltip("target:N", title="To"),
            alt.Tooltip("value:Q", title="Flow (thousands)"),
        ],
    )
)

# Labels split by alignment for correct text anchoring
label_base = {
    "x": alt.X("x:Q", scale=x_scale),
    "y": alt.Y("y:Q", scale=y_scale),
    "text": "entity:N",
    "color": alt.Color("entity:N", scale=color_scale, legend=None),
}

labels_left = (
    alt.Chart(labels_df[labels_df["align"] == "left"])
    .mark_text(fontSize=20, fontWeight="bold", align="left")
    .encode(**label_base)
)

labels_right = (
    alt.Chart(labels_df[labels_df["align"] == "right"])
    .mark_text(fontSize=20, fontWeight="bold", align="right")
    .encode(**label_base)
)

# Compose final chart with layering: minor chords behind, major in front
chart = (
    alt.layer(minor_chords, major_chords, arcs_layer, labels_left, labels_right)
    .properties(
        width=W,
        height=H,
        title=alt.Title(
            text="chord-basic · altair · pyplots.ai",
            subtitle="Dominant migration corridors highlighted — Africa→Europe and S. America→N. America lead",
            fontSize=28,
            subtitleFontSize=16,
            subtitleColor="#666666",
            anchor="middle",
        ),
    )
    .configure_view(strokeWidth=0)
    .configure_legend(padding=12, cornerRadius=5, fillColor="#FAFAFA", strokeColor="#DDDDDD")
)

chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
