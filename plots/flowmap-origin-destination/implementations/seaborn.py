"""pyplots.ai
flowmap-origin-destination: Origin-Destination Flow Map
Library: seaborn | Python 3.13
Quality: pending | Created: 2026-01-16
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data: Migration flows between major world cities
np.random.seed(42)

cities = {
    "New York": (40.71, -74.01),
    "London": (51.51, -0.13),
    "Tokyo": (35.68, 139.69),
    "Sydney": (-33.87, 151.21),
    "Dubai": (25.20, 55.27),
    "Singapore": (1.35, 103.82),
    "Paris": (48.86, 2.35),
    "Los Angeles": (34.05, -118.24),
    "Hong Kong": (22.32, 114.17),
    "Frankfurt": (50.11, 8.68),
    "Mumbai": (19.08, 72.88),
    "Sao Paulo": (-23.55, -46.63),
}

# Create flow data between cities
flows = [
    ("New York", "London", 850),
    ("New York", "Los Angeles", 720),
    ("London", "Paris", 580),
    ("London", "Dubai", 450),
    ("Tokyo", "Hong Kong", 620),
    ("Tokyo", "Singapore", 480),
    ("Sydney", "Singapore", 390),
    ("Dubai", "Mumbai", 510),
    ("Los Angeles", "Tokyo", 340),
    ("Paris", "Frankfurt", 420),
    ("Hong Kong", "Singapore", 550),
    ("New York", "Sao Paulo", 280),
    ("London", "Frankfurt", 380),
    ("Singapore", "Sydney", 310),
    ("Mumbai", "Dubai", 460),
    ("Frankfurt", "Dubai", 290),
    ("Paris", "New York", 410),
    ("Tokyo", "Los Angeles", 370),
]

df_flows = pd.DataFrame(flows, columns=["origin", "destination", "flow"])
df_flows["origin_lat"] = df_flows["origin"].map(lambda x: cities[x][0])
df_flows["origin_lon"] = df_flows["origin"].map(lambda x: cities[x][1])
df_flows["dest_lat"] = df_flows["destination"].map(lambda x: cities[x][0])
df_flows["dest_lon"] = df_flows["destination"].map(lambda x: cities[x][1])

# Normalize flow for line width
max_flow = df_flows["flow"].max()
df_flows["width"] = df_flows["flow"] / max_flow * 4 + 0.5

# City dataframe for scatter plot
df_cities = pd.DataFrame([{"city": name, "lat": coords[0], "lon": coords[1]} for name, coords in cities.items()])

# Plot
sns.set_context("talk", font_scale=1.2)
fig, ax = plt.subplots(figsize=(16, 9))
ax.set_facecolor("#f0f4f8")

# Set map bounds
ax.set_xlim(-180, 180)
ax.set_ylim(-60, 80)

# Color palette based on flow intensity
colors = sns.color_palette("YlOrRd", n_colors=len(df_flows))
sorted_indices = df_flows["flow"].argsort()

# Draw curved arcs for each flow
for idx, row in df_flows.iterrows():
    color_idx = sorted_indices.tolist().index(idx)
    color = colors[color_idx]

    # Create curved arc using FancyArrowPatch
    path = mpatches.FancyArrowPatch(
        (row["origin_lon"], row["origin_lat"]),
        (row["dest_lon"], row["dest_lat"]),
        connectionstyle="arc3,rad=0.2",
        arrowstyle="-",
        linewidth=row["width"],
        color=color,
        alpha=0.6,
        zorder=1,
    )
    ax.add_patch(path)

# Plot cities using seaborn scatterplot
sns.scatterplot(
    data=df_cities, x="lon", y="lat", s=300, color="#306998", edgecolor="white", linewidth=2, ax=ax, zorder=3
)

# Add city labels
for _, row in df_cities.iterrows():
    ax.annotate(
        row["city"],
        (row["lon"], row["lat"]),
        xytext=(5, 5),
        textcoords="offset points",
        fontsize=12,
        fontweight="bold",
        color="#333333",
        zorder=4,
    )

# Add grid for geographic reference
ax.axhline(y=0, color="#888888", linestyle="--", linewidth=0.5, alpha=0.5)
ax.axvline(x=0, color="#888888", linestyle="--", linewidth=0.5, alpha=0.5)

# Styling
ax.set_xlabel("Longitude", fontsize=20)
ax.set_ylabel("Latitude", fontsize=20)
ax.set_title("flowmap-origin-destination · seaborn · pyplots.ai", fontsize=24, fontweight="bold")
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, linestyle=":")

# Add legend for flow magnitude
sm = plt.cm.ScalarMappable(cmap="YlOrRd", norm=plt.Normalize(vmin=df_flows["flow"].min(), vmax=df_flows["flow"].max()))
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, shrink=0.6, aspect=20, pad=0.02)
cbar.set_label("Flow Volume", fontsize=16)
cbar.ax.tick_params(labelsize=14)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
