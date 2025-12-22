"""pyplots.ai
sudoku-basic: Basic Sudoku Grid
Library: matplotlib | Python 3.13
Quality: pending | Created: 2025-12-22
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - A partially filled Sudoku puzzle
# 0 represents empty cells
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

# Create figure (4800x2700 px at 300 dpi)
fig, ax = plt.subplots(figsize=(16, 9))

# Set equal aspect ratio for square cells
ax.set_aspect("equal")

# Set axis limits with padding for the grid
ax.set_xlim(-0.5, 9.5)
ax.set_ylim(-0.5, 9.5)

# Draw cell backgrounds (white)
for i in range(9):
    for j in range(9):
        rect = plt.Rectangle((j, 8 - i), 1, 1, facecolor="white", edgecolor="none")
        ax.add_patch(rect)

# Draw thin lines for individual cells
for i in range(10):
    # Horizontal lines
    ax.axhline(y=i, xmin=0, xmax=1, color="#306998", linewidth=1.5, clip_on=False, zorder=1)
    ax.plot([0, 9], [i, i], color="#306998", linewidth=1.5, zorder=1)
    # Vertical lines
    ax.plot([i, i], [0, 9], color="#306998", linewidth=1.5, zorder=1)

# Draw thick lines for 3x3 box boundaries
for i in range(0, 10, 3):
    ax.plot([0, 9], [i, i], color="#306998", linewidth=5, zorder=2)
    ax.plot([i, i], [0, 9], color="#306998", linewidth=5, zorder=2)

# Add numbers to cells
for i in range(9):
    for j in range(9):
        value = grid[i, j]
        if value != 0:
            # Center number in cell (j + 0.5 for x, 8-i + 0.5 for y to flip grid)
            ax.text(
                j + 0.5,
                8 - i + 0.5,
                str(value),
                fontsize=36,
                fontweight="bold",
                color="#306998",
                ha="center",
                va="center",
                zorder=3,
            )

# Remove axes and ticks
ax.set_xticks([])
ax.set_yticks([])
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["left"].set_visible(False)

# Add title
ax.set_title("sudoku-basic · matplotlib · pyplots.ai", fontsize=28, fontweight="bold", color="#306998", pad=20)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
