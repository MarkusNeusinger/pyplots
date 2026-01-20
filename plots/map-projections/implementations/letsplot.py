""" pyplots.ai
map-projections: World Map with Different Projections
Library: letsplot 4.8.2 | Python 3.13.11
Quality: 71/100 | Created: 2026-01-20
"""

import os
import shutil

import numpy as np
import pandas as pd
from lets_plot import *


LetsPlot.setup_html()

np.random.seed(42)

# Data: Generate graticule lines (lat/lon grid)
graticule_rows = []
line_id = 0

# Latitude lines every 30 degrees
for lat in range(-60, 61, 30):
    lons = np.linspace(-180, 180, 180)
    for lon in lons:
        graticule_rows.append({"lon": lon, "lat": lat, "line_id": line_id})
    line_id += 1

# Longitude lines every 60 degrees
for lon in range(-180, 181, 60):
    lats = np.linspace(-60, 60, 120)
    for lat in lats:
        graticule_rows.append({"lon": lon, "lat": lat, "line_id": line_id})
    line_id += 1

graticule = pd.DataFrame(graticule_rows)

# Data: Simplified continent outlines
continent_rows = []

# Africa
africa_coords = [
    (-17, 15),
    (10, 37),
    (35, 32),
    (51, 12),
    (51, -12),
    (42, -26),
    (32, -35),
    (10, -35),
    (-5, 5),
    (-17, 15),
]
for lon, lat in africa_coords:
    continent_rows.append({"lon": lon, "lat": lat, "continent": "Africa"})

# Europe
europe_coords = [
    (-10, 35),
    (0, 38),
    (10, 45),
    (25, 45),
    (40, 45),
    (60, 55),
    (60, 70),
    (25, 70),
    (10, 60),
    (-10, 45),
    (-10, 35),
]
for lon, lat in europe_coords:
    continent_rows.append({"lon": lon, "lat": lat, "continent": "Europe"})

# Asia
asia_coords = [(60, 30), (80, 10), (120, 10), (145, 40), (145, 70), (120, 70), (100, 50), (80, 50), (60, 40), (60, 30)]
for lon, lat in asia_coords:
    continent_rows.append({"lon": lon, "lat": lat, "continent": "Asia"})

# North America
na_coords = [(-170, 65), (-130, 55), (-80, 45), (-65, 25), (-80, 25), (-100, 20), (-125, 35), (-170, 55), (-170, 65)]
for lon, lat in na_coords:
    continent_rows.append({"lon": lon, "lat": lat, "continent": "North America"})

# South America
sa_coords = [(-80, 10), (-60, 10), (-40, -5), (-35, -25), (-55, -55), (-70, -55), (-80, -10), (-80, 10)]
for lon, lat in sa_coords:
    continent_rows.append({"lon": lon, "lat": lat, "continent": "South America"})

# Australia
aus_coords = [(115, -20), (130, -12), (153, -25), (153, -38), (140, -38), (115, -35), (115, -20)]
for lon, lat in aus_coords:
    continent_rows.append({"lon": lon, "lat": lat, "continent": "Australia"})

continents = pd.DataFrame(continent_rows)

# Data: Tissot indicatrices (circles showing projection distortion)
tissot_rows = []
circle_id = 0
radius = 5  # degrees

for lat in range(-60, 61, 30):
    for lon in range(-150, 151, 60):
        angles = np.linspace(0, 2 * np.pi, 36)
        cos_lat = np.cos(np.radians(lat + 0.01))
        for angle in angles:
            dlat = radius * np.cos(angle)
            dlon = radius * np.sin(angle) / cos_lat
            tissot_rows.append({"lon": lon + dlon, "lat": lat + dlat, "circle_id": circle_id})
        circle_id += 1

tissot = pd.DataFrame(tissot_rows)

# Plot: World map with coord_map projection (Mercator-like)
plot = (
    ggplot()
    # Graticule lines (lat/lon grid)
    + geom_path(
        data=graticule, mapping=aes(x="lon", y="lat", group="line_id"), color="#888888", size=0.5, linetype="dashed"
    )
    # Continent outlines
    + geom_polygon(
        data=continents,
        mapping=aes(x="lon", y="lat", group="continent"),
        fill="#306998",
        color="#1a3d5c",
        alpha=0.8,
        size=0.8,
    )
    # Tissot indicatrices
    + geom_polygon(
        data=tissot,
        mapping=aes(x="lon", y="lat", group="circle_id"),
        fill="#FFD43B",
        color="#b8962a",
        alpha=0.6,
        size=0.4,
    )
    # Apply Mercator-like projection
    + coord_map(xlim=[-180, 180], ylim=[-70, 70])
    # Labels and theme
    + labs(
        title="map-projections \u00b7 letsplot \u00b7 pyplots.ai",
        x="Longitude",
        y="Latitude",
        caption="Tissot indicatrices show projection distortion (circles become ellipses away from equator)",
    )
    + theme_minimal()
    + theme(
        plot_title=element_text(size=28, face="bold", hjust=0.5),
        axis_title=element_text(size=18),
        axis_text=element_text(size=14),
        plot_caption=element_text(size=12, hjust=0.5, color="#666666"),
        panel_grid_major=element_blank(),
        panel_grid_minor=element_blank(),
        plot_background=element_rect(fill="#f5f5f5"),
        panel_background=element_rect(fill="#e6f0f5"),
    )
    + ggsize(1600, 900)
)

# Save outputs
ggsave(plot, "plot.png", scale=3)
ggsave(plot, "plot.html")

# Move output files from lets-plot-images subdirectory to current directory
letsplot_dir = "lets-plot-images"
if os.path.isdir(letsplot_dir):
    for filename in ["plot.png", "plot.html"]:
        src = os.path.join(letsplot_dir, filename)
        if os.path.exists(src):
            shutil.move(src, filename)
    shutil.rmtree(letsplot_dir)
