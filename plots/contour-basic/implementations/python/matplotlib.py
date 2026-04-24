""" anyplot.ai
contour-basic: Basic Contour Plot
Library: matplotlib 3.10.9 | Python 3.14.4
Quality: 87/100 | Updated: 2026-04-24
"""

import os

import matplotlib.pyplot as plt
import numpy as np


# Theme tokens
THEME = os.getenv("ANYPLOT_THEME", "light")
PAGE_BG = "#FAF8F1" if THEME == "light" else "#1A1A17"
INK = "#1A1A17" if THEME == "light" else "#F0EFE8"
INK_SOFT = "#4A4A44" if THEME == "light" else "#B8B7B0"

# Data — simulated topographic elevation map of a 10km x 10km mountain region
x = np.linspace(0, 10, 80)
y = np.linspace(0, 10, 80)
X, Y = np.meshgrid(x, y)

elevation = (
    850 * np.exp(-((X - 7) ** 2 + (Y - 7) ** 2) / 4.0)
    + 550 * np.exp(-((X - 2.5) ** 2 + (Y - 3) ** 2) / 3.0)
    - 180 * np.exp(-((X - 5) ** 2 + (Y - 5) ** 2) / 8.0)
    + 12 * X
    + 350
)

# Plot
fig, ax = plt.subplots(figsize=(16, 9), facecolor=PAGE_BG)
ax.set_facecolor(PAGE_BG)

levels = np.arange(300, 1251, 50)
major_levels = np.arange(400, 1251, 200)

filled = ax.contourf(X, Y, elevation, levels=levels, cmap="viridis")
ax.contour(X, Y, elevation, levels=levels, colors="white", linewidths=0.6, alpha=0.30)
major = ax.contour(X, Y, elevation, levels=major_levels, colors="white", linewidths=1.8, alpha=0.85)
ax.clabel(major, inline=True, fontsize=13, fmt="%d m", inline_spacing=8)

# Colorbar
cbar = fig.colorbar(filled, ax=ax, shrink=0.9, aspect=28, pad=0.02)
cbar.set_label("Elevation (m)", fontsize=20, color=INK)
cbar.ax.tick_params(labelsize=16, colors=INK_SOFT)
cbar.outline.set_edgecolor(INK_SOFT)
cbar.outline.set_linewidth(0.6)

# Style
ax.set_xlabel("Distance East (km)", fontsize=20, color=INK)
ax.set_ylabel("Distance North (km)", fontsize=20, color=INK)
ax.set_title(
    "Mountain Terrain · contour-basic · matplotlib · anyplot.ai", fontsize=24, fontweight="medium", color=INK, pad=16
)
ax.tick_params(axis="both", labelsize=16, colors=INK_SOFT)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)
for spine in ("left", "bottom"):
    ax.spines[spine].set_color(INK_SOFT)
ax.set_aspect("equal")

plt.tight_layout()
plt.savefig(f"plot-{THEME}.png", dpi=300, bbox_inches="tight", facecolor=PAGE_BG)
