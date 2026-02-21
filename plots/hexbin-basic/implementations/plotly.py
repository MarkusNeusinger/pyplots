""" pyplots.ai
hexbin-basic: Basic Hexbin Plot
Library: plotly 6.5.2 | Python 3.14.3
Quality: 78/100 | Created: 2026-02-21
"""

import numpy as np
import plotly.graph_objects as go


# Data - generate clustered bivariate data (10,000 points)
np.random.seed(42)
n_points = 10000
centers = [(0, 0), (3, 3), (-2, 4)]
points_per_cluster = n_points // 3

x_data = []
y_data = []
for cx, cy in centers:
    x_data.extend(np.random.randn(points_per_cluster) * 1.2 + cx)
    y_data.extend(np.random.randn(points_per_cluster) * 1.2 + cy)

x = np.array(x_data)
y = np.array(y_data)

# Hexbin computation - pointy-top hexagonal tessellation
gridsize = 25
x_min, x_max = x.min() - 0.5, x.max() + 0.5
y_min, y_max = y.min() - 0.5, y.max() + 0.5

hex_size = (x_max - x_min) / gridsize / 2
hex_width = hex_size * np.sqrt(3)
hex_height = hex_size * 2
hex_horiz_spacing = hex_width
hex_vert_spacing = hex_height * 0.75

hex_bins = {}
for xi, yi in zip(x, y, strict=True):
    row = int((yi - y_min) / hex_vert_spacing)
    col_offset = (row % 2) * hex_width * 0.5
    col = int((xi - x_min - col_offset) / hex_horiz_spacing)
    hx = x_min + col * hex_horiz_spacing + col_offset + hex_width / 2
    hy = y_min + row * hex_vert_spacing + hex_height / 2
    key = (col, row)
    if key not in hex_bins:
        hex_bins[key] = {"x": hx, "y": hy, "count": 0}
    hex_bins[key]["count"] += 1

hex_centers_x = [v["x"] for v in hex_bins.values()]
hex_centers_y = [v["y"] for v in hex_bins.values()]
counts = np.array([v["count"] for v in hex_bins.values()])
max_count = counts.max()
normalized = counts / max_count

# Color mapping - viridis interpolation
viridis = [
    (0.0, (68, 1, 84)),
    (0.25, (59, 82, 139)),
    (0.5, (33, 145, 140)),
    (0.75, (94, 201, 98)),
    (1.0, (253, 231, 37)),
]

colors = []
for val in normalized:
    for i in range(len(viridis) - 1):
        v1, c1 = viridis[i]
        v2, c2 = viridis[i + 1]
        if v1 <= val <= v2:
            t = (val - v1) / (v2 - v1)
            r = int(c1[0] + t * (c2[0] - c1[0]))
            g = int(c1[1] + t * (c2[1] - c1[1]))
            b = int(c1[2] + t * (c2[2] - c1[2]))
            colors.append(f"rgb({r},{g},{b})")
            break

# Build hexagon shapes
angles = np.array([30, 90, 150, 210, 270, 330, 390]) * np.pi / 180
cos_a = np.cos(angles)
sin_a = np.sin(angles)
pad = hex_size * 1.02

shapes = []
for hx, hy, color in zip(hex_centers_x, hex_centers_y, colors, strict=True):
    vx = hx + pad * cos_a
    vy = hy + pad * sin_a
    path = f"M {vx[0]},{vy[0]}"
    for j in range(1, len(vx)):
        path += f" L {vx[j]},{vy[j]}"
    path += " Z"
    shapes.append({"type": "path", "path": path, "fillcolor": color, "line": {"width": 0.5, "color": color}})

# Plot
fig = go.Figure()

# Invisible scatter for hover info
fig.add_trace(
    go.Scatter(
        x=hex_centers_x,
        y=hex_centers_y,
        mode="markers",
        marker={"size": 1, "opacity": 0},
        text=[f"Count: {c}" for c in counts],
        hoverinfo="text",
        showlegend=False,
    )
)

# Colorbar via dummy trace
fig.add_trace(
    go.Scatter(
        x=[None],
        y=[None],
        mode="markers",
        marker={
            "colorscale": "Viridis",
            "cmin": 0,
            "cmax": int(max_count),
            "colorbar": {
                "title": {"text": "Count", "font": {"size": 22}},
                "tickfont": {"size": 18},
                "thickness": 25,
                "len": 0.8,
            },
            "showscale": True,
        },
        hoverinfo="skip",
        showlegend=False,
    )
)

# Style
fig.update_layout(
    title={"text": "hexbin-basic · plotly · pyplots.ai", "font": {"size": 32}, "x": 0.5, "xanchor": "center"},
    xaxis={
        "title": {"text": "X Value", "font": {"size": 24}},
        "tickfont": {"size": 18},
        "gridcolor": "rgba(128,128,128,0.2)",
        "zeroline": False,
    },
    yaxis={
        "title": {"text": "Y Value", "font": {"size": 24}},
        "tickfont": {"size": 18},
        "gridcolor": "rgba(128,128,128,0.2)",
        "zeroline": False,
        "scaleanchor": "x",
        "scaleratio": 1,
    },
    template="plotly_white",
    margin={"l": 100, "r": 140, "t": 100, "b": 100},
    shapes=shapes,
)

# Save
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs=True, full_html=True)
