"""
network-force-directed: Force-Directed Graph
Library: matplotlib
"""

import matplotlib.pyplot as plt
import numpy as np


# Data - Social network with communities
np.random.seed(42)

# Define nodes with community membership
nodes = {
    "Alice": "Engineering",
    "Bob": "Engineering",
    "Carol": "Engineering",
    "David": "Engineering",
    "Eve": "Engineering",
    "Frank": "Marketing",
    "Grace": "Marketing",
    "Henry": "Marketing",
    "Ivy": "Marketing",
    "Jack": "Sales",
    "Kate": "Sales",
    "Leo": "Sales",
    "Mia": "Sales",
    "Noah": "Sales",
    "Olivia": "Design",
    "Paul": "Design",
    "Quinn": "Design",
}

node_names = list(nodes.keys())
node_idx = {name: i for i, name in enumerate(node_names)}
n_nodes = len(node_names)

# Define edges (pairs of connected nodes)
edges = [
    # Engineering team connections
    ("Alice", "Bob"),
    ("Alice", "Carol"),
    ("Alice", "David"),
    ("Bob", "Carol"),
    ("Bob", "Eve"),
    ("Carol", "David"),
    ("Carol", "Eve"),
    ("David", "Eve"),
    # Marketing team connections
    ("Frank", "Grace"),
    ("Frank", "Henry"),
    ("Frank", "Ivy"),
    ("Grace", "Henry"),
    ("Grace", "Ivy"),
    ("Henry", "Ivy"),
    # Sales team connections
    ("Jack", "Kate"),
    ("Jack", "Leo"),
    ("Jack", "Mia"),
    ("Kate", "Leo"),
    ("Kate", "Noah"),
    ("Leo", "Mia"),
    ("Leo", "Noah"),
    ("Mia", "Noah"),
    # Design team connections
    ("Olivia", "Paul"),
    ("Olivia", "Quinn"),
    ("Paul", "Quinn"),
    # Cross-team connections
    ("Alice", "Frank"),
    ("Bob", "Jack"),
    ("Carol", "Olivia"),
    ("David", "Grace"),
    ("Eve", "Kate"),
    ("Frank", "Jack"),
    ("Henry", "Paul"),
    ("Ivy", "Quinn"),
    ("Leo", "Bob"),
    ("Mia", "Alice"),
]

# Convert edges to indices
edge_indices = [(node_idx[e[0]], node_idx[e[1]]) for e in edges]

# Calculate node degrees
degrees = np.zeros(n_nodes)
for e in edge_indices:
    degrees[e[0]] += 1
    degrees[e[1]] += 1

# Force-directed layout algorithm (Fruchterman-Reingold style)
positions = np.random.rand(n_nodes, 2) * 10
iterations = 300
area = 100.0
k = 1.2 * np.sqrt(area / n_nodes)

for iteration in range(iterations):
    forces = np.zeros((n_nodes, 2))

    # Repulsive forces between all node pairs
    for i in range(n_nodes):
        for j in range(n_nodes):
            if i != j:
                delta = positions[i] - positions[j]
                dist = max(np.linalg.norm(delta), 0.01)
                forces[i] += (delta / dist) * (k**2 / dist)

    # Attractive forces along edges
    for e in edge_indices:
        delta = positions[e[0]] - positions[e[1]]
        dist = max(np.linalg.norm(delta), 0.01)
        force = (delta / dist) * (dist**2 / k)
        forces[e[0]] -= force
        forces[e[1]] += force

    # Apply cooling (reduce movement over time)
    cooling = 1.0 - (iteration / iterations)
    max_move = 0.5 * cooling

    # Update positions with limited movement
    for i in range(n_nodes):
        force_mag = np.linalg.norm(forces[i])
        if force_mag > 0:
            positions[i] += (forces[i] / force_mag) * min(force_mag, max_move)

# Center the layout
positions -= positions.mean(axis=0)

# Community colors
community_colors = {
    "Engineering": "#306998",  # Python Blue
    "Marketing": "#FFD43B",  # Python Yellow
    "Sales": "#4CAF50",  # Green
    "Design": "#E91E63",  # Pink
}
node_colors = [community_colors[nodes[name]] for name in node_names]

# Node sizes based on degree
node_sizes = 300 + degrees * 100

# Plot
fig, ax = plt.subplots(figsize=(16, 9))

# Draw edges
for e in edge_indices:
    x_coords = [positions[e[0], 0], positions[e[1], 0]]
    y_coords = [positions[e[0], 1], positions[e[1], 1]]
    ax.plot(x_coords, y_coords, color="#888888", linewidth=2, alpha=0.5, zorder=1)

# Draw nodes
ax.scatter(positions[:, 0], positions[:, 1], s=node_sizes, c=node_colors, edgecolors="#333333", linewidths=2, zorder=2)

# Draw labels
for i, name in enumerate(node_names):
    ax.annotate(
        name, (positions[i, 0], positions[i, 1]), fontsize=11, fontweight="bold", ha="center", va="center", zorder=3
    )

# Style
ax.set_title("network-force-directed · matplotlib · pyplots.ai", fontsize=24)
ax.axis("off")
ax.set_aspect("equal")

# Create legend for communities
legend_handles = []
for name, color in community_colors.items():
    handle = ax.scatter([], [], c=color, s=300, label=name, edgecolors="#333333", linewidths=2)
    legend_handles.append(handle)

ax.legend(handles=legend_handles, loc="upper left", fontsize=14, title="Communities", title_fontsize=16, framealpha=0.9)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
