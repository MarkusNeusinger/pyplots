""" pyplots.ai
scatter-streaming: Streaming Scatter Plot
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 91/100 | Created: 2026-01-19
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Data - Simulated sensor readings arriving over time
np.random.seed(42)
n_points = 200  # Buffer of visible points

# Generate timestamps over a 60-second window
timestamps = pd.date_range("2025-01-19 10:00:00", periods=n_points, freq="300ms")

# Simulated sensor data: temperature vs humidity with some correlation and drift
base_temp = 22  # Base temperature in Celsius
base_humidity = 45  # Base humidity percentage

# Add gradual drift and random variation to simulate real sensor data
time_idx = np.arange(n_points)
temperature = base_temp + 0.02 * time_idx + np.random.randn(n_points) * 1.5
humidity = base_humidity + 0.015 * time_idx + 0.3 * (temperature - base_temp) + np.random.randn(n_points) * 3

# Calculate point age for opacity (newer = more opaque)
# Normalize age from 0 (oldest) to 1 (newest)
point_age = np.linspace(0, 1, n_points)
alpha_values = 0.15 + 0.85 * point_age  # Range from 0.15 to 1.0

# Color based on recency - newer points are brighter blue
colors = plt.cm.Blues(0.3 + 0.7 * point_age)

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

# Draw points with varying alpha to show temporal flow
# Older points first (background), newer points on top
for i in range(n_points):
    ax.scatter(
        temperature[i],
        humidity[i],
        s=150 + 100 * point_age[i],  # Newer points slightly larger
        c=[colors[i]],
        alpha=alpha_values[i],
        edgecolors="none",
        zorder=i + 1,
    )

# Add arrow indicating data flow direction (time progression)
ax.annotate(
    "",
    xy=(temperature[-1], humidity[-1]),
    xytext=(temperature[-15], humidity[-15]),
    arrowprops={"arrowstyle": "->", "color": "#306998", "lw": 2.5, "mutation_scale": 20},
    zorder=n_points + 10,
)

# Mark the most recent point with emphasis
ax.scatter(
    temperature[-1],
    humidity[-1],
    s=400,
    c="#FFD43B",
    edgecolors="#306998",
    linewidths=3,
    zorder=n_points + 20,
    label="Latest reading",
)

# Add subtle trail effect annotation
ax.text(
    0.02,
    0.98,
    f"Buffer: {n_points} points | Stream rate: ~3 pts/sec",
    transform=ax.transAxes,
    fontsize=14,
    verticalalignment="top",
    color="#666666",
    style="italic",
)

# Labels and styling
ax.set_xlabel("Temperature (°C)", fontsize=20)
ax.set_ylabel("Humidity (%)", fontsize=20)
ax.set_title("scatter-streaming · matplotlib · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, linestyle="--")
ax.legend(fontsize=16, loc="lower right")

# Add colorbar to show temporal encoding
sm = plt.cm.ScalarMappable(cmap=plt.cm.Blues, norm=plt.Normalize(0, 60))
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, shrink=0.8, aspect=30, pad=0.02)
cbar.set_label("Time (seconds ago)", fontsize=16)
cbar.ax.tick_params(labelsize=14)
cbar.ax.invert_yaxis()  # 0 at top = most recent

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
