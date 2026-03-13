""" pyplots.ai
scatter-connected-temporal: Connected Scatter Plot with Temporal Path
Library: matplotlib 3.10.8 | Python 3.14.3
Quality: 88/100 | Created: 2026-03-13
"""

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np


# Data - Phillips curve: unemployment vs inflation over 30 years
np.random.seed(42)
years = np.arange(1994, 2024)
n = len(years)

unemployment = np.zeros(n)
inflation = np.zeros(n)
unemployment[0] = 6.5
inflation[0] = 2.8

for i in range(1, n):
    cycle = np.sin(2 * np.pi * i / 10)
    unemployment[i] = unemployment[i - 1] + cycle * 0.4 + np.random.normal(0, 0.3)
    inflation[i] = inflation[i - 1] - 0.3 * (unemployment[i] - unemployment[i - 1]) + np.random.normal(0, 0.2)

unemployment = np.clip(unemployment, 3.0, 10.0)
inflation = np.clip(inflation, 0.5, 6.0)

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

cmap = plt.cm.viridis
norm = mcolors.Normalize(vmin=0, vmax=n - 1)

for i in range(n - 1):
    ax.plot(unemployment[i : i + 2], inflation[i : i + 2], color=cmap(norm(i)), linewidth=2.5, solid_capstyle="round")

ax.scatter(unemployment, inflation, c=np.arange(n), cmap="viridis", s=200, edgecolors="white", linewidth=1.0, zorder=5)

# Annotate key time points
label_indices = [0, 9, 19, n - 1]
offsets = [(12, -14), (-14, 12), (12, 10), (-14, -14)]
for idx, (dx, dy) in zip(label_indices, offsets, strict=True):
    ax.annotate(
        str(years[idx]),
        (unemployment[idx], inflation[idx]),
        textcoords="offset points",
        xytext=(dx, dy),
        fontsize=16,
        fontweight="bold",
        color=cmap(norm(idx)),
    )

# Colorbar for temporal progression
sm = plt.cm.ScalarMappable(cmap=cmap, norm=mcolors.Normalize(vmin=years[0], vmax=years[-1]))
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, pad=0.02, aspect=30, shrink=0.8)
cbar.set_label("Year", fontsize=18)
cbar.ax.tick_params(labelsize=14)

# Style
ax.set_xlabel("Unemployment Rate (%)", fontsize=20)
ax.set_ylabel("Inflation Rate (%)", fontsize=20)
ax.set_title("scatter-connected-temporal \u00b7 matplotlib \u00b7 pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, alpha=0.2, linewidth=0.8)
ax.xaxis.grid(True, alpha=0.2, linewidth=0.8)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
