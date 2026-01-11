"""pyplots.ai
ternary-density: Ternary Density Plot
Library: lets-plot | Python 3.13
Quality: pending | Created: 2026-01-11
"""

import numpy as np
import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_blank,
    element_text,
    geom_path,
    geom_raster,
    geom_segment,
    geom_text,
    ggplot,
    ggsave,
    ggsize,
    ggtitle,
    scale_fill_viridis,
    theme,
    theme_minimal,
    xlim,
    ylim,
)
from scipy.stats import gaussian_kde


LetsPlot.setup_html()

# Generate synthetic compositional data (sediment: sand/silt/clay)
np.random.seed(42)

# Create three clusters of compositions using Dirichlet distribution
# Cluster 1: Sandy sediments (high sand content)
n1 = 180
alpha1 = np.array([8, 2, 1])
comp1 = np.random.dirichlet(alpha1, n1) * 100

# Cluster 2: Silty sediments (high silt content)
n2 = 160
alpha2 = np.array([2, 7, 2])
comp2 = np.random.dirichlet(alpha2, n2) * 100

# Cluster 3: Clayey sediments (high clay content)
n3 = 160
alpha3 = np.array([1, 2, 8])
comp3 = np.random.dirichlet(alpha3, n3) * 100

# Combine all clusters
compositions = np.vstack([comp1, comp2, comp3])
sand = compositions[:, 0]
silt = compositions[:, 1]
clay = compositions[:, 2]

# Convert ternary to Cartesian coordinates
# Triangle vertices: Sand at (0, 0), Silt at (1, 0), Clay at (0.5, sqrt(3)/2)
total = sand + silt + clay
b_norm = silt / total
c_norm = clay / total
x_data = 0.5 * (2 * b_norm + c_norm)
y_data = (np.sqrt(3) / 2) * c_norm

# Create density grid
grid_resolution = 100
x_grid = np.linspace(0, 1, grid_resolution)
y_grid = np.linspace(0, np.sqrt(3) / 2, grid_resolution)
xx, yy = np.meshgrid(x_grid, y_grid)

# Compute kernel density estimation
points = np.vstack([x_data, y_data])
kde = gaussian_kde(points, bw_method="scott")

# Evaluate on grid
positions = np.vstack([xx.ravel(), yy.ravel()])
density = kde(positions).reshape(xx.shape)

# Create mask for valid ternary region (inside the triangle)
# Triangle vertices: (0, 0), (1, 0), (0.5, sqrt(3)/2)
# Using barycentric coordinates for vectorized mask
v0_x, v0_y = 0, 0
v1_x, v1_y = 1, 0
v2_x, v2_y = 0.5, np.sqrt(3) / 2

d1 = (xx - v2_x) * (v0_y - v2_y) - (v0_x - v2_x) * (yy - v2_y)
d2 = (xx - v0_x) * (v1_y - v0_y) - (v1_x - v0_x) * (yy - v0_y)
d3 = (xx - v1_x) * (v2_y - v1_y) - (v2_x - v1_x) * (yy - v1_y)

has_neg = (d1 < 0) | (d2 < 0) | (d3 < 0)
has_pos = (d1 > 0) | (d2 > 0) | (d3 > 0)
mask = ~(has_neg & has_pos)  # Inside triangle

# Apply mask - for points outside triangle, set very low density instead of NaN
# This creates a fade effect at the edges rather than a hard cutoff
density_masked = np.where(mask, density, 0)

# Normalize density to 0-1 range
density_min = density_masked[mask].min()
density_max = density_masked[mask].max()
density_norm = np.where(mask, (density_masked - density_min) / (density_max - density_min), np.nan)

# Create DataFrame for heatmap using geom_raster
tile_data = []
for i in range(grid_resolution):
    for j in range(grid_resolution):
        if mask[i, j]:  # Only include points inside triangle
            tile_data.append({"x": x_grid[j], "y": y_grid[i], "density": density_norm[i, j]})

df_tiles = pd.DataFrame(tile_data)

# Create triangle outline data
tri_x = [0, 1, 0.5, 0]
tri_y = [0, 0, np.sqrt(3) / 2, 0]
df_triangle = pd.DataFrame({"x": tri_x, "y": tri_y})

# Create grid lines data (fewer lines for cleaner look)
grid_lines = []
h = np.sqrt(3) / 2  # Triangle height
for pct in [0.2, 0.4, 0.6, 0.8]:
    # Lines parallel to bottom edge (constant clay %)
    y_line = pct * h
    x_left = pct / 2
    x_right = 1 - pct / 2
    grid_lines.append({"x": x_left, "y": y_line, "xend": x_right, "yend": y_line})

    # Lines parallel to left edge (constant silt %)
    # Start from bottom edge, end at right edge
    x_start = pct
    y_start = 0
    x_end = 0.5 + pct / 2
    y_end = h * (1 - pct)
    grid_lines.append({"x": x_start, "y": y_start, "xend": x_end, "yend": y_end})

    # Lines parallel to right edge (constant sand %)
    # Start from bottom edge, end at left edge
    x_start = 1 - pct
    y_start = 0
    x_end = 0.5 - pct / 2
    y_end = h * (1 - pct)
    grid_lines.append({"x": x_start, "y": y_start, "xend": x_end, "yend": y_end})

df_grid = pd.DataFrame(grid_lines)

# Create vertex labels data
labels_data = [
    {"x": -0.05, "y": -0.04, "label": "Sand"},
    {"x": 1.05, "y": -0.04, "label": "Silt"},
    {"x": 0.5, "y": np.sqrt(3) / 2 + 0.06, "label": "Clay"},
]
df_labels = pd.DataFrame(labels_data)

# Create percentage tick labels along edges
tick_labels = []
for pct in [20, 40, 60, 80]:
    frac = pct / 100
    # Bottom edge ticks (Sand percentage, 100% at left, 0% at right)
    tick_labels.append({"x": frac, "y": -0.04, "label": f"{100 - pct}%"})

    # Left edge ticks (Clay percentage)
    x_pos = frac / 2 - 0.04
    y_pos = frac * np.sqrt(3) / 2
    tick_labels.append({"x": x_pos, "y": y_pos, "label": f"{pct}%"})

    # Right edge ticks (Silt percentage)
    x_pos = 1 - frac / 2 + 0.04
    y_pos = frac * np.sqrt(3) / 2
    tick_labels.append({"x": x_pos, "y": y_pos, "label": f"{pct}%"})

df_ticks = pd.DataFrame(tick_labels)

# Build the plot using geom_raster for better performance with grid data
plot = (
    ggplot()
    # Density heatmap using geom_raster (optimized for regular grids)
    + geom_raster(aes(x="x", y="y", fill="density"), data=df_tiles)
    # Viridis color scale for density
    + scale_fill_viridis(name="Density", option="viridis")
    # Grid lines
    + geom_segment(aes(x="x", y="y", xend="xend", yend="yend"), data=df_grid, color="#306998", alpha=0.6, size=1.2)
    # Triangle outline
    + geom_path(aes(x="x", y="y"), data=df_triangle, color="#306998", size=3)
    # Vertex labels
    + geom_text(aes(x="x", y="y", label="label"), data=df_labels, size=24, color="#306998", fontface="bold")
    # Percentage tick labels
    + geom_text(aes(x="x", y="y", label="label"), data=df_ticks, size=12, color="#555555")
    # Title and theme
    + ggtitle("Sediment Composition · ternary-density · letsplot · pyplots.ai")
    # Use ggsize with aspect ratio matching the coordinate range
    # x: -0.15 to 1.15 = 1.3, y: -0.1 to 1.0 = 1.1, ratio ~1.18
    + ggsize(1200, 1020)
    + theme_minimal()
    + theme(
        plot_title=element_text(size=28, face="bold", color="#306998"),
        axis_title=element_blank(),
        axis_text=element_blank(),
        axis_ticks=element_blank(),
        panel_grid=element_blank(),
        legend_title=element_text(size=18),
        legend_text=element_text(size=14),
    )
    + xlim(-0.15, 1.15)
    + ylim(-0.1, 1.0)
)

# Save as PNG (scale 3x for high resolution = 3600 x 3060 px)
ggsave(plot, "plot.png", path=".", scale=3)

# Save interactive HTML
ggsave(plot, "plot.html", path=".")
