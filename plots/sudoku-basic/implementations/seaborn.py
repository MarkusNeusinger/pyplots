""" pyplots.ai
sudoku-basic: Basic Sudoku Grid
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 95/100 | Created: 2025-12-22
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Data - partially filled Sudoku puzzle
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

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))
sns.set_style("white")

# White background for the grid
ax.set_facecolor("white")
ax.set_xlim(-0.5, 8.5)
ax.set_ylim(-0.5, 8.5)
ax.set_aspect("equal")

# Draw thin lines for individual cells
for i in range(10):
    linewidth = 1.5
    ax.axhline(y=i - 0.5, color="black", linewidth=linewidth)
    ax.axvline(x=i - 0.5, color="black", linewidth=linewidth)

# Draw thick lines for 3x3 box boundaries
for i in range(0, 10, 3):
    linewidth = 4
    ax.axhline(y=i - 0.5, color="black", linewidth=linewidth)
    ax.axvline(x=i - 0.5, color="black", linewidth=linewidth)

# Add numbers to cells (invert y for correct orientation: row 0 at top)
for row in range(9):
    for col in range(9):
        value = grid[row, col]
        if value != 0:
            ax.text(
                col,
                8 - row,  # Invert y-axis so row 0 is at top
                str(value),
                ha="center",
                va="center",
                fontsize=36,
                fontweight="bold",
                color="black",
                fontfamily="monospace",
            )

# Remove axis labels and ticks (clean sudoku grid)
ax.set_xticks([])
ax.set_yticks([])
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["left"].set_visible(False)

# Title
ax.set_title("sudoku-basic · seaborn · pyplots.ai", fontsize=28, fontweight="bold", pad=20)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
