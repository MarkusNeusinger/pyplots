"""
hexbin-basic: Basic Hexbin Plot
Library: plotnine
"""

import numpy as np
import pandas as pd
from plotnine import aes, element_text, geom_polygon, ggplot, labs, scale_fill_continuous, theme, theme_minimal


def hexbin_polygons(x, y, gridsize=25):
    """Create hexagonal bin polygons with counts for plotnine."""
    x_min, x_max = x.min() - 0.5, x.max() + 0.5
    y_min, y_max = y.min() - 0.5, y.max() + 0.5

    # Flat-top hexagon geometry
    hex_width = (x_max - x_min) / gridsize
    hex_radius = hex_width / np.sqrt(3)
    row_height = hex_radius * 1.5

    # Generate hex grid
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

    # Count points per hexagon using proper hex distance
    points = np.column_stack([x, y])
    records = []
    hex_id = 0

    for cx, cy in centers:
        # Point-in-hexagon test (flat-top)
        dx = np.abs(points[:, 0] - cx)
        dy = np.abs(points[:, 1] - cy)
        in_hex = (
            (dy <= hex_radius)
            & (dx <= hex_width / 2)
            & (hex_radius * hex_width / 2 >= dx * hex_radius + dy * hex_width / 4)
        )
        count = np.sum(in_hex)

        if count > 0:
            # Create hexagon vertices (flat-top orientation)
            angles = np.arange(6) * np.pi / 3 + np.pi / 6
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

    return pd.DataFrame(records)


# Data - Generate clustered bivariate data
np.random.seed(42)
n_points = 5000

# Create multiple clusters for interesting density patterns
cluster1_x = np.random.normal(0, 1, n_points // 2)
cluster1_y = np.random.normal(0, 1, n_points // 2)
cluster2_x = np.random.normal(3, 0.8, n_points // 3)
cluster2_y = np.random.normal(2, 0.8, n_points // 3)
cluster3_x = np.random.normal(-2, 0.6, n_points // 6)
cluster3_y = np.random.normal(2.5, 0.6, n_points // 6)

x = np.concatenate([cluster1_x, cluster2_x, cluster3_x])
y = np.concatenate([cluster1_y, cluster2_y, cluster3_y])

# Compute hexagonal binning
hex_df = hexbin_polygons(x, y, gridsize=30)

# Plot
plot = (
    ggplot(hex_df, aes(x="x", y="y", group="hex_id", fill="count"))
    + geom_polygon(color="white", size=0.1)
    + scale_fill_continuous(cmap_name="viridis", name="Count")
    + labs(x="X Coordinate", y="Y Coordinate", title="hexbin-basic · plotnine · pyplots.ai")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        text=element_text(size=14),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        plot_title=element_text(size=24),
        legend_title=element_text(size=16),
        legend_text=element_text(size=14),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
