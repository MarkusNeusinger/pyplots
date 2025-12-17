"""
arc-basic: Basic Arc Diagram
Library: seaborn
"""

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Set seaborn style
sns.set_theme(style="whitegrid")

# Data - Character interactions in a story
nodes = ["Alice", "Bob", "Carol", "David", "Eve", "Frank", "Grace", "Henry"]
edges = [
    (0, 1),  # Alice - Bob
    (0, 3),  # Alice - David
    (1, 2),  # Bob - Carol
    (2, 4),  # Carol - Eve
    (3, 5),  # David - Frank
    (4, 6),  # Eve - Grace
    (5, 7),  # Frank - Henry
    (0, 7),  # Alice - Henry (long-range)
    (1, 5),  # Bob - Frank (medium-range)
    (2, 6),  # Carol - Grace (medium-range)
    (3, 4),  # David - Eve
]

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Node positions along horizontal axis
n_nodes = len(nodes)
x_positions = np.linspace(0.5, 9.5, n_nodes)
y_baseline = 0.5

# Draw arcs above the baseline
for src, tgt in edges:
    x_start = x_positions[src]
    x_end = x_positions[tgt]

    # Arc center and dimensions
    center_x = (x_start + x_end) / 2
    width = abs(x_end - x_start)
    # Height proportional to distance between nodes
    height = width * 0.6

    # Create arc (half ellipse above baseline)
    arc = patches.Arc(
        (center_x, y_baseline),
        width=width,
        height=height,
        angle=0,
        theta1=0,
        theta2=180,
        color="#306998",
        linewidth=2.5,
        alpha=0.6,
    )
    ax.add_patch(arc)

# Draw nodes
ax.scatter(x_positions, [y_baseline] * n_nodes, s=400, c="#FFD43B", edgecolors="#306998", linewidths=2.5, zorder=10)

# Add node labels
for x, name in zip(x_positions, nodes, strict=True):
    ax.text(x, y_baseline - 0.4, name, ha="center", va="top", fontsize=16, fontweight="bold")

# Style
ax.set_xlim(-0.2, 10.2)
ax.set_ylim(-1.0, 5.5)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("arc-basic · seaborn · pyplots.ai", fontsize=24, pad=20)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
