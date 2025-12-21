""" pyplots.ai
ternary-basic: Basic Ternary Plot
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 95/100 | Created: 2025-12-17
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - Soil composition samples (sand, silt, clay summing to 100%)
np.random.seed(42)
n_points = 50

# Generate random compositions that sum to 100
raw = np.random.dirichlet([2, 2, 2], n_points) * 100
sand = raw[:, 0]  # Component A
silt = raw[:, 1]  # Component B
clay = raw[:, 2]  # Component C


# Convert ternary coordinates to Cartesian (equilateral triangle)
def ternary_to_cartesian(a, b, c):
    """Convert ternary (a, b, c) to Cartesian (x, y).
    Triangle vertices: A at top, B at bottom-left, C at bottom-right.
    """
    total = a + b + c
    a, b, c = a / total, b / total, c / total
    x = 0.5 * (2 * c + a)
    y = (np.sqrt(3) / 2) * a
    return x, y


# Convert all points
x_points, y_points = ternary_to_cartesian(sand, silt, clay)

# Triangle vertices (A=top, B=bottom-left, C=bottom-right)
triangle_x = [0.5, 0, 1, 0.5]
triangle_y = [np.sqrt(3) / 2, 0, 0, np.sqrt(3) / 2]

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Draw triangle outline
ax.plot(triangle_x, triangle_y, color="black", linewidth=2)

# Draw grid lines at 20% intervals
grid_levels = [0.2, 0.4, 0.6, 0.8]
grid_alpha = 0.3
grid_color = "gray"

for level in grid_levels:
    # Lines parallel to each edge
    # Lines parallel to BC (bottom edge) - constant A
    a_const = level
    b_start, c_start = 0, 1 - a_const
    b_end, c_end = 1 - a_const, 0
    x1, y1 = ternary_to_cartesian(a_const, b_start, c_start)
    x2, y2 = ternary_to_cartesian(a_const, b_end, c_end)
    ax.plot([x1, x2], [y1, y2], color=grid_color, alpha=grid_alpha, linewidth=1, linestyle="--")

    # Lines parallel to AC (right edge) - constant B
    b_const = level
    a_start, c_start = 0, 1 - b_const
    a_end, c_end = 1 - b_const, 0
    x1, y1 = ternary_to_cartesian(a_start, b_const, c_start)
    x2, y2 = ternary_to_cartesian(a_end, b_const, c_end)
    ax.plot([x1, x2], [y1, y2], color=grid_color, alpha=grid_alpha, linewidth=1, linestyle="--")

    # Lines parallel to AB (left edge) - constant C
    c_const = level
    a_start, b_start = 0, 1 - c_const
    a_end, b_end = 1 - c_const, 0
    x1, y1 = ternary_to_cartesian(a_start, b_start, c_const)
    x2, y2 = ternary_to_cartesian(a_end, b_end, c_const)
    ax.plot([x1, x2], [y1, y2], color=grid_color, alpha=grid_alpha, linewidth=1, linestyle="--")

# Add tick labels at 20% intervals along each edge
tick_fontsize = 14
tick_offset = 0.05

for level in [0, 20, 40, 60, 80, 100]:
    frac = level / 100

    # Sand axis (A) - along left edge, reading from bottom to top
    x_tick, y_tick = ternary_to_cartesian(frac, 1 - frac, 0)
    ax.text(x_tick - tick_offset, y_tick, f"{level}", fontsize=tick_fontsize, ha="right", va="center")

    # Silt axis (B) - along bottom edge, reading from right to left
    x_tick, y_tick = ternary_to_cartesian(0, frac, 1 - frac)
    ax.text(x_tick, y_tick - tick_offset, f"{level}", fontsize=tick_fontsize, ha="center", va="top")

    # Clay axis (C) - along right edge, reading from top to bottom
    x_tick, y_tick = ternary_to_cartesian(1 - frac, 0, frac)
    ax.text(x_tick + tick_offset, y_tick, f"{level}", fontsize=tick_fontsize, ha="left", va="center")

# Plot data points
ax.scatter(x_points, y_points, s=200, color="#306998", alpha=0.7, edgecolors="white", linewidth=1, zorder=5)

# Add vertex labels
label_fontsize = 20
label_offset = 0.08
ax.text(
    0.5, np.sqrt(3) / 2 + label_offset, "Sand (%)", fontsize=label_fontsize, ha="center", va="bottom", fontweight="bold"
)
ax.text(-label_offset, -label_offset, "Silt (%)", fontsize=label_fontsize, ha="right", va="top", fontweight="bold")
ax.text(1 + label_offset, -label_offset, "Clay (%)", fontsize=label_fontsize, ha="left", va="top", fontweight="bold")

# Title
ax.set_title("Soil Composition · ternary-basic · matplotlib · pyplots.ai", fontsize=24, pad=20)

# Clean up axes
ax.set_aspect("equal")
ax.axis("off")

# Adjust limits to prevent clipping
ax.set_xlim(-0.2, 1.2)
ax.set_ylim(-0.15, 1.05)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
