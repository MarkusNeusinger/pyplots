"""pyplots.ai
map-animated-temporal: Animated Map over Time
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-01-20
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Set style
sns.set_context("talk", font_scale=1.0)
sns.set_style("whitegrid")

# Generate synthetic earthquake aftershock data over 6 time periods
np.random.seed(42)

# Simulate aftershock sequence spreading from epicenter
epicenter_lat, epicenter_lon = 35.0, -120.0
n_points_per_period = 15
n_periods = 6

data_records = []
for period in range(n_periods):
    # Spread increases over time (aftershocks diffuse outward)
    spread = 0.5 + period * 0.3
    n_points = n_points_per_period + period * 3

    lats = epicenter_lat + np.random.randn(n_points) * spread
    lons = epicenter_lon + np.random.randn(n_points) * spread
    # Magnitude decreases over time on average
    magnitudes = np.random.uniform(2.0, 5.5 - period * 0.4, n_points)

    for i in range(n_points):
        data_records.append(
            {
                "lat": lats[i],
                "lon": lons[i],
                "magnitude": magnitudes[i],
                "period": f"Day {period + 1}",
                "period_num": period,
            }
        )

df = pd.DataFrame(data_records)

# Create small multiples grid showing temporal snapshots
fig, axes = plt.subplots(2, 3, figsize=(16, 9))
axes = axes.flatten()

for idx, period in enumerate(sorted(df["period"].unique(), key=lambda x: int(x.split()[1]))):
    ax = axes[idx]
    period_data = df[df["period"] == period]

    # Plot points with size and color based on magnitude
    scatter = ax.scatter(
        period_data["lon"],
        period_data["lat"],
        c=period_data["magnitude"],
        s=period_data["magnitude"] ** 2 * 20,
        cmap="YlOrRd",
        alpha=0.7,
        edgecolors="black",
        linewidths=0.5,
        vmin=2.0,
        vmax=5.5,
    )

    # Mark epicenter
    ax.scatter(
        epicenter_lon,
        epicenter_lat,
        marker="*",
        s=400,
        c="#306998",
        edgecolors="white",
        linewidths=2,
        zorder=10,
        label="Epicenter" if idx == 0 else None,
    )

    # Set consistent axis limits for all panels
    ax.set_xlim(epicenter_lon - 3, epicenter_lon + 3)
    ax.set_ylim(epicenter_lat - 3, epicenter_lat + 3)

    # Style each subplot
    ax.set_title(period, fontsize=18, fontweight="bold")
    ax.set_xlabel("Longitude" if idx >= 3 else "", fontsize=14)
    ax.set_ylabel("Latitude" if idx % 3 == 0 else "", fontsize=14)
    ax.tick_params(axis="both", labelsize=12)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3, linestyle="--")

# Add shared colorbar
cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
cbar = fig.colorbar(scatter, cax=cbar_ax)
cbar.set_label("Magnitude", fontsize=16)
cbar.ax.tick_params(labelsize=12)

# Overall title
fig.suptitle(
    "Earthquake Aftershock Sequence · map-animated-temporal · seaborn · pyplots.ai",
    fontsize=20,
    fontweight="bold",
    y=1.02,
)

fig.subplots_adjust(left=0.06, right=0.88, top=0.92, bottom=0.08, wspace=0.25, hspace=0.3)
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
