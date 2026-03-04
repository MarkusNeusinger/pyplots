""" pyplots.ai
scatter-complex-plane: Complex Plane Visualization (Argand Diagram)
Library: altair 6.0.0 | Python 3.14.3
Quality: 86/100 | Created: 2026-03-04
"""

import altair as alt
import numpy as np
import pandas as pd


# Data
np.random.seed(42)

# 3rd roots of unity
n_roots = 3
roots_of_unity = [np.exp(2j * np.pi * k / n_roots) for k in range(n_roots)]

# Additional complex numbers spread across all quadrants
arbitrary_points = [2.5 + 1.5j, -1.8 + 2.2j, 1.0 - 2.0j, -0.5 - 1.5j, 2.0 + 0.5j]

# Complex multiplication example: rotate and scale
z_original = 1.5 + 0.8j
z_rotated = z_original * np.exp(1j * np.pi / 4)  # rotate 45 degrees

# Build point data inline (no helper functions for KISS)
all_points = []

for k, z in enumerate(roots_of_unity):
    r, i = round(z.real, 2), round(z.imag, 2)
    rect = f"{r}+{i}i" if i >= 0 else f"{r}{i}i"
    all_points.append(
        {"real": z.real, "imaginary": z.imag, "label": f"ω{k}", "rect_form": rect, "category": "Roots of Unity"}
    )

labels_arb = ["z₁", "z₂", "z₃", "z₄", "z₅"]
for lbl, z in zip(labels_arb, arbitrary_points, strict=True):
    r, i = round(z.real, 1), round(z.imag, 1)
    rect = f"{r}+{i}i" if i >= 0 else f"{r}{i}i"
    all_points.append({"real": z.real, "imaginary": z.imag, "label": lbl, "rect_form": rect, "category": "Arbitrary"})

for lbl, z, dec in [("z", z_original, 1), ("z·e^(iπ/4)", z_rotated, 2)]:
    r, i = round(z.real, dec), round(z.imag, dec)
    rect = f"{r}+{i}i" if i >= 0 else f"{r}{i}i"
    all_points.append(
        {"real": z.real, "imaginary": z.imag, "label": lbl, "rect_form": rect, "category": "Transformation"}
    )

df = pd.DataFrame(all_points)
df["annotation_text"] = df["label"] + " = " + df["rect_form"]

# Compute label positions in data coordinates to avoid overlap with vectors
# Axis range is 5.6 data units across 1200px; offset ~0.2 data units ≈ 43px
label_x = []
label_y = []
label_align = []
for _, row in df.iterrows():
    rx, iy = row["real"], row["imaginary"]
    if rx >= 0 and iy >= 0:  # Q1: push right and up
        label_x.append(rx + 0.12)
        label_y.append(iy + 0.18)
        label_align.append("left")
    elif rx < 0 and iy >= 0:  # Q2: push left and up
        label_x.append(rx - 0.12)
        label_y.append(iy + 0.18)
        label_align.append("right")
    elif rx < 0 and iy < 0:  # Q3: push left and down
        label_x.append(rx - 0.12)
        label_y.append(iy - 0.22)
        label_align.append("right")
    else:  # Q4: push right and down
        label_x.append(rx + 0.12)
        label_y.append(iy - 0.22)
        label_align.append("left")
df["label_x"] = label_x
df["label_y"] = label_y
df["label_align"] = label_align

# Unit circle data (parametric)
theta = np.linspace(0, 2 * np.pi, 200)
circle_df = pd.DataFrame({"x": np.cos(theta), "y": np.sin(theta), "order": range(len(theta))})

# Vector line segments (origin to each point)
arrow_data = []
for _, row in df.iterrows():
    arrow_data.append({"x": 0, "y": 0, "group": row["label"], "order": 0, "category": row["category"]})
    arrow_data.append(
        {"x": row["real"], "y": row["imaginary"], "group": row["label"], "order": 1, "category": row["category"]}
    )
arrow_df = pd.DataFrame(arrow_data)

# Arrowhead data: triangle markers near vector tips, offset slightly back so they
# remain visible beneath scatter points
arrowhead_data = []
head_offset = 0.08  # data units back along vector from the point
for _, row in df.iterrows():
    rx, iy = row["real"], row["imaginary"]
    mag = np.sqrt(rx**2 + iy**2)
    # Position arrowhead slightly before the endpoint
    if mag > 0:
        hx = rx - head_offset * rx / mag
        hy = iy - head_offset * iy / mag
    else:
        hx, hy = rx, iy
    # Vega-Lite angle: degrees clockwise from north
    math_angle = np.arctan2(iy, rx)
    vega_angle = 90 - np.degrees(math_angle)
    arrowhead_data.append({"x": hx, "y": hy, "angle": vega_angle, "category": row["category"]})
arrowhead_df = pd.DataFrame(arrowhead_data)

# Axis range
axis_limit = 2.8

# Axis lines through origin
axis_line_data = pd.DataFrame(
    {
        "x": [-axis_limit, axis_limit, 0, 0],
        "y": [0, 0, -axis_limit, axis_limit],
        "axis": ["real", "real", "imag", "imag"],
        "order": [0, 1, 0, 1],
    }
)

# Color palette
category_colors = ["#306998", "#E8822A", "#6A5ACD"]
category_domain = ["Roots of Unity", "Arbitrary", "Transformation"]
color_scale = alt.Scale(domain=category_domain, range=category_colors)

# --- Layers ---

# Axis lines
axes = (
    alt.Chart(axis_line_data)
    .mark_line(color="#888888", strokeWidth=1.5, opacity=0.6)
    .encode(x=alt.X("x:Q", axis=None), y=alt.Y("y:Q", axis=None), detail="axis:N", order="order:O")
)

# Unit circle (dashed)
unit_circle = (
    alt.Chart(circle_df)
    .mark_line(color="#999999", strokeWidth=2, strokeDash=[8, 6], opacity=0.6)
    .encode(x="x:Q", y="y:Q", order="order:O")
)

# Vector lines from origin
vectors = (
    alt.Chart(arrow_df)
    .mark_line(strokeWidth=2, opacity=0.7)
    .encode(
        x="x:Q",
        y="y:Q",
        detail="group:N",
        order="order:O",
        color=alt.Color("category:N", scale=color_scale, legend=None),
    )
)

# Arrowheads (triangle markers at vector tips, rotated to point outward)
arrowheads = (
    alt.Chart(arrowhead_df)
    .mark_point(shape="triangle-up", filled=True, size=250, opacity=0.9)
    .encode(x="x:Q", y="y:Q", angle=alt.Angle("angle:Q"), color=alt.Color("category:N", scale=color_scale, legend=None))
)

# Scatter points
points = (
    alt.Chart(df)
    .mark_point(filled=True, size=200, stroke="white", strokeWidth=1.5, opacity=0.9)
    .encode(
        x=alt.X(
            "real:Q",
            title="Real",
            scale=alt.Scale(domain=[-axis_limit, axis_limit]),
            axis=alt.Axis(
                tickCount=13,
                labelFontSize=16,
                titleFontSize=20,
                gridDash=[3, 3],
                gridOpacity=0.15,
                titleColor="#333333",
                labelColor="#555555",
            ),
        ),
        y=alt.Y(
            "imaginary:Q",
            title="Imaginary",
            scale=alt.Scale(domain=[-axis_limit, axis_limit]),
            axis=alt.Axis(
                tickCount=13,
                labelFontSize=16,
                titleFontSize=20,
                gridDash=[3, 3],
                gridOpacity=0.15,
                titleColor="#333333",
                labelColor="#555555",
            ),
        ),
        color=alt.Color(
            "category:N",
            scale=color_scale,
            legend=alt.Legend(
                title="Category",
                titleFontSize=18,
                labelFontSize=16,
                symbolType="circle",
                symbolSize=200,
                symbolStrokeWidth=0,
            ),
        ),
        tooltip=[
            alt.Tooltip("label:N", title="Label"),
            alt.Tooltip("rect_form:N", title="Value (a+bi)"),
            alt.Tooltip("category:N", title="Category"),
        ],
    )
)

# Point annotations at computed positions to avoid overlap with vectors
annotations = (
    alt.Chart(df)
    .mark_text(fontSize=15, fontWeight="bold", color="#333333")
    .encode(x="label_x:Q", y="label_y:Q", text="annotation_text:N")
)

# Axis endpoint labels (Re, Im)
axis_labels_df = pd.DataFrame({"x": [axis_limit - 0.15, 0.2], "y": [-0.2, axis_limit - 0.1], "text": ["Re", "Im"]})
axis_labels = (
    alt.Chart(axis_labels_df)
    .mark_text(fontSize=18, fontStyle="italic", fontWeight="bold", color="#666666")
    .encode(x="x:Q", y="y:Q", text="text:N")
)

# Compose all layers
chart = (
    alt.layer(axes, unit_circle, vectors, arrowheads, points, annotations, axis_labels)
    .properties(
        width=1200,
        height=1200,
        title=alt.Title(
            "scatter-complex-plane · altair · pyplots.ai",
            fontSize=28,
            anchor="middle",
            color="#222222",
            subtitle="Roots of unity, arbitrary points, and rotation in the complex plane",
            subtitleFontSize=16,
            subtitleColor="#777777",
        ),
    )
    .resolve_scale(color="independent")
    .configure_axis(titlePadding=12)
    .configure_view(strokeWidth=0)
    .interactive()
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
