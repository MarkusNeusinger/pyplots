"""pyplots.ai
bar-3d: 3D Bar Chart
Library: bokeh | Python 3.13
Quality: pending | Created: 2025-12-31
"""

import numpy as np
from bokeh.io import export_png, save
from bokeh.models import ColorBar, Label, LinearColorMapper, Range1d
from bokeh.palettes import Viridis256
from bokeh.plotting import figure
from bokeh.resources import CDN


# Data - Quarterly sales by product category (5 products x 4 quarters)
np.random.seed(42)

products = ["Product A", "Product B", "Product C", "Product D", "Product E"]
quarters = ["Q1", "Q2", "Q3", "Q4"]

n_products = len(products)
n_quarters = len(quarters)

# Sales data (thousands of units) - varied to show different bar heights
sales = np.array(
    [
        [85, 92, 78, 95],  # Product A
        [65, 70, 88, 82],  # Product B
        [120, 115, 130, 125],  # Product C (higher performer)
        [45, 55, 50, 60],  # Product D (lower performer)
        [90, 85, 95, 100],  # Product E
    ]
)

# 3D to 2D isometric projection parameters
elev_rad = np.radians(25)
azim_rad = np.radians(45)

# Bar dimensions in 3D space
bar_width = 0.6
bar_depth = 0.6
spacing_x = 1.2  # Space between products
spacing_y = 1.2  # Space between quarters


def project_point(x, y, z):
    """Project 3D point to 2D isometric view."""
    x_rot = x * np.cos(azim_rad) - y * np.sin(azim_rad)
    y_rot = x * np.sin(azim_rad) + y * np.cos(azim_rad)
    x_proj = x_rot
    z_proj = y_rot * np.sin(elev_rad) + z * np.cos(elev_rad)
    depth = y_rot * np.cos(elev_rad) - z * np.sin(elev_rad)
    return x_proj, z_proj, depth


def create_bar_faces(x_center, y_center, height, width, depth_3d):
    """Create the 3D bar faces (top, front, right side) for isometric projection."""
    hw = width / 2
    hd = depth_3d / 2

    faces = []

    # Top face (visible from above)
    top_corners_3d = [
        (x_center - hw, y_center - hd, height),
        (x_center + hw, y_center - hd, height),
        (x_center + hw, y_center + hd, height),
        (x_center - hw, y_center + hd, height),
    ]
    top_projected = [project_point(x, y, z) for x, y, z in top_corners_3d]
    top_xs = [p[0] for p in top_projected]
    top_ys = [p[1] for p in top_projected]
    avg_depth = np.mean([p[2] for p in top_projected])
    faces.append(("top", top_xs, top_ys, avg_depth, height))

    # Front face (facing viewer in isometric)
    front_corners_3d = [
        (x_center + hw, y_center - hd, 0),
        (x_center + hw, y_center + hd, 0),
        (x_center + hw, y_center + hd, height),
        (x_center + hw, y_center - hd, height),
    ]
    front_projected = [project_point(x, y, z) for x, y, z in front_corners_3d]
    front_xs = [p[0] for p in front_projected]
    front_ys = [p[1] for p in front_projected]
    avg_depth = np.mean([p[2] for p in front_projected])
    faces.append(("front", front_xs, front_ys, avg_depth, height))

    # Right side face
    right_corners_3d = [
        (x_center - hw, y_center + hd, 0),
        (x_center + hw, y_center + hd, 0),
        (x_center + hw, y_center + hd, height),
        (x_center - hw, y_center + hd, height),
    ]
    right_projected = [project_point(x, y, z) for x, y, z in right_corners_3d]
    right_xs = [p[0] for p in right_projected]
    right_ys = [p[1] for p in right_projected]
    avg_depth = np.mean([p[2] for p in right_projected])
    faces.append(("right", right_xs, right_ys, avg_depth, height))

    return faces


# Normalize sales for height scaling (0-5 range for good visual proportion)
sales_normalized = sales / sales.max() * 5

# Generate all bar faces
all_faces = []
z_min, z_max = 0, sales.max()

for i in range(n_products):
    for j in range(n_quarters):
        x_center = i * spacing_x
        y_center = j * spacing_y
        height = sales_normalized[i, j]
        original_value = sales[i, j]

        bar_faces = create_bar_faces(x_center, y_center, height, bar_width, bar_depth)
        for face_type, xs, ys, depth, h in bar_faces:
            all_faces.append((depth, face_type, xs, ys, original_value, h))

# Sort by depth (back to front - painter's algorithm)
all_faces.sort(key=lambda f: f[0], reverse=True)

# Color mapping using Viridis colormap based on original sales values
color_mapper = LinearColorMapper(palette=Viridis256, low=z_min, high=z_max)


def get_color(value, face_type):
    """Get color for a face, with shading for different face types."""
    idx = int((value - z_min) / (z_max - z_min) * 255)
    idx = max(0, min(255, idx))
    base_color = Viridis256[idx]

    # Convert hex to RGB for shading
    r = int(base_color[1:3], 16)
    g = int(base_color[3:5], 16)
    b = int(base_color[5:7], 16)

    # Apply shading: top is brightest, front slightly darker, right side darkest
    if face_type == "top":
        factor = 1.0
    elif face_type == "front":
        factor = 0.85
    else:  # right
        factor = 0.7

    r = int(min(255, r * factor))
    g = int(min(255, g * factor))
    b = int(min(255, b * factor))

    return f"#{r:02x}{g:02x}{b:02x}"


# Create Bokeh figure
p = figure(
    width=4800,
    height=2700,
    title="Quarterly Sales by Product · bar-3d · bokeh · pyplots.ai",
    toolbar_location="right",
    tools="pan,wheel_zoom,box_zoom,reset,save",
)

# Draw bar faces with shading
for _depth, face_type, xs, ys, value, _h in all_faces:
    color = get_color(value, face_type)
    p.patch(x=xs, y=ys, fill_color=color, line_color="#306998", line_width=1.5, line_alpha=0.6, alpha=0.95)

# Calculate plot range from all face coordinates
all_xs = [x for f in all_faces for x in f[2]]
all_ys = [y for f in all_faces for y in f[3]]

x_min, x_max = min(all_xs), max(all_xs)
y_min, y_max = min(all_ys), max(all_ys)

x_pad = (x_max - x_min) * 0.18
y_pad = (y_max - y_min) * 0.15

p.x_range = Range1d(x_min - x_pad * 1.5, x_max + x_pad * 1.5)
p.y_range = Range1d(y_min - y_pad * 1.5, y_max + y_pad)

# Hide default axes for cleaner 3D projection look
p.xaxis.visible = False
p.yaxis.visible = False

# Add 3D axis lines from origin
origin_x, origin_y, _ = project_point(-0.5, -0.5, 0)

axis_color = "#444444"
axis_width = 4

# X-axis (products direction)
x_axis_end_3d = ((n_products - 1) * spacing_x + 0.8, -0.5, 0)
x_axis_end_x, x_axis_end_y, _ = project_point(*x_axis_end_3d)
p.line(x=[origin_x, x_axis_end_x], y=[origin_y, x_axis_end_y], line_color=axis_color, line_width=axis_width)

# Y-axis (quarters direction)
y_axis_end_3d = (-0.5, (n_quarters - 1) * spacing_y + 0.8, 0)
y_axis_end_x, y_axis_end_y, _ = project_point(*y_axis_end_3d)
p.line(x=[origin_x, y_axis_end_x], y=[origin_y, y_axis_end_y], line_color=axis_color, line_width=axis_width)

# Z-axis (height direction)
z_axis_end_3d = (-0.5, -0.5, 5.8)
z_axis_end_x, z_axis_end_y, _ = project_point(*z_axis_end_3d)
p.line(x=[origin_x, z_axis_end_x], y=[origin_y, z_axis_end_y], line_color=axis_color, line_width=axis_width)

# Add product labels along X-axis
for i, product in enumerate(products):
    label_pos_3d = (i * spacing_x, -1.0, 0)
    label_x, label_y, _ = project_point(*label_pos_3d)
    label = Label(
        x=label_x, y=label_y - 0.3, text=product, text_font_size="26pt", text_color="#333333", text_align="center"
    )
    p.add_layout(label)

# Add quarter labels along Y-axis
for j, quarter in enumerate(quarters):
    label_pos_3d = (-1.0, j * spacing_y, 0)
    label_x, label_y, _ = project_point(*label_pos_3d)
    label = Label(
        x=label_x - 0.4, y=label_y, text=quarter, text_font_size="26pt", text_color="#333333", text_align="right"
    )
    p.add_layout(label)

# Add axis titles
products_label = Label(
    x=x_axis_end_x + 0.3,
    y=x_axis_end_y - 0.4,
    text="Products",
    text_font_size="32pt",
    text_color="#333333",
    text_font_style="bold",
)
p.add_layout(products_label)

quarters_label = Label(
    x=y_axis_end_x - 1.0,
    y=y_axis_end_y - 0.3,
    text="Quarters",
    text_font_size="32pt",
    text_color="#333333",
    text_font_style="bold",
)
p.add_layout(quarters_label)

# Z-axis label removed - color bar already shows "Sales (thousands)"

# Add color bar for sales value scale
color_bar = ColorBar(
    color_mapper=color_mapper,
    width=60,
    location=(0, 0),
    title="Sales (thousands)",
    title_text_font_size="28pt",
    major_label_text_font_size="22pt",
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
save(p, filename="plot.html", resources=CDN, title="bar-3d · bokeh · pyplots.ai")
