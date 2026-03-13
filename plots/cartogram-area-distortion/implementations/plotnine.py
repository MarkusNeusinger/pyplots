"""pyplots.ai
cartogram-area-distortion: Cartogram with Area Distortion by Data Value
Library: plotnine | Python 3.13
Quality: pending | Created: 2026-03-13
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


# Data: European countries with population (millions) and GDP per capita (USD thousands)
np.random.seed(42)

countries_polygons = {
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
    "Romania": [(11, 0), (14, -1), (15, 1), (14, 3), (12, 3), (11, 2)],
}

# Population in millions (2024 estimates) - this drives the area distortion
population = {
    "France": 68.0,
    "Germany": 84.5,
    "Spain": 48.0,
    "Italy": 59.0,
    "Poland": 37.8,
    "UK": 67.7,
    "Sweden": 10.5,
    "Norway": 5.5,
    "Finland": 5.6,
    "Austria": 9.1,
    "Netherlands": 17.8,
    "Belgium": 11.7,
    "Switzerland": 8.8,
    "Portugal": 10.3,
    "Denmark": 5.9,
    "Romania": 19.0,
}

# GDP per capita in thousands USD (secondary color variable)
gdp_per_capita = {
    "France": 44.4,
    "Germany": 51.4,
    "Spain": 30.1,
    "Italy": 34.8,
    "Poland": 18.3,
    "UK": 46.1,
    "Sweden": 55.2,
    "Norway": 82.8,
    "Finland": 50.6,
    "Austria": 53.6,
    "Netherlands": 57.1,
    "Belgium": 49.5,
    "Switzerland": 93.3,
    "Portugal": 24.5,
    "Denmark": 67.8,
    "Romania": 15.8,
}

# Non-contiguous cartogram: shrink all polygons first, then scale by population
# This creates visible gaps so distorted regions don't overlap
median_pop = np.median(list(population.values()))
base_shrink = 0.45  # Shrink base size to create gaps between regions

# Build scaled polygon data and centroid data
polygon_rows = []
centroid_rows = []

for country, coords in countries_polygons.items():
    pop = population[country]
    gdp = gdp_per_capita[country]

    # Compute centroid
    cx = np.mean([c[0] for c in coords])
    cy = np.mean([c[1] for c in coords])

    # Scale factor: base_shrink * sqrt(population / median) so area ~ population
    scale = base_shrink * np.sqrt(pop / median_pop)

    # Scale polygon around centroid
    closed_coords = coords + [coords[0]]
    for i, (x, y) in enumerate(closed_coords):
        sx = cx + (x - cx) * scale
        sy = cy + (y - cy) * scale
        polygon_rows.append({"country": country, "x": sx, "y": sy, "order": i, "gdp_pc": gdp, "population": pop})

    centroid_rows.append({"country": country, "x": cx, "y": cy, "gdp_pc": gdp, "population": pop})

df_polygons = pd.DataFrame(polygon_rows)
df_centroids = pd.DataFrame(centroid_rows)

# Abbreviation labels for cleaner display
abbrevs = {
    "France": "FR",
    "Germany": "DE",
    "Spain": "ES",
    "Italy": "IT",
    "Poland": "PL",
    "UK": "UK",
    "Sweden": "SE",
    "Norway": "NO",
    "Finland": "FI",
    "Austria": "AT",
    "Netherlands": "NL",
    "Belgium": "BE",
    "Switzerland": "CH",
    "Portugal": "PT",
    "Denmark": "DK",
    "Romania": "RO",
}
df_centroids["abbrev"] = df_centroids["country"].map(abbrevs)

# Plot
plot = (
    ggplot()
    + geom_polygon(df_polygons, aes(x="x", y="y", group="country", fill="gdp_pc"), color="#333333", size=0.6, alpha=0.9)
    + geom_text(df_centroids, aes(x="x", y="y", label="abbrev"), size=8, color="#111111", fontweight="bold")
    + scale_fill_cmap(cmap_name="YlOrRd", name="GDP per Capita\n(k USD)")
    + coord_fixed(ratio=1.0)
    + labs(title="cartogram-area-distortion · plotnine · pyplots.ai")
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=22, ha="center", weight="bold", margin={"b": 20}),
        legend_title=element_text(size=18),
        legend_text=element_text(size=14),
        legend_position="right",
        legend_key_width=25,
        legend_key_height=150,
        legend_background=element_rect(fill="white", alpha=0.9),
        panel_background=element_rect(fill="#f4f7fa"),
        plot_background=element_rect(fill="white"),
        axis_text=element_blank(),
        axis_title=element_blank(),
        axis_ticks=element_blank(),
        panel_grid=element_blank(),
    )
)

# Save
plot.save("plot.png", dpi=300, verbose=False)
