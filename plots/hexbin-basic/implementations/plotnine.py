""" pyplots.ai
hexbin-basic: Basic Hexbin Plot
Library: plotnine 0.15.3 | Python 3.14.3
Quality: 79/100 | Created: 2026-02-21
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_line,
    element_text,
    geom_polygon,
    ggplot,
    labs,
    scale_fill_continuous,
    theme,
    theme_minimal,
)


# Data - Simulated seismic sensor readings with clustered epicenters
np.random.seed(42)

# Primary fault zone (high activity)
fault_lon = np.random.normal(35.5, 0.8, 2500)
fault_lat = np.random.normal(37.0, 0.7, 2500)

# Secondary cluster (aftershock region)
after_lon = np.random.normal(37.5, 0.5, 1200)
after_lat = np.random.normal(38.5, 0.5, 1200)

# Scattered background seismicity
bg_lon = np.random.normal(33.5, 0.4, 600)
bg_lat = np.random.normal(36.5, 0.4, 600)

# Diffuse regional activity
diffuse_lon = np.random.uniform(32.0, 39.0, 700)
diffuse_lat = np.random.uniform(35.0, 40.0, 700)

longitude = np.concatenate([fault_lon, after_lon, bg_lon, diffuse_lon])
latitude = np.concatenate([fault_lat, after_lat, bg_lat, diffuse_lat])

# Hexagonal binning (inline, no functions)
gridsize = 30
x_min, x_max = longitude.min() - 0.5, longitude.max() + 0.5
y_min, y_max = latitude.min() - 0.5, latitude.max() + 0.5

hex_width = (x_max - x_min) / gridsize
hex_radius = hex_width / np.sqrt(3)
row_height = hex_radius * 1.5

# Build hex grid centers
centers = []
row = 0
y_pos = y_min
while y_pos <= y_max:
    x_offset = (hex_width / 2) if row % 2 else 0
    x_pos = x_min + x_offset
    while x_pos <= x_max:
        centers.append((x_pos, y_pos))
        x_pos += hex_width
    y_pos += row_height
    row += 1

# Count points per hexagon and build polygon vertices
points = np.column_stack([longitude, latitude])
records = []
hex_id = 0
angles = np.arange(6) * np.pi / 3 + np.pi / 6

for cx, cy in centers:
    dx = np.abs(points[:, 0] - cx)
    dy = np.abs(points[:, 1] - cy)
    in_hex = (
        (dy <= hex_radius)
        & (dx <= hex_width / 2)
        & (hex_radius * hex_width / 2 >= dx * hex_radius + dy * hex_width / 4)
    )
    count = int(np.sum(in_hex))
    if count > 0:
        for angle in angles:
            records.append(
                {
                    "x": cx + hex_radius * np.cos(angle),
                    "y": cy + hex_radius * np.sin(angle),
                    "hex_id": hex_id,
                    "count": count,
                }
            )
        hex_id += 1

hex_df = pd.DataFrame(records)

# Plot
plot = (
    ggplot(hex_df, aes(x="x", y="y", group="hex_id", fill="count"))
    + geom_polygon(color="white", size=0.15, alpha=0.9)
    + scale_fill_continuous(cmap_name="viridis", name="Event Count")
    + labs(x="Longitude (°E)", y="Latitude (°N)", title="Seismic Event Density · hexbin-basic · plotnine · pyplots.ai")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=22),
        legend_title=element_text(size=16),
        legend_text=element_text(size=14),
        panel_grid_major=element_line(size=0.4, alpha=0.2),
        panel_grid_minor=element_blank(),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
