""" pyplots.ai
line-3d-trajectory: 3D Line Plot for Trajectory Visualization
Library: bokeh 3.8.2 | Python 3.13.11
Quality: 82/100 | Created: 2026-01-07
"""

import numpy as np
from bokeh.io import export_png, save
from bokeh.models import ColorBar, ColumnDataSource, Label, LinearColorMapper, Range1d
from bokeh.palettes import Viridis256
from bokeh.plotting import figure
from bokeh.resources import CDN


# Data - Lorenz attractor trajectory (classic chaotic system)
np.random.seed(42)

# Lorenz system parameters
sigma = 10.0
rho = 28.0
beta = 8.0 / 3.0


# Lorenz equations
def lorenz_step(x, y, z, dt):
    dx = sigma * (y - x) * dt
    dy = (x * (rho - z) - y) * dt
    dz = (x * y - beta * z) * dt
    return x + dx, y + dy, z + dz


# Generate trajectory with 1500 points for smooth visualization
n_points = 1500
dt = 0.01
x, y, z = [0.1], [0.0], [0.0]  # Initial conditions

for _ in range(n_points - 1):
    x_new, y_new, z_new = lorenz_step(x[-1], y[-1], z[-1], dt)
    x.append(x_new)
    y.append(y_new)
    z.append(z_new)

x = np.array(x)
y = np.array(y)
z = np.array(z)

# Normalize coordinates for better visualization
x = (x - x.mean()) / x.std() * 2
y = (y - y.mean()) / y.std() * 2
z = (z - z.mean()) / z.std() * 2

# 3D to 2D isometric projection (elevation=20°, azimuth=55°)
elev_rad = np.radians(20)
azim_rad = np.radians(55)

# Rotation around z-axis (azimuth)
x_rot = x * np.cos(azim_rad) - y * np.sin(azim_rad)
y_rot = x * np.sin(azim_rad) + y * np.cos(azim_rad)

# Rotation around x-axis (elevation) and project to 2D
x_proj = x_rot
z_proj = y_rot * np.sin(elev_rad) + z * np.cos(elev_rad)

# Time/progression for color gradient (shows trajectory evolution)
time_progress = np.linspace(0, 1, n_points)

# Color mapping using time progression
color_mapper = LinearColorMapper(palette=Viridis256, low=0, high=1)

# Create segments for multi-colored line with gradient
# Each line segment has its own color based on time
n_segments = n_points - 1
xs = [[x_proj[i], x_proj[i + 1]] for i in range(n_segments)]
ys = [[z_proj[i], z_proj[i + 1]] for i in range(n_segments)]

# Map time values to colors
colors = []
for i in range(n_segments):
    t_val = time_progress[i]
    idx = int(t_val * 255)
    idx = max(0, min(255, idx))
    colors.append(Viridis256[idx])

# Create ColumnDataSource for line segments
source = ColumnDataSource(data={"xs": xs, "ys": ys, "color": colors})

# Create Bokeh figure with interactive tools
p = figure(
    width=4800,
    height=2700,
    title="Lorenz Attractor · line-3d-trajectory · bokeh · pyplots.ai",
    toolbar_location="right",
    tools="pan,wheel_zoom,box_zoom,reset,save",
)

# Draw trajectory as multi-line with color gradient showing time progression
p.multi_line(xs="xs", ys="ys", line_color="color", line_width=3, line_alpha=0.85, source=source)

# Set appropriate ranges with padding
x_min, x_max = x_proj.min(), x_proj.max()
y_min, y_max = z_proj.min(), z_proj.max()
x_pad = (x_max - x_min) * 0.15
y_pad = (y_max - y_min) * 0.15

# Center the plot with balanced padding
p.x_range = Range1d(x_min - x_pad * 1.5, x_max + x_pad * 1.2)
p.y_range = Range1d(y_min - y_pad * 1.2, y_max + y_pad)

# Hide default axes for cleaner 3D projection look
p.xaxis.visible = False
p.yaxis.visible = False

# Custom 3D axis lines positioned at the projected origin
origin_3d_x, origin_3d_y, origin_3d_z = 0, 0, 0
origin_x_rot = origin_3d_x * np.cos(azim_rad) - origin_3d_y * np.sin(azim_rad)
origin_y_rot = origin_3d_x * np.sin(azim_rad) + origin_3d_y * np.cos(azim_rad)
origin_x = origin_x_rot
origin_y = origin_y_rot * np.sin(elev_rad) + origin_3d_z * np.cos(elev_rad)

# Axis styling
axis_color = "#444444"
axis_width = 4
axis_length = 2.5

# Project 3D axis endpoints to 2D
# X-axis: point (axis_length, 0, 0)
x_end_x_rot = axis_length * np.cos(azim_rad)
x_end_y_rot = axis_length * np.sin(azim_rad)
x_axis_end_x = x_end_x_rot
x_axis_end_y = x_end_y_rot * np.sin(elev_rad)

# Y-axis: point (0, axis_length, 0)
y_end_x_rot = -axis_length * np.sin(azim_rad)
y_end_y_rot = axis_length * np.cos(azim_rad)
y_axis_end_x = y_end_x_rot
y_axis_end_y = y_end_y_rot * np.sin(elev_rad)

# Z-axis: point (0, 0, axis_length)
z_axis_end_x = origin_x
z_axis_end_y = origin_y + axis_length * np.cos(elev_rad)

# Draw axis lines from projected origin
p.line(x=[origin_x, x_axis_end_x], y=[origin_y, x_axis_end_y], line_color=axis_color, line_width=axis_width)
p.line(x=[origin_x, y_axis_end_x], y=[origin_y, y_axis_end_y], line_color=axis_color, line_width=axis_width)
p.line(x=[origin_x, z_axis_end_x], y=[origin_y, z_axis_end_y], line_color=axis_color, line_width=axis_width)

# Add axis arrows (small triangles at the end of each axis)
arrow_size = 0.18

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

# Add descriptive axis labels
x_label = Label(
    x=x_axis_end_x + 0.2,
    y=x_axis_end_y - 0.15,
    text="X",
    text_font_size="40pt",
    text_color="#333333",
    text_font_style="bold",
)
p.add_layout(x_label)

y_label = Label(
    x=y_axis_end_x - 0.35,
    y=y_axis_end_y - 0.35,
    text="Y",
    text_font_size="40pt",
    text_color="#333333",
    text_font_style="bold",
)
p.add_layout(y_label)

z_label = Label(
    x=z_axis_end_x + 0.15,
    y=z_axis_end_y + 0.1,
    text="Z",
    text_font_size="40pt",
    text_color="#333333",
    text_font_style="bold",
)
p.add_layout(z_label)

# Add color bar for time progression
color_bar = ColorBar(
    color_mapper=color_mapper,
    width=60,
    location=(0, 0),
    title="Time Progression",
    title_text_font_size="32pt",
    major_label_text_font_size="24pt",
    title_standoff=20,
    margin=40,
    padding=20,
)
p.add_layout(color_bar, "right")

# Title styling for large canvas
p.title.text_font_size = "44pt"
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
save(p, filename="plot.html", resources=CDN, title="line-3d-trajectory · bokeh · pyplots.ai")
