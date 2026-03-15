"""pyplots.ai
stereonet-equal-area: Structural Geology Stereonet (Equal-Area Projection)
Library: bokeh | Python 3.13
Quality: pending | Created: 2026-03-15
"""

import matplotlib


matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import ColumnDataSource, Label, Legend, LegendItem
from bokeh.plotting import figure
from scipy.stats import gaussian_kde


# Data - Synthetic structural geology measurements (strike, dip, feature_type)
np.random.seed(42)

# Bedding planes: consistent NE strike with moderate dip
bedding_strike = np.random.normal(45, 12, 40) % 360
bedding_dip = np.random.normal(35, 8, 40).clip(5, 85)

# Joint set 1: roughly E-W strike, steep dip
joints_strike = np.random.normal(270, 15, 35) % 360
joints_dip = np.random.normal(75, 10, 35).clip(5, 89)

# Fault set: NW strike, moderate-steep dip
faults_strike = np.random.normal(315, 10, 25) % 360
faults_dip = np.random.normal(60, 12, 25).clip(5, 89)

all_strikes = np.concatenate([bedding_strike, joints_strike, faults_strike])
all_dips = np.concatenate([bedding_dip, joints_dip, faults_dip])
all_types = ["Bedding"] * 40 + ["Joints"] * 35 + ["Faults"] * 25
colors_map = {"Bedding": "#306998", "Joints": "#E8833A", "Faults": "#8B5CF6"}

# Equal-area projection: convert pole (plunge, trend) to x, y
# Pole to a plane: trend = dip_direction + 180, plunge = 90 - dip
# Dip direction = strike + 90 (right-hand rule)
R_net = 1.0

pole_trends = (all_strikes + 90 + 180) % 360
pole_plunges = 90.0 - all_dips
pole_trends_rad = np.radians(pole_trends)
pole_plunges_rad = np.radians(pole_plunges)

pole_r = R_net * np.sqrt(2) * np.sin((np.pi / 2 - pole_plunges_rad) / 2)
pole_x = pole_r * np.sin(pole_trends_rad)
pole_y = pole_r * np.cos(pole_trends_rad)

# Great circles for each plane
# Parameterize: for rake angle alpha from 0 to pi, compute line in the plane
# then project to equal-area
gc_xs = []
gc_ys = []
gc_types = []

for i in range(len(all_strikes)):
    strike_rad = np.radians(all_strikes[i])
    dip_rad = np.radians(all_dips[i])
    dd_rad = strike_rad + np.pi / 2

    # Strike vector (horizontal, in plane)
    sx = np.sin(strike_rad)
    sy = np.cos(strike_rad)

    # Down-dip vector (in the plane, dipping)
    dx = np.sin(dd_rad) * np.cos(dip_rad)
    dy = np.cos(dd_rad) * np.cos(dip_rad)
    dz = -np.sin(dip_rad)

    # Parameterize great circle: v = cos(alpha)*s_vec + sin(alpha)*d_vec
    alpha = np.linspace(0, np.pi, 90)
    vx = np.cos(alpha) * sx + np.sin(alpha) * dx
    vy = np.cos(alpha) * sy + np.sin(alpha) * dy
    vz = np.sin(alpha) * dz

    # Convert to plunge and trend
    horiz = np.sqrt(vx**2 + vy**2)
    plunge = np.arctan2(-vz, horiz)
    trend = np.arctan2(vx, vy)

    # Equal-area projection
    r = R_net * np.sqrt(2) * np.sin((np.pi / 2 - plunge) / 2)
    gx = r * np.sin(trend)
    gy = r * np.cos(trend)

    gc_xs.append(gx.tolist())
    gc_ys.append(gy.tolist())
    gc_types.append(all_types[i])

# Kamb density contours on pole data
grid_n = 200
gx_lin = np.linspace(-1.05, 1.05, grid_n)
gy_lin = np.linspace(-1.05, 1.05, grid_n)
gx_grid, gy_grid = np.meshgrid(gx_lin, gy_lin)

# Mask to circular region
dist_grid = np.sqrt(gx_grid**2 + gy_grid**2)
mask = dist_grid <= R_net

# KDE on pole positions
pole_xy = np.vstack([pole_x, pole_y])
kde = gaussian_kde(pole_xy, bw_method=0.2)
density = kde(np.vstack([gx_grid.ravel(), gy_grid.ravel()])).reshape(grid_n, grid_n)
density[~mask] = 0

# Extract contour lines using matplotlib (computation only, not for display)
fig_temp, ax_temp = plt.subplots()
levels = np.linspace(density[mask].max() * 0.2, density[mask].max() * 0.9, 5)
cs = ax_temp.contour(gx_lin, gy_lin, density, levels=levels)
contour_xs = []
contour_ys = []
for level_segs in cs.allsegs:
    for seg in level_segs:
        # Clip to circle
        d = np.sqrt(seg[:, 0] ** 2 + seg[:, 1] ** 2)
        inside = d <= R_net * 1.01
        if np.sum(inside) > 2:
            contour_xs.append(seg[inside, 0].tolist())
            contour_ys.append(seg[inside, 1].tolist())
plt.close(fig_temp)

# Plot - Square format for circular stereonet
p = figure(
    width=3600,
    height=3600,
    title="stereonet-equal-area · bokeh · pyplots.ai",
    x_range=(-1.45, 1.45),
    y_range=(-1.40, 1.45),
    tools="pan,wheel_zoom,reset,save",
    toolbar_location=None,
    match_aspect=True,
)

# Primitive circle (outer boundary)
theta_circle = np.linspace(0, 2 * np.pi, 360)
circle_x = R_net * np.cos(theta_circle)
circle_y = R_net * np.sin(theta_circle)
p.line(circle_x, circle_y, line_color="#333333", line_width=3)

# Tick marks every 10 degrees around perimeter
for deg in range(0, 360, 10):
    rad = np.radians(deg)
    x_inner = 0.96 * R_net * np.sin(rad)
    y_inner = 0.96 * R_net * np.cos(rad)
    x_outer = 1.03 * R_net * np.sin(rad)
    y_outer = 1.03 * R_net * np.cos(rad)
    lw = 3 if deg % 90 == 0 else 2
    p.line([x_inner, x_outer], [y_inner, y_outer], line_color="#333333", line_width=lw)

# Cardinal direction labels
for deg, label in [(0, "N"), (90, "E"), (180, "S"), (270, "W")]:
    rad = np.radians(deg)
    lx = 1.12 * R_net * np.sin(rad)
    ly = 1.12 * R_net * np.cos(rad)
    fs = "26pt" if label == "N" else "20pt"
    fw = "bold" if label == "N" else "normal"
    p.add_layout(
        Label(
            x=lx,
            y=ly,
            text=label,
            text_font_size=fs,
            text_font_style=fw,
            text_align="center",
            text_baseline="middle",
            text_color="#333333",
        )
    )

# Density contour lines
for cx, cy in zip(contour_xs, contour_ys, strict=True):
    p.line(cx, cy, line_color="#888888", line_width=2, line_alpha=0.5, line_dash="dotted")

# Great circles by feature type (draw with low alpha for clarity)
renderers_gc = {}
for ftype in ["Bedding", "Joints", "Faults"]:
    idxs = [j for j, t in enumerate(gc_types) if t == ftype]
    fxs = [gc_xs[j] for j in idxs]
    fys = [gc_ys[j] for j in idxs]
    r = p.multi_line(fxs, fys, line_color=colors_map[ftype], line_width=2, line_alpha=0.35)
    renderers_gc[ftype] = r

# Poles by feature type
renderers_pole = {}
for ftype in ["Bedding", "Joints", "Faults"]:
    idxs = [j for j, t in enumerate(all_types) if t == ftype]
    px = pole_x[idxs]
    py = pole_y[idxs]
    source = ColumnDataSource(data={"x": px, "y": py})
    r = p.scatter(
        "x", "y", source=source, size=18, color=colors_map[ftype], line_color="white", line_width=1.5, alpha=0.85
    )
    renderers_pole[ftype] = r

# Legend
legend_items = []
for ftype in ["Bedding", "Joints", "Faults"]:
    legend_items.append(LegendItem(label=ftype, renderers=[renderers_gc[ftype], renderers_pole[ftype]]))

legend = Legend(items=legend_items, location="top_right")
legend.label_text_font_size = "20pt"
legend.glyph_height = 30
legend.glyph_width = 30
legend.spacing = 10
legend.background_fill_alpha = 0.85
legend.border_line_color = "#cccccc"
legend.border_line_width = 2
legend.padding = 15
p.add_layout(legend)

# Style
p.title.text_font_size = "30pt"
p.title.align = "center"
p.xaxis.visible = False
p.yaxis.visible = False
p.xgrid.visible = False
p.ygrid.visible = False
p.outline_line_color = None
p.background_fill_color = "white"

# Save
export_png(p, filename="plot.png")
output_file("plot.html")
save(p)
