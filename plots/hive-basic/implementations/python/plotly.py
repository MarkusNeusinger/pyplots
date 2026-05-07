"""anyplot.ai
hive-basic: Basic Hive Plot
Library: plotly | Python 3.13
Quality: 88/100 | Updated: 2025-05-07
"""

import os

import numpy as np
import plotly.graph_objects as go


# Theme tokens
THEME = os.getenv("ANYPLOT_THEME", "light")
PAGE_BG = "#FAF8F1" if THEME == "light" else "#1A1A17"
ELEVATED_BG = "#FFFDF6" if THEME == "light" else "#242420"
INK = "#1A1A17" if THEME == "light" else "#F0EFE8"
INK_SOFT = "#4A4A44" if THEME == "light" else "#B8B7B0"
GRID = "rgba(26,26,23,0.10)" if THEME == "light" else "rgba(240,239,232,0.10)"

# Okabe-Ito palette - first three for the three axes
OKABE_ITO = ["#009E73", "#D55E00", "#0072B2"]

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
axis_angles = [90, 210, 330]
axis_colors = {cat: OKABE_ITO[i] for i, cat in enumerate(categories)}

# Create node lookup
node_lookup = {n["id"]: n for n in nodes}

# Group nodes by category and sort by degree
nodes_by_category = {cat: [] for cat in categories}
for node in nodes:
    nodes_by_category[node["category"]].append(node)

for cat in categories:
    nodes_by_category[cat].sort(key=lambda x: x["degree"], reverse=True)

# Hive plot parameters
inner_radius = 0.25
outer_radius = 0.95

# Calculate all node positions
node_positions = {}
for node in nodes:
    cat_idx = categories.index(node["category"])
    angle_deg = axis_angles[cat_idx]
    angle_rad = np.radians(angle_deg)
    cat_nodes = nodes_by_category[node["category"]]
    rank = cat_nodes.index(node)
    n_nodes = len(cat_nodes)
    t = rank / (n_nodes - 1) if n_nodes > 1 else 0.5
    radius = inner_radius + t * (outer_radius - inner_radius)
    x = radius * np.cos(angle_rad)
    y = radius * np.sin(angle_rad)
    node_positions[node["id"]] = (x, y, radius)

# Create figure
fig = go.Figure()

# Draw axes
for i, cat in enumerate(categories):
    angle_rad = np.radians(axis_angles[i])
    x_start = inner_radius * 0.7 * np.cos(angle_rad)
    y_start = inner_radius * 0.7 * np.sin(angle_rad)
    x_end = outer_radius * 1.05 * np.cos(angle_rad)
    y_end = outer_radius * 1.05 * np.sin(angle_rad)

    fig.add_trace(
        go.Scatter(
            x=[x_start, x_end],
            y=[y_start, y_end],
            mode="lines",
            line={"color": axis_colors[cat], "width": 5},
            showlegend=False,
            hoverinfo="skip",
        )
    )

# Draw edges as curved paths
for source, target in edges:
    if source not in node_positions or target not in node_positions:
        continue

    x0, y0 = node_positions[source][0], node_positions[source][1]
    x1, y1 = node_positions[target][0], node_positions[target][1]

    # Quadratic bezier curve
    cx = (x0 + x1) / 2 * 0.25
    cy = (y0 + y1) / 2 * 0.25
    t = np.linspace(0, 1, 40)
    curve_x = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t**2 * x1
    curve_y = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t**2 * y1

    source_cat = node_lookup[source]["category"]
    edge_color = axis_colors[source_cat]

    fig.add_trace(
        go.Scatter(
            x=curve_x,
            y=curve_y,
            mode="lines",
            line={"color": edge_color, "width": 2.5},
            opacity=0.35,
            showlegend=False,
            hoverinfo="skip",
        )
    )

# Draw nodes
label_offset_map = {"core": "top right", "utility": "bottom left", "interface": "bottom right"}

for cat in categories:
    cat_nodes = nodes_by_category[cat]
    xs = [node_positions[n["id"]][0] for n in cat_nodes]
    ys = [node_positions[n["id"]][1] for n in cat_nodes]
    sizes = [n["degree"] * 5 + 18 for n in cat_nodes]
    labels = [n["id"] for n in cat_nodes]
    degrees = [n["degree"] for n in cat_nodes]

    fig.add_trace(
        go.Scatter(
            x=xs,
            y=ys,
            mode="markers+text",
            marker={"size": sizes, "color": axis_colors[cat], "line": {"color": PAGE_BG, "width": 2.5}},
            text=labels,
            textposition=label_offset_map[cat],
            textfont={"size": 18, "color": INK},
            name=cat.capitalize(),
            hovertemplate="<b>%{text}</b><br>Degree: %{customdata}<extra></extra>",
            customdata=degrees,
        )
    )

# Add axis labels
for i, cat in enumerate(categories):
    angle_rad = np.radians(axis_angles[i])
    label_x = outer_radius * 1.35 * np.cos(angle_rad)
    label_y = outer_radius * 1.35 * np.sin(angle_rad)
    fig.add_annotation(
        x=label_x,
        y=label_y,
        text=f"<b>{cat.upper()}</b><br><span style='font-size:14px'>(sorted by degree)</span>",
        showarrow=False,
        font={"size": 22, "color": axis_colors[cat]},
    )

# Layout
fig.update_layout(
    title={
        "text": "hive-basic · plotly · anyplot.ai<br><sup>Software Dependency Network: nodes by module type, positioned by degree</sup>",
        "font": {"size": 32, "color": INK},
        "x": 0.5,
        "xanchor": "center",
    },
    showlegend=True,
    legend={
        "title": {"text": "Module Type", "font": {"size": 20, "color": INK}},
        "font": {"size": 18, "color": INK_SOFT},
        "x": 0.01,
        "y": 0.99,
        "bgcolor": ELEVATED_BG,
        "bordercolor": INK_SOFT,
        "borderwidth": 1,
    },
    xaxis={"showgrid": False, "zeroline": False, "showticklabels": False, "range": [-1.5, 1.5]},
    yaxis={
        "showgrid": False,
        "zeroline": False,
        "showticklabels": False,
        "range": [-1.5, 1.5],
        "scaleanchor": "x",
        "scaleratio": 1,
    },
    plot_bgcolor=PAGE_BG,
    paper_bgcolor=PAGE_BG,
    margin={"l": 40, "r": 40, "t": 120, "b": 40},
)

# Save outputs
fig.write_image(f"plot-{THEME}.png", width=1200, height=1200, scale=3)
fig.write_html(f"plot-{THEME}.html", include_plotlyjs="cdn")
