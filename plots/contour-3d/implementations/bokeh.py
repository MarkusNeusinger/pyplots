""" pyplots.ai
contour-3d: 3D Contour Plot
Library: bokeh 3.8.2 | Python 3.13.11
Quality: 88/100 | Created: 2026-01-07
"""

import numpy as np
from bokeh.io import export_png, save
from bokeh.models import ColorBar, Label, LinearColorMapper, Range1d
from bokeh.palettes import Viridis256
from bokeh.plotting import figure
from bokeh.resources import CDN
from contourpy import contour_generator


# Data - create a surface with multiple features to demonstrate contour visualization
np.random.seed(42)

# Grid setup - 40x40 for clear contour detail
n_points = 40
x = np.linspace(-3, 3, n_points)
y = np.linspace(-3, 3, n_points)
X, Y = np.meshgrid(x, y)

# Surface function: Gaussian peaks with different heights
# Primary peak at origin, secondary peak offset, creating interesting contours
Z = 1.0 * np.exp(-(X**2 + Y**2) / 1.5) + 0.6 * np.exp(-((X - 1.5) ** 2 + (Y + 1.2) ** 2) / 0.8)

# Normalize Z for better visualization
z_min, z_max = Z.min(), Z.max()

# 3D to 2D isometric projection parameters
elev_rad = np.radians(25)
azim_rad = np.radians(45)
cos_azim = np.cos(azim_rad)
sin_azim = np.sin(azim_rad)
sin_elev = np.sin(elev_rad)
cos_elev = np.cos(elev_rad)

# Scale Z for visualization (height range 0-2 for proportion)
Z_scaled = (Z - z_min) / (z_max - z_min) * 2

# Project surface grid to 2D using inline isometric projection
X_proj = np.zeros_like(X)
Z_proj = np.zeros_like(X)
Depth = np.zeros_like(X)

for i in range(n_points):
    for j in range(n_points):
        x_3d, y_3d, z_3d = X[i, j], Y[i, j], Z_scaled[i, j]
        x_rot = x_3d * cos_azim - y_3d * sin_azim
        y_rot = x_3d * sin_azim + y_3d * cos_azim
        X_proj[i, j] = x_rot
        Z_proj[i, j] = y_rot * sin_elev + z_3d * cos_elev
        Depth[i, j] = y_rot * cos_elev - z_3d * sin_elev

# Generate contour levels for the surface
n_levels = 10
levels = np.linspace(z_min, z_max, n_levels)

# Color mapper for z-values
color_mapper = LinearColorMapper(palette=Viridis256, low=z_min, high=z_max)

# Collect surface quads for rendering (sorted by depth for painter's algorithm)
surface_quads = []
for i in range(n_points - 1):
    for j in range(n_points - 1):
        # Quad corners in projected 2D
        xs = [X_proj[i, j], X_proj[i + 1, j], X_proj[i + 1, j + 1], X_proj[i, j + 1]]
        ys = [Z_proj[i, j], Z_proj[i + 1, j], Z_proj[i + 1, j + 1], Z_proj[i, j + 1]]

        # Average depth for sorting
        avg_depth = (Depth[i, j] + Depth[i + 1, j] + Depth[i + 1, j + 1] + Depth[i, j + 1]) / 4

        # Average Z value for coloring
        avg_z = (Z[i, j] + Z[i + 1, j] + Z[i + 1, j + 1] + Z[i, j + 1]) / 4

        # Map Z value to color index
        idx = int((avg_z - z_min) / (z_max - z_min) * 255)
        idx = max(0, min(255, idx))
        color = Viridis256[idx]

        surface_quads.append((avg_depth, xs, ys, color))

# Sort by depth (back to front - painter's algorithm)
surface_quads.sort(key=lambda q: q[0], reverse=True)

# Generate 3D contour lines on the surface
# For each contour level, find the contour and project it to 3D
contour_lines_3d = []

cont_gen = contour_generator(x=x, y=y, z=Z, line_type="SeparateCode")
for level_idx, level in enumerate(levels):
    z_height = (level - z_min) / (z_max - z_min) * 2  # Scale to same range as surface

    lines, codes = cont_gen.lines(level)
    for line in lines:
        if len(line) > 1:
            # Project each point of the contour to 3D then to 2D (inline projection)
            line_xs = []
            line_ys = []
            line_depths = []
            for pt in line:
                x_pt, y_pt = pt
                x_rot = x_pt * cos_azim - y_pt * sin_azim
                y_rot = x_pt * sin_azim + y_pt * cos_azim
                line_xs.append(x_rot)
                line_ys.append(y_rot * sin_elev + z_height * cos_elev)
                line_depths.append(y_rot * cos_elev - z_height * sin_elev)

            avg_depth = np.mean(line_depths)
            contour_lines_3d.append((avg_depth, line_xs, line_ys, level_idx))

# Generate projected contours on the base plane (z=0)
base_contours = []
for level_idx, level in enumerate(levels):
    lines, codes = cont_gen.lines(level)
    for line in lines:
        if len(line) > 1:
            line_xs = []
            line_ys = []
            line_depths = []
            for pt in line:
                x_pt, y_pt = pt
                # Inline projection with z=0 for base plane
                x_rot = x_pt * cos_azim - y_pt * sin_azim
                y_rot = x_pt * sin_azim + y_pt * cos_azim
                line_xs.append(x_rot)
                line_ys.append(y_rot * sin_elev)
                line_depths.append(y_rot * cos_elev)

            avg_depth = np.mean(line_depths)
            # Color based on level
            idx = int(level_idx * 255 / (n_levels - 1))
            color = Viridis256[idx]
            base_contours.append((avg_depth, line_xs, line_ys, color))

# Create Bokeh figure
p = figure(
    width=4800,
    height=2700,
    title="contour-3d · bokeh · pyplots.ai",
    toolbar_location="right",
    tools="pan,wheel_zoom,box_zoom,reset,save",
)

# Hide default axes for 3D visualization
p.xaxis.visible = False
p.yaxis.visible = False

# Draw base plane contours first (behind surface) - reference projection
for _depth, xs, ys, color in sorted(base_contours, key=lambda c: c[0], reverse=True):
    p.line(x=xs, y=ys, line_color=color, line_width=2.5, line_alpha=0.4, line_dash="dashed")

# Draw surface quads
for _depth, xs, ys, color in surface_quads:
    p.patch(x=xs, y=ys, fill_color=color, line_color="#444444", line_width=0.5, line_alpha=0.3, alpha=0.9)

# Draw 3D contour lines on surface (on top of surface)
for _depth, xs, ys, _level_idx in sorted(contour_lines_3d, key=lambda c: c[0], reverse=False):
    p.line(x=xs, y=ys, line_color="#222222", line_width=2.5, line_alpha=0.8)

# Calculate plot range from all elements
all_x_coords = [x for quad in surface_quads for x in quad[1]]
all_y_coords = [y for quad in surface_quads for y in quad[2]]

x_min_plot, x_max_plot = min(all_x_coords), max(all_x_coords)
y_min_plot, y_max_plot = min(all_y_coords), max(all_y_coords)

x_pad = (x_max_plot - x_min_plot) * 0.12
y_pad = (y_max_plot - y_min_plot) * 0.10

p.x_range = Range1d(x_min_plot - x_pad * 1.2, x_max_plot + x_pad * 1.8)
p.y_range = Range1d(y_min_plot - y_pad * 0.8, y_max_plot + y_pad * 1.2)

# Custom 3D axis lines (inline projection)
ox, oy, oz = -3.5, -3.5, 0
origin_x = ox * cos_azim - oy * sin_azim
origin_y = (ox * sin_azim + oy * cos_azim) * sin_elev + oz * cos_elev

axis_color = "#444444"
axis_width = 5

# X-axis end point
ax, ay, az = 3.5, -3.5, 0
x_axis_end_x = ax * cos_azim - ay * sin_azim
x_axis_end_y = (ax * sin_azim + ay * cos_azim) * sin_elev + az * cos_elev
p.line(x=[origin_x, x_axis_end_x], y=[origin_y, x_axis_end_y], line_color=axis_color, line_width=axis_width)

# Y-axis end point
bx, by, bz = -3.5, 3.5, 0
y_axis_end_x = bx * cos_azim - by * sin_azim
y_axis_end_y = (bx * sin_azim + by * cos_azim) * sin_elev + bz * cos_elev
p.line(x=[origin_x, y_axis_end_x], y=[origin_y, y_axis_end_y], line_color=axis_color, line_width=axis_width)

# Z-axis end point
cx, cy, cz = -3.5, -3.5, 2.5
z_axis_end_x = cx * cos_azim - cy * sin_azim
z_axis_end_y = (cx * sin_azim + cy * cos_azim) * sin_elev + cz * cos_elev
p.line(x=[origin_x, z_axis_end_x], y=[origin_y, z_axis_end_y], line_color=axis_color, line_width=axis_width)

# Axis arrows
arrow_size = 0.2

# X-axis arrow
x_dir = np.array([x_axis_end_x - origin_x, x_axis_end_y - origin_y])
x_dir = x_dir / np.linalg.norm(x_dir)
x_perp = np.array([-x_dir[1], x_dir[0]])
p.patch(
    x=[
        x_axis_end_x,
        x_axis_end_x - arrow_size * x_dir[0] + arrow_size * 0.5 * x_perp[0],
        x_axis_end_x - arrow_size * x_dir[0] - arrow_size * 0.5 * x_perp[0],
    ],
    y=[
        x_axis_end_y,
        x_axis_end_y - arrow_size * x_dir[1] + arrow_size * 0.5 * x_perp[1],
        x_axis_end_y - arrow_size * x_dir[1] - arrow_size * 0.5 * x_perp[1],
    ],
    fill_color=axis_color,
    line_color=axis_color,
)

# Y-axis arrow
y_dir = np.array([y_axis_end_x - origin_x, y_axis_end_y - origin_y])
y_dir = y_dir / np.linalg.norm(y_dir)
y_perp = np.array([-y_dir[1], y_dir[0]])
p.patch(
    x=[
        y_axis_end_x,
        y_axis_end_x - arrow_size * y_dir[0] + arrow_size * 0.5 * y_perp[0],
        y_axis_end_x - arrow_size * y_dir[0] - arrow_size * 0.5 * y_perp[0],
    ],
    y=[
        y_axis_end_y,
        y_axis_end_y - arrow_size * y_dir[1] + arrow_size * 0.5 * y_perp[1],
        y_axis_end_y - arrow_size * y_dir[1] - arrow_size * 0.5 * y_perp[1],
    ],
    fill_color=axis_color,
    line_color=axis_color,
)

# Z-axis arrow
z_dir = np.array([z_axis_end_x - origin_x, z_axis_end_y - origin_y])
z_dir = z_dir / np.linalg.norm(z_dir)
z_perp = np.array([-z_dir[1], z_dir[0]])
p.patch(
    x=[
        z_axis_end_x,
        z_axis_end_x - arrow_size * z_dir[0] + arrow_size * 0.5 * z_perp[0],
        z_axis_end_x - arrow_size * z_dir[0] - arrow_size * 0.5 * z_perp[0],
    ],
    y=[
        z_axis_end_y,
        z_axis_end_y - arrow_size * z_dir[1] + arrow_size * 0.5 * z_perp[1],
        z_axis_end_y - arrow_size * z_dir[1] - arrow_size * 0.5 * z_perp[1],
    ],
    fill_color=axis_color,
    line_color=axis_color,
)

# Axis labels (descriptive with units)
x_label = Label(
    x=x_axis_end_x + 0.15,
    y=x_axis_end_y - 0.4,
    text="Position X (units)",
    text_font_size="36pt",
    text_color="#333333",
    text_font_style="bold",
)
p.add_layout(x_label)

y_label = Label(
    x=y_axis_end_x - 0.3,
    y=y_axis_end_y + 0.25,
    text="Position Y (units)",
    text_font_size="36pt",
    text_color="#333333",
    text_font_style="bold",
)
p.add_layout(y_label)

z_label = Label(
    x=z_axis_end_x + 0.2,
    y=z_axis_end_y + 0.15,
    text="Amplitude (a.u.)",
    text_font_size="36pt",
    text_color="#333333",
    text_font_style="bold",
)
p.add_layout(z_label)

# Add colorbar for surface amplitude
color_bar = ColorBar(
    color_mapper=color_mapper,
    width=70,
    location=(0, 0),
    title="Amplitude (a.u.)",
    title_text_font_size="36pt",
    major_label_text_font_size="28pt",
    title_standoff=25,
    margin=40,
    padding=20,
)
p.add_layout(color_bar, "right")

# Title styling (larger for visibility at 4800x2700)
p.title.text_font_size = "56pt"
p.title.text_font_style = "bold"

# Grid styling - subtle
p.xgrid.grid_line_color = "#dddddd"
p.ygrid.grid_line_color = "#dddddd"
p.xgrid.grid_line_alpha = 0.2
p.ygrid.grid_line_alpha = 0.2
p.xgrid.grid_line_dash = [6, 4]
p.ygrid.grid_line_dash = [6, 4]

# Background styling
p.background_fill_color = "#f9f9f9"
p.border_fill_color = "white"
p.outline_line_color = None
p.min_border_right = 220

# Save PNG
export_png(p, filename="plot.png")

# Save HTML for interactive version
save(p, filename="plot.html", resources=CDN, title="contour-3d · bokeh · pyplots.ai")
