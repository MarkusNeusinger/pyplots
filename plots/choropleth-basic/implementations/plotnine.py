""" pyplots.ai
choropleth-basic: Choropleth Map with Regional Coloring
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 72/100 | Created: 2025-12-31
"""

import numpy as np
import pandas as pd
from plotnine import aes, coord_fixed, element_text, geom_polygon, ggplot, labs, scale_fill_cmap, theme, theme_void


# Seed for reproducibility
np.random.seed(42)

# Create a grid-based choropleth map representing regions
# Using a hexagonal-style grid layout for clean visualization
regions_data = []

# Define a 6x4 grid of regions (24 regions total)
# Each region is a cell in the grid representing different areas
region_names = [
    "Region A1",
    "Region A2",
    "Region A3",
    "Region A4",
    "Region A5",
    "Region A6",
    "Region B1",
    "Region B2",
    "Region B3",
    "Region B4",
    "Region B5",
    "Region B6",
    "Region C1",
    "Region C2",
    "Region C3",
    "Region C4",
    "Region C5",
    "Region C6",
    "Region D1",
    "Region D2",
    "Region D3",
    "Region D4",
    "Region D5",
    "Region D6",
]

# Grid dimensions
n_cols = 6
n_rows = 4
cell_width = 10
cell_height = 8
gap = 0.5  # Small gap between cells for visibility

# Create polygon vertices for each region
for idx, region_name in enumerate(region_names):
    row = idx // n_cols
    col = idx % n_cols

    # Calculate cell corners with gaps
    x_min = col * (cell_width + gap)
    x_max = x_min + cell_width
    y_min = row * (cell_height + gap)
    y_max = y_min + cell_height

    # Four corners (counter-clockwise for proper fill)
    corners = [
        (x_min, y_min),
        (x_max, y_min),
        (x_max, y_max),
        (x_min, y_max),
        (x_min, y_min),  # Close the polygon
    ]
    for x, y in corners:
        regions_data.append({"region": region_name, "x": x, "y": y})

df_polygons = pd.DataFrame(regions_data)

# Create data values for each region (e.g., temperature anomaly index)
region_values = pd.DataFrame({"region": region_names, "value": np.random.uniform(10, 100, len(region_names))})

# Merge polygon data with values
df = df_polygons.merge(region_values, on="region")

# Create the choropleth plot
plot = (
    ggplot(df, aes(x="x", y="y", group="region", fill="value"))
    + geom_polygon(color="#333333", size=0.8, alpha=0.9)
    + scale_fill_cmap(cmap_name="Blues", name="Value\nIndex")
    + coord_fixed(ratio=1.0)
    + labs(title="choropleth-basic · plotnine · pyplots.ai")
    + theme_void()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=28, ha="center", weight="bold"),
        legend_title=element_text(size=20),
        legend_text=element_text(size=16),
        legend_position="right",
        legend_key_width=30,
        legend_key_height=180,
    )
)

# Save the plot
plot.save("plot.png", dpi=300, verbose=False)
