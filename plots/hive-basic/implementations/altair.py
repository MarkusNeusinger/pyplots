"""pyplots.ai
hive-basic: Basic Hive Plot
Library: altair | Python 3.13
Quality: pending | Created: 2025-12-24
"""

import altair as alt
import numpy as np
import pandas as pd


# Data: Software module dependency network
np.random.seed(42)

# Define nodes with module types (axis assignment) and importance (position on axis)
# Spread importance values more evenly to avoid label overlap
nodes_data = [
    # Core modules (axis 0) - foundational components
    {"id": "core_main", "name": "Main", "axis": "Core", "importance": 1.0},
    {"id": "core_db", "name": "Database", "axis": "Core", "importance": 0.85},
    {"id": "core_config", "name": "Config", "axis": "Core", "importance": 0.70},
    {"id": "core_logger", "name": "Logger", "axis": "Core", "importance": 0.55},
    {"id": "core_events", "name": "Events", "axis": "Core", "importance": 0.40},
    {"id": "core_cache", "name": "Cache", "axis": "Core", "importance": 0.25},
    # Utility modules (axis 1) - helper components
    {"id": "util_http", "name": "HTTP", "axis": "Utility", "importance": 1.0},
    {"id": "util_file", "name": "File", "axis": "Utility", "importance": 0.80},
    {"id": "util_string", "name": "String", "axis": "Utility", "importance": 0.60},
    {"id": "util_date", "name": "Date", "axis": "Utility", "importance": 0.40},
    {"id": "util_crypto", "name": "Crypto", "axis": "Utility", "importance": 0.20},
    # Interface modules (axis 2) - external-facing components
    {"id": "iface_api", "name": "API", "axis": "Interface", "importance": 1.0},
    {"id": "iface_web", "name": "WebUI", "axis": "Interface", "importance": 0.80},
    {"id": "iface_cli", "name": "CLI", "axis": "Interface", "importance": 0.60},
    {"id": "iface_ws", "name": "WebSocket", "axis": "Interface", "importance": 0.40},
    {"id": "iface_rpc", "name": "RPC", "axis": "Interface", "importance": 0.20},
]

# Define edges (dependencies between modules)
edges_data = [
    # Core to Utility connections
    ("core_main", "util_string"),
    ("core_main", "util_file"),
    ("core_config", "util_file"),
    ("core_config", "util_string"),
    ("core_logger", "util_date"),
    ("core_logger", "util_file"),
    ("core_cache", "util_crypto"),
    ("core_db", "util_string"),
    ("core_events", "util_date"),
    # Core to Interface connections
    ("core_main", "iface_api"),
    ("core_main", "iface_cli"),
    ("core_config", "iface_api"),
    ("core_db", "iface_api"),
    ("core_logger", "iface_web"),
    ("core_events", "iface_ws"),
    ("core_cache", "iface_rpc"),
    # Utility to Interface connections
    ("util_http", "iface_api"),
    ("util_http", "iface_web"),
    ("util_string", "iface_cli"),
    ("util_file", "iface_cli"),
    ("util_crypto", "iface_api"),
    ("util_date", "iface_web"),
    ("util_crypto", "iface_rpc"),
    ("util_http", "iface_ws"),
]

# Convert to DataFrame
nodes_df = pd.DataFrame(nodes_data)

# Axis configuration
axis_config = {
    "Core": {"angle": 90, "color": "#306998"},  # Python Blue - top
    "Utility": {"angle": 210, "color": "#FFD43B"},  # Python Yellow - bottom left
    "Interface": {"angle": 330, "color": "#4ECDC4"},  # Teal - bottom right
}

# Calculate node positions in polar coordinates, then convert to Cartesian
# Nodes are placed along their axis based on importance (distance from center)
min_radius = 0.2  # Start nodes away from center
max_radius = 0.9  # Maximum distance from center


def polar_to_cartesian(angle_deg, radius):
    angle_rad = np.radians(angle_deg)
    x = radius * np.cos(angle_rad)
    y = radius * np.sin(angle_rad)
    return x, y


# Calculate node positions
node_positions = {}
nodes_df["x"] = 0.0
nodes_df["y"] = 0.0

for idx, row in nodes_df.iterrows():
    axis = row["axis"]
    angle = axis_config[axis]["angle"]
    radius = min_radius + (max_radius - min_radius) * row["importance"]
    x, y = polar_to_cartesian(angle, radius)
    nodes_df.at[idx, "x"] = x
    nodes_df.at[idx, "y"] = y
    nodes_df.at[idx, "color"] = axis_config[axis]["color"]
    node_positions[row["id"]] = (x, y)

# Create edges DataFrame with start and end coordinates
edges_list = []
for source, target in edges_data:
    if source in node_positions and target in node_positions:
        x1, y1 = node_positions[source]
        x2, y2 = node_positions[target]
        # Get axis colors for gradient effect
        source_axis = nodes_df[nodes_df["id"] == source]["axis"].values[0]
        target_axis = nodes_df[nodes_df["id"] == target]["axis"].values[0]
        edges_list.append(
            {
                "x": x1,
                "y": y1,
                "x2": x2,
                "y2": y2,
                "source": source,
                "target": target,
                "connection": f"{source_axis} to {target_axis}",
            }
        )

edges_df = pd.DataFrame(edges_list)

# Create axis lines (from center outward)
axis_lines = []
for axis_name, config in axis_config.items():
    x_end, y_end = polar_to_cartesian(config["angle"], 1.0)
    axis_lines.append({"x": 0, "y": 0, "x2": x_end, "y2": y_end, "axis": axis_name, "color": config["color"]})
axis_df = pd.DataFrame(axis_lines)

# Create axis labels
axis_labels = []
for axis_name, config in axis_config.items():
    x, y = polar_to_cartesian(config["angle"], 1.1)
    axis_labels.append({"x": x, "y": y, "label": axis_name})
axis_labels_df = pd.DataFrame(axis_labels)

# Plot: Layer edges, axis lines, nodes, and labels

# Edge lines with transparency
edges_chart = (
    alt.Chart(edges_df)
    .mark_rule(strokeWidth=1.5, opacity=0.4, color="#888888")
    .encode(
        x=alt.X("x:Q", scale=alt.Scale(domain=[-1.3, 1.3])),
        y=alt.Y("y:Q", scale=alt.Scale(domain=[-1.3, 1.3])),
        x2="x2:Q",
        y2="y2:Q",
        tooltip=["source:N", "target:N", "connection:N"],
    )
)

# Axis lines
axis_chart = (
    alt.Chart(axis_df)
    .mark_rule(strokeWidth=3, opacity=0.8)
    .encode(
        x="x:Q",
        y="y:Q",
        x2="x2:Q",
        y2="y2:Q",
        color=alt.Color(
            "axis:N",
            scale=alt.Scale(domain=["Core", "Utility", "Interface"], range=["#306998", "#FFD43B", "#4ECDC4"]),
            legend=alt.Legend(title="Module Type", titleFontSize=18, labelFontSize=16),
        ),
    )
)

# Nodes
nodes_chart = (
    alt.Chart(nodes_df)
    .mark_circle(size=400, opacity=0.9, stroke="white", strokeWidth=2)
    .encode(
        x="x:Q",
        y="y:Q",
        color=alt.Color(
            "axis:N",
            scale=alt.Scale(domain=["Core", "Utility", "Interface"], range=["#306998", "#FFD43B", "#4ECDC4"]),
            legend=None,
        ),
        tooltip=["name:N", "axis:N", "importance:Q"],
    )
)

# Node labels - position offset based on axis angle
# For Core (top), offset below; for Utility (bottom-left), offset right; for Interface (bottom-right), offset left
node_labels_data = nodes_df.copy()
# Calculate label positions with offset
label_offset = 0.08
for idx, row in node_labels_data.iterrows():
    axis = row["axis"]
    if axis == "Core":
        # Labels to the right of nodes
        node_labels_data.at[idx, "label_x"] = row["x"] + label_offset
        node_labels_data.at[idx, "label_y"] = row["y"]
    elif axis == "Utility":
        # Labels to the lower-left of nodes
        node_labels_data.at[idx, "label_x"] = row["x"] - label_offset * 0.7
        node_labels_data.at[idx, "label_y"] = row["y"] - label_offset * 0.5
    else:  # Interface
        # Labels to the lower-right of nodes
        node_labels_data.at[idx, "label_x"] = row["x"] + label_offset * 0.7
        node_labels_data.at[idx, "label_y"] = row["y"] - label_offset * 0.5

node_labels = (
    alt.Chart(node_labels_data)
    .mark_text(fontSize=14, fontWeight="bold", align="left")
    .encode(x="label_x:Q", y="label_y:Q", text="name:N", color=alt.value("#333333"))
)

# Axis labels
axis_label_chart = (
    alt.Chart(axis_labels_df)
    .mark_text(fontSize=24, fontWeight="bold")
    .encode(x="x:Q", y="y:Q", text="label:N", color=alt.value("#222222"))
)

# Combine all layers
chart = (
    (edges_chart + axis_chart + nodes_chart + node_labels + axis_label_chart)
    .properties(
        width=1600,
        height=900,
        title=alt.Title(
            text="Software Module Dependencies · hive-basic · altair · pyplots.ai", fontSize=28, anchor="middle"
        ),
    )
    .configure_view(strokeWidth=0)
    .configure_axis(grid=False, domain=False, labels=False, ticks=False, title=None)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
