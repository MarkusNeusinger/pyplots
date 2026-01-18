""" pyplots.ai
contour-map-geographic: Contour Lines on Geographic Map
Library: letsplot 4.8.2 | Python 3.13.11
Quality: 82/100 | Created: 2026-01-17
"""

import numpy as np
import pandas as pd
from lets_plot import *


LetsPlot.setup_html()

# Data - Create synthetic elevation data for a geographic region (Western US mountains)
np.random.seed(42)

# Grid covering a region (e.g., mountain range area)
lat_range = np.linspace(35, 45, 50)  # Latitude range
lon_range = np.linspace(-120, -105, 60)  # Longitude range
lon_grid, lat_grid = np.meshgrid(lon_range, lat_range)

# Generate realistic elevation data with mountain peaks
elevation = np.zeros_like(lat_grid)

# Add several mountain peaks
peaks = [
    (40.5, -111.5, 3500, 2.0),  # Peak near Salt Lake City
    (39.0, -114.0, 3200, 1.8),  # Nevada peak
    (43.5, -110.5, 4000, 2.5),  # Tetons area
    (37.5, -118.5, 4400, 2.2),  # Sierra Nevada
    (41.0, -106.5, 3600, 2.0),  # Colorado peak
]

for peak_lat, peak_lon, peak_height, spread in peaks:
    distance = np.sqrt((lat_grid - peak_lat) ** 2 + (lon_grid - peak_lon) ** 2)
    elevation += peak_height * np.exp(-(distance**2) / (2 * spread**2))

# Add base elevation and some noise
elevation += 1000 + np.random.randn(*elevation.shape) * 50

# Flatten for lets-plot
df = pd.DataFrame({"lon": lon_grid.flatten(), "lat": lat_grid.flatten(), "elevation": elevation.flatten()})

# Create contour plot with filled regions
plot = (
    ggplot(df, aes(x="lon", y="lat", z="elevation"))
    + geom_contourf(aes(fill="..level.."), bins=15, alpha=0.85)
    + geom_contour(color="white", size=0.3, bins=15, alpha=0.6)
    + scale_fill_gradient2(low="#1a5e1a", mid="#c4a35a", high="#ffffff", midpoint=2500, name="Elevation (m)")
    + labs(title="contour-map-geographic \u00b7 letsplot \u00b7 pyplots.ai", x="Longitude", y="Latitude")
    + theme_minimal()
    + theme(
        plot_title=element_text(size=24),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        legend_title=element_text(size=18),
        legend_text=element_text(size=14),
    )
    + ggsize(1600, 900)
    + coord_fixed(ratio=1.0)
)

# Save
ggsave(plot, "plot.png", scale=3)
ggsave(plot, "plot.html")
