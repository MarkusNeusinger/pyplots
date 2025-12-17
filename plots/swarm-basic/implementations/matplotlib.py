"""
swarm-basic: Basic Swarm Plot
Library: matplotlib
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - Employee performance scores by department
np.random.seed(42)

departments = ["Engineering", "Sales", "Marketing", "Support"]
n_points = [50, 45, 40, 55]

# Generate scores with different distributions to showcase the plot
scores = {
    "Engineering": np.random.normal(78, 12, n_points[0]),
    "Sales": np.random.normal(72, 15, n_points[1]),
    "Marketing": np.random.normal(82, 10, n_points[2]),
    "Support": np.random.normal(68, 14, n_points[3]),
}

# Clip scores to realistic range (0-100)
for dept in scores:
    scores[dept] = np.clip(scores[dept], 0, 100)

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

colors = ["#306998", "#FFD43B", "#4CAF50", "#FF7043"]


def compute_swarm(values, point_size, y_range):
    """Compute x-offsets for swarm plot using bin-based algorithm."""
    n = len(values)
    offsets = np.zeros(n)

    # Sort by value and process in order
    sorted_idx = np.argsort(values)

    # Estimate point radius in data coordinates
    point_radius = point_size / 150 * 0.03 * (y_range[1] - y_range[0])

    for i, idx in enumerate(sorted_idx):
        val = values[idx]
        # Find nearby points already placed
        placed_idx = sorted_idx[:i]
        nearby = [(offsets[j], values[j]) for j in placed_idx if abs(values[j] - val) < point_radius * 2.5]

        if not nearby:
            offsets[idx] = 0
            continue

        # Try positions outward from center
        best_offset = 0
        for offset in np.linspace(0, 0.35, 50):
            for sign in [1, -1]:
                test_x = sign * offset
                collision = False
                for ox, oy in nearby:
                    dx = test_x - ox
                    dy = (val - oy) / point_radius
                    if dx * dx + dy * dy < 4:  # Collision if distance < 2*radius
                        collision = True
                        break
                if not collision:
                    best_offset = test_x
                    break
            if not collision:
                break
        offsets[idx] = best_offset

    return offsets


# Calculate y-range for proper scaling
all_values = np.concatenate(list(scores.values()))
y_range = (all_values.min() - 5, all_values.max() + 5)

# Plot each department
for i, dept in enumerate(departments):
    vals = scores[dept]
    x_offsets = compute_swarm(vals, 150, y_range)

    ax.scatter(i + x_offsets, vals, s=150, alpha=0.7, color=colors[i], edgecolors="white", linewidth=0.5, label=dept)

    # Add mean marker
    mean_val = np.mean(vals)
    ax.scatter(i, mean_val, s=350, color=colors[i], marker="D", edgecolors="black", linewidth=2, zorder=5)

# Styling
ax.set_xlabel("Department", fontsize=20)
ax.set_ylabel("Performance Score", fontsize=20)
ax.set_title("swarm-basic · matplotlib · pyplots.ai", fontsize=24)
ax.set_xticks(range(len(departments)))
ax.set_xticklabels(departments)
ax.tick_params(axis="both", labelsize=16)
ax.set_ylim(25, 105)
ax.set_xlim(-0.6, 3.6)
ax.grid(True, alpha=0.3, linestyle="--", axis="y")

# Legend for mean marker
ax.scatter([], [], s=350, color="gray", marker="D", edgecolors="black", linewidth=2, label="Mean")
ax.legend(fontsize=16, loc="upper right")

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
