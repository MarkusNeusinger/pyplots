"""pyplots.ai
arc-basic: Basic Arc Diagram
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 82/100 | Created: 2025-12-23
"""

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.lines import Line2D


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

# Create figure with seaborn styling
sns.set_theme(style="white", context="talk", font_scale=1.1)
fig, ax = plt.subplots(figsize=(16, 9))

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
ax.set_title("arc-basic · seaborn · pyplots.ai", fontsize=24)
ax.set_xlabel("")
ax.set_ylabel("")

# Remove axes - arc diagrams are abstract visualizations
ax.set_xticks([])
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_visible(False)

# Add a subtle horizontal baseline
ax.axhline(y=0, color="#306998", linewidth=2, alpha=0.3, zorder=1)

# Add legend for arc thickness (interaction strength)
legend_elements = [
    Line2D([0], [0], color="#FFD43B", linewidth=1.3, alpha=0.6, label="Weak (1)"),
    Line2D([0], [0], color="#FFD43B", linewidth=2.9, alpha=0.6, label="Medium (3)"),
    Line2D([0], [0], color="#FFD43B", linewidth=4.5, alpha=0.6, label="Strong (5)"),
]
ax.legend(handles=legend_elements, title="Interaction Strength", loc="upper right", fontsize=14, title_fontsize=16)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
