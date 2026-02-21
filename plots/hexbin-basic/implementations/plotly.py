""" pyplots.ai
hexbin-basic: Basic Hexbin Plot
Library: plotly 6.5.2 | Python 3.14.3
Quality: 85/100 | Created: 2026-02-21
"""

import numpy as np
import plotly.graph_objects as go


# Data - ride-share pickup density across a metro area
np.random.seed(42)
n_points = 10000

# Three pickup hotspots with different densities and spreads
# Downtown (dense hub), Airport (tight cluster), University (diffuse)
clusters = [(-4, 1.0, 1.3, 4000), (1.5, 3.5, 0.9, 3500), (6, 1.5, 1.1, 2500)]

x_all, y_all = [], []
for cx, cy, spread, n in clusters:
    x_all.extend(np.random.randn(n) * spread + cx)
    y_all.extend(np.random.randn(n) * spread + cy)

x = np.array(x_all)
y = np.array(y_all)

# Hexagonal binning (plotly lacks native hexbin)
gridsize = 25
x_min, x_max = x.min() - 0.5, x.max() + 0.5
y_min, y_max = y.min() - 0.5, y.max() + 0.5

hex_size = (x_max - x_min) / (gridsize * 2)
hex_w = hex_size * np.sqrt(3)
hex_h = hex_size * 2
vert_spacing = hex_h * 0.75

hex_bins = {}
for xi, yi in zip(x, y, strict=True):
    row = int((yi - y_min) / vert_spacing)
    offset = (row % 2) * hex_w * 0.5
    col = int((xi - x_min - offset) / hex_w)
    hx = x_min + col * hex_w + offset + hex_w / 2
    hy = y_min + row * vert_spacing + hex_h / 2
    key = (col, row)
    if key not in hex_bins:
        hex_bins[key] = [hx, hy, 0]
    hex_bins[key][2] += 1

hex_x = np.array([v[0] for v in hex_bins.values()])
hex_y = np.array([v[1] for v in hex_bins.values()])
counts = np.array([v[2] for v in hex_bins.values()])

# Marker size: match hexagon circumradius to hex grid spacing
fig_w, fig_h = 1600, 900
margins = {"l": 100, "r": 140, "t": 100, "b": 100}
plot_w = fig_w - margins["l"] - margins["r"]
plot_h = fig_h - margins["t"] - margins["b"]
ax_x_range = (hex_x.max() + hex_w) - (hex_x.min() - hex_w)
ax_y_range = (hex_y.max() + hex_h) - (hex_y.min() - hex_h)
px_per_unit = min(plot_w / ax_x_range, plot_h / ax_y_range)
marker_size = 2 * hex_size * px_per_unit * 1.2

# Single scatter trace with native hexagon markers, colorscale, and colorbar
fig = go.Figure(
    go.Scatter(
        x=hex_x,
        y=hex_y,
        mode="markers",
        marker={
            "symbol": "hexagon2",
            "size": marker_size,
            "color": counts,
            "colorscale": "Viridis",
            "cmin": 0,
            "cmax": int(counts.max()),
            "colorbar": {
                "title": {"text": "Pickups", "font": {"size": 22}},
                "tickfont": {"size": 18},
                "thickness": 25,
                "len": 0.75,
            },
            "line": {"width": 0.5, "color": "rgba(255,255,255,0.25)"},
        },
        customdata=counts,
        hovertemplate=("East: %{x:.1f} km<br>North: %{y:.1f} km<br>Pickups: %{customdata}<extra></extra>"),
        showlegend=False,
    )
)

fig.update_layout(
    title={
        "text": "hexbin-basic · plotly · pyplots.ai",
        "font": {"size": 32, "color": "#2d2d2d"},
        "x": 0.5,
        "xanchor": "center",
    },
    xaxis={
        "title": {"text": "Distance East (km)", "font": {"size": 24}},
        "tickfont": {"size": 18},
        "showgrid": False,
        "zeroline": False,
        "range": [hex_x.min() - hex_w, hex_x.max() + hex_w],
    },
    yaxis={
        "title": {"text": "Distance North (km)", "font": {"size": 24}},
        "tickfont": {"size": 18},
        "showgrid": False,
        "zeroline": False,
        "scaleanchor": "x",
        "scaleratio": 1,
        "range": [hex_y.min() - hex_h, hex_y.max() + hex_h],
    },
    template="plotly_white",
    margin=margins,
    plot_bgcolor="#f8f9fa",
)

fig.write_image("plot.png", width=fig_w, height=fig_h, scale=3)
fig.write_html("plot.html", include_plotlyjs=True, full_html=True)
