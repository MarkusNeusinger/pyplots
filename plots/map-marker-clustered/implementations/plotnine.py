""" pyplots.ai
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
# Major city centers - spread out more to reduce overlap
cities = {
    "Seattle": (47.6, -122.3),
    "Portland": (45.5, -122.7),
    "San Francisco": (37.8, -122.4),
    "Los Angeles": (34.1, -118.2),
    "San Diego": (32.7, -117.2),
}

# Generate 400 store locations clustered around major cities
n_points = 400
lats = []
lons = []
categories = []

category_types = ["Retail", "Restaurant", "Service", "Entertainment"]
city_names = list(cities.keys())

for _ in range(n_points):
    # Pick a random city center
    city = np.random.choice(city_names)
    center_lat, center_lon = cities[city]

    # Add random offset (within ~30 miles of city center) - tighter clustering
    lat = center_lat + np.random.normal(0, 0.25)
    lon = center_lon + np.random.normal(0, 0.25)

    lats.append(lat)
    lons.append(lon)
    categories.append(np.random.choice(category_types))

df = pd.DataFrame({"lat": lats, "lon": lons, "category": categories})

# Apply hierarchical clustering to group nearby markers
# Use a larger threshold to create fewer, more distinct clusters
coords = df[["lat", "lon"]].values
Z = linkage(coords, method="ward")
cluster_labels = fcluster(Z, t=2.0, criterion="distance")
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
individual_mask = cluster_data["count"] == 1
individual_clusters = cluster_data[individual_mask]["cluster"].tolist()
cluster_markers = cluster_data[~individual_mask].copy()

# For individual markers, get original data with category
individual_df = df[df["cluster"].isin(individual_clusters)].copy()

# Define colors for categories (colorblind-friendly palette)
category_colors = {
    "Retail": "#4477AA",  # Blue
    "Restaurant": "#EE6677",  # Red/pink
    "Service": "#228833",  # Green
    "Entertainment": "#CCBB44",  # Yellow
}

# Create combined data for plotting with proper legend display
# We'll use a single color scale and differentiate by marker type

# Prepare individual markers data
individual_df["marker_type"] = "Individual"
individual_df["size_val"] = 1
individual_df["label"] = ""

# Prepare cluster markers data - rename dominant_category to category for unified legend
cluster_markers = cluster_markers.rename(columns={"dominant_category": "category"})
cluster_markers["marker_type"] = "Cluster"
cluster_markers["size_val"] = cluster_markers["count"]
cluster_markers["label"] = cluster_markers["count"].astype(str)

# Create the plot
plot = (
    ggplot()
    # Plot individual markers (small points)
    + geom_point(data=individual_df, mapping=aes(x="lon", y="lat", color="category"), size=2.5, alpha=0.7)
    # Plot cluster markers (larger circles)
    + geom_point(
        data=cluster_markers, mapping=aes(x="lon", y="lat", size="count", color="category"), alpha=0.85, stroke=0.8
    )
    # Add count labels on clusters
    + geom_text(
        data=cluster_markers, mapping=aes(x="lon", y="lat", label="count"), size=8, color="white", fontweight="bold"
    )
    # Color scale - unified for all markers
    + scale_color_manual(values=category_colors, name="Category")
    # Size scale for cluster markers
    + scale_size_continuous(range=(6, 16), name="Cluster Size", breaks=[10, 30, 50, 70])
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
        legend_box="vertical",
        panel_grid_major=element_line(color="#cccccc", size=0.3),
        panel_grid_minor=element_line(color="#eeeeee", size=0.2),
        panel_background=element_rect(fill="#f8f8f8"),
        plot_background=element_rect(fill="white"),
    )
    + guides(
        color=guide_legend(override_aes={"size": 6, "alpha": 1}),
        size=guide_legend(override_aes={"color": "#4477AA", "alpha": 0.85}),
    )
)

# Save the plot
plot.save("plot.png", dpi=300, width=16, height=9, verbose=False)
