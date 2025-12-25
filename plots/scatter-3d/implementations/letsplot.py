""" pyplots.ai
scatter-3d: 3D Scatter Plot
Library: letsplot 4.8.2 | Python 3.13.11
Quality: 79/100 | Created: 2025-12-25
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_blank,
    element_text,
    geom_point,
    geom_segment,
    ggplot,
    ggsize,
    labs,
    layer_tooltips,
    scale_color_viridis,
    scale_size_identity,
    theme,
    theme_minimal,
)
from lets_plot.export import ggsave


LetsPlot.setup_html()

# Data - Generate 3D clustered data for demonstration
np.random.seed(42)

# Create 3 clusters in 3D space
n_per_cluster = 50
clusters = []

# Cluster 1: centered at (2, 2, 2)
c1_x = np.random.randn(n_per_cluster) * 0.8 + 2
c1_y = np.random.randn(n_per_cluster) * 0.8 + 2
c1_z = np.random.randn(n_per_cluster) * 0.8 + 2

# Cluster 2: centered at (-2, -1, 3)
c2_x = np.random.randn(n_per_cluster) * 0.6 - 2
c2_y = np.random.randn(n_per_cluster) * 0.6 - 1
c2_z = np.random.randn(n_per_cluster) * 0.6 + 3

# Cluster 3: centered at (0, -2, -1)
c3_x = np.random.randn(n_per_cluster) * 0.7
c3_y = np.random.randn(n_per_cluster) * 0.7 - 2
c3_z = np.random.randn(n_per_cluster) * 0.7 - 1

x = np.concatenate([c1_x, c2_x, c3_x])
y = np.concatenate([c1_y, c2_y, c3_y])
z = np.concatenate([c1_z, c2_z, c3_z])

# 3D to 2D isometric projection
# Rotation angles for good viewing angle
elev = np.radians(20)  # elevation angle
azim = np.radians(-60)  # azimuth angle

# Apply rotation transformations
# First rotate around z-axis (azimuth)
x_rot = x * np.cos(azim) - y * np.sin(azim)
y_rot = x * np.sin(azim) + y * np.cos(azim)

# Then rotate around x-axis (elevation) and project to 2D
x_proj = x_rot
y_proj = y_rot * np.sin(elev) + z * np.cos(elev)

# Depth for sorting (points in back rendered first)
depth = y_rot * np.cos(elev) - z * np.sin(elev)

# Normalize depth for size variation (perspective effect)
depth_norm = (depth - depth.min()) / (depth.max() - depth.min())
# Points closer (higher depth) appear larger
point_sizes = 4 + depth_norm * 6  # sizes from 4 to 10

# Create DataFrame
df = pd.DataFrame({"x_proj": x_proj, "y_proj": y_proj, "z": z, "depth": depth, "size": point_sizes})

# Sort by depth (back to front - painter's algorithm)
df = df.sort_values("depth").reset_index(drop=True)

# Create axis lines for 3D orientation
axis_length = 4
# Origin in 3D
origin = np.array([0, 0, 0])

# Axis endpoints
x_end = np.array([axis_length, 0, 0])
y_end = np.array([0, axis_length, 0])
z_end = np.array([0, 0, axis_length])

# Project axis endpoints


def project_point(px, py, pz):
    x_r = px * np.cos(azim) - py * np.sin(azim)
    y_r = px * np.sin(azim) + py * np.cos(azim)
    return x_r, y_r * np.sin(elev) + pz * np.cos(elev)


o_proj = project_point(0, 0, 0)
x_proj_axis = project_point(axis_length, 0, 0)
y_proj_axis = project_point(0, axis_length, 0)
z_proj_axis = project_point(0, 0, axis_length)

# Create axes dataframe
axes_df = pd.DataFrame(
    {
        "x": [o_proj[0], o_proj[0], o_proj[0]],
        "y": [o_proj[1], o_proj[1], o_proj[1]],
        "xend": [x_proj_axis[0], y_proj_axis[0], z_proj_axis[0]],
        "yend": [x_proj_axis[1], y_proj_axis[1], z_proj_axis[1]],
        "axis": ["X", "Y", "Z"],
    }
)

# Create the plot
plot = (
    ggplot()
    # Add axis lines first (behind points)
    + geom_segment(
        data=axes_df, mapping=aes(x="x", y="y", xend="xend", yend="yend"), color="#888888", size=1.5, alpha=0.7
    )
    # Add scatter points with color encoding z-value
    + geom_point(
        data=df,
        mapping=aes(x="x_proj", y="y_proj", color="z", size="size"),
        alpha=0.8,
        tooltips=layer_tooltips().line("Z Value|@z").line("Depth|@depth"),
    )
    + scale_color_viridis(name="Z Value", option="viridis")
    + scale_size_identity()
    + labs(x="X-Y Projection", y="Z Projection", title="scatter-3d · letsplot · pyplots.ai")
    + theme_minimal()
    + theme(
        axis_title=element_text(size=22),
        axis_text=element_text(size=18),
        plot_title=element_text(size=28),
        legend_text=element_text(size=16),
        legend_title=element_text(size=18),
        panel_grid=element_blank(),
    )
    + ggsize(1600, 900)
)

# Save PNG (scale=3 gives 4800x2700)
ggsave(plot, "plot.png", path=".", scale=3)

# Save HTML for interactivity
ggsave(plot, "plot.html", path=".")
