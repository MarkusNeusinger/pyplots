"""
sankey-basic: Basic Sankey Diagram
Library: altair
"""

import altair as alt
import pandas as pd


# Data: Energy flow from sources to consumption sectors
flows_data = [
    {"source": "Coal", "target": "Industrial", "value": 12},
    {"source": "Coal", "target": "Residential", "value": 8},
    {"source": "Coal", "target": "Losses", "value": 5},
    {"source": "Natural Gas", "target": "Industrial", "value": 10},
    {"source": "Natural Gas", "target": "Residential", "value": 12},
    {"source": "Natural Gas", "target": "Commercial", "value": 8},
    {"source": "Natural Gas", "target": "Losses", "value": 5},
    {"source": "Renewables", "target": "Residential", "value": 8},
    {"source": "Renewables", "target": "Commercial", "value": 7},
    {"source": "Renewables", "target": "Transportation", "value": 5},
    {"source": "Nuclear", "target": "Industrial", "value": 8},
    {"source": "Nuclear", "target": "Commercial", "value": 5},
    {"source": "Nuclear", "target": "Transportation", "value": 4},
    {"source": "Nuclear", "target": "Losses", "value": 3},
]

df = pd.DataFrame(flows_data)

# Define node order
source_nodes = ["Coal", "Natural Gas", "Renewables", "Nuclear"]
target_nodes = ["Industrial", "Residential", "Commercial", "Transportation", "Losses"]

# Colors for source nodes
source_colors = {"Coal": "#306998", "Natural Gas": "#FFD43B", "Renewables": "#059669", "Nuclear": "#8B5CF6"}

target_colors = {
    "Industrial": "#DC2626",
    "Residential": "#F97316",
    "Commercial": "#059669",
    "Transportation": "#8B5CF6",
    "Losses": "#666666",
}

# Layout parameters
NODE_WIDTH = 15
GAP = 8
LEFT_X = 50
RIGHT_X = 350
TOTAL_HEIGHT = 200

# Calculate node heights based on flow totals
source_totals = df.groupby("source")["value"].sum().reindex(source_nodes).fillna(0)
target_totals = df.groupby("target")["value"].sum().reindex(target_nodes).fillna(0)

# Scale to fit
total_source = source_totals.sum()
total_target = target_totals.sum()
source_gaps = (len(source_nodes) - 1) * GAP
target_gaps = (len(target_nodes) - 1) * GAP

source_scale = (TOTAL_HEIGHT - source_gaps) / total_source
target_scale = (TOTAL_HEIGHT - target_gaps) / total_target

# Compute node positions
source_positions = {}
y = 0
for node in source_nodes:
    h = source_totals[node] * source_scale
    source_positions[node] = {"x": LEFT_X, "y0": y, "y1": y + h, "h": h}
    y += h + GAP

target_positions = {}
y = 0
for node in target_nodes:
    h = target_totals[node] * target_scale
    target_positions[node] = {"x": RIGHT_X, "y0": y, "y1": y + h, "h": h}
    y += h + GAP

# Build node rectangles data
node_data = []
for node in source_nodes:
    pos = source_positions[node]
    node_data.append(
        {
            "node": node,
            "x": pos["x"],
            "x2": pos["x"] + NODE_WIDTH,
            "y0": pos["y0"],
            "y1": pos["y1"],
            "color": source_colors[node],
            "type": "source",
        }
    )
for node in target_nodes:
    pos = target_positions[node]
    node_data.append(
        {
            "node": node,
            "x": pos["x"],
            "x2": pos["x"] + NODE_WIDTH,
            "y0": pos["y0"],
            "y1": pos["y1"],
            "color": target_colors[node],
            "type": "target",
        }
    )

nodes_df = pd.DataFrame(node_data)

# Build link paths - track used y positions for stacking flows
source_used = {node: pos["y0"] for node, pos in source_positions.items()}
target_used = {node: pos["y0"] for node, pos in target_positions.items()}

# Create polygon paths for each flow link
link_polygons = []
flow_idx = 0
for _, row in df.iterrows():
    src = row["source"]
    tgt = row["target"]
    val = row["value"]

    # Source band positions
    sy0 = source_used[src]
    sy1 = sy0 + val * source_scale
    source_used[src] = sy1

    # Target band positions
    ty0 = target_used[tgt]
    ty1 = ty0 + val * target_scale
    target_used[tgt] = ty1

    # Create bezier curve points for the link band
    sx = LEFT_X + NODE_WIDTH
    tx = RIGHT_X
    flow_id = f"{src}-{tgt}-{flow_idx}"
    flow_idx += 1

    # Generate points along top edge (left to right)
    steps = 30
    top_points = []
    bottom_points = []
    for i in range(steps):
        t = i / (steps - 1)
        # Cubic bezier for x position
        cx1 = sx + (tx - sx) * 0.4
        cx2 = sx + (tx - sx) * 0.6
        x = (1 - t) ** 3 * sx + 3 * (1 - t) ** 2 * t * cx1 + 3 * (1 - t) * t**2 * cx2 + t**3 * tx
        # Linear interpolation for y positions
        y_top = sy0 * (1 - t) + ty0 * t
        y_bottom = sy1 * (1 - t) + ty1 * t
        top_points.append((x, y_top))
        bottom_points.append((x, y_bottom))

    # Combine into polygon: top edge left-to-right, then bottom edge right-to-left
    polygon_points = top_points + bottom_points[::-1]

    for idx, (px, py) in enumerate(polygon_points):
        link_polygons.append(
            {"flow_id": flow_id, "source": src, "target": tgt, "value": val, "x": px, "y": py, "order": idx}
        )

paths_df = pd.DataFrame(link_polygons)

# Create links chart using line mark with filled area
links_chart = (
    alt.Chart(paths_df)
    .mark_line(filled=True, opacity=0.5, strokeWidth=0)
    .encode(
        x=alt.X("x:Q", scale=alt.Scale(domain=[0, 400])),
        y=alt.Y("y:Q", scale=alt.Scale(domain=[-10, TOTAL_HEIGHT + 10])),
        color=alt.Color(
            "source:N",
            scale=alt.Scale(domain=source_nodes, range=[source_colors[n] for n in source_nodes]),
            legend=alt.Legend(title="Energy Source", orient="bottom", columns=4, labelFontSize=14, titleFontSize=16),
        ),
        detail="flow_id:N",
        order="order:O",
        tooltip=["source:N", "target:N", "value:Q"],
    )
)

# Create nodes chart using rect mark
nodes_chart = (
    alt.Chart(nodes_df)
    .mark_rect(stroke="#333", strokeWidth=1)
    .encode(
        x=alt.X("x:Q"),
        x2="x2:Q",
        y=alt.Y("y0:Q"),
        y2="y1:Q",
        color=alt.Color("color:N", scale=None),
        tooltip=["node:N"],
    )
)

# Create source labels (left side, right-aligned)
source_labels_df = nodes_df[nodes_df["type"] == "source"].copy()
source_labels_df["y_mid"] = (source_labels_df["y0"] + source_labels_df["y1"]) / 2
source_labels_df["label_x"] = source_labels_df["x"] - 5

source_labels = (
    alt.Chart(source_labels_df)
    .mark_text(align="right", fontSize=16, fontWeight="bold")
    .encode(x="label_x:Q", y="y_mid:Q", text="node:N")
)

# Create target labels (right side, left-aligned)
target_labels_df = nodes_df[nodes_df["type"] == "target"].copy()
target_labels_df["y_mid"] = (target_labels_df["y0"] + target_labels_df["y1"]) / 2
target_labels_df["label_x"] = target_labels_df["x2"] + 5

target_labels = (
    alt.Chart(target_labels_df)
    .mark_text(align="left", fontSize=16, fontWeight="bold")
    .encode(x="label_x:Q", y="y_mid:Q", text="node:N")
)

# Combine all layers
chart = (
    alt.layer(links_chart, nodes_chart, source_labels, target_labels)
    .properties(
        width=1600,
        height=900,
        title=alt.Title(text="Energy Flow: Sources to Consumption Sectors", fontSize=28, anchor="middle"),
    )
    .configure_view(strokeWidth=0)
    .configure_axis(grid=False, domain=False, ticks=False, labels=False, title=None)
)

# Save outputs
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
