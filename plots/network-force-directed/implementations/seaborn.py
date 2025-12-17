"""
network-force-directed: Force-Directed Graph
Library: seaborn
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Set seaborn style
sns.set_theme(style="white")

# Set seed for reproducibility
np.random.seed(42)

# Data: Team collaboration network with 40 people across 4 departments
# Demonstrates force-directed layout naturally revealing community structure
nodes = [
    # Engineering department (group 0)
    {"id": 0, "label": "Alice", "group": 0},
    {"id": 1, "label": "Bob", "group": 0},
    {"id": 2, "label": "Carol", "group": 0},
    {"id": 3, "label": "David", "group": 0},
    {"id": 4, "label": "Eve", "group": 0},
    {"id": 5, "label": "Frank", "group": 0},
    {"id": 6, "label": "Grace", "group": 0},
    {"id": 7, "label": "Henry", "group": 0},
    {"id": 8, "label": "Ivy", "group": 0},
    {"id": 9, "label": "Jack", "group": 0},
    # Design department (group 1)
    {"id": 10, "label": "Kate", "group": 1},
    {"id": 11, "label": "Leo", "group": 1},
    {"id": 12, "label": "Mia", "group": 1},
    {"id": 13, "label": "Noah", "group": 1},
    {"id": 14, "label": "Olivia", "group": 1},
    {"id": 15, "label": "Paul", "group": 1},
    {"id": 16, "label": "Quinn", "group": 1},
    {"id": 17, "label": "Ryan", "group": 1},
    {"id": 18, "label": "Sara", "group": 1},
    {"id": 19, "label": "Tom", "group": 1},
    # Marketing department (group 2)
    {"id": 20, "label": "Uma", "group": 2},
    {"id": 21, "label": "Victor", "group": 2},
    {"id": 22, "label": "Wendy", "group": 2},
    {"id": 23, "label": "Xavier", "group": 2},
    {"id": 24, "label": "Yara", "group": 2},
    {"id": 25, "label": "Zack", "group": 2},
    {"id": 26, "label": "Amy", "group": 2},
    {"id": 27, "label": "Brian", "group": 2},
    {"id": 28, "label": "Chloe", "group": 2},
    {"id": 29, "label": "Derek", "group": 2},
    # Sales department (group 3)
    {"id": 30, "label": "Emma", "group": 3},
    {"id": 31, "label": "Finn", "group": 3},
    {"id": 32, "label": "Gina", "group": 3},
    {"id": 33, "label": "Hugo", "group": 3},
    {"id": 34, "label": "Iris", "group": 3},
    {"id": 35, "label": "James", "group": 3},
    {"id": 36, "label": "Kelly", "group": 3},
    {"id": 37, "label": "Liam", "group": 3},
    {"id": 38, "label": "Maya", "group": 3},
    {"id": 39, "label": "Nick", "group": 3},
]

# Edges with weights representing collaboration intensity
edges = [
    # Engineering internal (dense connections)
    (0, 1, 3),
    (0, 2, 2),
    (0, 3, 2),
    (1, 2, 3),
    (1, 4, 2),
    (2, 3, 2),
    (2, 5, 1),
    (3, 4, 3),
    (3, 6, 2),
    (4, 5, 2),
    (4, 7, 1),
    (5, 6, 3),
    (5, 8, 2),
    (6, 7, 2),
    (6, 9, 1),
    (7, 8, 3),
    (7, 9, 2),
    (8, 9, 2),
    (0, 9, 1),
    (1, 8, 1),
    # Design internal (dense connections)
    (10, 11, 3),
    (10, 12, 2),
    (10, 13, 2),
    (11, 12, 3),
    (11, 14, 2),
    (12, 13, 2),
    (12, 15, 1),
    (13, 14, 3),
    (13, 16, 2),
    (14, 15, 2),
    (14, 17, 1),
    (15, 16, 3),
    (15, 18, 2),
    (16, 17, 2),
    (16, 19, 1),
    (17, 18, 3),
    (17, 19, 2),
    (18, 19, 2),
    (10, 19, 1),
    (11, 18, 1),
    # Marketing internal (dense connections)
    (20, 21, 3),
    (20, 22, 2),
    (20, 23, 2),
    (21, 22, 3),
    (21, 24, 2),
    (22, 23, 2),
    (22, 25, 1),
    (23, 24, 3),
    (23, 26, 2),
    (24, 25, 2),
    (24, 27, 1),
    (25, 26, 3),
    (25, 28, 2),
    (26, 27, 2),
    (26, 29, 1),
    (27, 28, 3),
    (27, 29, 2),
    (28, 29, 2),
    (20, 29, 1),
    (21, 28, 1),
    # Sales internal (dense connections)
    (30, 31, 3),
    (30, 32, 2),
    (30, 33, 2),
    (31, 32, 3),
    (31, 34, 2),
    (32, 33, 2),
    (32, 35, 1),
    (33, 34, 3),
    (33, 36, 2),
    (34, 35, 2),
    (34, 37, 1),
    (35, 36, 3),
    (35, 38, 2),
    (36, 37, 2),
    (36, 39, 1),
    (37, 38, 3),
    (37, 39, 2),
    (38, 39, 2),
    (30, 39, 1),
    (31, 38, 1),
    # Cross-department bridges (weaker connections)
    (0, 10, 1),
    (2, 12, 1),
    (5, 15, 1),  # Engineering-Design
    (10, 20, 1),
    (14, 24, 1),
    (18, 28, 1),  # Design-Marketing
    (20, 30, 1),
    (23, 33, 1),
    (27, 37, 1),  # Marketing-Sales
    (9, 39, 1),
    (4, 34, 1),  # Engineering-Sales
    (3, 23, 1),
    (7, 27, 1),  # Engineering-Marketing
    (13, 33, 1),
    (16, 36, 1),  # Design-Sales
]

# Force-directed layout algorithm (Fruchterman-Reingold inspired)
n = len(nodes)
positions = np.random.rand(n, 2) * 2 - 1  # Random initial positions

# Algorithm parameters
k = 0.3  # Optimal spring length
iterations = 200
temperature = 1.0

for iteration in range(iterations):
    displacement = np.zeros((n, 2))

    # Repulsive forces: all nodes push each other apart
    for i in range(n):
        for j in range(i + 1, n):
            diff = positions[i] - positions[j]
            dist = max(np.linalg.norm(diff), 0.01)
            # Repulsive force inversely proportional to distance
            force_magnitude = (k * k) / dist
            force = force_magnitude * (diff / dist)
            displacement[i] += force
            displacement[j] -= force

    # Attractive forces: connected nodes pull together
    for src, tgt, weight in edges:
        diff = positions[src] - positions[tgt]
        dist = max(np.linalg.norm(diff), 0.01)
        # Attractive force proportional to distance, scaled by edge weight
        force_magnitude = (dist * dist / k) * (weight / 3)
        force = force_magnitude * (diff / dist)
        displacement[src] -= force
        displacement[tgt] += force

    # Apply displacement with simulated annealing (cooling)
    cooling = temperature * (1 - iteration / iterations)
    for i in range(n):
        disp_norm = np.linalg.norm(displacement[i])
        if disp_norm > 0:
            # Limit maximum displacement by temperature
            positions[i] += (displacement[i] / disp_norm) * min(disp_norm, cooling * 0.1)

# Normalize positions to [0.05, 0.95] range for plot margins
pos_min = positions.min(axis=0)
pos_max = positions.max(axis=0)
positions = (positions - pos_min) / (pos_max - pos_min + 1e-6) * 0.9 + 0.05
pos = {node["id"]: positions[i] for i, node in enumerate(nodes)}

# Calculate node degrees for sizing (more connections = larger node)
degrees = {node["id"]: 0 for node in nodes}
for src, tgt, _ in edges:
    degrees[src] += 1
    degrees[tgt] += 1

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))

# Color palette for departments
palette = sns.color_palette(["#306998", "#FFD43B", "#4CAF50", "#FF7043"])
group_labels = ["Engineering", "Design", "Marketing", "Sales"]

# Draw edges with thickness based on weight
for src, tgt, weight in edges:
    x_coords = [pos[src][0], pos[tgt][0]]
    y_coords = [pos[src][1], pos[tgt][1]]
    # Different groups get different edge styling
    if nodes[src]["group"] == nodes[tgt]["group"]:
        ax.plot(x_coords, y_coords, color="#555555", linewidth=1.5 + weight * 0.5, alpha=0.4, zorder=1)
    else:
        # Cross-department edges are dashed
        ax.plot(x_coords, y_coords, color="#999999", linewidth=2, alpha=0.6, linestyle="--", zorder=1)

# Draw nodes using scatter for each department
for group_id in range(4):
    group_nodes = [node for node in nodes if node["group"] == group_id]
    x_vals = [pos[node["id"]][0] for node in group_nodes]
    y_vals = [pos[node["id"]][1] for node in group_nodes]
    # Size proportional to degree (number of connections)
    sizes = [400 + degrees[node["id"]] * 80 for node in group_nodes]
    ax.scatter(
        x_vals,
        y_vals,
        s=sizes,
        c=[palette[group_id]],
        edgecolors="#333333",
        linewidths=2,
        alpha=0.9,
        zorder=2,
        label=group_labels[group_id],
    )

# Style
ax.set_title("Team Collaboration · network-force-directed · seaborn · pyplots.ai", fontsize=24)
ax.set_xlim(-0.02, 1.02)
ax.set_ylim(-0.02, 1.02)
ax.axis("off")

# Legend
ax.legend(loc="upper left", fontsize=16, framealpha=0.9, title="Departments", title_fontsize=18, markerscale=0.6)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
