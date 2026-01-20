"""pyplots.ai
hexbin-map-geographic: Hexagonal Binning Map
Library: plotly 6.5.2 | Python 3.13.11
Quality: 67/100 | Created: 2026-01-20
"""

import h3
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

lats, lons, fares = [], [], []
for size in cluster_sizes:
    clat = lat_center + np.random.uniform(-lat_spread, lat_spread)
    clon = lon_center + np.random.uniform(-lon_spread, lon_spread)
    lats.extend(np.random.normal(clat, 0.015, size))
    lons.extend(np.random.normal(clon, 0.02, size))
    fares.extend(np.random.exponential(15, size) + 5)

df = pd.DataFrame({"lat": lats, "lon": lons, "fare": fares})

# Configurable hexagon resolution (H3 resolution 9 gives ~0.1 km^2 cells)
hex_resolution = 9

# Convert lat/lon to H3 hexagonal cells
df["h3_cell"] = df.apply(lambda row: h3.latlng_to_cell(row["lat"], row["lon"], hex_resolution), axis=1)

# Aggregate by hexagonal cell: count, sum, and mean fare
hex_agg = (
    df.groupby("h3_cell")
    .agg(count=("fare", "size"), total_fare=("fare", "sum"), mean_fare=("fare", "mean"))
    .reset_index()
)

# Create GeoJSON features for hexagons
features = []
for _, row in hex_agg.iterrows():
    boundary = h3.cell_to_boundary(row["h3_cell"])
    coords = [[coord[1], coord[0]] for coord in boundary]
    coords.append(coords[0])
    feature = {
        "type": "Feature",
        "id": row["h3_cell"],
        "properties": {
            "count": int(row["count"]),
            "mean_fare": round(row["mean_fare"], 2),
            "total_fare": round(row["total_fare"], 2),
        },
        "geometry": {"type": "Polygon", "coordinates": [coords]},
    }
    features.append(feature)

geojson = {"type": "FeatureCollection", "features": features}

# Create choropleth map with hexagonal bins
fig = px.choropleth_map(
    hex_agg,
    geojson=geojson,
    locations="h3_cell",
    color="count",
    color_continuous_scale="YlOrRd",
    opacity=0.7,
    center={"lat": lat_center, "lon": lon_center},
    zoom=11,
    map_style="carto-positron",
    hover_data={"h3_cell": False, "count": True, "mean_fare": ":.2f"},
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
        "title": {"text": "Pickup Count", "font": {"size": 20}},
        "tickfont": {"size": 16},
        "len": 0.7,
        "thickness": 25,
    },
    margin={"l": 20, "r": 20, "t": 80, "b": 20},
)

# Update traces to show hexagon boundaries
fig.update_traces(marker_line_width=1, marker_line_color="rgba(50, 50, 50, 0.5)")

# Save as PNG
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Save as HTML for interactivity
fig.write_html("plot.html", include_plotlyjs="cdn")
