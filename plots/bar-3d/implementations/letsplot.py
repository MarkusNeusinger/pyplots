"""pyplots.ai
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

        # Project all corners to 2D (inline projection math)
        corners_2d = {}
        for name, (cx, cy, cz) in corners_3d.items():
            x_rot = cx * cos_azim - cy * sin_azim
            y_rot = cx * sin_azim + cy * cos_azim
            px = x_rot
            py = y_rot * sin_elev + cz * cos_elev
            corners_2d[name] = (px, py)

        # Calculate bar center depth for ordering (inline projection)
        center_x = x_base + bar_width / 2
        center_y = y_base + bar_depth / 2
        center_z = height / 2
        cx_rot = center_x * cos_azim - center_y * sin_azim
        cy_rot = center_x * sin_azim + center_y * cos_azim
        bar_depth_value = cy_rot * cos_elev - center_z * sin_elev

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
    # Inline projection for start point
    x_rot_s = x_min * cos_azim - y_line * sin_azim
    y_rot_s = x_min * sin_azim + y_line * cos_azim
    start_x = x_rot_s
    start_y = y_rot_s * sin_elev + z_floor * cos_elev
    # Inline projection for end point
    x_rot_e = x_max * cos_azim - y_line * sin_azim
    y_rot_e = x_max * sin_azim + y_line * cos_azim
    end_x = x_rot_e
    end_y = y_rot_e * sin_elev + z_floor * cos_elev
    grid_lines.append({"x": start_x, "y": start_y, "xend": end_x, "yend": end_y})

# Grid lines parallel to Y axis
for j in range(len(quarters) + 1):
    x_line = j * spacing_x - 0.3 + bar_width / 2
    # Inline projection for start point
    x_rot_s = x_line * cos_azim - y_min * sin_azim
    y_rot_s = x_line * sin_azim + y_min * cos_azim
    start_x = x_rot_s
    start_y = y_rot_s * sin_elev + z_floor * cos_elev
    # Inline projection for end point
    x_rot_e = x_line * cos_azim - y_max * sin_azim
    y_rot_e = x_line * sin_azim + y_max * cos_azim
    end_x = x_rot_e
    end_y = y_rot_e * sin_elev + z_floor * cos_elev
    grid_lines.append({"x": start_x, "y": start_y, "xend": end_x, "yend": end_y})

df_grid = pd.DataFrame(grid_lines)

# Create axis lines from corner (inline projection)
origin_x, origin_y, origin_z = x_min - 1.5, y_min - 1.5, z_floor
x_rot_o = origin_x * cos_azim - origin_y * sin_azim
y_rot_o = origin_x * sin_azim + origin_y * cos_azim
axis_origin_x = x_rot_o
axis_origin_y = y_rot_o * sin_elev + origin_z * cos_elev

axis_len_x = (x_max - x_min) * 0.4
axis_len_y = (y_max - y_min) * 0.4
axis_len_z = revenue.max() * 0.4

# X axis end (inline projection)
x_end_3d = origin_x + axis_len_x
x_rot_xe = x_end_3d * cos_azim - origin_y * sin_azim
y_rot_xe = x_end_3d * sin_azim + origin_y * cos_azim
x_axis_end_x = x_rot_xe
x_axis_end_y = y_rot_xe * sin_elev + origin_z * cos_elev

# Y axis end (inline projection)
y_end_3d = origin_y + axis_len_y
x_rot_ye = origin_x * cos_azim - y_end_3d * sin_azim
y_rot_ye = origin_x * sin_azim + y_end_3d * cos_azim
y_axis_end_x = x_rot_ye
y_axis_end_y = y_rot_ye * sin_elev + origin_z * cos_elev

# Z axis end (inline projection)
z_end_3d = origin_z + axis_len_z
z_axis_end_x = x_rot_o
z_axis_end_y = y_rot_o * sin_elev + z_end_3d * cos_elev

axes_df = pd.DataFrame(
    {
        "x": [axis_origin_x, axis_origin_x, axis_origin_x],
        "y": [axis_origin_y, axis_origin_y, axis_origin_y],
        "xend": [x_axis_end_x, y_axis_end_x, z_axis_end_x],
        "yend": [x_axis_end_y, y_axis_end_y, z_axis_end_y],
    }
)

# Revenue label on Z axis (positioned at top of z-axis, slightly right to avoid cutoff)
z_label_df = pd.DataFrame({"x": [z_axis_end_x + 0.3], "y": [z_axis_end_y + 1.0], "label": ["Revenue ($M)"]})

# Product labels positioned at front-left, well away from the bars
product_labels = []
for i, product in enumerate(products):
    y_pos = i * spacing_y + bar_depth / 2
    # Position labels at front-left corner, outside the grid area
    label_x_3d = -2.5
    label_y_3d = -3.5
    x_rot_p = label_x_3d * cos_azim - label_y_3d * sin_azim
    y_rot_p = label_x_3d * sin_azim + label_y_3d * cos_azim
    # Stack vertically with consistent spacing
    px = x_rot_p
    py = y_rot_p * sin_elev + z_floor * cos_elev + i * 2.5
    product_labels.append({"x": px, "y": py, "label": product})
df_product_labels = pd.DataFrame(product_labels)

# Quarter labels positioned further forward to avoid overlap with bars
quarter_labels = []
for j, quarter in enumerate(quarters):
    x_pos = j * spacing_x + bar_width / 2
    # Inline projection - move labels much further forward (-4.0 instead of -2.0)
    label_y_3d = -4.0
    x_rot_q = x_pos * cos_azim - label_y_3d * sin_azim
    y_rot_q = x_pos * sin_azim + label_y_3d * cos_azim
    px = x_rot_q
    py = y_rot_q * sin_elev + z_floor * cos_elev
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
    # Product labels (positioned to left of bars, left-aligned to avoid cutoff)
    + geom_text(
        data=df_product_labels,
        mapping=aes(x="x", y="y", label="label"),
        color="#1a1a1a",
        size=11,
        hjust=0,
        fontface="bold",
    )
    # Quarter labels (further forward)
    + geom_text(
        data=df_quarter_labels, mapping=aes(x="x", y="y", label="label"), color="#1a1a1a", size=11, fontface="bold"
    )
    # Revenue axis label
    + geom_text(data=z_label_df, mapping=aes(x="x", y="y", label="label"), color="#1a1a1a", size=12, fontface="bold")
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

# Save HTML for interactivity (interactive rotation available via HTML export)
ggsave(plot, "plot.html", path=".")
