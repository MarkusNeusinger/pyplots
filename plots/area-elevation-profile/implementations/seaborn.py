""" pyplots.ai
area-elevation-profile: Terrain Elevation Profile Along Transect
Library: seaborn 0.13.2 | Python 3.14.3
Quality: 86/100 | Created: 2026-03-15
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap


# Data
np.random.seed(42)

total_distance = 120
n_points = 480
distance = np.linspace(0, total_distance, n_points)

base_profile = (
    800
    + 600 * np.sin(distance / total_distance * np.pi * 0.8)
    + 400 * np.sin(distance / total_distance * np.pi * 2.5 + 0.5)
    + 200 * np.sin(distance / total_distance * np.pi * 5 + 1.2)
    + 150 * np.cos(distance / total_distance * np.pi * 3.8)
)
noise = np.cumsum(np.random.normal(0, 2, n_points))
noise -= np.linspace(noise[0], noise[-1], n_points)
elevation = base_profile + noise
elevation = np.clip(elevation, 400, None)

df = pd.DataFrame({"distance_km": distance, "elevation_m": elevation})

landmarks = pd.DataFrame(
    {
        "name": ["Trailhead", "North Peak", "Lake Valley", "Ridge Pass", "River Crossing", "Summit", "End Station"],
        "distance_km": [0.0, 8.0, 28.0, 52.0, 75.0, 105.0, 120.0],
    }
)
landmark_elevations = []
for d in landmarks["distance_km"]:
    idx = np.argmin(np.abs(distance - d))
    landmark_elevations.append(elevation[idx])
landmarks["elevation_m"] = landmark_elevations

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

sns.lineplot(data=df, x="distance_km", y="elevation_m", ax=ax, color="#306998", linewidth=2.5, legend=False)

cmap = LinearSegmentedColormap.from_list("terrain_fill", ["#a8c686", "#5a8a3c", "#306998"])
y_min = ax.get_ylim()[0]
n_bands = 80
elev_min_val = elevation.min()
elev_max_val = elevation.max()
for i in range(n_bands):
    frac_low = i / n_bands
    frac_high = (i + 1) / n_bands
    band_low = elev_min_val + frac_low * (elev_max_val - elev_min_val)
    band_high = elev_min_val + frac_high * (elev_max_val - elev_min_val)
    clipped = np.clip(elevation, band_low, band_high)
    bottom = np.full_like(distance, band_low)
    color = cmap(frac_low)
    ax.fill_between(distance, bottom, clipped, color=color, alpha=0.85, linewidth=0)

ax.fill_between(distance, y_min, np.full_like(distance, elev_min_val), color="#a8c686", alpha=0.85, linewidth=0)

# Landmarks
for _, lm in landmarks.iterrows():
    ax.vlines(lm["distance_km"], y_min, lm["elevation_m"], color="#555555", linewidth=1, linestyle="--", alpha=0.5)
    label_text = f"{lm['name']}\n{int(lm['elevation_m'])} m"
    y_offset = 60 if lm["elevation_m"] < (elev_max_val - 200) else -120
    ax.annotate(
        label_text,
        xy=(lm["distance_km"], lm["elevation_m"]),
        xytext=(0, y_offset),
        textcoords="offset points",
        fontsize=11,
        fontweight="bold",
        color="#333333",
        ha="center",
        va="bottom" if y_offset > 0 else "top",
        bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "edgecolor": "#cccccc", "alpha": 0.85},
    )
    ax.plot(
        lm["distance_km"],
        lm["elevation_m"],
        "o",
        color="#306998",
        markersize=8,
        markeredgecolor="white",
        markeredgewidth=1.5,
        zorder=5,
    )

# Style
ax.set_xlabel("Distance (km)", fontsize=20)
ax.set_ylabel("Elevation (m)", fontsize=20)
ax.set_title("area-elevation-profile · seaborn · pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8)
ax.set_xlim(0, total_distance)

note_text = "Vertical exaggeration ~10×"
ax.text(0.98, 0.02, note_text, transform=ax.transAxes, fontsize=12, color="#888888", ha="right", va="bottom")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
