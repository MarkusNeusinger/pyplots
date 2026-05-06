""" anyplot.ai
heatmap-annotated: Annotated Heatmap
Library: matplotlib 3.10.9 | Python 3.13.13
Quality: 84/100 | Updated: 2026-05-06
"""

import os

import matplotlib.pyplot as plt
import numpy as np


# Theme tokens
THEME = os.getenv("ANYPLOT_THEME", "light")
PAGE_BG = "#FAF8F1" if THEME == "light" else "#1A1A17"
ELEVATED_BG = "#FFFDF6" if THEME == "light" else "#242420"
INK = "#1A1A17" if THEME == "light" else "#F0EFE8"
INK_SOFT = "#4A4A44" if THEME == "light" else "#B8B7B0"

# Data: Laboratory measurement correlations
np.random.seed(42)
measurements = ["Temperature", "pH", "Viscosity", "Density", "Turbidity", "Conductivity", "Salinity", "Pressure"]
n = len(measurements)

# Generate a realistic correlation matrix (symmetric, diagonal = 1)
base = np.random.randn(n, n) * 0.3
correlation = (base + base.T) / 2
np.fill_diagonal(correlation, 1.0)
correlation = np.clip(correlation, -1, 1)

# Add realistic scientific correlations
correlation[0, 1] = correlation[1, 0] = -0.68  # Temperature-pH: negative
correlation[0, 2] = correlation[2, 0] = 0.55  # Temperature-Viscosity: positive
correlation[3, 5] = correlation[5, 3] = 0.77  # Density-Conductivity: strong positive
correlation[4, 5] = correlation[5, 4] = -0.62  # Turbidity-Conductivity: negative
correlation[6, 7] = correlation[7, 6] = 0.81  # Salinity-Pressure: strong positive
correlation[1, 4] = correlation[4, 1] = 0.45  # pH-Turbidity: positive

# Create plot (square format for heatmap)
fig, ax = plt.subplots(figsize=(12, 12), facecolor=PAGE_BG)
ax.set_facecolor(PAGE_BG)

# Create heatmap with diverging colormap
im = ax.imshow(correlation, cmap="BrBG", vmin=-1, vmax=1, aspect="equal")

# Add colorbar with theme-adaptive styling
cbar = ax.figure.colorbar(im, ax=ax, shrink=0.8, aspect=30)
cbar.ax.tick_params(labelsize=16, colors=INK_SOFT)
cbar.ax.set_facecolor(PAGE_BG)
cbar.set_label("Correlation Coefficient", fontsize=18, labelpad=15, color=INK)
cbar.outline.set_edgecolor(INK_SOFT)
cbar.outline.set_linewidth(1)

# Set ticks and labels
ax.set_xticks(np.arange(n))
ax.set_yticks(np.arange(n))
ax.set_xticklabels(measurements, fontsize=16, color=INK_SOFT)
ax.set_yticklabels(measurements, fontsize=16, color=INK_SOFT)

# Rotate x-axis labels for readability
plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

# Add text annotations in each cell
for i in range(n):
    for j in range(n):
        value = correlation[i, j]
        # Choose text color based on background intensity
        text_color = INK if abs(value) > 0.5 else INK_SOFT
        ax.text(j, i, f"{value:.2f}", ha="center", va="center", color=text_color, fontsize=14, fontweight="bold")

# Styling
ax.set_title("heatmap-annotated · matplotlib · anyplot.ai", fontsize=24, pad=20, color=INK)
ax.set_xlabel("Laboratory Measurements", fontsize=20, labelpad=15, color=INK)
ax.set_ylabel("Laboratory Measurements", fontsize=20, labelpad=15, color=INK)

# Add subtle grid between cells
ax.set_xticks(np.arange(n + 1) - 0.5, minor=True)
ax.set_yticks(np.arange(n + 1) - 0.5, minor=True)
ax.grid(which="minor", color=INK_SOFT, linestyle="-", linewidth=1, alpha=0.3)
ax.tick_params(which="minor", bottom=False, left=False)

plt.tight_layout()
plt.savefig(f"plot-{THEME}.png", dpi=300, bbox_inches="tight", facecolor=PAGE_BG)
