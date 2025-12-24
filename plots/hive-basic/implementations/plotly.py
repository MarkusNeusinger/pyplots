"""pyplots.ai
hive-basic: Basic Hive Plot
Library: plotly | Python 3.13
Quality: pending | Created: 2025-12-24
"""

import numpy as np
import plotly.graph_objects as go


# Data: Software module dependency network
np.random.seed(42)

# Define nodes with categories (axis assignment) and positions
# Categories: core, utility, interface (3 axes)
nodes = [
    # Core modules (axis 0)
    {"id": "engine", "category": "core", "degree": 8},
    {"id": "runtime", "category": "core", "degree": 6},
    {"id": "compiler", "category": "core", "degree": 5},
    {"id": "memory", "category": "core", "degree": 4},
    {"id": "scheduler", "category": "core", "degree": 3},
    # Utility modules (axis 1)
    {"id": "logger", "category": "utility", "degree": 7},
    {"id": "config", "category": "utility", "degree": 5},
    {"id": "cache", "category": "utility", "degree": 4},
    {"id": "parser", "category": "utility", "degree": 6},
    {"id": "validator", "category": "utility", "degree": 3},
    {"id": "formatter", "category": "utility", "degree": 2},
    # Interface modules (axis 2)
    {"id": "api", "category": "interface", "degree": 9},
    {"id": "cli", "category": "interface", "degree": 5},
    {"id": "web", "category": "interface", "degree": 6},
    {"id": "rest", "category": "interface", "degree": 4},
    {"id": "grpc", "category": "interface", "degree": 3},
]

# Define edges (dependencies between modules)
edges = [
    ("api", "engine"),
    ("api", "logger"),
    ("api", "config"),
    ("api", "cache"),
    ("cli", "engine"),
    ("cli", "parser"),
    ("cli", "formatter"),
    ("web", "runtime"),
    ("web", "logger"),
    ("web", "cache"),
    ("rest", "engine"),
    ("rest", "validator"),
    ("grpc", "runtime"),
    ("grpc", "config"),
    ("engine", "memory"),
    ("engine", "scheduler"),
    ("engine", "logger"),
    ("runtime", "memory"),
    ("runtime", "cache"),
    ("compiler", "parser"),
    ("compiler", "memory"),
    ("logger", "config"),
    ("cache", "memory"),
    ("parser", "validator"),
]

# Axis configuration
categories = ["core", "utility", "interface"]
axis_angles = [90, 210, 330]  # degrees, evenly spaced

# Create node lookup
node_lookup = {n["id"]: n for n in nodes}

# Group nodes by category and sort by degree
nodes_by_category = {cat: [] for cat in categories}
for node in nodes:
    nodes_by_category[node["category"]].append(node)

# Sort each category by degree (position along axis)
for cat in categories:
    nodes_by_category[cat].sort(key=lambda x: x["degree"], reverse=True)

# Calculate node positions on hive plot
# Each axis extends from center; nodes placed along axis based on degree rank
inner_radius = 0.2
outer_radius = 1.0


def get_node_position(node):
    """Calculate x, y position for a node on its axis."""
    cat_idx = categories.index(node["category"])
    angle_deg = axis_angles[cat_idx]
    angle_rad = np.radians(angle_deg)

    # Position along axis based on rank within category
    cat_nodes = nodes_by_category[node["category"]]
    rank = cat_nodes.index(node)
    n_nodes = len(cat_nodes)

    # Distribute nodes along axis from inner to outer radius
    if n_nodes > 1:
        t = rank / (n_nodes - 1)
    else:
        t = 0.5
    radius = inner_radius + t * (outer_radius - inner_radius)

    x = radius * np.cos(angle_rad)
    y = radius * np.sin(angle_rad)
    return x, y, radius


# Calculate all node positions
node_positions = {}
for node in nodes:
    x, y, r = get_node_position(node)
    node_positions[node["id"]] = (x, y, r)

# Create figure
fig = go.Figure()

# Draw axes
axis_colors = {"core": "#306998", "utility": "#FFD43B", "interface": "#4ECDC4"}
for i, cat in enumerate(categories):
    angle_rad = np.radians(axis_angles[i])
    x_start = inner_radius * 0.8 * np.cos(angle_rad)
    y_start = inner_radius * 0.8 * np.sin(angle_rad)
    x_end = outer_radius * 1.1 * np.cos(angle_rad)
    y_end = outer_radius * 1.1 * np.sin(angle_rad)

    fig.add_trace(
        go.Scatter(
            x=[x_start, x_end],
            y=[y_start, y_end],
            mode="lines",
            line=dict(color=axis_colors[cat], width=4),
            showlegend=False,
            hoverinfo="skip",
        )
    )

    # Axis labels
    label_x = outer_radius * 1.2 * np.cos(angle_rad)
    label_y = outer_radius * 1.2 * np.sin(angle_rad)
    fig.add_annotation(
        x=label_x, y=label_y, text=f"<b>{cat.upper()}</b>", showarrow=False, font=dict(size=20, color=axis_colors[cat])
    )


# Draw edges as curved bezier-like paths
def bezier_curve(p0, p1, num_points=50):
    """Create a curved path between two points through center region."""
    x0, y0 = p0
    x1, y1 = p1

    # Control point towards center for curvature
    cx = (x0 + x1) / 2 * 0.3
    cy = (y0 + y1) / 2 * 0.3

    t = np.linspace(0, 1, num_points)
    # Quadratic bezier
    x = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t**2 * x1
    y = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t**2 * y1
    return x, y


# Group edges by source-target category pairs for coloring
for source, target in edges:
    if source not in node_positions or target not in node_positions:
        continue

    x0, y0, _ = node_positions[source][0], node_positions[source][1], None
    x1, y1, _ = node_positions[target][0], node_positions[target][1], None

    # Get source position properly
    x0, y0 = node_positions[source][0], node_positions[source][1]
    x1, y1 = node_positions[target][0], node_positions[target][1]

    # Create curved edge
    curve_x, curve_y = bezier_curve((x0, y0), (x1, y1))

    # Color based on source category
    source_cat = node_lookup[source]["category"]
    edge_color = axis_colors[source_cat]

    fig.add_trace(
        go.Scatter(
            x=curve_x,
            y=curve_y,
            mode="lines",
            line=dict(color=edge_color, width=2),
            opacity=0.4,
            showlegend=False,
            hoverinfo="skip",
        )
    )

# Draw nodes
for cat in categories:
    cat_nodes = nodes_by_category[cat]
    xs = [node_positions[n["id"]][0] for n in cat_nodes]
    ys = [node_positions[n["id"]][1] for n in cat_nodes]
    sizes = [n["degree"] * 4 + 15 for n in cat_nodes]  # Scale marker size by degree
    labels = [n["id"] for n in cat_nodes]
    degrees = [n["degree"] for n in cat_nodes]

    fig.add_trace(
        go.Scatter(
            x=xs,
            y=ys,
            mode="markers+text",
            marker=dict(size=sizes, color=axis_colors[cat], line=dict(color="white", width=2)),
            text=labels,
            textposition="top center",
            textfont=dict(size=14, color="#333333"),
            name=cat.capitalize(),
            hovertemplate="<b>%{text}</b><br>Degree: %{customdata}<extra></extra>",
            customdata=degrees,
        )
    )

# Layout
fig.update_layout(
    title=dict(text="hive-basic · plotly · pyplots.ai", font=dict(size=32, color="#333333"), x=0.5, xanchor="center"),
    showlegend=True,
    legend=dict(
        title=dict(text="Module Type", font=dict(size=18)),
        font=dict(size=16),
        x=0.02,
        y=0.98,
        bgcolor="rgba(255,255,255,0.8)",
    ),
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.5, 1.5]),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.5, 1.5], scaleanchor="x", scaleratio=1),
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=50, r=50, t=100, b=50),
)

# Add annotation explaining the plot
fig.add_annotation(
    x=0.5,
    y=-0.12,
    xref="paper",
    yref="paper",
    text="Nodes positioned by module type (axis) and dependency degree (position along axis)",
    showarrow=False,
    font=dict(size=16, color="#666666"),
)

# Save outputs
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs="cdn")
