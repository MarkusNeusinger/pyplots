"""
arc-basic: Basic Arc Diagram
Library: matplotlib
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np


# Data: Character interactions in a story chapter
np.random.seed(42)

nodes = ["Alice", "Bob", "Carol", "David", "Eve", "Frank", "Grace", "Henry", "Iris", "Jack"]
n_nodes = len(nodes)

# Edges: pairs of connected nodes with weights
edges = [
    (0, 1, 3),  # Alice-Bob (strong connection)
    (0, 3, 2),  # Alice-David
    (1, 2, 2),  # Bob-Carol
    (2, 4, 1),  # Carol-Eve
    (3, 5, 2),  # David-Frank
    (4, 6, 1),  # Eve-Grace
    (0, 7, 1),  # Alice-Henry (long-range)
    (1, 5, 2),  # Bob-Frank
    (2, 3, 3),  # Carol-David (strong)
    (5, 8, 1),  # Frank-Iris
    (6, 9, 2),  # Grace-Jack
    (0, 9, 1),  # Alice-Jack (longest range)
    (3, 7, 2),  # David-Henry
    (7, 8, 1),  # Henry-Iris
    (8, 9, 2),  # Iris-Jack
]

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))

# Node positions along x-axis
x_positions = np.linspace(0, 1, n_nodes)
y_baseline = 0.1

# Draw arcs
for start, end, weight in edges:
    x_start = x_positions[start]
    x_end = x_positions[end]

    # Arc height proportional to distance between nodes
    distance = abs(end - start)
    height = 0.08 * distance

    # Center and width of the arc
    x_center = (x_start + x_end) / 2
    arc_width = abs(x_end - x_start)

    # Arc thickness based on weight
    linewidth = 1.5 + weight * 1.0

    # Semi-transparent arcs
    alpha = 0.6

    # Create arc using Arc patch
    arc = mpatches.Arc(
        (x_center, y_baseline),
        width=arc_width,
        height=height * 2,
        angle=0,
        theta1=0,
        theta2=180,
        color="#306998",
        linewidth=linewidth,
        alpha=alpha,
    )
    ax.add_patch(arc)

# Draw nodes
ax.scatter(x_positions, [y_baseline] * n_nodes, s=400, c="#FFD43B", edgecolors="#306998", linewidths=2, zorder=5)

# Add node labels
for x, name in zip(x_positions, nodes, strict=True):
    ax.text(x, y_baseline - 0.05, name, ha="center", va="top", fontsize=14, fontweight="bold", color="#306998")

# Styling
ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.1, 0.9)
ax.set_aspect("equal")

# Remove axes
ax.axis("off")

ax.set_title("Character Interactions · arc-basic · matplotlib · pyplots.ai", fontsize=24, pad=20)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
