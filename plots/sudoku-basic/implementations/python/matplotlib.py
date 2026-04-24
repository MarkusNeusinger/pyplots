"""anyplot.ai
sudoku-basic: Basic Sudoku Grid
Library: matplotlib | Python 3.13
Quality: pending | Updated: 2026-04-24
"""

import os

import matplotlib.pyplot as plt
import numpy as np


# Theme tokens
THEME = os.getenv("ANYPLOT_THEME", "light")
PAGE_BG = "#FAF8F1" if THEME == "light" else "#1A1A17"
INK = "#1A1A17" if THEME == "light" else "#F0EFE8"

# Data - A partially filled Sudoku puzzle (0 = empty cell)
grid = np.array(
    [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
)

# Plot (square canvas: 3600x3600 px at dpi=300)
fig, ax = plt.subplots(figsize=(12, 12), facecolor=PAGE_BG)
ax.set_facecolor(PAGE_BG)
ax.set_aspect("equal")
ax.set_xlim(-0.15, 9.15)
ax.set_ylim(-0.15, 9.15)

# Thin lines for individual cell boundaries
for i in range(10):
    ax.plot([0, 9], [i, i], color=INK, linewidth=1.5, zorder=1)
    ax.plot([i, i], [0, 9], color=INK, linewidth=1.5, zorder=1)

# Thick lines for 3x3 box boundaries
for i in range(0, 10, 3):
    ax.plot([0, 9], [i, i], color=INK, linewidth=5, zorder=2, solid_capstyle="projecting")
    ax.plot([i, i], [0, 9], color=INK, linewidth=5, zorder=2, solid_capstyle="projecting")

# Numbers centered in cells
for i in range(9):
    for j in range(9):
        value = grid[i, j]
        if value != 0:
            ax.text(
                j + 0.5,
                8 - i + 0.5,
                str(value),
                fontsize=42,
                fontweight="bold",
                color=INK,
                ha="center",
                va="center",
                zorder=3,
            )

# Style - hide axes, ticks, and spines (grid itself is the visual frame)
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

ax.set_title("sudoku-basic · matplotlib · anyplot.ai", fontsize=24, fontweight="medium", color=INK, pad=28)

plt.tight_layout()
plt.savefig(f"plot-{THEME}.png", dpi=300, bbox_inches="tight", facecolor=PAGE_BG)
