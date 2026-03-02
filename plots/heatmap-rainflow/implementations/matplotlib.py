""" pyplots.ai
heatmap-rainflow: Rainflow Counting Matrix for Fatigue Analysis
Library: matplotlib 3.10.8 | Python 3.14.3
Quality: 86/100 | Created: 2026-03-02
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm


# Data - simulate rainflow counting results from a variable-amplitude fatigue signal
np.random.seed(42)

n_amp_bins = 20
n_mean_bins = 20
amp_edges = np.linspace(0, 200, n_amp_bins + 1)
mean_edges = np.linspace(-50, 250, n_mean_bins + 1)
amp_centers = (amp_edges[:-1] + amp_edges[1:]) / 2
mean_centers = (mean_edges[:-1] + mean_edges[1:]) / 2

mean_grid, amp_grid = np.meshgrid(mean_centers, amp_centers)

# Realistic pattern: dominant cycles at low amplitude near mean load (~100 MPa)
raw_counts = 3000 * np.exp(-amp_grid / 30) * np.exp(-((mean_grid - 100) ** 2) / (2 * 50**2))

# Secondary cluster from occasional overload events
raw_counts += 400 * np.exp(-((amp_grid - 70) ** 2) / (2 * 20**2)) * np.exp(-((mean_grid - 160) ** 2) / (2 * 30**2))

# Discretize to integer counts
cycle_counts = np.round(raw_counts).astype(int)
cycle_counts = np.clip(cycle_counts, 0, None)

# Mask zero-count bins for visual distinction
masked_counts = np.ma.masked_where(cycle_counts == 0, cycle_counts)

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

im = ax.pcolormesh(
    mean_edges, amp_edges, masked_counts, cmap="inferno", norm=LogNorm(vmin=1, vmax=cycle_counts.max()), shading="flat"
)

ax.set_facecolor("#f5f5f5")

# Colorbar
cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03, aspect=30)
cbar.ax.tick_params(labelsize=16)
cbar.set_label("Cycle Count", fontsize=20, labelpad=12)
cbar.outline.set_visible(False)

# Style
ax.set_xlabel("Mean Stress (MPa)", fontsize=20)
ax.set_ylabel("Stress Amplitude (MPa)", fontsize=20)
ax.set_title("heatmap-rainflow · matplotlib · pyplots.ai", fontsize=24, fontweight="medium")
ax.tick_params(axis="both", labelsize=16)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
