"""
waffle-basic: Basic Waffle Chart
Library: seaborn
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Data - Budget allocation percentages (sum to 100)
categories = ["Housing", "Food", "Transport", "Entertainment", "Savings"]
values = [35, 25, 20, 12, 8]  # Percentages

# Colors - Python Blue and Yellow first, then colorblind-safe colors
colors = ["#306998", "#FFD43B", "#8FBC8F", "#CD853F", "#9370DB"]

# Create 10x10 grid (100 squares)
grid_size = 10
total_squares = grid_size * grid_size

# Build waffle grid - fill row by row from bottom-left
waffle = np.zeros((grid_size, grid_size), dtype=int)
current_square = 0

for idx, value in enumerate(values):
    num_squares = int(round(value))
    for _ in range(num_squares):
        if current_square < total_squares:
            row = current_square // grid_size
            col = current_square % grid_size
            waffle[row, col] = idx
            current_square += 1

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Draw squares using seaborn-style approach with matplotlib patches
square_size = 0.9  # Size of each square (with gap)
gap = 0.1

for i in range(grid_size):
    for j in range(grid_size):
        category_idx = int(waffle[i, j])
        rect = plt.Rectangle(
            (j + gap / 2, i + gap / 2),
            square_size,
            square_size,
            facecolor=colors[category_idx],
            edgecolor="white",
            linewidth=2,
        )
        ax.add_patch(rect)

# Set axis limits and remove ticks
ax.set_xlim(0, grid_size)
ax.set_ylim(0, grid_size)
ax.set_aspect("equal")
ax.axis("off")

# Create legend with category names and percentages
legend_patches = [
    mpatches.Patch(color=colors[i], label=f"{categories[i]}: {values[i]}%") for i in range(len(categories))
]
ax.legend(
    handles=legend_patches,
    loc="center left",
    bbox_to_anchor=(1.02, 0.5),
    fontsize=18,
    frameon=True,
    fancybox=True,
    shadow=True,
)

# Title
ax.set_title("Monthly Budget Allocation · waffle-basic · seaborn · pyplots.ai", fontsize=24, pad=20)

# Apply seaborn style
sns.set_style("whitegrid")
sns.despine(left=True, bottom=True)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
