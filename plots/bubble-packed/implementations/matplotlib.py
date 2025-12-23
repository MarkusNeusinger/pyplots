""" pyplots.ai
bubble-packed: Basic Packed Bubble Chart
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-23
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np


# Data - Department budget allocation (in thousands)
np.random.seed(42)
labels = [
    "Engineering",
    "Marketing",
    "Sales",
    "Operations",
    "HR",
    "Finance",
    "R&D",
    "Customer Support",
    "Legal",
    "IT",
    "Design",
    "Product",
    "Data Science",
    "Security",
    "QA",
]
values = [850, 420, 680, 320, 180, 290, 750, 210, 150, 380, 240, 550, 460, 170, 195]

# Colors by group (Python Blue primary, Yellow secondary, others colorblind-safe)
colors = [
    "#306998",  # Engineering - Blue (Tech)
    "#FFD43B",  # Marketing - Yellow (Business)
    "#306998",  # Sales - Blue (Revenue)
    "#4A90A4",  # Operations - Teal (Support)
    "#4A90A4",  # HR - Teal (Support)
    "#4A90A4",  # Finance - Teal (Support)
    "#FFD43B",  # R&D - Yellow (Innovation)
    "#4A90A4",  # Customer Support - Teal (Support)
    "#7B9E89",  # Legal - Sage (Compliance)
    "#306998",  # IT - Blue (Tech)
    "#FFD43B",  # Design - Yellow (Creative)
    "#306998",  # Product - Blue (Tech)
    "#FFD43B",  # Data Science - Yellow (Analytics)
    "#7B9E89",  # Security - Sage (Compliance)
    "#7B9E89",  # QA - Sage (Quality)
]

# Scale values to radius (sqrt for area-proportional sizing)
min_radius = 0.35
max_radius = 1.9
values_array = np.array(values)
radii = min_radius + (max_radius - min_radius) * np.sqrt(
    (values_array - values_array.min()) / (values_array.max() - values_array.min())
)

# Circle packing using physics simulation
n = len(labels)

# Initial positions in grid
grid_size = int(np.ceil(np.sqrt(n)))
positions = np.zeros((n, 2))
for i in range(n):
    positions[i] = [(i % grid_size) * 4 - grid_size * 2, (i // grid_size) * 4 - grid_size * 2]

# Sort by size (largest first) for better packing
order = np.argsort(-radii)
positions = positions[order]
radii_sorted = radii[order]
labels_sorted = [labels[i] for i in order]
values_sorted = [values[i] for i in order]
colors_sorted = [colors[i] for i in order]

# Physics simulation for packing
for iteration in range(350):
    # Pull toward center with decreasing strength
    pull_strength = 0.06 * (1 - iteration / 400)
    for i in range(n):
        dist = np.sqrt(positions[i, 0] ** 2 + positions[i, 1] ** 2)
        if dist > 0.01:
            positions[i] -= pull_strength * positions[i] / dist

    # Push apart overlapping circles
    for i in range(n):
        for j in range(i + 1, n):
            dx = positions[j, 0] - positions[i, 0]
            dy = positions[j, 1] - positions[i, 1]
            dist = np.sqrt(dx**2 + dy**2)
            min_dist = radii_sorted[i] + radii_sorted[j] + 0.05  # Small gap between circles

            if dist < min_dist and dist > 0.001:
                overlap = (min_dist - dist) / 2
                dx_norm = dx / dist
                dy_norm = dy / dist
                positions[i, 0] -= overlap * dx_norm
                positions[i, 1] -= overlap * dy_norm
                positions[j, 0] += overlap * dx_norm
                positions[j, 1] += overlap * dy_norm

# Create plot (4800x2700 px at 300 dpi)
fig, ax = plt.subplots(figsize=(16, 9))

# Draw circles
for i in range(n):
    circle = mpatches.Circle(
        (positions[i, 0], positions[i, 1]),
        radii_sorted[i],
        facecolor=colors_sorted[i],
        edgecolor="white",
        linewidth=2.5,
        alpha=0.88,
    )
    ax.add_patch(circle)

    # Add labels inside larger circles
    label_len = len(labels_sorted[i])
    min_radius_for_label = 0.55 + label_len * 0.025
    if radii_sorted[i] > min_radius_for_label:
        font_scale = min(1.0, radii_sorted[i] / 1.4)
        label_fontsize = max(9, int(15 * font_scale))
        value_fontsize = max(8, int(13 * font_scale))
        ax.text(
            positions[i, 0],
            positions[i, 1] + radii_sorted[i] * 0.1,
            labels_sorted[i],
            ha="center",
            va="center",
            fontsize=label_fontsize,
            fontweight="bold",
            color="white",
        )
        ax.text(
            positions[i, 0],
            positions[i, 1] - radii_sorted[i] * 0.22,
            f"${values_sorted[i]}K",
            ha="center",
            va="center",
            fontsize=value_fontsize,
            color="white",
            alpha=0.95,
        )

# Set axis limits with padding
all_x = positions[:, 0]
all_y = positions[:, 1]
max_r = radii_sorted.max()
padding = 0.6
ax.set_xlim(all_x.min() - max_r - padding, all_x.max() + max_r + padding)
ax.set_ylim(all_y.min() - max_r - padding, all_y.max() + max_r + padding)
ax.set_aspect("equal")

# Remove axes for clean visualization
ax.axis("off")

# Title
ax.set_title(
    "Department Budget Allocation · bubble-packed · matplotlib · pyplots.ai", fontsize=24, fontweight="bold", pad=20
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
