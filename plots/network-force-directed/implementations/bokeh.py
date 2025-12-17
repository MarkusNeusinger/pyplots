"""
network-force-directed: Force-Directed Graph
Library: bokeh
"""

import networkx as nx
import numpy as np
from bokeh.io import export_png, save
from bokeh.models import ColumnDataSource, LabelSet, Range1d
from bokeh.plotting import figure
from bokeh.resources import CDN


# Data: Create a social network with communities
np.random.seed(42)

# Create a network with clear community structure
G = nx.Graph()

# Define communities (groups of people)
communities = {
    "Tech": ["Alice", "Bob", "Carol", "Dave", "Eve"],
    "Marketing": ["Frank", "Grace", "Henry", "Ivy"],
    "Design": ["Jack", "Kate", "Leo", "Mia", "Nina"],
    "Management": ["Oscar", "Paul", "Quinn"],
}

# Add nodes with community labels
for community, members in communities.items():
    for member in members:
        G.add_node(member, community=community)

# Add edges within communities (dense connections)
for _community, members in communities.items():
    for i, m1 in enumerate(members):
        for m2 in members[i + 1 :]:
            if np.random.random() < 0.7:  # 70% chance of connection within community
                G.add_edge(m1, m2, weight=np.random.uniform(1, 3))

# Add edges between communities (sparse connections)
all_members = list(G.nodes())
for _ in range(10):
    n1, n2 = np.random.choice(all_members, 2, replace=False)
    if not G.has_edge(n1, n2) and G.nodes[n1]["community"] != G.nodes[n2]["community"]:
        G.add_edge(n1, n2, weight=np.random.uniform(0.5, 1.5))

# Compute force-directed layout
pos = nx.spring_layout(G, k=2, iterations=100, seed=42)

# Extract node positions and properties
node_x = [pos[node][0] for node in G.nodes()]
node_y = [pos[node][1] for node in G.nodes()]
node_names = list(G.nodes())
node_communities = [G.nodes[node]["community"] for node in G.nodes()]
node_degrees = [G.degree(node) for node in G.nodes()]

# Scale node size by degree
min_size, max_size = 25, 60
min_deg, max_deg = min(node_degrees), max(node_degrees)
if max_deg > min_deg:
    node_sizes = [min_size + (d - min_deg) / (max_deg - min_deg) * (max_size - min_size) for d in node_degrees]
else:
    node_sizes = [min_size] * len(node_degrees)

# Color mapping for communities
community_colors = {
    "Tech": "#306998",  # Python Blue
    "Marketing": "#FFD43B",  # Python Yellow
    "Design": "#E74C3C",  # Red
    "Management": "#27AE60",  # Green
}
node_colors = [community_colors[c] for c in node_communities]

# Extract edge data
edge_x = []
edge_y = []
edge_weights = []
for u, v, data in G.edges(data=True):
    edge_x.append([pos[u][0], pos[v][0]])
    edge_y.append([pos[u][1], pos[v][1]])
    edge_weights.append(data.get("weight", 1))

# Create figure
p = figure(
    width=4800,
    height=2700,
    title="network-force-directed · bokeh · pyplots.ai",
    x_axis_label="",
    y_axis_label="",
    tools="",
    toolbar_location=None,
)

# Hide axes for network visualization
p.xaxis.visible = False
p.yaxis.visible = False
p.xgrid.visible = False
p.ygrid.visible = False
p.outline_line_color = None

# Draw edges
for i, (ex, ey) in enumerate(zip(edge_x, edge_y, strict=True)):
    line_width = 1 + edge_weights[i] * 1.5  # Scale line width by weight
    p.line(ex, ey, line_width=line_width, color="#AAAAAA", alpha=0.6)

# Create node data source
node_source = ColumnDataSource(
    data={
        "x": node_x,
        "y": node_y,
        "name": node_names,
        "community": node_communities,
        "size": node_sizes,
        "color": node_colors,
        "degree": node_degrees,
    }
)

# Draw nodes
p.scatter(x="x", y="y", size="size", color="color", alpha=0.9, line_color="white", line_width=2, source=node_source)

# Add labels
labels = LabelSet(
    x="x",
    y="y",
    text="name",
    x_offset=8,
    y_offset=8,
    source=node_source,
    text_font_size="14pt",
    text_color="#333333",
    text_alpha=0.8,
)
p.add_layout(labels)

# Style title
p.title.text_font_size = "28pt"
p.title.align = "center"

# Add legend manually using scatter with legend_label
# Create dummy points for legend (outside visible area)
x_range = [min(node_x) - 0.5, max(node_x) + 0.5]
y_range = [min(node_y) - 0.5, max(node_y) + 0.5]
p.x_range = Range1d(x_range[0], x_range[1])
p.y_range = Range1d(y_range[0], y_range[1])

# Add legend items
for community, color in community_colors.items():
    p.scatter(x=[-999], y=[-999], size=20, color=color, legend_label=community)

p.legend.location = "top_right"
p.legend.label_text_font_size = "18pt"
p.legend.glyph_height = 30
p.legend.glyph_width = 30
p.legend.spacing = 10
p.legend.padding = 15
p.legend.background_fill_alpha = 0.8

# Save outputs
export_png(p, filename="plot.png")
save(p, filename="plot.html", resources=CDN, title="Force-Directed Network Graph")
