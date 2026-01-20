""" pyplots.ai
map-marker-clustered: Clustered Marker Map
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 78/100 | Created: 2026-01-20
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster import AgglomerativeClustering


# Generate sample geographic data - coffee shop locations across a city region
np.random.seed(42)
n_points = 500

# Create clustered geographic data (simulating city with neighborhoods)
n_neighborhoods = 8
neighborhood_centers = np.random.uniform(-0.5, 0.5, (n_neighborhoods, 2))
points_per_neighborhood = n_points // n_neighborhoods

lats, lons, categories = [], [], []
category_names = ["Coffee Shop", "Restaurant", "Bookstore", "Gym"]

for i, center in enumerate(neighborhood_centers):
    n_pts = points_per_neighborhood + (n_points % n_neighborhoods if i == 0 else 0)
    lat = np.random.normal(center[0], 0.08, n_pts) + 40.7  # NYC-like latitude
    lon = np.random.normal(center[1], 0.08, n_pts) - 74.0  # NYC-like longitude
    lats.extend(lat)
    lons.extend(lon)
    categories.extend(np.random.choice(category_names, n_pts))

df = pd.DataFrame({"lat": lats, "lon": lons, "category": categories})

# Apply hierarchical clustering to group nearby markers
coords = df[["lat", "lon"]].values
clustering = AgglomerativeClustering(n_clusters=None, distance_threshold=0.05, linkage="ward")
df["cluster"] = clustering.fit_predict(coords)

# Calculate cluster centers and sizes
cluster_stats = (
    df.groupby("cluster")
    .agg(
        lat_center=("lat", "mean"),
        lon_center=("lon", "mean"),
        count=("lat", "size"),
        dominant_category=("category", lambda x: x.mode().iloc[0]),
    )
    .reset_index()
)

# Create the plot
fig, ax = plt.subplots(figsize=(16, 9))
sns.set_style("whitegrid")

# Define color palette for categories
palette = {"Coffee Shop": "#306998", "Restaurant": "#FFD43B", "Bookstore": "#4CAF50", "Gym": "#E91E63"}

# Plot individual points with low alpha (background layer)
sns.scatterplot(data=df, x="lon", y="lat", hue="category", palette=palette, s=30, alpha=0.2, ax=ax, legend=False)

# Plot cluster markers (foreground layer)
# Size proportional to count, color by dominant category
sizes = cluster_stats["count"] * 15  # Scale factor for visibility
colors = cluster_stats["dominant_category"].map(palette)

ax.scatter(
    cluster_stats["lon_center"],
    cluster_stats["lat_center"],
    s=sizes,
    c=colors,
    alpha=0.8,
    edgecolors="white",
    linewidths=2,
    zorder=5,
)

# Add count labels to clusters
for _, row in cluster_stats.iterrows():
    if row["count"] > 3:  # Only label clusters with more than 3 points
        ax.annotate(
            str(int(row["count"])),
            (row["lon_center"], row["lat_center"]),
            ha="center",
            va="center",
            fontsize=10,
            fontweight="bold",
            color="white",
            zorder=6,
        )

# Create legend for categories
legend_elements = [
    plt.scatter([], [], s=200, c=color, label=cat, edgecolors="white", linewidths=1) for cat, color in palette.items()
]
ax.legend(handles=legend_elements, title="Category", loc="upper left", fontsize=14, title_fontsize=16, framealpha=0.9)

# Styling
ax.set_xlabel("Longitude", fontsize=20)
ax.set_ylabel("Latitude", fontsize=20)
ax.set_title("map-marker-clustered · seaborn · pyplots.ai", fontsize=24, fontweight="bold")
ax.tick_params(axis="both", labelsize=16)

# Add subtle grid for geographic reference
ax.grid(True, alpha=0.3, linestyle="--")

# Add note about static visualization
ax.text(
    0.98,
    0.02,
    f"{n_points} locations · {len(cluster_stats)} clusters",
    transform=ax.transAxes,
    fontsize=12,
    ha="right",
    va="bottom",
    style="italic",
    alpha=0.7,
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
