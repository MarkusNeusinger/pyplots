"""
network-force-directed: Force-Directed Graph
Library: seaborn
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Set seaborn style
sns.set_theme(style="white")

# Seed for reproducibility
np.random.seed(42)

# Generate sample social network data with community structure (50 nodes)
n_nodes = 50
communities = {
    "Tech": list(range(0, 15)),
    "Marketing": list(range(15, 28)),
    "Design": list(range(28, 40)),
    "Management": list(range(40, 50)),
}

# Build adjacency list and edge list
edges = []
adjacency = {i: [] for i in range(n_nodes)}

# Add edges within communities (high probability)
for _community, nodes in communities.items():
    for i, n1 in enumerate(nodes):
        for n2 in nodes[i + 1 :]:
            if np.random.random() < 0.35:
                weight = np.random.uniform(0.5, 1.0)
                edges.append((n1, n2, weight))
                adjacency[n1].append(n2)
                adjacency[n2].append(n1)

# Add edges between communities (lower probability)
community_list = list(communities.values())
for i, comm1 in enumerate(community_list):
    for comm2 in community_list[i + 1 :]:
        for n1 in comm1:
            for n2 in comm2:
                if np.random.random() < 0.03:
                    weight = np.random.uniform(0.2, 0.5)
                    edges.append((n1, n2, weight))
                    adjacency[n1].append(n2)
                    adjacency[n2].append(n1)

# Calculate node degrees
degrees = {i: len(adjacency[i]) for i in range(n_nodes)}

# Force-directed layout algorithm (Fruchterman-Reingold style)
positions = np.random.rand(n_nodes, 2) * 10 - 5

# Layout parameters
k = 1.5  # Optimal distance
iterations = 150
cooling_factor = 0.95
temperature = 2.0

for _iteration in range(iterations):
    # Calculate repulsive forces (all nodes push each other away)
    displacement = np.zeros((n_nodes, 2))

    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            delta = positions[i] - positions[j]
            distance = max(np.linalg.norm(delta), 0.01)
            # Repulsive force: k^2 / d
            force = (k * k / distance) * (delta / distance)
            displacement[i] += force
            displacement[j] -= force

    # Calculate attractive forces (connected nodes pull together)
    for n1, n2, weight in edges:
        delta = positions[n1] - positions[n2]
        distance = max(np.linalg.norm(delta), 0.01)
        # Attractive force: d^2 / k, scaled by weight
        force = (distance * distance / k) * weight * (delta / distance)
        displacement[n1] -= force
        displacement[n2] += force

    # Apply displacement with temperature limiting
    for i in range(n_nodes):
        disp_norm = max(np.linalg.norm(displacement[i]), 0.01)
        positions[i] += (displacement[i] / disp_norm) * min(disp_norm, temperature)

    # Cool down
    temperature *= cooling_factor

# Normalize positions to [-1, 1] range
pos_min = positions.min(axis=0)
pos_max = positions.max(axis=0)
positions = 2 * (positions - pos_min) / (pos_max - pos_min + 0.001) - 1

# Map nodes to communities
node_community = {}
for comm_name, nodes in communities.items():
    for n in nodes:
        node_community[n] = comm_name

# Define colors using Python palette plus colorblind-safe additions
community_colors = {
    "Tech": "#306998",  # Python Blue
    "Marketing": "#FFD43B",  # Python Yellow
    "Design": "#8B4B8B",  # Purple
    "Management": "#2E8B57",  # Sea Green
}

node_colors = [community_colors[node_community[i]] for i in range(n_nodes)]
node_sizes = [300 + degrees[i] * 150 for i in range(n_nodes)]

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Draw edges with varying thickness based on weight
for n1, n2, weight in edges:
    x = [positions[n1, 0], positions[n2, 0]]
    y = [positions[n1, 1], positions[n2, 1]]
    ax.plot(x, y, color="#888888", linewidth=weight * 3, alpha=0.4, zorder=1)

# Draw nodes using scatter
x_coords = positions[:, 0]
y_coords = positions[:, 1]

ax.scatter(x_coords, y_coords, s=node_sizes, c=node_colors, alpha=0.85, edgecolors="white", linewidths=2, zorder=2)

# Add labels for high-degree nodes only (to avoid clutter)
degree_threshold = np.percentile(list(degrees.values()), 75)
for node in range(n_nodes):
    if degrees[node] >= degree_threshold:
        ax.annotate(
            f"{node}",
            (positions[node, 0], positions[node, 1]),
            fontsize=11,
            ha="center",
            va="center",
            fontweight="bold",
            color="white",
            zorder=3,
        )

# Create legend for communities
legend_handles = [
    plt.scatter([], [], s=300, c=color, label=comm, edgecolors="white", linewidths=2)
    for comm, color in community_colors.items()
]
ax.legend(handles=legend_handles, title="Department", title_fontsize=18, fontsize=14, loc="upper left", framealpha=0.9)

# Styling
ax.set_title("network-force-directed · seaborn · pyplots.ai", fontsize=24, pad=20)
ax.set_xlabel("Force-Directed X Position", fontsize=20)
ax.set_ylabel("Force-Directed Y Position", fontsize=20)
ax.tick_params(axis="both", labelsize=16)

# Remove spines and ticks for cleaner network look
sns.despine(left=True, bottom=True)
ax.set_xticks([])
ax.set_yticks([])

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
