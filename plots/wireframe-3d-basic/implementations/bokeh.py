"""
wireframe-3d-basic: Basic 3D Wireframe Plot
Library: bokeh
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

# Remove axis labels for cleaner 3D projection look
p.xaxis.visible = False
p.yaxis.visible = False

# Draw wireframe using multi_line with Python Blue
p.multi_line(xs=all_xs, ys=all_ys, line_color="#306998", line_width=2, line_alpha=0.8)

# Set equal aspect ratio and appropriate ranges
x_min, x_max = min(min(xs) for xs in all_xs), max(max(xs) for xs in all_xs)
y_min, y_max = min(min(ys) for ys in all_ys), max(max(ys) for ys in all_ys)

# Add padding
x_pad = (x_max - x_min) * 0.1
y_pad = (y_max - y_min) * 0.1

p.x_range = Range1d(x_min - x_pad, x_max + x_pad)
p.y_range = Range1d(y_min - y_pad, y_max + y_pad)

# Add text annotations for axes
p.text(x=[x_max + x_pad * 0.5], y=[0], text=["X"], text_font_size="28pt", text_color="#666666", text_align="center")
p.text(
    x=[x_min - x_pad * 0.3],
    y=[y_min - y_pad * 0.2],
    text=["Y"],
    text_font_size="28pt",
    text_color="#666666",
    text_align="center",
)
p.text(
    x=[x_min - x_pad * 0.5],
    y=[y_max + y_pad * 0.3],
    text=["Z"],
    text_font_size="28pt",
    text_color="#666666",
    text_align="center",
)

# Styling for 4800x2700 px
p.title.text_font_size = "32pt"

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
