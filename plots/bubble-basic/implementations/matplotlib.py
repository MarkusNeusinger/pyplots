""" pyplots.ai
bubble-basic: Basic Bubble Chart
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 100/100 | Created: 2025-12-14
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - three correlated variables
np.random.seed(42)
n_points = 50

x = np.random.uniform(10, 100, n_points)
y = x * 0.6 + np.random.randn(n_points) * 15 + 20
size_values = np.random.uniform(50, 500, n_points)

# Scale sizes for visual perception (area-based scaling)
# Map size_values to reasonable bubble sizes for 4800x2700 canvas
size_scaled = (size_values / size_values.max()) * 2000 + 200

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

scatter = ax.scatter(x, y, s=size_scaled, alpha=0.6, c="#306998", edgecolors="#1a3d5c", linewidths=1.5)

# Create size legend
size_legend_values = [100, 250, 500]
size_legend_scaled = [(v / size_values.max()) * 2000 + 200 for v in size_legend_values]

for val, scaled in zip(size_legend_values, size_legend_scaled, strict=True):
    ax.scatter([], [], s=scaled, c="#306998", alpha=0.6, edgecolors="#1a3d5c", linewidths=1.5, label=f"{val}")

ax.legend(title="Size Value", title_fontsize=18, fontsize=16, loc="upper left", framealpha=0.9, scatterpoints=1)

# Labels and styling
ax.set_xlabel("X Value", fontsize=20)
ax.set_ylabel("Y Value", fontsize=20)
ax.set_title("bubble-basic · matplotlib · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)
ax.grid(True, alpha=0.3, linestyle="--")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
