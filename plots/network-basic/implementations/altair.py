"""
network-basic: Basic Network Graph
Library: altair
"""

import altair as alt
import networkx as nx
import numpy as np
import pandas as pd


# Data: Small social network (friendship connections)
np.random.seed(42)

# Create network with community structure
G = nx.karate_club_graph()  # Classic 34-node social network dataset

# Compute spring layout positions with padding
pos = nx.spring_layout(G, seed=42, k=2)

# Scale positions to leave margin for labels
positions = np.array(list(pos.values()))
min_pos, max_pos = positions.min(), positions.max()
margin = 0.08  # Leave margin for edge labels
for node_id in pos:
    x, y = pos[node_id]
    pos[node_id] = (
        margin + (x - min_pos) / (max_pos - min_pos) * (1 - 2 * margin),
        margin + (y - min_pos) / (max_pos - min_pos) * (1 - 2 * margin),
    )

# Prepare node data
node_data = []
for node_id in G.nodes():
    x, y = pos[node_id]
    degree = G.degree(node_id)
    node_data.append({"id": node_id, "x": x, "y": y, "label": f"P{node_id}", "degree": degree})
nodes_df = pd.DataFrame(node_data)

# Prepare edge data
edge_data = []
for source, target in G.edges():
    edge_data.append(
        {
            "source": source,
            "target": target,
            "x": pos[source][0],
            "y": pos[source][1],
            "x2": pos[target][0],
            "y2": pos[target][1],
        }
    )
edges_df = pd.DataFrame(edge_data)

# Create edge layer (lines)
edges = (
    alt.Chart(edges_df)
    .mark_rule(strokeWidth=1.5, opacity=0.4, color="#888888")
    .encode(
        x=alt.X("x:Q", axis=None, scale=alt.Scale(domain=[0, 1])),
        y=alt.Y("y:Q", axis=None, scale=alt.Scale(domain=[0, 1])),
        x2="x2:Q",
        y2="y2:Q",
    )
)

# Create node layer (circles) - size encodes degree
nodes = (
    alt.Chart(nodes_df)
    .mark_circle(stroke="white", strokeWidth=2)
    .encode(
        x=alt.X("x:Q", axis=None, scale=alt.Scale(domain=[0, 1])),
        y=alt.Y("y:Q", axis=None, scale=alt.Scale(domain=[0, 1])),
        size=alt.Size("degree:Q", scale=alt.Scale(range=[400, 2000]), legend=None),
        color=alt.value("#306998"),
        tooltip=["label:N", "degree:Q"],
    )
)

# Create label layer
labels = (
    alt.Chart(nodes_df)
    .mark_text(fontSize=14, fontWeight="bold", color="white", align="center", baseline="middle")
    .encode(
        x=alt.X("x:Q", scale=alt.Scale(domain=[0, 1])), y=alt.Y("y:Q", scale=alt.Scale(domain=[0, 1])), text="label:N"
    )
)

# Combine layers
chart = (
    (edges + nodes + labels)
    .properties(
        width=1600, height=900, title=alt.Title("network-basic · altair · pyplots.ai", fontSize=32, anchor="middle")
    )
    .configure_view(
        strokeWidth=0  # Remove border
    )
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
