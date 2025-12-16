"""
bubble-packed: Basic Packed Bubble Chart
Library: seaborn
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Data - synthetic category values representing budget allocation
np.random.seed(42)
categories = [
    "Engineering",
    "Marketing",
    "Sales",
    "Operations",
    "HR",
    "Finance",
    "R&D",
    "IT",
    "Legal",
    "Customer Support",
    "Product",
    "Design",
    "Quality",
    "Logistics",
    "Admin",
]
values = [85, 62, 58, 45, 32, 28, 72, 38, 22, 35, 55, 42, 18, 25, 15]

# Scale values to reasonable radii (area proportional to value)
values_arr = np.array(values, dtype=float)
# Normalize radii based on sqrt of values for proper area scaling
radii = np.sqrt(values_arr / values_arr.max())
# Scale to reasonable size
radii = radii * 0.18 + 0.04  # Range from ~0.04 to ~0.22

n_circles = len(categories)


def pack_circles_front_chain(radii):
    """
    Circle packing using a front-chain algorithm.
    Places circles one by one, each touching at least one previous circle.
    """
    n = len(radii)
    # Sort by radius descending for better packing
    order = np.argsort(radii)[::-1]
    radii_sorted = radii[order]

    positions = np.zeros((n, 2))

    # Place first circle at origin
    positions[0] = [0, 0]

    if n > 1:
        # Place second circle to the right of first
        positions[1] = [radii_sorted[0] + radii_sorted[1], 0]

    if n > 2:
        # Place third circle tangent to first two
        r0, r1, r2 = radii_sorted[0], radii_sorted[1], radii_sorted[2]
        d01 = r0 + r1  # distance between centers of circles 0 and 1
        d02 = r0 + r2  # required distance from circle 0
        d12 = r1 + r2  # required distance from circle 1

        # Find position using circle intersection
        x2 = (d02**2 - d12**2 + d01**2) / (2 * d01)
        y2_sq = d02**2 - x2**2
        y2 = np.sqrt(max(0, y2_sq))
        positions[2] = [x2, y2]

    # Place remaining circles
    for i in range(3, n):
        r_new = radii_sorted[i]
        best_pos = None
        best_dist = float("inf")

        # Try placing tangent to each pair of existing circles
        for j in range(i):
            for k in range(j + 1, i):
                r_j, r_k = radii_sorted[j], radii_sorted[k]
                p_j, p_k = positions[j], positions[k]

                # Find positions tangent to both circles j and k
                d_jk = np.sqrt((p_k[0] - p_j[0]) ** 2 + (p_k[1] - p_j[1]) ** 2)
                d_j_new = r_j + r_new
                d_k_new = r_k + r_new

                # Check if tangent placement is possible
                if d_jk > d_j_new + d_k_new or d_jk < abs(d_j_new - d_k_new):
                    continue

                # Calculate intersection points of two circles centered at j and k
                a = (d_j_new**2 - d_k_new**2 + d_jk**2) / (2 * d_jk)
                h_sq = d_j_new**2 - a**2
                if h_sq < 0:
                    continue
                h = np.sqrt(h_sq)

                # Unit vector from j to k
                ux = (p_k[0] - p_j[0]) / d_jk
                uy = (p_k[1] - p_j[1]) / d_jk

                # Two possible positions
                for sign in [1, -1]:
                    px = p_j[0] + a * ux + sign * h * (-uy)
                    py = p_j[1] + a * uy + sign * h * ux
                    pos_candidate = np.array([px, py])

                    # Check for overlaps with all existing circles
                    valid = True
                    for m in range(i):
                        dist_m = np.sqrt(
                            (pos_candidate[0] - positions[m, 0]) ** 2 + (pos_candidate[1] - positions[m, 1]) ** 2
                        )
                        if dist_m < radii_sorted[m] + r_new - 0.001:
                            valid = False
                            break

                    if valid:
                        # Prefer positions closer to center
                        dist_center = np.sqrt(px**2 + py**2)
                        if dist_center < best_dist:
                            best_dist = dist_center
                            best_pos = pos_candidate

        if best_pos is not None:
            positions[i] = best_pos
        else:
            # Fallback: place on outer edge
            angle = 2 * np.pi * i / n
            max_r = np.max(radii_sorted[:i]) + r_new
            positions[i] = [max_r * np.cos(angle), max_r * np.sin(angle)]

    # Restore original order
    final_positions = np.zeros((n, 2))
    for i, orig_idx in enumerate(order):
        final_positions[orig_idx] = positions[i]

    return final_positions


# Pack circles
positions = pack_circles_front_chain(radii)

# Center and scale positions to fit in plot
x_min, x_max = positions[:, 0].min(), positions[:, 0].max()
y_min, y_max = positions[:, 1].min(), positions[:, 1].max()
r_max = radii.max()

# Calculate bounding box including radii
bbox_x_min = x_min - r_max
bbox_x_max = x_max + r_max
bbox_y_min = y_min - r_max
bbox_y_max = y_max + r_max

# Scale to fit in [0.1, 0.9] range
width = bbox_x_max - bbox_x_min
height = bbox_y_max - bbox_y_min
scale = 0.8 / max(width, height)

positions = (positions - np.array([x_min + x_max, y_min + y_max]) / 2) * scale + 0.5
radii = radii * scale

# Assign colors using a seaborn palette
colors = sns.color_palette("Set2", n_colors=n_circles)

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))
ax.set_facecolor("#f8f9fa")

# Draw circles
for i in range(n_circles):
    circle = mpatches.Circle(
        (positions[i, 0], positions[i, 1]), radii[i], facecolor=colors[i], edgecolor="white", linewidth=3, alpha=0.9
    )
    ax.add_patch(circle)

    # Add labels inside circles
    # Calculate font size based on radius
    fontsize_label = max(8, int(radii[i] * 180))
    fontsize_value = max(6, int(radii[i] * 140))

    # Only show text if it will fit
    if radii[i] > 0.04:
        # Truncate long labels
        label = categories[i] if len(categories[i]) <= 10 else categories[i][:8] + ".."
        ax.text(
            positions[i, 0],
            positions[i, 1] + radii[i] * 0.15,
            label,
            ha="center",
            va="center",
            fontsize=fontsize_label,
            fontweight="bold",
            color="white",
        )
        ax.text(
            positions[i, 0],
            positions[i, 1] - radii[i] * 0.25,
            f"${values[i]}K",
            ha="center",
            va="center",
            fontsize=fontsize_value,
            color="white",
            alpha=0.95,
        )

# Configure axes
ax.set_xlim(0.05, 0.95)
ax.set_ylim(0.05, 0.95)
ax.set_aspect("equal")
ax.axis("off")

# Title
ax.set_title(
    "Department Budget Allocation\nbubble-packed \u00b7 seaborn \u00b7 pyplots.ai",
    fontsize=24,
    fontweight="bold",
    pad=20,
    color="#333333",
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
