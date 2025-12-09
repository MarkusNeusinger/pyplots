"""
ridgeline-basic: Ridgeline Plot
Library: matplotlib
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - Monthly temperature distributions
np.random.seed(42)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Generate temperature data with seasonal variation
temperature_data = []
base_temps = [2, 4, 8, 13, 17, 21, 24, 23, 19, 13, 7, 3]
for i in range(len(months)):
    temperature_data.append(np.random.normal(base_temps[i], 4, 200))

# Color palette - gradient from cool to warm
colors = [
    "#306998",
    "#3A7CA5",
    "#4A90B2",
    "#5BA4BF",
    "#7BB8C9",
    "#9CCCD3",
    "#FFD43B",
    "#FFCC33",
    "#F9B926",
    "#F9A619",
    "#F97316",
    "#DC2626",
]

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))

# X-axis range for KDE
x_range = np.linspace(-10, 35, 500)

# KDE bandwidth (Silverman's rule-of-thumb)
bandwidth = 2.0

# Overlap factor and scale
overlap = 0.25
scale = 0.85

# Plot each distribution from top to bottom
for i, month in enumerate(reversed(months)):
    idx = len(months) - 1 - i
    data = temperature_data[idx]

    # Compute Gaussian KDE (inline, no scipy)
    n = len(data)
    density = np.zeros_like(x_range)
    for d in data:
        density += np.exp(-0.5 * ((x_range - d) / bandwidth) ** 2)
    density /= n * bandwidth * np.sqrt(2 * np.pi)

    # Normalize density
    density = density / density.max() * scale

    # Vertical offset
    offset = i * overlap

    # Plot filled density
    ax.fill_between(x_range, offset, density + offset, alpha=0.7, color=colors[idx], edgecolor="white", linewidth=1.5)

    # Add month label
    ax.text(-12, offset + 0.15, month, fontsize=16, fontweight="bold", va="center", ha="right")

# Styling
ax.set_xlabel("Temperature (°C)", fontsize=20)
ax.set_title("Monthly Temperature Distribution", fontsize=20, fontweight="bold", pad=20)

# Clean up axes
ax.set_xlim(-15, 35)
ax.set_ylim(-0.1, len(months) * overlap + scale + 0.1)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.set_yticks([])
ax.tick_params(axis="x", labelsize=16)

# Add subtle grid on x-axis only
ax.xaxis.grid(True, alpha=0.3, linestyle="--")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
