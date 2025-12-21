""" pyplots.ai
hexbin-basic: Basic Hexbin Plot
Library: plotly 6.5.0 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-14
"""

import numpy as np
import plotly.graph_objects as go


# Data - generate clustered bivariate data (10,000 points)
np.random.seed(42)
n_points = 10000

# Create clustered distribution with 3 centers
centers = [(0, 0), (3, 3), (-2, 4)]
points_per_cluster = n_points // 3

x_data = []
y_data = []

for cx, cy in centers:
    x_data.extend(np.random.randn(points_per_cluster) * 1.2 + cx)
    y_data.extend(np.random.randn(points_per_cluster) * 1.2 + cy)

x = np.array(x_data)
y = np.array(y_data)

# Hexbin parameters
gridsize = 25
x_min, x_max = x.min() - 0.5, x.max() + 0.5
y_min, y_max = y.min() - 0.5, y.max() + 0.5

# Hexagon geometry: pointy-top orientation for proper tessellation
hex_size = (x_max - x_min) / gridsize / 2  # radius
hex_width = hex_size * np.sqrt(3)
hex_height = hex_size * 2
hex_horiz_spacing = hex_width
hex_vert_spacing = hex_height * 0.75

# Compute hexagonal bin centers and counts
hex_bins = {}
for xi, yi in zip(x, y, strict=True):
    # Convert to hex grid coordinates (offset coordinates)
    row = int((yi - y_min) / hex_vert_spacing)
    col_offset = (row % 2) * hex_width * 0.5
    col = int((xi - x_min - col_offset) / hex_horiz_spacing)

    # Snap to hex center
    hx = x_min + col * hex_horiz_spacing + col_offset + hex_width / 2
    hy = y_min + row * hex_vert_spacing + hex_height / 2

    key = (col, row)
    if key not in hex_bins:
        hex_bins[key] = {"x": hx, "y": hy, "count": 0}
    hex_bins[key]["count"] += 1

# Extract bin data
hex_centers_x = [v["x"] for v in hex_bins.values()]
hex_centers_y = [v["y"] for v in hex_bins.values()]
counts = np.array([v["count"] for v in hex_bins.values()])

# Normalize counts for color mapping
max_count = counts.max()
normalized_counts = counts / max_count

# Viridis colorscale values (sampled at key points)
viridis_colors = [(0.0, "#440154"), (0.25, "#3b528b"), (0.5, "#21918c"), (0.75, "#5ec962"), (1.0, "#fde725")]


def get_viridis_color(val):
    """Interpolate viridis color for value between 0 and 1."""
    for i in range(len(viridis_colors) - 1):
        v1, c1 = viridis_colors[i]
        v2, c2 = viridis_colors[i + 1]
        if v1 <= val <= v2:
            t = (val - v1) / (v2 - v1)
            r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
            r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
            r = int(r1 + t * (r2 - r1))
            g = int(g1 + t * (g2 - g1))
            b = int(b1 + t * (b2 - b1))
            return f"rgb({r}, {g}, {b})"
    return viridis_colors[-1][1]


def hexagon_vertices(cx, cy, size):
    """Generate vertices for a pointy-top hexagon centered at (cx, cy)."""
    angles = np.array([30, 90, 150, 210, 270, 330, 390]) * np.pi / 180
    vx = cx + size * np.cos(angles)
    vy = cy + size * np.sin(angles)
    return vx, vy


# Create figure
fig = go.Figure()

# Add hexagons as shapes
shapes = []
for hx, hy, norm_count in zip(hex_centers_x, hex_centers_y, normalized_counts, strict=True):
    vx, vy = hexagon_vertices(hx, hy, hex_size * 1.02)  # Slight overlap to avoid gaps
    color = get_viridis_color(norm_count)

    # Build SVG path for hexagon
    path = f"M {vx[0]},{vy[0]}"
    for j in range(1, len(vx)):
        path += f" L {vx[j]},{vy[j]}"
    path += " Z"

    shapes.append(
        {
            "type": "path",
            "path": path,
            "fillcolor": color,
            "line": {"width": 0.5, "color": color},  # Match line to fill to eliminate gaps
        }
    )

# Add invisible scatter for hover functionality
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

# Add a dummy scatter for colorbar
fig.add_trace(
    go.Scatter(
        x=[None],
        y=[None],
        mode="markers",
        marker={
            "colorscale": "Viridis",
            "cmin": 0,
            "cmax": max_count,
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

# Layout
fig.update_layout(
    title={"text": "hexbin-basic · plotly · pyplots.ai", "font": {"size": 32}, "x": 0.5, "xanchor": "center"},
    xaxis={
        "title": {"text": "X Value", "font": {"size": 24}},
        "tickfont": {"size": 18},
        "gridcolor": "rgba(128, 128, 128, 0.2)",
        "gridwidth": 1,
        "zeroline": False,
    },
    yaxis={
        "title": {"text": "Y Value", "font": {"size": 24}},
        "tickfont": {"size": 18},
        "gridcolor": "rgba(128, 128, 128, 0.2)",
        "gridwidth": 1,
        "zeroline": False,
        "scaleanchor": "x",
        "scaleratio": 1,
    },
    template="plotly_white",
    margin={"l": 100, "r": 140, "t": 100, "b": 100},
    shapes=shapes,
)

# Save as PNG (4800x2700 px)
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save interactive HTML
fig.write_html("plot.html", include_plotlyjs=True, full_html=True)
