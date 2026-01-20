""" pyplots.ai
map-marker-clustered: Clustered Marker Map
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 82/100 | Created: 2026-01-20
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster import AgglomerativeClustering


# Generate sample geographic data - business locations across NYC region
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

# Set seaborn context and style for the entire plot
sns.set_theme(style="whitegrid", context="talk", font_scale=1.2)

# Use colorblind-friendly palette from seaborn
palette = sns.color_palette("colorblind", n_colors=4)
category_palette = dict(zip(category_names, palette, strict=True))

# Create the plot
fig, ax = plt.subplots(figsize=(16, 9))

# Plot individual points as background layer using seaborn scatterplot
sns.scatterplot(
    data=df, x="lon", y="lat", hue="category", palette=category_palette, s=40, alpha=0.3, ax=ax, legend=False
)

# Create cluster dataframe for seaborn visualization
cluster_stats["size_scaled"] = cluster_stats["count"] * 20
cluster_stats["color"] = cluster_stats["dominant_category"].map(category_palette)

# Plot cluster markers using seaborn scatterplot with size encoding
sns.scatterplot(
    data=cluster_stats,
    x="lon_center",
    y="lat_center",
    size="count",
    hue="dominant_category",
    palette=category_palette,
    sizes=(100, 800),
    alpha=0.85,
    edgecolor="white",
    linewidth=2,
    ax=ax,
    legend=False,
)

# Add count labels to larger clusters
for _, row in cluster_stats.iterrows():
    if row["count"] > 4:
        ax.annotate(
            str(int(row["count"])),
            (row["lon_center"], row["lat_center"]),
            ha="center",
            va="center",
            fontsize=11,
            fontweight="bold",
            color="white",
            zorder=10,
        )

# Create custom legend with seaborn styling
handles = [
    plt.scatter([], [], s=250, c=[category_palette[cat]], label=cat, edgecolors="white", linewidths=1.5)
    for cat in category_names
]
legend = ax.legend(
    handles=handles,
    title="Business Type",
    loc="lower right",
    fontsize=14,
    title_fontsize=16,
    framealpha=0.95,
    edgecolor="gray",
)
legend.get_frame().set_linewidth(1.5)

# Styling with seaborn-friendly axis formatting
ax.set_xlabel("Longitude (°)", fontsize=20)
ax.set_ylabel("Latitude (°)", fontsize=20)
ax.set_title("map-marker-clustered · seaborn · pyplots.ai", fontsize=24, fontweight="bold", pad=15)
ax.tick_params(axis="both", labelsize=16)

# Customize grid using seaborn despine and grid settings
sns.despine(ax=ax, left=False, bottom=False)
ax.grid(True, alpha=0.3, linestyle="--", color="gray")

# Add annotation about clustering
ax.text(
    0.02,
    0.02,
    f"{n_points} locations · {len(cluster_stats)} clusters",
    transform=ax.transAxes,
    fontsize=13,
    ha="left",
    va="bottom",
    style="italic",
    color="dimgray",
    bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "alpha": 0.8, "edgecolor": "lightgray"},
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
