"""
network-force-directed: Force-Directed Graph
Library: altair
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Social network representing team collaborations
np.random.seed(42)

# Define nodes (people in a company)
nodes = [
    {"id": 0, "name": "Alice", "group": "Engineering"},
    {"id": 1, "name": "Bob", "group": "Engineering"},
    {"id": 2, "name": "Carol", "group": "Engineering"},
    {"id": 3, "name": "David", "group": "Engineering"},
    {"id": 4, "name": "Eve", "group": "Design"},
    {"id": 5, "name": "Frank", "group": "Design"},
    {"id": 6, "name": "Grace", "group": "Design"},
    {"id": 7, "name": "Henry", "group": "Product"},
    {"id": 8, "name": "Ivy", "group": "Product"},
    {"id": 9, "name": "Jack", "group": "Product"},
    {"id": 10, "name": "Kate", "group": "Marketing"},
    {"id": 11, "name": "Leo", "group": "Marketing"},
    {"id": 12, "name": "Mia", "group": "Sales"},
    {"id": 13, "name": "Noah", "group": "Sales"},
    {"id": 14, "name": "Olivia", "group": "HR"},
]

# Define edges (collaboration connections)
edges = [
    # Engineering team connections (dense)
    {"source": 0, "target": 1, "weight": 3},
    {"source": 0, "target": 2, "weight": 2},
    {"source": 0, "target": 3, "weight": 2},
    {"source": 1, "target": 2, "weight": 3},
    {"source": 1, "target": 3, "weight": 1},
    {"source": 2, "target": 3, "weight": 2},
    # Design team connections
    {"source": 4, "target": 5, "weight": 3},
    {"source": 4, "target": 6, "weight": 2},
    {"source": 5, "target": 6, "weight": 2},
    # Product team connections
    {"source": 7, "target": 8, "weight": 3},
    {"source": 7, "target": 9, "weight": 2},
    {"source": 8, "target": 9, "weight": 2},
    # Marketing team connections
    {"source": 10, "target": 11, "weight": 3},
    # Sales team connections
    {"source": 12, "target": 13, "weight": 3},
    # Cross-team connections (Alice is a hub)
    {"source": 0, "target": 4, "weight": 2},  # Eng-Design
    {"source": 0, "target": 7, "weight": 2},  # Eng-Product
    {"source": 0, "target": 10, "weight": 1},  # Eng-Marketing
    # Design-Product collaboration
    {"source": 4, "target": 7, "weight": 2},
    {"source": 5, "target": 8, "weight": 1},
    {"source": 6, "target": 9, "weight": 1},
    # Product-Marketing collaboration
    {"source": 7, "target": 10, "weight": 2},
    {"source": 8, "target": 11, "weight": 1},
    # Sales-Marketing collaboration
    {"source": 10, "target": 12, "weight": 2},
    {"source": 11, "target": 13, "weight": 1},
    # HR connections (isolated but connected to leadership)
    {"source": 14, "target": 0, "weight": 1},
    {"source": 14, "target": 7, "weight": 1},
    {"source": 14, "target": 10, "weight": 1},
]

n_nodes = len(nodes)
n_edges = len(edges)

# Calculate node degrees for sizing
degrees = np.zeros(n_nodes)
for edge in edges:
    degrees[edge["source"]] += 1
    degrees[edge["target"]] += 1

# Target output: 4800x2700 px with scale_factor=3.0
# Internal canvas: 1600x900 pixels
width = 1600
height = 900
center_x = width / 2
center_y = height / 2

# Force-directed layout using simple physics simulation
# Initialize positions randomly in center area
x_pos = np.random.uniform(center_x - 200, center_x + 200, n_nodes)
y_pos = np.random.uniform(center_y - 150, center_y + 150, n_nodes)

# Build adjacency for attraction forces
adjacency = {i: [] for i in range(n_nodes)}
for edge in edges:
    adjacency[edge["source"]].append((edge["target"], edge["weight"]))
    adjacency[edge["target"]].append((edge["source"], edge["weight"]))

# Force-directed simulation parameters
iterations = 800
k = 120  # Optimal distance between nodes
cooling = 0.97  # Temperature cooling rate
temperature = 80  # Initial temperature

for _ in range(iterations):
    # Calculate forces
    fx = np.zeros(n_nodes)
    fy = np.zeros(n_nodes)

    # Repulsive forces between all nodes (Coulomb's law)
    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            dx = x_pos[i] - x_pos[j]
            dy = y_pos[i] - y_pos[j]
            dist = np.sqrt(dx**2 + dy**2) + 0.1  # Avoid division by zero
            # Repulsive force proportional to k^2 / distance
            force = (k * k) / dist
            fx[i] += (dx / dist) * force
            fy[i] += (dy / dist) * force
            fx[j] -= (dx / dist) * force
            fy[j] -= (dy / dist) * force

    # Attractive forces along edges (Hooke's law)
    for edge in edges:
        i = edge["source"]
        j = edge["target"]
        w = edge["weight"]
        dx = x_pos[i] - x_pos[j]
        dy = y_pos[i] - y_pos[j]
        dist = np.sqrt(dx**2 + dy**2) + 0.1
        # Attractive force proportional to distance / k, scaled by weight
        force = (dist / k) * w * 0.5
        fx[i] -= (dx / dist) * force
        fy[i] -= (dy / dist) * force
        fx[j] += (dx / dist) * force
        fy[j] += (dy / dist) * force

    # Centering force (gentle pull toward center)
    for i in range(n_nodes):
        fx[i] -= (x_pos[i] - center_x) * 0.01
        fy[i] -= (y_pos[i] - center_y) * 0.01

    # Apply forces with temperature limiting
    for i in range(n_nodes):
        force_mag = np.sqrt(fx[i] ** 2 + fy[i] ** 2) + 0.1
        # Limit displacement by temperature
        scale = min(temperature, force_mag) / force_mag
        x_pos[i] += fx[i] * scale
        y_pos[i] += fy[i] * scale

    # Cool down
    temperature *= cooling

    # Keep nodes within bounds
    margin = 100
    x_pos = np.clip(x_pos, margin, width - margin)
    y_pos = np.clip(y_pos, margin, height - margin - 50)  # Extra margin for title

# Color palette by group
group_colors = {
    "Engineering": "#306998",  # Python Blue
    "Design": "#FFD43B",  # Python Yellow
    "Product": "#4ECDC4",  # Teal
    "Marketing": "#FF6B6B",  # Coral
    "Sales": "#95E1D3",  # Mint
    "HR": "#A86EDB",  # Purple
}

# Create nodes DataFrame
nodes_df = pd.DataFrame(nodes)
nodes_df["x"] = x_pos
nodes_df["y"] = y_pos
nodes_df["degree"] = degrees
nodes_df["color"] = nodes_df["group"].map(group_colors)
# Scale node size by degree (more connections = larger node)
min_size = 600
max_size = 2000
nodes_df["size"] = min_size + (degrees - degrees.min()) / (degrees.max() - degrees.min() + 0.1) * (max_size - min_size)

# Create edges DataFrame with line segments
edges_data = []
for edge in edges:
    i = edge["source"]
    j = edge["target"]
    edges_data.append(
        {
            "edge_id": f"{i}-{j}",
            "x": x_pos[i],
            "y": y_pos[i],
            "x2": x_pos[j],
            "y2": y_pos[j],
            "weight": edge["weight"],
            "order": 0,
        }
    )

edges_df = pd.DataFrame(edges_data)
# Scale edge width by weight
edges_df["strokeWidth"] = edges_df["weight"] * 2

# Create edges using mark_rule for straight lines
edges_chart = (
    alt.Chart(edges_df)
    .mark_rule(color="#999999", opacity=0.6)
    .encode(
        x=alt.X("x:Q", scale=alt.Scale(domain=[0, width]), axis=None),
        y=alt.Y("y:Q", scale=alt.Scale(domain=[0, height]), axis=None),
        x2="x2:Q",
        y2="y2:Q",
        strokeWidth=alt.StrokeWidth("strokeWidth:Q", legend=None),
        tooltip=[alt.Tooltip("weight:Q", title="Connection Strength")],
    )
)

# Create nodes using mark_circle
nodes_chart = (
    alt.Chart(nodes_df)
    .mark_circle(stroke="white", strokeWidth=2, opacity=0.9)
    .encode(
        x=alt.X("x:Q", scale=alt.Scale(domain=[0, width]), axis=None),
        y=alt.Y("y:Q", scale=alt.Scale(domain=[0, height]), axis=None),
        size=alt.Size("size:Q", legend=None),
        color=alt.Color(
            "group:N",
            scale=alt.Scale(domain=list(group_colors.keys()), range=list(group_colors.values())),
            legend=alt.Legend(title="Department", titleFontSize=18, labelFontSize=14, orient="right", symbolSize=300),
        ),
        tooltip=[
            alt.Tooltip("name:N", title="Name"),
            alt.Tooltip("group:N", title="Department"),
            alt.Tooltip("degree:Q", title="Connections"),
        ],
    )
)

# Create labels for nodes
labels_chart = (
    alt.Chart(nodes_df)
    .mark_text(fontSize=14, fontWeight="bold", dy=-25, color="#333333")
    .encode(
        x=alt.X("x:Q", scale=alt.Scale(domain=[0, width])),
        y=alt.Y("y:Q", scale=alt.Scale(domain=[0, height])),
        text="name:N",
    )
)

# Combine layers (edges first, then nodes, then labels)
chart = (
    alt.layer(edges_chart, nodes_chart, labels_chart)
    .properties(
        width=width,
        height=height,
        title=alt.Title(
            text="Team Collaboration Network · network-force-directed · altair · pyplots.ai",
            fontSize=28,
            anchor="middle",
        ),
        autosize=alt.AutoSizeParams(type="fit", contains="padding"),
    )
    .configure_view(strokeWidth=0)
    .configure_legend(padding=10, cornerRadius=5, fillColor="#FFFFFF", strokeColor="#DDDDDD")
)

# Save as PNG (4800x2700 px with scale_factor=3.0) and HTML
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
