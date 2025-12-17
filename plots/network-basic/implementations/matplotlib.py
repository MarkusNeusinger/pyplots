"""
network-basic: Basic Network Graph
Library: matplotlib
"""

import matplotlib.pyplot as plt
import numpy as np


# Data: Small social network with 20 people
np.random.seed(42)

# Nodes with groups (departments in a company)
nodes = [
    {"id": 0, "label": "Alice", "group": "Engineering"},
    {"id": 1, "label": "Bob", "group": "Engineering"},
    {"id": 2, "label": "Carol", "group": "Engineering"},
    {"id": 3, "label": "David", "group": "Engineering"},
    {"id": 4, "label": "Eve", "group": "Engineering"},
    {"id": 5, "label": "Frank", "group": "Marketing"},
    {"id": 6, "label": "Grace", "group": "Marketing"},
    {"id": 7, "label": "Henry", "group": "Marketing"},
    {"id": 8, "label": "Ivy", "group": "Marketing"},
    {"id": 9, "label": "Jack", "group": "Sales"},
    {"id": 10, "label": "Kate", "group": "Sales"},
    {"id": 11, "label": "Leo", "group": "Sales"},
    {"id": 12, "label": "Mia", "group": "Sales"},
    {"id": 13, "label": "Noah", "group": "HR"},
    {"id": 14, "label": "Olivia", "group": "HR"},
    {"id": 15, "label": "Paul", "group": "HR"},
    {"id": 16, "label": "Quinn", "group": "Finance"},
    {"id": 17, "label": "Rose", "group": "Finance"},
    {"id": 18, "label": "Sam", "group": "Finance"},
    {"id": 19, "label": "Tina", "group": "Finance"},
]

# Edges representing friendships/collaborations
edges = [
    # Engineering cluster (dense internal connections)
    (0, 1),
    (0, 2),
    (0, 3),
    (1, 2),
    (1, 4),
    (2, 3),
    (2, 4),
    (3, 4),
    # Marketing cluster
    (5, 6),
    (5, 7),
    (6, 7),
    (6, 8),
    (7, 8),
    # Sales cluster
    (9, 10),
    (9, 11),
    (10, 11),
    (10, 12),
    (11, 12),
    # HR cluster
    (13, 14),
    (13, 15),
    (14, 15),
    # Finance cluster
    (16, 17),
    (16, 18),
    (17, 18),
    (17, 19),
    (18, 19),
    # Cross-department connections (bridges)
    (0, 5),
    (2, 9),
    (4, 13),  # Engineering to other departments
    (5, 9),
    (7, 10),  # Marketing-Sales
    (13, 16),
    (14, 17),  # HR-Finance
    (1, 16),
    (3, 14),  # Engineering-Finance, Engineering-HR
]

n_nodes = len(nodes)

# Calculate node degrees for sizing
degrees = [0] * n_nodes
for src, tgt in edges:
    degrees[src] += 1
    degrees[tgt] += 1

# Spring layout (force-directed placement)
positions = np.random.rand(n_nodes, 2) * 2 - 1
k = 0.3  # optimal distance factor

for iteration in range(200):
    displacement = np.zeros((n_nodes, 2))

    # Repulsive forces between all pairs
    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            diff = positions[i] - positions[j]
            dist = max(np.linalg.norm(diff), 0.01)
            force = k * k / dist
            direction = diff / dist
            displacement[i] += direction * force
            displacement[j] -= direction * force

    # Attractive forces along edges
    for src, tgt in edges:
        diff = positions[src] - positions[tgt]
        dist = max(np.linalg.norm(diff), 0.01)
        force = dist * dist / k
        direction = diff / dist
        displacement[src] -= direction * force
        displacement[tgt] += direction * force

    # Apply displacement with cooling
    cooling = 1 - iteration / 200
    max_disp = np.max(np.linalg.norm(displacement, axis=1))
    if max_disp > 0:
        positions += displacement / max_disp * cooling * 0.1

# Normalize to [-1, 1]
positions -= positions.mean(axis=0)
positions /= np.abs(positions).max() + 0.01

# Color mapping by group
group_colors = {
    "Engineering": "#306998",  # Python Blue
    "Marketing": "#FFD43B",  # Python Yellow
    "Sales": "#2E8B57",  # Sea Green
    "HR": "#DC143C",  # Crimson
    "Finance": "#9370DB",  # Medium Purple
}

node_colors = [group_colors[node["group"]] for node in nodes]
# Scale node sizes by degree (larger = more connections)
node_sizes = [300 + degrees[i] * 100 for i in range(n_nodes)]

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

# Draw edges first (behind nodes)
for src, tgt in edges:
    ax.plot(
        [positions[src, 0], positions[tgt, 0]],
        [positions[src, 1], positions[tgt, 1]],
        color="#AAAAAA",
        linewidth=2,
        alpha=0.6,
        zorder=1,
    )

# Draw nodes
ax.scatter(positions[:, 0], positions[:, 1], s=node_sizes, c=node_colors, edgecolors="white", linewidths=2, zorder=2)

# Draw labels
for i, node in enumerate(nodes):
    ax.annotate(
        node["label"],
        (positions[i, 0], positions[i, 1]),
        fontsize=12,
        fontweight="bold",
        ha="center",
        va="center",
        zorder=3,
    )

# Create legend for groups
for group, color in group_colors.items():
    ax.scatter([], [], c=color, s=300, label=group, edgecolors="white", linewidths=2)

ax.legend(fontsize=16, loc="upper left", framealpha=0.9)

ax.set_title("network-basic · matplotlib · pyplots.ai", fontsize=24)
ax.axis("off")
ax.set_xlim(-1.3, 1.3)
ax.set_ylim(-1.3, 1.3)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
