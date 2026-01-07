"""pyplots.ai
line-animated-progressive: Animated Line Plot Over Time
Library: matplotlib | Python 3.13
Quality: pending | Created: 2026-01-07
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap


# Data - Monthly temperature data over 5 years showing seasonal patterns
np.random.seed(42)
n_points = 60  # 5 years of monthly data

# Create numeric time axis (representing months)
months_numeric = np.arange(n_points)

# Create temperature data with seasonal pattern and trend
base_temp = 15  # Average temperature in Celsius
seasonal = 10 * np.sin(2 * np.pi * months_numeric / 12 - np.pi / 2)  # Seasonal variation
trend = 0.02 * months_numeric  # Slight warming trend
noise = np.random.randn(n_points) * 1.5
temperatures = base_temp + seasonal + trend + noise

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Create gradient colormap from light to Python Blue
colors = ["#c4d9ed", "#306998"]  # Light blue to Python Blue
cmap = LinearSegmentedColormap.from_list("progressive", colors, N=256)

# Create line segments for gradient effect (progressive reveal)
points = np.array([months_numeric, temperatures]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

# Normalize colors based on position (left to right)
norm = plt.Normalize(0, n_points - 1)
lc = LineCollection(segments, cmap=cmap, norm=norm, linewidths=4, capstyle="round")
lc.set_array(np.arange(n_points - 1))
ax.add_collection(lc)

# Add markers that grow in size along the progression
marker_sizes = np.linspace(30, 200, n_points)
marker_colors = cmap(np.linspace(0, 1, n_points))

for i in range(n_points):
    ax.scatter(
        months_numeric[i],
        temperatures[i],
        s=marker_sizes[i],
        c=[marker_colors[i]],
        zorder=3,
        edgecolors="white",
        linewidths=1,
    )

# Highlight the final point with glow effect
ax.scatter(
    months_numeric[-1], temperatures[-1], s=400, c="#FFD43B", zorder=5, edgecolors="#306998", linewidths=3, marker="o"
)
ax.scatter(months_numeric[-1], temperatures[-1], s=600, c="#FFD43B", alpha=0.3, zorder=4)

# Add arrow indicator showing progression direction
ax.annotate(
    "",
    xy=(months_numeric[-1] + 2, temperatures[-1]),
    xytext=(months_numeric[-1], temperatures[-1]),
    arrowprops={"arrowstyle": "->", "color": "#306998", "lw": 3},
)

# Set axis limits
ax.set_xlim(-2, n_points + 3)
ax.set_ylim(temperatures.min() - 5, temperatures.max() + 5)

# X-axis with year labels
year_ticks = [0, 12, 24, 36, 48]
year_labels = ["2020", "2021", "2022", "2023", "2024"]
ax.set_xticks(year_ticks)
ax.set_xticklabels(year_labels)

# Labels and styling
ax.set_xlabel("Year", fontsize=20)
ax.set_ylabel("Temperature (°C)", fontsize=20)
ax.set_title("Monthly Temperature Readings · line-animated-progressive · matplotlib · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, linestyle="--")

# Add text annotation explaining the visualization
ax.text(
    0.02,
    0.98,
    "Progressive reveal: gradient shows temporal direction →",
    transform=ax.transAxes,
    fontsize=14,
    verticalalignment="top",
    bbox={"boxstyle": "round", "facecolor": "white", "alpha": 0.8, "edgecolor": "#306998"},
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
