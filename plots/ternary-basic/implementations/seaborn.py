"""
ternary-basic: Basic Ternary Plot
Library: seaborn
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Set seaborn style
sns.set_theme(style="whitegrid")

# Data - soil composition samples (sand, silt, clay)
np.random.seed(42)
n_points = 50

# Generate random compositions that sum to 100
raw = np.random.dirichlet(alpha=[2, 2, 2], size=n_points) * 100
sand = raw[:, 0]
silt = raw[:, 1]
clay = raw[:, 2]


# Helper functions to convert ternary to Cartesian coordinates
# In a ternary plot: A at top, B at bottom-left, C at bottom-right
def ternary_to_cartesian(a, b, c):
    """Convert ternary coordinates (a, b, c) to Cartesian (x, y)."""
    total = a + b + c
    a, b, c = a / total, b / total, c / total
    x = 0.5 * (2 * c + a)
    y = (np.sqrt(3) / 2) * a
    return x, y


# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Draw triangle border
triangle_x = [0.5, 0, 1, 0.5]
triangle_y = [np.sqrt(3) / 2, 0, 0, np.sqrt(3) / 2]
ax.plot(triangle_x, triangle_y, color="black", linewidth=2.5)

# Draw grid lines at 20% intervals
grid_color = "#cccccc"
for i in range(1, 5):
    frac = i / 5
    # Lines parallel to each side
    # Parallel to bottom (constant A)
    x1, y1 = ternary_to_cartesian(frac * 100, (1 - frac) * 100, 0)
    x2, y2 = ternary_to_cartesian(frac * 100, 0, (1 - frac) * 100)
    ax.plot([x1, x2], [y1, y2], color=grid_color, linewidth=1, linestyle="--", alpha=0.7)

    # Parallel to left side (constant C)
    x1, y1 = ternary_to_cartesian(0, frac * 100, (1 - frac) * 100)
    x2, y2 = ternary_to_cartesian((1 - frac) * 100, frac * 100, 0)
    ax.plot([x1, x2], [y1, y2], color=grid_color, linewidth=1, linestyle="--", alpha=0.7)

    # Parallel to right side (constant B)
    x1, y1 = ternary_to_cartesian(0, (1 - frac) * 100, frac * 100)
    x2, y2 = ternary_to_cartesian((1 - frac) * 100, 0, frac * 100)
    ax.plot([x1, x2], [y1, y2], color=grid_color, linewidth=1, linestyle="--", alpha=0.7)

# Add tick labels along edges
tick_fontsize = 14
offset = 0.04
for i in range(0, 6):
    frac = i / 5
    label = f"{int(frac * 100)}"

    # Left edge (Sand %) - reading from bottom to top
    x, y = ternary_to_cartesian(frac * 100, (1 - frac) * 100, 0)
    ax.text(x - offset, y, label, fontsize=tick_fontsize, ha="right", va="center")

    # Right edge (Silt %)
    x, y = ternary_to_cartesian(frac * 100, 0, (1 - frac) * 100)
    ax.text(x + offset, y, label, fontsize=tick_fontsize, ha="left", va="center")

    # Bottom edge (Clay %)
    x, y = ternary_to_cartesian(0, (1 - frac) * 100, frac * 100)
    ax.text(x, y - offset, label, fontsize=tick_fontsize, ha="center", va="top")

# Convert data to Cartesian and plot
x_data, y_data = ternary_to_cartesian(sand, silt, clay)
ax.scatter(x_data, y_data, s=200, color="#306998", alpha=0.7, edgecolors="white", linewidth=1.5)

# Add vertex labels
label_offset = 0.06
ax.text(0.5, np.sqrt(3) / 2 + label_offset, "Sand (%)", fontsize=20, ha="center", va="bottom", fontweight="bold")
ax.text(-label_offset - 0.02, -label_offset, "Silt (%)", fontsize=20, ha="right", va="top", fontweight="bold")
ax.text(1 + label_offset + 0.02, -label_offset, "Clay (%)", fontsize=20, ha="left", va="top", fontweight="bold")

# Add axis labels for edge readings
ax.text(-0.08, np.sqrt(3) / 4, "Sand →", fontsize=16, ha="center", va="center", rotation=60, color="#306998")
ax.text(1.08, np.sqrt(3) / 4, "← Silt", fontsize=16, ha="center", va="center", rotation=-60, color="#306998")
ax.text(0.5, -0.12, "← Clay →", fontsize=16, ha="center", va="top", color="#306998")

# Title - placed with more padding to avoid overlap with vertex labels
ax.set_title("Soil Composition · ternary-basic · seaborn · pyplots.ai", fontsize=24, pad=40)

# Clean up axes
ax.set_aspect("equal")
ax.axis("off")

# Adjust layout
plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
