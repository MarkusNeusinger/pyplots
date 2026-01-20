"""pyplots.ai
map-marker-clustered: Clustered Marker Map
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 75/100 | Created: 2026-01-20
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    element_line,
    element_rect,
    element_text,
    geom_point,
    geom_text,
    ggplot,
    guide_legend,
    guides,
    labs,
    scale_color_manual,
    scale_size_continuous,
    theme,
    theme_minimal,
)
from scipy.cluster.hierarchy import fcluster, linkage


# Random seed for reproducibility
np.random.seed(42)

# Generate sample store locations (simulating US West Coast region)
# Major city centers - well separated to avoid cluster overlap
cities = {
    "Seattle": (47.6, -122.3),
    "Portland": (45.5, -122.7),
    "San Francisco": (37.8, -122.4),
    "Los Angeles": (34.1, -118.2),
    "San Diego": (32.7, -117.2),
}

# Generate 300 store locations clustered around major cities
n_points = 300
lats = []
lons = []
categories = []

category_types = ["Retail", "Restaurant", "Service", "Entertainment"]
city_names = list(cities.keys())

for _ in range(n_points):
    # Pick a random city center
    city = np.random.choice(city_names)
    center_lat, center_lon = cities[city]

    # Add random offset (within ~15 miles of city center) - tight clustering to avoid overlap
    lat = center_lat + np.random.normal(0, 0.15)
    lon = center_lon + np.random.normal(0, 0.15)

    lats.append(lat)
    lons.append(lon)
    categories.append(np.random.choice(category_types))

df = pd.DataFrame({"lat": lats, "lon": lons, "category": categories})

# Apply hierarchical clustering to group nearby markers
# Use a larger threshold (3.5) to create fewer, more distinct clusters per city
coords = df[["lat", "lon"]].values
Z = linkage(coords, method="ward")
cluster_labels = fcluster(Z, t=3.5, criterion="distance")
df["cluster"] = cluster_labels

# Calculate cluster centers and counts
cluster_data = (
    df.groupby("cluster")
    .agg(
        lat=("lat", "mean"),
        lon=("lon", "mean"),
        count=("cluster", "size"),
        dominant_category=("category", lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else x.iloc[0]),
    )
    .reset_index()
)

# All points are in clusters for this visualization (no single-point markers)
# This simplifies the legend and avoids confusion
cluster_markers = cluster_data.copy()
cluster_markers = cluster_markers.rename(columns={"dominant_category": "category"})
cluster_markers["label"] = cluster_markers["count"].astype(str)

# Define colors for categories (colorblind-friendly palette)
category_colors = {
    "Retail": "#4477AA",  # Blue
    "Restaurant": "#EE6677",  # Red/pink
    "Service": "#228833",  # Green
    "Entertainment": "#CCBB44",  # Yellow
}

# Create the plot - single layer for clusters with unified legend
plot = (
    ggplot(cluster_markers, aes(x="lon", y="lat"))
    # Plot cluster markers with size and color
    + geom_point(aes(size="count", color="category"), alpha=0.8, stroke=1.0)
    # Add count labels on clusters
    + geom_text(aes(label="label"), size=9, color="white", fontweight="bold")
    # Color scale - shows all categories
    + scale_color_manual(values=category_colors, name="Category")
    # Size scale for cluster markers
    + scale_size_continuous(range=(8, 20), name="Points in\nCluster", breaks=[20, 40, 60, 80])
    # Labels with units
    + labs(title="map-marker-clustered · plotnine · pyplots.ai", x="Longitude (°W)", y="Latitude (°N)")
    # Theme
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=24, weight="bold"),
        axis_title=element_text(size=20),
        axis_text=element_text(size=16),
        legend_title=element_text(size=16),
        legend_text=element_text(size=14),
        legend_position="right",
        legend_box="vertical",
        panel_grid_major=element_line(color="#cccccc", size=0.3),
        panel_grid_minor=element_line(color="#eeeeee", size=0.2),
        panel_background=element_rect(fill="#f8f8f8"),
        plot_background=element_rect(fill="white"),
    )
    + guides(
        color=guide_legend(override_aes={"size": 8, "alpha": 1}),
        size=guide_legend(override_aes={"color": "#4477AA", "alpha": 0.8}),
    )
)

# Save the plot
plot.save("plot.png", dpi=300, width=16, height=9, verbose=False)
