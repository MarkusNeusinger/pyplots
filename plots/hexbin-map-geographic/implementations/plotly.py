"""pyplots.ai
hexbin-map-geographic: Hexagonal Binning Map
Library: plotly | Python 3.13
Quality: pending | Created: 2025-01-20
"""

import numpy as np
import pandas as pd
import plotly.express as px


# Data: Simulate taxi pickup locations in NYC area
np.random.seed(42)
n_points = 5000

# NYC area bounds (Manhattan and surrounding boroughs)
lat_center, lon_center = 40.7580, -73.9855
lat_spread, lon_spread = 0.08, 0.10

# Generate clustered pickup locations (simulating hotspots)
n_clusters = 8
cluster_weights = np.random.dirichlet(np.ones(n_clusters))
cluster_sizes = (cluster_weights * n_points).astype(int)
cluster_sizes[-1] = n_points - cluster_sizes[:-1].sum()

lats, lons, values = [], [], []
for size in cluster_sizes:
    # Random cluster center
    clat = lat_center + np.random.uniform(-lat_spread, lat_spread)
    clon = lon_center + np.random.uniform(-lon_spread, lon_spread)
    # Points around cluster
    lats.extend(np.random.normal(clat, 0.015, size))
    lons.extend(np.random.normal(clon, 0.02, size))
    # Random fare values
    values.extend(np.random.exponential(15, size) + 5)

df = pd.DataFrame({"lat": lats, "lon": lons, "fare": values})

# Create hexbin map using density_map (replaces deprecated density_mapbox)
fig = px.density_map(
    df,
    lat="lat",
    lon="lon",
    z="fare",
    radius=15,
    center={"lat": lat_center, "lon": lon_center},
    zoom=11,
    map_style="carto-positron",
    color_continuous_scale="YlOrRd",
    opacity=0.7,
)

# Update layout
fig.update_layout(
    title={
        "text": "NYC Taxi Pickups · hexbin-map-geographic · plotly · pyplots.ai",
        "font": {"size": 28},
        "x": 0.5,
        "xanchor": "center",
    },
    coloraxis_colorbar={
        "title": {"text": "Avg Fare ($)", "font": {"size": 20}},
        "tickfont": {"size": 16},
        "len": 0.7,
        "thickness": 25,
    },
    margin={"l": 20, "r": 20, "t": 80, "b": 20},
)

# Save as PNG
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save as HTML for interactivity
fig.write_html("plot.html", include_plotlyjs="cdn")
