""" pyplots.ai
bar-3d: 3D Bar Chart
Library: letsplot 4.8.2 | Python 3.13.11
Quality: 82/100 | Created: 2025-12-31
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_blank,
    element_text,
    geom_polygon,
    geom_segment,
    geom_text,
    ggplot,
    ggsize,
    labs,
    layer_tooltips,
    scale_fill_viridis,
    theme,
    theme_minimal,
)
from lets_plot.export import ggsave


LetsPlot.setup_html()

# Data - Quarterly sales performance across product categories
np.random.seed(42)

products = ["Electronics", "Clothing", "Home", "Sports", "Books"]
quarters = ["Q1", "Q2", "Q3", "Q4"]

# Revenue data in millions
revenue = np.array(
    [
        [45, 52, 48, 65],  # Electronics
        [32, 38, 42, 55],  # Clothing
        [28, 30, 35, 40],  # Home
        [20, 35, 45, 30],  # Sports
        [15, 18, 22, 28],  # Books
    ]
)

# 3D to 2D isometric projection settings
elev = np.radians(25)  # elevation angle
azim = np.radians(-50)  # azimuth angle
cos_azim, sin_azim = np.cos(azim), np.sin(azim)
cos_elev, sin_elev = np.cos(elev), np.sin(elev)


def project_3d_to_2d(x, y, z):
    """Project 3D coordinates to 2D isometric view."""
    x_rot = x * cos_azim - y * sin_azim
    y_rot = x * sin_azim + y * cos_azim
    x_proj = x_rot
    y_proj = y_rot * sin_elev + z * cos_elev
    depth = y_rot * cos_elev - z * sin_elev
    return x_proj, y_proj, depth


# Bar dimensions - good spacing for clarity
bar_width = 0.5
bar_depth = 0.5
spacing_x = 1.4
spacing_y = 1.6

# Create bar polygons (each bar is a 3D box with visible faces)
bar_polygons = []
bar_id = 0

for i, product in enumerate(products):
    for j, quarter in enumerate(quarters):
        x_base = j * spacing_x
        y_base = i * spacing_y
        height = revenue[i, j]

        # Define the 8 corners of the bar
        corners_3d = {
            "front_bottom_left": (x_base, y_base, 0),
            "front_bottom_right": (x_base + bar_width, y_base, 0),
            "front_top_left": (x_base, y_base, height),
            "front_top_right": (x_base + bar_width, y_base, height),
            "back_bottom_left": (x_base, y_base + bar_depth, 0),
            "back_bottom_right": (x_base + bar_width, y_base + bar_depth, 0),
            "back_top_left": (x_base, y_base + bar_depth, height),
            "back_top_right": (x_base + bar_width, y_base + bar_depth, height),
        }

        # Project all corners to 2D
        corners_2d = {}
        for name, (cx, cy, cz) in corners_3d.items():
            px, py, d = project_3d_to_2d(cx, cy, cz)
            corners_2d[name] = (px, py)

        # Calculate bar center depth for ordering
        center_x = x_base + bar_width / 2
        center_y = y_base + bar_depth / 2
        center_z = height / 2
        _, _, bar_depth_value = project_3d_to_2d(center_x, center_y, center_z)

        # Define the 3 visible faces (front, top, right side)
        front_face = [
            corners_2d["front_bottom_left"],
            corners_2d["front_bottom_right"],
            corners_2d["front_top_right"],
            corners_2d["front_top_left"],
        ]

        top_face = [
            corners_2d["front_top_left"],
            corners_2d["front_top_right"],
            corners_2d["back_top_right"],
            corners_2d["back_top_left"],
        ]

        right_face = [
            corners_2d["front_bottom_right"],
            corners_2d["back_bottom_right"],
            corners_2d["back_top_right"],
            corners_2d["front_top_right"],
        ]

        # Add each face as a polygon
        for face_name, face_coords in [("front", front_face), ("top", top_face), ("right", right_face)]:
            for k, (fx, fy) in enumerate(face_coords):
                bar_polygons.append(
                    {
                        "x": fx,
                        "y": fy,
                        "bar_id": bar_id,
                        "face": face_name,
                        "face_id": f"{bar_id}_{face_name}",
                        "height": height,
                        "depth": bar_depth_value,
                        "product": product,
                        "quarter": quarter,
                        "order": k,
                    }
                )
        bar_id += 1

df_bars = pd.DataFrame(bar_polygons)

# Sort by depth (back to front) for proper rendering order
df_bars = df_bars.sort_values(["depth", "face_id", "order"])

# Create floor grid for depth perception
grid_lines = []
x_min, x_max = -0.3, (len(quarters) - 1) * spacing_x + bar_width + 0.3
y_min, y_max = -0.3, (len(products) - 1) * spacing_y + bar_depth + 0.3
z_floor = -3

# Grid lines parallel to X axis
for i in range(len(products) + 1):
    y_line = i * spacing_y - 0.3 + bar_depth / 2
    start = project_3d_to_2d(x_min, y_line, z_floor)
    end = project_3d_to_2d(x_max, y_line, z_floor)
    grid_lines.append({"x": start[0], "y": start[1], "xend": end[0], "yend": end[1]})

# Grid lines parallel to Y axis
for j in range(len(quarters) + 1):
    x_line = j * spacing_x - 0.3 + bar_width / 2
    start = project_3d_to_2d(x_line, y_min, z_floor)
    end = project_3d_to_2d(x_line, y_max, z_floor)
    grid_lines.append({"x": start[0], "y": start[1], "xend": end[0], "yend": end[1]})

df_grid = pd.DataFrame(grid_lines)

# Create axis lines from corner
axis_origin = project_3d_to_2d(x_min - 1.5, y_min - 1.5, z_floor)
axis_len_x = (x_max - x_min) * 0.4
axis_len_y = (y_max - y_min) * 0.4
axis_len_z = revenue.max() * 0.4

x_axis_end = project_3d_to_2d(x_min - 1.5 + axis_len_x, y_min - 1.5, z_floor)
y_axis_end = project_3d_to_2d(x_min - 1.5, y_min - 1.5 + axis_len_y, z_floor)
z_axis_end = project_3d_to_2d(x_min - 1.5, y_min - 1.5, z_floor + axis_len_z)

axes_df = pd.DataFrame(
    {
        "x": [axis_origin[0], axis_origin[0], axis_origin[0]],
        "y": [axis_origin[1], axis_origin[1], axis_origin[1]],
        "xend": [x_axis_end[0], y_axis_end[0], z_axis_end[0]],
        "yend": [x_axis_end[1], y_axis_end[1], z_axis_end[1]],
    }
)

# Revenue label on Z axis (positioned at top of z-axis)
z_label_df = pd.DataFrame({"x": [z_axis_end[0] - 0.5], "y": [z_axis_end[1] + 1.0], "label": ["Revenue ($M)"]})

# Product labels positioned on the left side (near front-left)
product_labels = []
for i, product in enumerate(products):
    y_pos = i * spacing_y + bar_depth / 2
    px, py, _ = project_3d_to_2d(-2.0, y_pos, z_floor)
    product_labels.append({"x": px, "y": py, "label": product})
df_product_labels = pd.DataFrame(product_labels)

# Quarter labels positioned at the front (near front-left, below products)
quarter_labels = []
for j, quarter in enumerate(quarters):
    x_pos = j * spacing_x + bar_width / 2
    px, py, _ = project_3d_to_2d(x_pos, -2.0, z_floor)
    quarter_labels.append({"x": px, "y": py, "label": quarter})
df_quarter_labels = pd.DataFrame(quarter_labels)

# Create the plot
plot = (
    ggplot()
    # Floor grid
    + geom_segment(
        data=df_grid, mapping=aes(x="x", y="y", xend="xend", yend="yend"), color="#CCCCCC", size=0.5, alpha=0.5
    )
    # Axis lines
    + geom_segment(
        data=axes_df, mapping=aes(x="x", y="y", xend="xend", yend="yend"), color="#666666", size=1.5, alpha=0.8
    )
    # Bar faces (rendered back to front due to sorting)
    + geom_polygon(
        data=df_bars,
        mapping=aes(x="x", y="y", group="face_id", fill="height"),
        color="#333333",
        size=0.6,
        alpha=0.85,
        tooltips=layer_tooltips().line("@product").line("@quarter").line("Revenue|$@{height}M"),
    )
    # Product labels (on left side)
    + geom_text(data=df_product_labels, mapping=aes(x="x", y="y", label="label"), color="#333333", size=10, hjust=1)
    # Quarter labels (at front)
    + geom_text(data=df_quarter_labels, mapping=aes(x="x", y="y", label="label"), color="#333333", size=10)
    # Revenue axis label
    + geom_text(data=z_label_df, mapping=aes(x="x", y="y", label="label"), color="#444444", size=11, fontface="bold")
    + scale_fill_viridis(name="Revenue ($M)", option="viridis")
    + labs(x="", y="", title="bar-3d \u00b7 letsplot \u00b7 pyplots.ai")
    + theme_minimal()
    + theme(
        axis_title=element_blank(),
        axis_text=element_blank(),
        axis_ticks=element_blank(),
        panel_grid=element_blank(),
        plot_title=element_text(size=32, face="bold"),
        legend_text=element_text(size=16),
        legend_title=element_text(size=18),
    )
    + ggsize(1600, 900)
)

# Save PNG (scale=3 gives 4800x2700)
ggsave(plot, "plot.png", path=".", scale=3)

# Save HTML for interactivity
ggsave(plot, "plot.html", path=".")
