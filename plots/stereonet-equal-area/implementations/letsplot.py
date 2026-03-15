""" pyplots.ai
stereonet-equal-area: Structural Geology Stereonet (Equal-Area Projection)
Library: letsplot 4.9.0 | Python 3.14.3
Quality: 79/100 | Created: 2026-03-15
"""

import numpy as np
import pandas as pd
from lets_plot import *  # noqa: F403
from lets_plot.export import ggsave


LetsPlot.setup_html()

# Data - Field measurements from a structural geology mapping campaign
np.random.seed(42)

# Bedding planes (NE strike ~045, moderate dip ~35° SE)
n_bedding = 25
bedding_strike = np.random.normal(45, 12, n_bedding) % 360
bedding_dip = np.clip(np.random.normal(35, 8, n_bedding), 5, 85)

# Joint set 1 (N-S striking ~000, steep dip ~78° W)
n_j1 = 12
j1_strike = np.random.normal(355, 10, n_j1) % 360
j1_dip = np.clip(np.random.normal(78, 7, n_j1), 10, 89)

# Joint set 2 (E-W striking ~090, steep dip ~80° N)
n_j2 = 10
j2_strike = np.random.normal(90, 10, n_j2) % 360
j2_dip = np.clip(np.random.normal(80, 6, n_j2), 10, 89)

# Faults (NW-SE striking ~150, moderate-steep dip ~60°)
n_faults = 13
faults_strike = np.random.uniform(130, 170, n_faults)
faults_dip = np.clip(np.random.normal(60, 12, n_faults), 10, 89)

strikes = np.concatenate([bedding_strike, j1_strike, j2_strike, faults_strike])
dips = np.concatenate([bedding_dip, j1_dip, j2_dip, faults_dip])
feature_types = ["Bedding"] * n_bedding + ["Joint"] * (n_j1 + n_j2) + ["Fault"] * n_faults

# Equal-area (Schmidt net) lower-hemisphere projection
strike_rad = np.radians(strikes)
dip_rad = np.radians(dips)
dip_dir_rad = strike_rad + np.pi / 2

# Pole 3D coordinates (lower hemisphere normal to each plane)
pole_x_3d = np.sin(dip_rad) * np.sin(dip_dir_rad)
pole_y_3d = np.sin(dip_rad) * np.cos(dip_dir_rad)
pole_z_3d = -np.cos(dip_rad)

# Lambert azimuthal equal-area projection
pole_scale = 1.0 / np.sqrt(1.0 - pole_z_3d)
pole_x = pole_x_3d * pole_scale
pole_y = pole_y_3d * pole_scale

poles_df = pd.DataFrame({"x": pole_x, "y": pole_y, "feature_type": feature_types})

# Great circle paths for each plane
gc_rows = []
alphas = np.linspace(0, np.pi, 60)
cos_a = np.cos(alphas)
sin_a = np.sin(alphas)

for i in range(len(strikes)):
    s = strike_rad[i]
    d = dip_rad[i]
    dd = dip_dir_rad[i]

    # Strike vector (horizontal) and dip vector (in the plane, pointing downdip)
    sv_x, sv_y = np.sin(s), np.cos(s)
    dv_x = np.cos(d) * np.sin(dd)
    dv_y = np.cos(d) * np.cos(dd)
    dv_z = -np.sin(d)

    # Parametric great circle: P(a) = cos(a)*strike_vec + sin(a)*dip_vec
    px = cos_a * sv_x + sin_a * dv_x
    py = cos_a * sv_y + sin_a * dv_y
    pz = sin_a * dv_z

    # Equal-area projection
    sc = 1.0 / np.sqrt(1.0 - pz)
    gx = px * sc
    gy = py * sc

    for j in range(len(alphas)):
        gc_rows.append({"x": gx[j], "y": gy[j], "group": i, "feature_type": feature_types[i]})

gc_df = pd.DataFrame(gc_rows)

# Kamb-style density contours using Gaussian KDE on projected pole coordinates
grid_n = 100
gx_arr = np.linspace(-1.0, 1.0, grid_n)
gy_arr = np.linspace(-1.0, 1.0, grid_n)
gxx, gyy = np.meshgrid(gx_arr, gy_arr)
inside_circle = (gxx**2 + gyy**2) <= 1.0

# Manual Gaussian KDE
n_pts = len(pole_x)
bw = 0.15
density = np.zeros((grid_n, grid_n))
for k in range(n_pts):
    dx = gxx - pole_x[k]
    dy = gyy - pole_y[k]
    density += np.exp(-0.5 * (dx**2 + dy**2) / bw**2)
density /= n_pts * 2 * np.pi * bw**2
density[~inside_circle] = np.nan

# Extract contour paths manually using marching squares
# Compute contour levels
d_valid = density[inside_circle]
d_max = np.nanmax(d_valid)
d_min = np.nanmin(d_valid[d_valid > 0])
levels = np.linspace(d_min + (d_max - d_min) * 0.2, d_max * 0.85, 5)

contour_rows = []
contour_id = 0
dx_step = gx_arr[1] - gx_arr[0]
dy_step = gy_arr[1] - gy_arr[0]

for level in levels:
    # Find cells where contour crosses (simple marching squares)
    for row in range(grid_n - 1):
        for col in range(grid_n - 1):
            corners = [density[row, col], density[row, col + 1], density[row + 1, col + 1], density[row + 1, col]]
            if any(np.isnan(c) for c in corners):
                continue
            above = [c >= level for c in corners]
            if all(above) or not any(above):
                continue

            # Find intersection points on edges
            edges = []
            edge_pairs = [(0, 1), (1, 2), (2, 3), (3, 0)]
            corner_coords = [
                (gx_arr[col], gy_arr[row]),
                (gx_arr[col + 1], gy_arr[row]),
                (gx_arr[col + 1], gy_arr[row + 1]),
                (gx_arr[col], gy_arr[row + 1]),
            ]
            for ci, cj in edge_pairs:
                if above[ci] != above[cj]:
                    t = (level - corners[ci]) / (corners[cj] - corners[ci])
                    ex = corner_coords[ci][0] + t * (corner_coords[cj][0] - corner_coords[ci][0])
                    ey = corner_coords[ci][1] + t * (corner_coords[cj][1] - corner_coords[ci][1])
                    if ex**2 + ey**2 <= 1.02:
                        edges.append((ex, ey))

            if len(edges) >= 2:
                contour_rows.append({"x": edges[0][0], "y": edges[0][1], "group": contour_id})
                contour_rows.append({"x": edges[1][0], "y": edges[1][1], "group": contour_id})
                contour_id += 1

contour_df = pd.DataFrame(contour_rows)

# Primitive circle (outer boundary)
theta = np.linspace(0, 2 * np.pi, 200)
circle_df = pd.DataFrame({"x": np.cos(theta), "y": np.sin(theta)})

# Tick marks every 10° (longer every 30°)
tick_rows = []
for deg in range(0, 360, 10):
    rad = np.radians(deg)
    inner_r = 0.95 if deg % 30 != 0 else 0.92
    tick_rows.append({"x": np.sin(rad) * inner_r, "y": np.cos(rad) * inner_r, "xend": np.sin(rad), "yend": np.cos(rad)})

tick_df = pd.DataFrame(tick_rows)

# Reference cross lines (N-S, E-W)
ref_df = pd.DataFrame(
    [{"x": 0, "y": -1, "xend": 0, "yend": 1, "group": 0}, {"x": -1, "y": 0, "xend": 1, "yend": 0, "group": 1}]
)

# Cardinal direction labels
label_df = pd.DataFrame({"x": [0, 1.09, 0, -1.09], "y": [1.09, 0, -1.09, 0], "label": ["N", "E", "S", "W"]})

# Colorblind-safe palette
color_values = ["#306998", "#CC79A7", "#E69F00"]

# Plot
plot = (
    ggplot()
    # Reference cross lines
    + geom_segment(
        aes(x="x", y="y", xend="xend", yend="yend"), data=ref_df, color="#DDDDDD", size=0.5, linetype="dashed"
    )
    # Density contour segments (Kamb-style)
    + geom_line(aes(x="x", y="y", group="group"), data=contour_df, color="#999999", size=0.5, alpha=0.5)
    # Great circles
    + geom_path(aes(x="x", y="y", group="group", color="feature_type"), data=gc_df, size=0.5, alpha=0.35)
    # Poles to planes
    + geom_point(aes(x="x", y="y", color="feature_type"), data=poles_df, size=5, alpha=0.85)
    # Primitive circle
    + geom_path(aes(x="x", y="y"), data=circle_df, color="#333333", size=1.2)
    # Tick marks
    + geom_segment(aes(x="x", y="y", xend="xend", yend="yend"), data=tick_df, color="#333333", size=0.7)
    # Cardinal labels
    + geom_text(aes(x="x", y="y", label="label"), data=label_df, size=18, color="#333333", fontface="bold")
    # Color scale
    + scale_color_manual(values=color_values, name="Feature Type")
    # Fixed aspect ratio
    + coord_fixed()
    + scale_x_continuous(limits=[-1.25, 1.25])
    + scale_y_continuous(limits=[-1.25, 1.25])
    # Title
    + labs(title="stereonet-equal-area · letsplot · pyplots.ai")
    # Theme
    + theme(
        plot_title=element_text(size=24, hjust=0.5),
        legend_title=element_text(size=18),
        legend_text=element_text(size=16),
        legend_position="right",
        axis_title=element_blank(),
        axis_text=element_blank(),
        axis_ticks=element_blank(),
        axis_line=element_blank(),
        panel_grid=element_blank(),
    )
    + ggsize(1200, 1200)
)

# Save
ggsave(plot, "plot.png", path=".", scale=3)
ggsave(plot, "plot.html", path=".")
