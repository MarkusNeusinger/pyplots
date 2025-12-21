""" pyplots.ai
network-basic: Basic Network Graph
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 94/100 | Created: 2025-12-17
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.collections import LineCollection


# Set seaborn style for aesthetic defaults
sns.set_theme(style="white")

# Set seed for reproducibility
np.random.seed(42)

# Data: A small social network with 20 people in 4 communities
nodes = [
    {"id": 0, "label": "Alice", "group": 0},
    {"id": 1, "label": "Bob", "group": 0},
    {"id": 2, "label": "Carol", "group": 0},
    {"id": 3, "label": "David", "group": 0},
    {"id": 4, "label": "Eve", "group": 0},
    {"id": 5, "label": "Frank", "group": 1},
    {"id": 6, "label": "Grace", "group": 1},
    {"id": 7, "label": "Henry", "group": 1},
    {"id": 8, "label": "Ivy", "group": 1},
    {"id": 9, "label": "Jack", "group": 1},
    {"id": 10, "label": "Kate", "group": 2},
    {"id": 11, "label": "Leo", "group": 2},
    {"id": 12, "label": "Mia", "group": 2},
    {"id": 13, "label": "Noah", "group": 2},
    {"id": 14, "label": "Olivia", "group": 2},
    {"id": 15, "label": "Paul", "group": 3},
    {"id": 16, "label": "Quinn", "group": 3},
    {"id": 17, "label": "Ryan", "group": 3},
    {"id": 18, "label": "Sara", "group": 3},
    {"id": 19, "label": "Tom", "group": 3},
]

# Edges: Friendship connections (within and between groups)
edges = [
    # Group 0 internal connections
    (0, 1),
    (0, 2),
    (1, 2),
    (1, 3),
    (2, 4),
    (3, 4),
    # Group 1 internal connections
    (5, 6),
    (5, 7),
    (6, 8),
    (7, 8),
    (7, 9),
    (8, 9),
    # Group 2 internal connections
    (10, 11),
    (10, 12),
    (11, 13),
    (12, 13),
    (12, 14),
    (13, 14),
    # Group 3 internal connections
    (15, 16),
    (15, 17),
    (16, 18),
    (17, 18),
    (17, 19),
    (18, 19),
    # Cross-group connections (bridges between communities)
    (0, 5),
    (4, 10),
    (9, 15),
    (14, 19),
    (2, 6),
    (8, 11),
    (13, 16),
]

# Calculate spring layout (force-directed algorithm)
n = len(nodes)
positions = np.random.rand(n, 2) * 2 - 1
k = 0.4  # Optimal distance parameter

for iteration in range(150):
    displacement = np.zeros((n, 2))

    # Repulsive forces between all node pairs
    for i in range(n):
        for j in range(i + 1, n):
            diff = positions[i] - positions[j]
            dist = max(np.linalg.norm(diff), 0.01)
            force = (k * k / dist) * (diff / dist)
            displacement[i] += force
            displacement[j] -= force

    # Attractive forces for edges
    for src, tgt in edges:
        diff = positions[src] - positions[tgt]
        dist = max(np.linalg.norm(diff), 0.01)
        force = (dist * dist / k) * (diff / dist)
        displacement[src] -= force
        displacement[tgt] += force

    # Apply displacement with cooling
    cooling = 1 - iteration / 150
    for i in range(n):
        disp_norm = np.linalg.norm(displacement[i])
        if disp_norm > 0:
            positions[i] += (displacement[i] / disp_norm) * min(disp_norm, 0.1 * cooling)

# Normalize positions to [0.1, 0.9] range
pos_min = positions.min(axis=0)
pos_max = positions.max(axis=0)
positions = (positions - pos_min) / (pos_max - pos_min + 1e-6) * 0.8 + 0.1
pos = {node["id"]: positions[i] for i, node in enumerate(nodes)}

# Calculate node degrees for sizing
degrees = {node["id"]: 0 for node in nodes}
for src, tgt in edges:
    degrees[src] += 1
    degrees[tgt] += 1

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))

# Use seaborn color palette for groups
palette = sns.color_palette(["#306998", "#FFD43B", "#4CAF50", "#FF7043"])

# Draw edges first
edge_lines = [[(pos[src][0], pos[src][1]), (pos[tgt][0], pos[tgt][1])] for src, tgt in edges]
lc = LineCollection(edge_lines, colors="#888888", linewidths=2.5, alpha=0.5, zorder=1)
ax.add_collection(lc)

# Draw nodes using seaborn scatterplot for each group
for group_id in range(4):
    group_nodes = [node for node in nodes if node["group"] == group_id]
    x_vals = [pos[node["id"]][0] for node in group_nodes]
    y_vals = [pos[node["id"]][1] for node in group_nodes]
    sizes = [800 + degrees[node["id"]] * 200 for node in group_nodes]
    color = palette[group_id]
    ax.scatter(
        x_vals,
        y_vals,
        s=sizes,
        c=[color],
        edgecolors="#333333",
        linewidths=2,
        alpha=0.9,
        zorder=2,
        label=f"Group {chr(65 + group_id)}",
    )

# Draw labels
for node in nodes:
    x, y = pos[node["id"]]
    ax.text(x, y, node["label"], fontsize=11, fontweight="bold", ha="center", va="center", color="#222222", zorder=3)

# Styling
ax.set_title("Social Network · network-basic · seaborn · pyplots.ai", fontsize=24)
ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.05, 1.05)
ax.axis("off")

# Add legend
ax.legend(loc="upper left", fontsize=16, framealpha=0.9, title="Communities", title_fontsize=18, markerscale=0.5)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
