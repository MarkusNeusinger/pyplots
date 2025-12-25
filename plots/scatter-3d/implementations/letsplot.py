"""pyplots.ai
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

# Data - Simulated 3D spatial measurements (e.g., sensor readings in a volume)
np.random.seed(42)

# Create 3 distinct clusters with varied characteristics
n_points = 150

# Cluster 1: Dense spherical cluster (tight sensor group) - 60 points
n1 = 60
c1_x = np.random.randn(n1) * 0.5 + 3
c1_y = np.random.randn(n1) * 0.5 + 2
c1_z = np.random.randn(n1) * 0.5 + 1

# Cluster 2: Elongated ellipsoid (stretched along X) - 50 points
n2 = 50
c2_x = np.random.randn(n2) * 1.8 - 2
c2_y = np.random.randn(n2) * 0.4 - 1
c2_z = np.random.randn(n2) * 0.6 + 3.5

# Cluster 3: Flat disk (spread in X-Y plane, thin in Z) - 40 points
n3 = 40
c3_x = np.random.randn(n3) * 1.2 + 0.5
c3_y = np.random.randn(n3) * 1.2 - 2.5
c3_z = np.random.randn(n3) * 0.2 - 1.5

x = np.concatenate([c1_x, c2_x, c3_x])
y = np.concatenate([c1_y, c2_y, c3_y])
z = np.concatenate([c1_z, c2_z, c3_z])

# 3D to 2D isometric projection with rotation angles for good viewing
elev = np.radians(25)  # elevation angle
azim = np.radians(-50)  # azimuth angle

# Apply rotation: first around z-axis (azimuth), then x-axis (elevation)
cos_azim, sin_azim = np.cos(azim), np.sin(azim)
cos_elev, sin_elev = np.cos(elev), np.sin(elev)

x_rot = x * cos_azim - y * sin_azim
y_rot = x * sin_azim + y * cos_azim

# Project to 2D
x_proj = x_rot
y_proj = y_rot * sin_elev + z * cos_elev

# Depth for sorting (painter's algorithm - back to front)
depth = y_rot * cos_elev - z * sin_elev
depth_norm = (depth - depth.min()) / (depth.max() - depth.min())
point_sizes = 4 + depth_norm * 6  # perspective: closer points larger

# Create DataFrame and sort by depth
df = pd.DataFrame({"x_proj": x_proj, "y_proj": y_proj, "altitude": z, "depth": depth, "size": point_sizes})
df = df.sort_values("depth").reset_index(drop=True)

# Project axis endpoints inline (no helper function)
axis_length = 4
ox, oy = 0.0, 0.0  # origin projection
ax_x = axis_length * cos_azim
ax_y = axis_length * sin_azim * sin_elev
ay_x = -axis_length * sin_azim
ay_y = axis_length * cos_azim * sin_elev
az_x = 0.0
az_y = axis_length * cos_elev

axes_df = pd.DataFrame(
    {
        "x": [ox, ox, ox],
        "y": [oy, oy, oy],
        "xend": [ax_x, ay_x, az_x],
        "yend": [ax_y, ay_y, az_y],
        "axis": ["X", "Y", "Z"],
    }
)

# Create the plot
plot = (
    ggplot()
    + geom_segment(
        data=axes_df, mapping=aes(x="x", y="y", xend="xend", yend="yend"), color="#888888", size=1.5, alpha=0.7
    )
    + geom_point(
        data=df,
        mapping=aes(x="x_proj", y="y_proj", color="altitude", size="size"),
        alpha=0.75,
        tooltips=layer_tooltips().line("Altitude|@altitude").line("Depth|@depth"),
    )
    + scale_color_viridis(name="Altitude (m)", option="viridis")
    + scale_size_identity()
    + labs(x="Horizontal Position (m)", y="Vertical Position (m)", title="scatter-3d · letsplot · pyplots.ai")
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
