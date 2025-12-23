"""pyplots.ai
arc-basic: Basic Arc Diagram
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Data: Character interactions in a story
np.random.seed(42)
nodes = ["Alice", "Bob", "Carol", "Dave", "Eve", "Frank", "Grace", "Henry"]
n_nodes = len(nodes)

# Create edges with weights (character interaction strength)
edges = [
    (0, 1, 5),  # Alice - Bob (close friends)
    (0, 3, 2),  # Alice - Dave
    (1, 2, 4),  # Bob - Carol
    (1, 4, 3),  # Bob - Eve
    (2, 5, 2),  # Carol - Frank
    (3, 4, 5),  # Dave - Eve (close)
    (3, 6, 3),  # Dave - Grace
    (4, 7, 4),  # Eve - Henry
    (5, 6, 2),  # Frank - Grace
    (0, 7, 1),  # Alice - Henry (distant)
    (2, 6, 3),  # Carol - Grace
    (1, 5, 2),  # Bob - Frank
]

# Node positions along x-axis
x_positions = np.arange(n_nodes)

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))
sns.set_style("whitegrid")

# Plot nodes as points using seaborn
node_data = pd.DataFrame({"x": x_positions, "y": np.zeros(n_nodes), "node": nodes})
sns.scatterplot(data=node_data, x="x", y="y", s=600, color="#306998", zorder=5, ax=ax, legend=False)

# Draw arcs for each edge
for start, end, weight in edges:
    x1, x2 = x_positions[start], x_positions[end]
    # Arc height proportional to distance between nodes
    distance = abs(x2 - x1)
    height = distance * 0.4

    # Arc thickness based on weight
    linewidth = weight * 0.8 + 0.5

    # Create arc using matplotlib patches
    center_x = (x1 + x2) / 2
    width = abs(x2 - x1)

    arc = patches.Arc(
        (center_x, 0),
        width,
        height * 2,
        angle=0,
        theta1=0,
        theta2=180,
        color="#FFD43B",
        linewidth=linewidth,
        alpha=0.6,
        zorder=2,
    )
    ax.add_patch(arc)

# Add node labels below the axis
for i, name in enumerate(nodes):
    ax.text(x_positions[i], -0.15, name, ha="center", va="top", fontsize=16, fontweight="bold", color="#306998")

# Styling
ax.set_xlim(-0.8, n_nodes - 0.2)
ax.set_ylim(-0.8, 3.5)
ax.set_xlabel("Character Sequence", fontsize=20)
ax.set_ylabel("Connection Arc Height", fontsize=20)
ax.set_title("arc-basic · seaborn · pyplots.ai", fontsize=24)
ax.tick_params(axis="both", labelsize=16)

# Remove x-axis ticks (nodes are labeled)
ax.set_xticks([])

# Add a subtle horizontal baseline
ax.axhline(y=0, color="#306998", linewidth=2, alpha=0.3, zorder=1)

# Adjust grid
ax.grid(True, alpha=0.3, linestyle="--")
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
