""" pyplots.ai
network-force-directed: Force-Directed Graph
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 93/100 | Created: 2025-12-17
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection


# Set seed for reproducibility
np.random.seed(42)

# Data: A social network with 50 nodes in 3 communities
# Demonstrates force-directed layout with clear community structure
nodes = []
edges = []

# Create 3 communities
community_sizes = [18, 17, 15]  # Total: 50 nodes
community_names = ["Engineering", "Marketing", "Sales"]
node_id = 0

for comm_idx, size in enumerate(community_sizes):
    for _ in range(size):
        nodes.append({"id": node_id, "community": comm_idx})
        node_id += 1

# Intra-community edges (dense connections within communities)
# Engineering: nodes 0-17
for i in range(18):
    for j in range(i + 1, 18):
        if np.random.random() < 0.3:
            edges.append((i, j))

# Marketing: nodes 18-34
for i in range(18, 35):
    for j in range(i + 1, 35):
        if np.random.random() < 0.3:
            edges.append((i, j))

# Sales: nodes 35-49
for i in range(35, 50):
    for j in range(i + 1, 50):
        if np.random.random() < 0.3:
            edges.append((i, j))

# Inter-community edges (sparse bridges between communities)
bridge_edges = [(0, 18), (5, 20), (10, 25), (18, 35), (22, 40), (30, 45), (8, 38), (15, 48)]
edges.extend(bridge_edges)

# Force-directed layout algorithm (Fruchterman-Reingold)
n = len(nodes)
positions = np.random.rand(n, 2) * 2 - 1  # Initial random positions

# Optimal distance parameter
k = 0.5
iterations = 200

for iteration in range(iterations):
    displacement = np.zeros((n, 2))

    # Repulsive forces between all node pairs (nodes push apart)
    for i in range(n):
        for j in range(i + 1, n):
            diff = positions[i] - positions[j]
            dist = max(np.linalg.norm(diff), 0.01)
            repulsive_force = (k * k / dist) * (diff / dist)
            displacement[i] += repulsive_force
            displacement[j] -= repulsive_force

    # Attractive forces along edges (connected nodes pull together)
    for src, tgt in edges:
        diff = positions[src] - positions[tgt]
        dist = max(np.linalg.norm(diff), 0.01)
        attractive_force = (dist * dist / k) * (diff / dist)
        displacement[src] -= attractive_force
        displacement[tgt] += attractive_force

    # Apply displacement with cooling (decreasing temperature)
    temperature = 1 - iteration / iterations
    for i in range(n):
        disp_norm = np.linalg.norm(displacement[i])
        if disp_norm > 0:
            # Limit movement by temperature
            positions[i] += (displacement[i] / disp_norm) * min(disp_norm, 0.15 * temperature)

# Normalize positions to [0.05, 0.95] range
pos_min = positions.min(axis=0)
pos_max = positions.max(axis=0)
positions = (positions - pos_min) / (pos_max - pos_min + 1e-6) * 0.9 + 0.05
pos = {node["id"]: positions[i] for i, node in enumerate(nodes)}

# Calculate node degrees (number of connections)
degrees = {node["id"]: 0 for node in nodes}
for src, tgt in edges:
    degrees[src] += 1
    degrees[tgt] += 1

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))

# Community colors
community_colors = ["#306998", "#FFD43B", "#FF6B6B"]

# Draw edges first (behind nodes)
edge_lines = [[(pos[src][0], pos[src][1]), (pos[tgt][0], pos[tgt][1])] for src, tgt in edges]
lc = LineCollection(edge_lines, colors="#AAAAAA", linewidths=1.5, alpha=0.4, zorder=1)
ax.add_collection(lc)

# Draw nodes sized by degree
for node in nodes:
    x, y = pos[node["id"]]
    degree = degrees[node["id"]]
    size = 400 + degree * 100  # Scale size by connections
    color = community_colors[node["community"]]
    ax.scatter(x, y, s=size, c=color, edgecolors="#333333", linewidths=1.5, alpha=0.85, zorder=2)

# Label only high-degree nodes (hubs)
for node in nodes:
    if degrees[node["id"]] >= 7:
        x, y = pos[node["id"]]
        ax.text(
            x, y + 0.035, "Hub", fontsize=12, fontweight="bold", ha="center", va="bottom", color="#333333", zorder=3
        )

# Styling
ax.set_title("network-force-directed · matplotlib · pyplots.ai", fontsize=24)
ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.05, 1.05)
ax.axis("off")

# Legend for communities
legend_handles = [
    ax.scatter([], [], c=color, s=500, edgecolors="#333333", linewidths=1.5, label=name)
    for color, name in zip(community_colors, community_names, strict=True)
]
ax.legend(handles=legend_handles, loc="upper left", fontsize=16, framealpha=0.9, title="Teams", title_fontsize=18)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
