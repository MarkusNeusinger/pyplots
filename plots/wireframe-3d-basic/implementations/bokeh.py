"""pyplots.ai
wireframe-3d-basic: Basic 3D Wireframe Plot
Library: bokeh 3.8.1 | Python 3.13.11
Quality: 82/100 | Created: 2025-12-24
"""

import numpy as np
from bokeh.io import export_png, save
from bokeh.models import Range1d
from bokeh.plotting import figure
from bokeh.resources import CDN


# Data - create a ripple surface z = sin(sqrt(x^2 + y^2))
np.random.seed(42)

# Grid setup - 30x30 for clear wireframe
n_points = 30
x = np.linspace(-4, 4, n_points)
y = np.linspace(-4, 4, n_points)
X, Y = np.meshgrid(x, y)

# Ripple function
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)

# 3D to 2D projection (elevation=30, azimuth=45)
elev_rad = np.radians(30)
azim_rad = np.radians(45)

# Rotation around z-axis (azimuth)
X_rot = X * np.cos(azim_rad) - Y * np.sin(azim_rad)
Y_rot = X * np.sin(azim_rad) + Y * np.cos(azim_rad)

# Rotation around x-axis (elevation) and project
X_proj = X_rot
Z_proj = Y_rot * np.sin(elev_rad) + Z * np.cos(elev_rad)

# Collect wireframe lines
# Lines along x-direction (rows)
x_lines_xs = []
x_lines_ys = []
for i in range(n_points):
    x_lines_xs.append(X_proj[i, :].tolist())
    x_lines_ys.append(Z_proj[i, :].tolist())

# Lines along y-direction (columns)
y_lines_xs = []
y_lines_ys = []
for j in range(n_points):
    y_lines_xs.append(X_proj[:, j].tolist())
    y_lines_ys.append(Z_proj[:, j].tolist())

# Combine all lines
all_xs = x_lines_xs + y_lines_xs
all_ys = x_lines_ys + y_lines_ys

# Create Bokeh figure
p = figure(width=4800, height=2700, title="wireframe-3d-basic · bokeh · pyplots.ai", toolbar_location=None, tools="")

# Hide default axes since we're doing custom 3D axis visualization
p.xaxis.visible = False
p.yaxis.visible = False

# Draw wireframe using multi_line with Python Blue
p.multi_line(xs=all_xs, ys=all_ys, line_color="#306998", line_width=2, line_alpha=0.8)

# Set appropriate ranges with padding
x_min, x_max = min(min(xs) for xs in all_xs), max(max(xs) for xs in all_xs)
y_min, y_max = min(min(ys) for ys in all_ys), max(max(ys) for ys in all_ys)

x_pad = (x_max - x_min) * 0.15
y_pad = (y_max - y_min) * 0.15

p.x_range = Range1d(x_min - x_pad, x_max + x_pad)
p.y_range = Range1d(y_min - y_pad, y_max + y_pad)

# Custom 3D axis lines (origin at projected center)
axis_color = "#333333"
axis_width = 3
axis_length = 4.5

# Project 3D axis endpoints to 2D
# X-axis: (axis_length, 0, 0)
x_axis_end_x = axis_length * np.cos(azim_rad)
x_axis_end_y = 0 * np.sin(elev_rad)

# Y-axis: (0, axis_length, 0)
y_axis_end_x = -axis_length * np.sin(azim_rad)
y_axis_end_y = axis_length * np.sin(elev_rad)

# Z-axis: (0, 0, axis_length)
z_axis_end_x = 0
z_axis_end_y = axis_length * np.cos(elev_rad)

# Draw axis lines from origin
p.line(x=[0, x_axis_end_x], y=[0, x_axis_end_y], line_color=axis_color, line_width=axis_width)
p.line(x=[0, y_axis_end_x], y=[0, y_axis_end_y], line_color=axis_color, line_width=axis_width)
p.line(x=[0, z_axis_end_x], y=[0, z_axis_end_y], line_color=axis_color, line_width=axis_width)

# Add tick marks along each axis
tick_length = 0.15
tick_count = 5
label_font_size = "36pt"
tick_font_size = "24pt"

# X-axis tick marks and labels
for i in range(1, tick_count + 1):
    t = i / tick_count
    tx = t * x_axis_end_x
    ty = t * x_axis_end_y
    # Perpendicular tick
    p.line(x=[tx, tx], y=[ty - tick_length, ty + tick_length], line_color=axis_color, line_width=2)
    if i in [2, 4]:  # Show some tick labels
        val = int(t * axis_length)
        p.text(
            x=[tx],
            y=[ty - tick_length * 3],
            text=[str(val)],
            text_font_size=tick_font_size,
            text_color="#555555",
            text_align="center",
            text_baseline="top",
        )

# Y-axis tick marks and labels
for i in range(1, tick_count + 1):
    t = i / tick_count
    tx = t * y_axis_end_x
    ty = t * y_axis_end_y
    p.line(x=[tx - tick_length, tx + tick_length], y=[ty, ty], line_color=axis_color, line_width=2)
    if i in [2, 4]:
        val = int(t * axis_length)
        p.text(
            x=[tx - tick_length * 3],
            y=[ty],
            text=[str(val)],
            text_font_size=tick_font_size,
            text_color="#555555",
            text_align="right",
            text_baseline="middle",
        )

# Z-axis tick marks and labels
for i in range(1, tick_count + 1):
    t = i / tick_count
    tx = t * z_axis_end_x
    ty = t * z_axis_end_y
    p.line(x=[tx - tick_length, tx + tick_length], y=[ty, ty], line_color=axis_color, line_width=2)
    if i in [2, 4]:
        val = round(t * 1, 1)  # Z goes from 0 to ~1 (sin values)
        p.text(
            x=[tx - tick_length * 3],
            y=[ty],
            text=[str(val)],
            text_font_size=tick_font_size,
            text_color="#555555",
            text_align="right",
            text_baseline="middle",
        )

# Descriptive axis labels with units
p.text(
    x=[x_axis_end_x + 0.5],
    y=[x_axis_end_y],
    text=["X Position (units)"],
    text_font_size=label_font_size,
    text_color="#333333",
    text_align="left",
    text_baseline="middle",
)
p.text(
    x=[y_axis_end_x - 0.3],
    y=[y_axis_end_y + 0.3],
    text=["Y Position (units)"],
    text_font_size=label_font_size,
    text_color="#333333",
    text_align="right",
    text_baseline="bottom",
)
p.text(
    x=[z_axis_end_x + 0.3],
    y=[z_axis_end_y + 0.3],
    text=["Z = sin(r)"],
    text_font_size=label_font_size,
    text_color="#333333",
    text_align="left",
    text_baseline="bottom",
)

# Styling for 4800x2700 px - larger title for high-res canvas
p.title.text_font_size = "48pt"

# Grid styling - subtle
p.xgrid.grid_line_color = "#cccccc"
p.ygrid.grid_line_color = "#cccccc"
p.xgrid.grid_line_alpha = 0.3
p.ygrid.grid_line_alpha = 0.3
p.xgrid.grid_line_dash = [6, 4]
p.ygrid.grid_line_dash = [6, 4]

# Background
p.background_fill_color = "#fafafa"
p.border_fill_color = "white"
p.outline_line_color = None

# Save PNG
export_png(p, filename="plot.png")

# Save HTML for interactive version
save(p, filename="plot.html", resources=CDN, title="wireframe-3d-basic · bokeh · pyplots.ai")
