""" pyplots.ai
choropleth-basic: Choropleth Map with Regional Coloring
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 82/100 | Created: 2025-12-31
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    coord_fixed,
    element_blank,
    element_rect,
    element_text,
    geom_polygon,
    geom_text,
    ggplot,
    labs,
    scale_fill_cmap,
    theme,
)


# Seed for reproducibility
np.random.seed(42)

# Simplified European country boundaries (approximate polygon coordinates)
# Using stylized country shapes for a clean visualization
countries = {
    "France": [(0, 0), (3, 0), (4, 2), (3, 4), (1, 4), (0, 2)],
    "Germany": [(4, 2), (7, 1), (8, 3), (7, 5), (4, 5), (3, 4)],
    "Spain": [(-3, -3), (1, -3), (2, -1), (0, 0), (-2, 0), (-3, -1)],
    "Italy": [(5, -2), (7, -3), (9, -1), (8, 2), (6, 1), (5, 0)],
    "Poland": [(8, 3), (12, 2), (13, 5), (11, 6), (8, 5), (7, 5)],
    "UK": [(-2, 4), (1, 4), (2, 6), (1, 8), (-1, 8), (-2, 6)],
    "Sweden": [(7, 7), (10, 6), (11, 9), (10, 12), (8, 11), (7, 9)],
    "Norway": [(5, 9), (7, 7), (8, 11), (7, 14), (5, 13), (4, 11)],
    "Finland": [(11, 9), (14, 8), (15, 12), (13, 14), (11, 12), (10, 12)],
    "Austria": [(6, 1), (8, 0), (10, 1), (9, 3), (7, 3), (6, 2)],
    "Netherlands": [(2, 5), (4, 5), (5, 6), (4, 7), (2, 7), (1, 6)],
    "Belgium": [(1, 4), (3, 4), (4, 5), (2, 5), (1, 5)],
    "Switzerland": [(3, 1), (5, 0), (6, 1), (5, 2), (4, 2), (3, 2)],
    "Portugal": [(-4, -2), (-3, -3), (-2, -1), (-3, 0), (-4, 0)],
    "Denmark": [(5, 6), (7, 5), (8, 6), (7, 7), (5, 7)],
}

# Population density data (people per sq km) - realistic values for 2024
population_density = {
    "France": 119,
    "Germany": 238,
    "Spain": 94,
    "Italy": 201,
    "Poland": 123,
    "UK": 277,
    "Sweden": 25,
    "Norway": 15,
    "Finland": 18,
    "Austria": 109,
    "Netherlands": 521,
    "Belgium": 383,
    "Switzerland": 219,
    "Portugal": 111,
    "Denmark": 137,
}

# Build polygon dataframe
polygon_data = []
for country, coords in countries.items():
    # Close the polygon
    closed_coords = coords + [coords[0]]
    for i, (x, y) in enumerate(closed_coords):
        polygon_data.append({"country": country, "x": x, "y": y, "order": i, "density": population_density[country]})

df = pd.DataFrame(polygon_data)

# Calculate centroids for country labels
centroids = []
for country, coords in countries.items():
    cx = np.mean([c[0] for c in coords])
    cy = np.mean([c[1] for c in coords])
    centroids.append({"country": country, "x": cx, "y": cy, "density": population_density[country]})

df_centroids = pd.DataFrame(centroids)

# Create the choropleth map
plot = (
    ggplot()
    + geom_polygon(df, aes(x="x", y="y", group="country", fill="density"), color="#444444", size=0.6, alpha=0.95)
    + geom_text(df_centroids, aes(x="x", y="y", label="country"), size=8, color="#222222", fontweight="bold")
    + scale_fill_cmap(cmap_name="Blues", name="Population\nDensity\n(per km²)")
    + coord_fixed(ratio=1.0)
    + labs(title="choropleth-basic · plotnine · pyplots.ai")
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=28, ha="center", weight="bold", margin={"b": 20}),
        legend_title=element_text(size=18),
        legend_text=element_text(size=14),
        legend_position="right",
        legend_key_width=25,
        legend_key_height=150,
        legend_background=element_rect(fill="white", alpha=0.9),
        panel_background=element_rect(fill="#f0f5fa"),
        plot_background=element_rect(fill="white"),
        axis_text=element_blank(),
        axis_title=element_blank(),
        axis_ticks=element_blank(),
        panel_grid=element_blank(),
    )
)

# Save the plot
plot.save("plot.png", dpi=300, verbose=False)
