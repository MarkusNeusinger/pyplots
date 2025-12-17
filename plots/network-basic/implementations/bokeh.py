"""
network-basic: Basic Network Graph
Library: bokeh
"""

import numpy as np
from bokeh.io import export_png, save
from bokeh.models import ColumnDataSource, HoverTool, LabelSet
from bokeh.plotting import figure


# Data - Small social network with 20 people and friendship connections
np.random.seed(42)

# Create nodes with names and groups (communities)
node_names = [
    "Alice",
    "Bob",
    "Carol",
    "David",
    "Eva",
    "Frank",
    "Grace",
    "Henry",
    "Ivy",
    "Jack",
    "Kate",
    "Leo",
    "Mia",
    "Nick",
    "Olivia",
    "Paul",
    "Quinn",
    "Rosa",
    "Sam",
    "Tina",
]

# Assign groups (3 communities)
groups = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2]

# Define edges (friendships) - connections within and between communities
edges = [
    # Community 0 (tightly connected)
    ("Alice", "Bob"),
    ("Alice", "Carol"),
    ("Bob", "Carol"),
    ("Bob", "David"),
    ("Carol", "Eva"),
    ("David", "Eva"),
    ("Alice", "Frank"),
    ("David", "Frank"),
    # Community 1 (tightly connected)
    ("Grace", "Henry"),
    ("Grace", "Ivy"),
    ("Henry", "Jack"),
    ("Ivy", "Kate"),
    ("Jack", "Leo"),
    ("Kate", "Mia"),
    ("Henry", "Mia"),
    ("Leo", "Mia"),
    ("Grace", "Leo"),
    # Community 2 (tightly connected)
    ("Nick", "Olivia"),
    ("Nick", "Paul"),
    ("Olivia", "Quinn"),
    ("Paul", "Rosa"),
    ("Quinn", "Sam"),
    ("Rosa", "Tina"),
    ("Nick", "Tina"),
    ("Sam", "Tina"),
    ("Paul", "Quinn"),
    # Between-community connections (bridges)
    ("Frank", "Grace"),
    ("Eva", "Henry"),  # 0 <-> 1
    ("Mia", "Nick"),
    ("Leo", "Olivia"),  # 1 <-> 2
    ("Carol", "Paul"),  # 0 <-> 2
]

# Build adjacency list and calculate degrees
name_to_idx = {name: i for i, name in enumerate(node_names)}
n_nodes = len(node_names)
adjacency = [[] for _ in range(n_nodes)]
for src, tgt in edges:
    i, j = name_to_idx[src], name_to_idx[tgt]
    adjacency[i].append(j)
    adjacency[j].append(i)

degrees = [len(adj) for adj in adjacency]


# Spring layout algorithm (force-directed)
def spring_layout(n_nodes, adjacency, iterations=100, k=0.5, seed=42):
    """Simple spring layout using force-directed algorithm."""
    rng = np.random.RandomState(seed)
    # Initialize random positions
    pos = rng.rand(n_nodes, 2) * 2 - 1

    for _ in range(iterations):
        forces = np.zeros((n_nodes, 2))

        # Repulsive forces between all pairs
        for i in range(n_nodes):
            for j in range(i + 1, n_nodes):
                diff = pos[i] - pos[j]
                dist = max(np.linalg.norm(diff), 0.01)
                force = k * k / dist * diff / dist
                forces[i] += force
                forces[j] -= force

        # Attractive forces along edges
        for i, neighbors in enumerate(adjacency):
            for j in neighbors:
                if i < j:
                    diff = pos[j] - pos[i]
                    dist = max(np.linalg.norm(diff), 0.01)
                    force = dist * dist / k * diff / dist
                    forces[i] += force
                    forces[j] -= force

        # Apply forces with cooling
        cooling = 1 - _ / iterations
        pos += forces * 0.1 * cooling

        # Keep within bounds
        pos = np.clip(pos, -1, 1)

    return pos


# Calculate spring layout positions
positions = spring_layout(n_nodes, adjacency, iterations=150, k=0.4, seed=42)

# Extract node positions
node_x = positions[:, 0].tolist()
node_y = positions[:, 1].tolist()
# Scale degrees to reasonable marker sizes (larger for visibility at 4800x2700)
min_size, max_size = 40, 90
min_deg, max_deg = min(degrees), max(degrees)
if max_deg > min_deg:
    node_sizes = [min_size + (d - min_deg) / (max_deg - min_deg) * (max_size - min_size) for d in degrees]
else:
    node_sizes = [60] * len(degrees)

# Colors for groups (colorblind-safe)
group_colors = ["#306998", "#FFD43B", "#E69F00"]
node_colors = [group_colors[g] for g in groups]

# Create edge data using node positions
edge_xs = []
edge_ys = []
for source, target in edges:
    src_idx = name_to_idx[source]
    tgt_idx = name_to_idx[target]
    edge_xs.append([node_x[src_idx], node_x[tgt_idx]])
    edge_ys.append([node_y[src_idx], node_y[tgt_idx]])

# Create figure
p = figure(
    width=4800,
    height=2700,
    title="network-basic · bokeh · pyplots.ai",
    tools="hover,pan,wheel_zoom,reset,save",
    x_range=(-1.5, 1.5),
    y_range=(-1.3, 1.3),
)

# Remove axes and grid for cleaner network visualization
p.axis.visible = False
p.grid.visible = False
p.outline_line_color = None

# Style title
p.title.text_font_size = "32pt"
p.title.align = "center"

# Draw edges
p.multi_line(xs=edge_xs, ys=edge_ys, line_color="#888888", line_alpha=0.6, line_width=3)

# Draw nodes
node_source = ColumnDataSource(
    data={
        "x": node_x,
        "y": node_y,
        "name": node_names,
        "group": [f"Community {g + 1}" for g in groups],
        "connections": degrees,
        "size": node_sizes,
        "color": node_colors,
    }
)

nodes = p.scatter(
    x="x", y="y", source=node_source, size="size", fill_color="color", fill_alpha=0.85, line_color="white", line_width=3
)

# Add hover tool
hover = p.select(type=HoverTool)
hover.tooltips = [("Name", "@name"), ("Community", "@group"), ("Connections", "@connections")]
hover.renderers = [nodes]

# Add labels for nodes (larger font for 4800x2700 canvas)
labels = LabelSet(
    x="x",
    y="y",
    text="name",
    source=node_source,
    text_font_size="18pt",
    text_color="#333333",
    text_align="center",
    y_offset=12,
    text_baseline="bottom",
    text_font_style="bold",
)
p.add_layout(labels)

# Add legend manually
legend_x = 1.15
legend_y = 1.1
legend_labels = ["Community 1", "Community 2", "Community 3"]
for i, (label, color) in enumerate(zip(legend_labels, group_colors, strict=True)):
    y_pos = legend_y - i * 0.15
    p.scatter(x=[legend_x - 0.08], y=[y_pos], size=25, fill_color=color, line_color="white", line_width=2)
    p.text(x=[legend_x], y=[y_pos], text=[label], text_font_size="20pt", text_baseline="middle", text_color="#333333")

# Save as PNG
export_png(p, filename="plot.png")

# Save as HTML (interactive)
save(p, filename="plot.html", title="network-basic · bokeh · pyplots.ai")
