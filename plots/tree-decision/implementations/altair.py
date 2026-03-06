""" pyplots.ai
tree-decision: Decision Tree Visualization with Probabilities
Library: altair 6.0.0 | Python 3.14.3
Quality: 82/100 | Created: 2026-03-06
"""

import altair as alt
import pandas as pd


# Data - Two-stage investment decision tree
# Structure: Invest vs Don't Invest, then High/Low demand for each investment option
nodes = [
    {"id": "D1", "type": "decision", "x": 0, "y": 300, "label": "", "emv": "$152K"},
    {"id": "C1", "type": "chance", "x": 200, "y": 150, "label": "Invest\nLarge", "emv": "$152K"},
    {"id": "C2", "type": "chance", "x": 200, "y": 450, "label": "Invest\nSmall", "emv": "$95K"},
    {"id": "T1", "type": "terminal", "x": 420, "y": 50, "label": "High Demand", "payoff": "$300K"},
    {"id": "T2", "type": "terminal", "x": 420, "y": 170, "label": "Moderate", "payoff": "$120K"},
    {"id": "T3", "type": "terminal", "x": 420, "y": 250, "label": "Low Demand", "payoff": "$-40K"},
    {"id": "T4", "type": "terminal", "x": 420, "y": 370, "label": "High Demand", "payoff": "$180K"},
    {"id": "T5", "type": "terminal", "x": 420, "y": 450, "label": "Moderate", "payoff": "$90K"},
    {"id": "T6", "type": "terminal", "x": 420, "y": 530, "label": "Low Demand", "payoff": "$20K"},
]

edges = [
    {"x": 0, "y": 300, "x2": 200, "y2": 150, "label": "Invest Large", "prob": "", "pruned": False},
    {"x": 0, "y": 300, "x2": 200, "y2": 450, "label": "Invest Small", "prob": "", "pruned": True},
    {"x": 200, "y": 150, "x2": 420, "y2": 50, "label": "", "prob": "0.40", "pruned": False},
    {"x": 200, "y": 150, "x2": 420, "y2": 170, "label": "", "prob": "0.35", "pruned": False},
    {"x": 200, "y": 150, "x2": 420, "y2": 250, "label": "", "prob": "0.25", "pruned": False},
    {"x": 200, "y": 450, "x2": 420, "y2": 370, "label": "", "prob": "0.40", "pruned": True},
    {"x": 200, "y": 450, "x2": 420, "y2": 450, "label": "", "prob": "0.35", "pruned": True},
    {"x": 200, "y": 450, "x2": 420, "y2": 530, "label": "", "prob": "0.25", "pruned": True},
]

nodes_df = pd.DataFrame(nodes)
edges_df = pd.DataFrame(edges)

decision_df = nodes_df[nodes_df["type"] == "decision"]
chance_df = nodes_df[nodes_df["type"] == "chance"]
terminal_df = nodes_df[nodes_df["type"] == "terminal"]

# Edges - split by pruned status
edges_active = edges_df[~edges_df["pruned"]]
edges_pruned = edges_df[edges_df["pruned"]]

# Edge midpoints for labels
edges_df["mx"] = (edges_df["x"] + edges_df["x2"]) / 2
edges_df["my"] = (edges_df["y"] + edges_df["y2"]) / 2
edge_labels_branch = edges_df[edges_df["label"] != ""]
edge_labels_prob = edges_df[edges_df["prob"] != ""]

x_scale = alt.Scale(domain=[-60, 560])
y_scale = alt.Scale(domain=[620, -40])

# Active branches (solid lines)
active_lines = (
    alt.Chart(edges_active)
    .mark_rule(strokeWidth=3, color="#555555")
    .encode(x=alt.X("x:Q", scale=x_scale, axis=None), y=alt.Y("y:Q", scale=y_scale, axis=None), x2="x2:Q", y2="y2:Q")
)

# Pruned branches (dashed lines, lower opacity)
pruned_lines = (
    alt.Chart(edges_pruned)
    .mark_rule(strokeWidth=2, strokeDash=[8, 6], opacity=0.35, color="#888888")
    .encode(x=alt.X("x:Q", scale=x_scale, axis=None), y=alt.Y("y:Q", scale=y_scale, axis=None), x2="x2:Q", y2="y2:Q")
)

# Pruned cross marks
pruned_marks_df = edges_pruned.copy()
pruned_marks_df["cx"] = pruned_marks_df["x"] * 0.6 + pruned_marks_df["x2"] * 0.4
pruned_marks_df["cy"] = pruned_marks_df["y"] * 0.6 + pruned_marks_df["y2"] * 0.4

# Only show one cross mark per pruned decision branch
pruned_cross_df = pruned_marks_df.drop_duplicates(subset=["x", "y"]).head(1)

pruned_crosses = (
    alt.Chart(pruned_cross_df)
    .mark_text(fontSize=28, fontWeight="bold", color="#C0392B", text="✕")
    .encode(x=alt.X("cx:Q", scale=x_scale, axis=None), y=alt.Y("cy:Q", scale=y_scale, axis=None))
)

# Decision nodes (squares)
decision_nodes = (
    alt.Chart(decision_df)
    .mark_square(size=1800, color="#306998", stroke="#1A3A5C", strokeWidth=2)
    .encode(x=alt.X("x:Q", scale=x_scale, axis=None), y=alt.Y("y:Q", scale=y_scale, axis=None))
)

# Chance nodes (circles)
chance_nodes = (
    alt.Chart(chance_df)
    .mark_circle(size=1800, color="#FFD43B", stroke="#B8960F", strokeWidth=2)
    .encode(x=alt.X("x:Q", scale=x_scale, axis=None), y=alt.Y("y:Q", scale=y_scale, axis=None))
)

# Terminal nodes (triangles pointing right)
terminal_nodes = (
    alt.Chart(terminal_df)
    .mark_point(shape="triangle-right", size=1200, filled=True, color="#2ECC71", stroke="#1A8B4E", strokeWidth=2)
    .encode(x=alt.X("x:Q", scale=x_scale, axis=None), y=alt.Y("y:Q", scale=y_scale, axis=None))
)

# EMV labels on decision and chance nodes
emv_nodes = nodes_df[nodes_df["type"].isin(["decision", "chance"])]

emv_labels = (
    alt.Chart(emv_nodes)
    .mark_text(fontSize=16, fontWeight="bold", dy=-30, color="#1A1A1A")
    .encode(x=alt.X("x:Q", scale=x_scale, axis=None), y=alt.Y("y:Q", scale=y_scale, axis=None), text="emv:N")
)

# Payoff labels on terminal nodes
payoff_labels = (
    alt.Chart(terminal_df)
    .mark_text(fontSize=16, fontWeight="bold", dx=50, align="left", color="#1A1A1A")
    .encode(x=alt.X("x:Q", scale=x_scale, axis=None), y=alt.Y("y:Q", scale=y_scale, axis=None), text="payoff:N")
)

# Terminal node description labels
terminal_desc = (
    alt.Chart(terminal_df)
    .mark_text(fontSize=14, dx=50, dy=18, align="left", color="#666666")
    .encode(x=alt.X("x:Q", scale=x_scale, axis=None), y=alt.Y("y:Q", scale=y_scale, axis=None), text="label:N")
)

# Branch labels (decision option names)
branch_labels = (
    alt.Chart(edge_labels_branch)
    .mark_text(fontSize=15, fontWeight="bold", dy=-14, color="#306998")
    .encode(x=alt.X("mx:Q", scale=x_scale, axis=None), y=alt.Y("my:Q", scale=y_scale, axis=None), text="label:N")
)

# Probability labels on chance branches
prob_labels = (
    alt.Chart(edge_labels_prob)
    .mark_text(fontSize=14, dy=-12, color="#B8960F", fontWeight="bold")
    .encode(x=alt.X("mx:Q", scale=x_scale, axis=None), y=alt.Y("my:Q", scale=y_scale, axis=None), text="prob:N")
)

# Legend entries
legend_data = pd.DataFrame(
    [
        {"x": 20, "y": 590, "label": "Decision Node", "shape": "square", "color": "#306998"},
        {"x": 170, "y": 590, "label": "Chance Node", "shape": "circle", "color": "#FFD43B"},
        {"x": 320, "y": 590, "label": "Terminal Node", "shape": "triangle", "color": "#2ECC71"},
    ]
)

legend_squares = (
    alt.Chart(legend_data[legend_data["shape"] == "square"])
    .mark_square(size=500, color="#306998", stroke="#1A3A5C", strokeWidth=1.5)
    .encode(x=alt.X("x:Q", scale=x_scale, axis=None), y=alt.Y("y:Q", scale=y_scale, axis=None))
)

legend_circles = (
    alt.Chart(legend_data[legend_data["shape"] == "circle"])
    .mark_circle(size=500, color="#FFD43B", stroke="#B8960F", strokeWidth=1.5)
    .encode(x=alt.X("x:Q", scale=x_scale, axis=None), y=alt.Y("y:Q", scale=y_scale, axis=None))
)

legend_triangles = (
    alt.Chart(legend_data[legend_data["shape"] == "triangle"])
    .mark_point(shape="triangle-right", size=400, filled=True, color="#2ECC71", stroke="#1A8B4E", strokeWidth=1.5)
    .encode(x=alt.X("x:Q", scale=x_scale, axis=None), y=alt.Y("y:Q", scale=y_scale, axis=None))
)

legend_text = (
    alt.Chart(legend_data)
    .mark_text(fontSize=13, dx=18, align="left", color="#555555")
    .encode(x=alt.X("x:Q", scale=x_scale, axis=None), y=alt.Y("y:Q", scale=y_scale, axis=None), text="label:N")
)

# Combine all layers
chart = (
    alt.layer(
        active_lines,
        pruned_lines,
        pruned_crosses,
        decision_nodes,
        chance_nodes,
        terminal_nodes,
        emv_labels,
        payoff_labels,
        terminal_desc,
        branch_labels,
        prob_labels,
        legend_squares,
        legend_circles,
        legend_triangles,
        legend_text,
    )
    .properties(width=1600, height=900, title=alt.Title("tree-decision · altair · pyplots.ai", fontSize=28))
    .configure_view(strokeWidth=0)
)

# Save
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
