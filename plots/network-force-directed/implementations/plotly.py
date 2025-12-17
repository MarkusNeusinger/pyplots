"""
network-force-directed: Force-Directed Graph
Library: plotly
"""

import numpy as np
import plotly.graph_objects as go


# Data - Create a social network with community structure
np.random.seed(42)

# Define nodes with communities
# Community 1: Tech team (nodes 0-14)
# Community 2: Marketing team (nodes 15-29)
# Community 3: Sales team (nodes 30-44)
num_nodes = 45
communities = ["Tech"] * 15 + ["Marketing"] * 15 + ["Sales"] * 15

# Generate edges
edges = []
# Dense connections within communities
for comm_start, comm_end in [(0, 15), (15, 30), (30, 45)]:
    for i in range(comm_start, comm_end):
        for j in range(i + 1, comm_end):
            if np.random.random() < 0.3:  # 30% probability
                edges.append((i, j))

# Sparse connections between communities
cross_community = [(0, 15, 15, 30), (15, 30, 30, 45), (0, 15, 30, 45)]
for s1, e1, s2, e2 in cross_community:
    for _ in range(3):
        n1 = np.random.randint(s1, e1)
        n2 = np.random.randint(s2, e2)
        edges.append((n1, n2))

# Calculate node degrees
degrees = [0] * num_nodes
for n1, n2 in edges:
    degrees[n1] += 1
    degrees[n2] += 1


# Force-directed layout algorithm
def force_directed_layout(num_nodes, edges, iterations=200, k=1.0):
    """Simple force-directed layout using Fruchterman-Reingold algorithm."""
    # Initialize random positions
    pos = np.random.rand(num_nodes, 2) * 2 - 1

    # Optimal distance
    area = 4.0  # Area = 2 x 2
    optimal_dist = k * np.sqrt(area / num_nodes)

    # Build adjacency for attractive forces
    adj = {i: [] for i in range(num_nodes)}
    for n1, n2 in edges:
        adj[n1].append(n2)
        adj[n2].append(n1)

    for iteration in range(iterations):
        # Temperature decreases over iterations (cooling)
        temp = 0.5 * (1 - iteration / iterations)

        # Calculate repulsive forces (all pairs)
        displacement = np.zeros((num_nodes, 2))

        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                delta = pos[i] - pos[j]
                dist = np.linalg.norm(delta)
                if dist < 0.01:
                    dist = 0.01
                # Repulsive force
                force = (optimal_dist**2) / dist
                direction = delta / dist
                displacement[i] += direction * force
                displacement[j] -= direction * force

        # Calculate attractive forces (connected pairs)
        for n1, n2 in edges:
            delta = pos[n1] - pos[n2]
            dist = np.linalg.norm(delta)
            if dist < 0.01:
                dist = 0.01
            # Attractive force
            force = (dist**2) / optimal_dist
            direction = delta / dist
            displacement[n1] -= direction * force
            displacement[n2] += direction * force

        # Apply displacement with temperature limit
        for i in range(num_nodes):
            disp_norm = np.linalg.norm(displacement[i])
            if disp_norm > 0:
                pos[i] += (displacement[i] / disp_norm) * min(disp_norm, temp)

        # Keep within bounds
        pos = np.clip(pos, -1, 1)

    return pos


# Run force-directed layout
positions = force_directed_layout(num_nodes, edges, iterations=200)

# Prepare node data
node_x = positions[:, 0]
node_y = positions[:, 1]

# Color map for communities
color_map = {"Tech": "#306998", "Marketing": "#FFD43B", "Sales": "#E55934"}
node_colors = [color_map[comm] for comm in communities]

# Scale node sizes by degree (more connections = larger node)
min_size = 20
max_size = 50
if max(degrees) > min(degrees):
    node_sizes = [
        min_size + (max_size - min_size) * (d - min(degrees)) / (max(degrees) - min(degrees)) for d in degrees
    ]
else:
    node_sizes = [35] * len(degrees)

# Prepare edge data
edge_x = []
edge_y = []
for n1, n2 in edges:
    edge_x.extend([node_x[n1], node_x[n2], None])
    edge_y.extend([node_y[n1], node_y[n2], None])

# Create figure
fig = go.Figure()

# Add edges
fig.add_trace(
    go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line={"width": 1.5, "color": "rgba(150, 150, 150, 0.5)"},
        hoverinfo="none",
        showlegend=False,
    )
)

# Add nodes for each community (for legend)
for community, color in color_map.items():
    comm_indices = [i for i, c in enumerate(communities) if c == community]
    fig.add_trace(
        go.Scatter(
            x=[node_x[i] for i in comm_indices],
            y=[node_y[i] for i in comm_indices],
            mode="markers",
            marker={
                "size": [node_sizes[i] for i in comm_indices],
                "color": color,
                "line": {"width": 2, "color": "white"},
            },
            text=[f"Node {i}<br>Community: {community}<br>Connections: {degrees[i]}" for i in comm_indices],
            hoverinfo="text",
            name=community,
        )
    )

# Update layout
fig.update_layout(
    title={"text": "network-force-directed · plotly · pyplots.ai", "font": {"size": 36}, "x": 0.5, "xanchor": "center"},
    xaxis={"showgrid": False, "zeroline": False, "showticklabels": False, "title": ""},
    yaxis={"showgrid": False, "zeroline": False, "showticklabels": False, "title": "", "scaleanchor": "x"},
    template="plotly_white",
    showlegend=True,
    legend={
        "font": {"size": 22},
        "title": {"text": "Community", "font": {"size": 24}},
        "itemsizing": "constant",
        "x": 1.02,
        "y": 0.5,
        "yanchor": "middle",
    },
    margin={"l": 40, "r": 180, "t": 100, "b": 40},
)

# Save as PNG and HTML
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs="cdn")
