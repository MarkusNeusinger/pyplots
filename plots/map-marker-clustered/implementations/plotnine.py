""" pyplots.ai
map-marker-clustered: Clustered Marker Map
Library: plotnine 0.15.2 | Python 3.13.11
Quality: 72/100 | Created: 2026-01-20
"""

import numpy as np
import pandas as pd
from plotnine import (
    aes,
    coord_fixed,
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
    scale_fill_manual,
    scale_size_continuous,
    theme,
    theme_minimal,
)
from scipy.cluster.hierarchy import fcluster, linkage


# Random seed for reproducibility
np.random.seed(42)

# Generate sample store locations (simulating US West Coast region)
# Major city centers
cities = {
    "Seattle": (47.6, -122.3),
    "Portland": (45.5, -122.7),
    "San Francisco": (37.8, -122.4),
    "Los Angeles": (34.1, -118.2),
    "San Diego": (32.7, -117.2),
}

# Generate 500 store locations clustered around major cities
n_points = 500
lats = []
lons = []
categories = []
store_names = []

category_types = ["Retail", "Restaurant", "Service", "Entertainment"]
city_names = list(cities.keys())

for i in range(n_points):
    # Pick a random city center
    city = np.random.choice(city_names)
    center_lat, center_lon = cities[city]

    # Add random offset (within ~50 miles of city center)
    lat = center_lat + np.random.normal(0, 0.4)
    lon = center_lon + np.random.normal(0, 0.4)

    lats.append(lat)
    lons.append(lon)
    categories.append(np.random.choice(category_types))
    store_names.append(f"Store {i + 1}")

df = pd.DataFrame({"lat": lats, "lon": lons, "category": categories, "name": store_names})

# Apply hierarchical clustering to group nearby markers
# This simulates what would happen at a "zoomed out" view
coords = df[["lat", "lon"]].values
Z = linkage(coords, method="ward")
cluster_labels = fcluster(Z, t=0.8, criterion="distance")
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

# Separate single-point clusters (individual markers) from multi-point clusters
individual_markers = cluster_data[cluster_data["count"] == 1].copy()
cluster_markers = cluster_data[cluster_data["count"] > 1].copy()

# For individual markers, get original category
individual_df = df[df["cluster"].isin(individual_markers["cluster"])].copy()
individual_df["display_type"] = "Individual"

# Prepare cluster data for display
cluster_markers["display_type"] = "Cluster"

# Define colors for categories (Python-inspired palette)
category_colors = {
    "Retail": "#306998",  # Python blue
    "Restaurant": "#FFD43B",  # Python yellow
    "Service": "#4B8BBE",  # Lighter blue
    "Entertainment": "#646464",  # Gray
}

# Create the plot
# Show both individual markers and cluster markers
plot = (
    ggplot()
    # Plot individual markers (small points)
    + geom_point(data=individual_df, mapping=aes(x="lon", y="lat", color="category"), size=3, alpha=0.8)
    # Plot cluster markers (larger circles showing aggregation)
    + geom_point(
        data=cluster_markers,
        mapping=aes(x="lon", y="lat", size="count", fill="dominant_category"),
        color="#333333",
        shape="o",
        alpha=0.7,
        stroke=0.5,
    )
    # Add count labels on clusters
    + geom_text(
        data=cluster_markers, mapping=aes(x="lon", y="lat", label="count"), size=10, color="white", fontweight="bold"
    )
    # Color scales
    + scale_color_manual(values=category_colors, name="Category")
    + scale_fill_manual(values=category_colors, name="Cluster Category")
    + scale_size_continuous(range=(8, 20), name="Points in Cluster")
    # Labels
    + labs(title="map-marker-clustered · plotnine · pyplots.ai", x="Longitude", y="Latitude")
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
        panel_grid_major=element_line(color="#cccccc", size=0.3),
        panel_grid_minor=element_line(color="#eeeeee", size=0.2),
        panel_background=element_rect(fill="#f5f5f5"),
        plot_background=element_rect(fill="white"),
    )
    + coord_fixed(ratio=1.2)  # Approximate lat/lon aspect ratio for this region
    + guides(fill=guide_legend(override_aes={"size": 10}), size=guide_legend(override_aes={"fill": "#306998"}))
)

# Save the plot
plot.save("plot.png", dpi=300, width=16, height=9, verbose=False)
