"""pyplots.ai
tree-decision: Decision Tree Visualization with Probabilities
Library: plotly 6.6.0 | Python 3.14.3
Quality: 81/100 | Created: 2026-03-06
"""

import plotly.graph_objects as go


# Data - Two-stage product launch investment decision
nodes = {
    "D1": {
        "type": "decision",
        "parent": None,
        "label": None,
        "prob": None,
        "payoff": None,
        "emv": 280,
        "pruned": False,
    },
    "C1": {
        "type": "chance",
        "parent": "D1",
        "label": "Launch Product",
        "prob": None,
        "payoff": None,
        "emv": 280,
        "pruned": False,
    },
    "T1": {
        "type": "terminal",
        "parent": "C1",
        "label": "High Demand",
        "prob": 0.6,
        "payoff": 500,
        "emv": None,
        "pruned": False,
    },
    "T2": {
        "type": "terminal",
        "parent": "C1",
        "label": "Low Demand",
        "prob": 0.4,
        "payoff": -50,
        "emv": None,
        "pruned": False,
    },
    "C2": {
        "type": "chance",
        "parent": "D1",
        "label": "License Tech",
        "prob": None,
        "payoff": None,
        "emv": 170,
        "pruned": True,
    },
    "T3": {
        "type": "terminal",
        "parent": "C2",
        "label": "Accepted",
        "prob": 0.7,
        "payoff": 200,
        "emv": None,
        "pruned": True,
    },
    "T4": {
        "type": "terminal",
        "parent": "C2",
        "label": "Rejected",
        "prob": 0.3,
        "payoff": 100,
        "emv": None,
        "pruned": True,
    },
    "T5": {
        "type": "terminal",
        "parent": "D1",
        "label": "Do Nothing",
        "prob": None,
        "payoff": 0,
        "emv": None,
        "pruned": True,
    },
}

# Layout positions (x, y) - left-to-right tree, tighter vertical spread
positions = {
    "D1": (0.0, 0.50),
    "C1": (0.35, 0.82),
    "T1": (0.72, 0.96),
    "T2": (0.72, 0.68),
    "C2": (0.35, 0.30),
    "T3": (0.72, 0.43),
    "T4": (0.72, 0.17),
    "T5": (0.35, 0.08),
}

# Colors
decision_color = "#306998"
chance_color = "#E8833A"
terminal_color = "#4CAF50"
pruned_color = "#9E9E9E"
optimal_edge = "#2D5F8A"
bg_color = "#FAFBFC"

# Plot
fig = go.Figure()

# Draw edges (branches)
for nid, n in nodes.items():
    if n["parent"] is None:
        continue
    px, py = positions[n["parent"]]
    cx, cy = positions[nid]
    line_color = pruned_color if n["pruned"] else optimal_edge
    dash = "dash" if n["pruned"] else "solid"
    line_width = 2.5 if n["pruned"] else 4
    opacity = 0.5 if n["pruned"] else 1.0

    # Build hover text for edges
    edge_hover = f"<b>{n['label'] or ''}</b>"
    if n["prob"] is not None:
        edge_hover += f"<br>Probability: {n['prob']:.0%}"
    if n["payoff"] is not None:
        edge_hover += f"<br>Payoff: ${n['payoff']:+,}"
    if n["pruned"]:
        edge_hover += "<br><i>Pruned (suboptimal)</i>"

    fig.add_trace(
        go.Scatter(
            x=[px, cx],
            y=[py, cy],
            mode="lines",
            line={"color": line_color, "width": line_width, "dash": dash},
            opacity=opacity,
            hoverinfo="skip",
            showlegend=False,
        )
    )

    # Branch label - offset more for less crowding near D1
    t = 0.45 if n["parent"] == "D1" else 0.5
    mid_x = px + (cx - px) * t
    mid_y = py + (cy - py) * t
    label_text = n["label"] or ""
    if n["prob"] is not None:
        label_text = f"{n['label']} (p={n['prob']})"
    text_color = pruned_color if n["pruned"] else "#2B2B2B"

    fig.add_annotation(
        x=mid_x,
        y=mid_y,
        text=f"<b>{label_text}</b>",
        showarrow=False,
        font={"size": 16, "color": text_color},
        yshift=18,
    )

# Draw pruned marks on pruned branches
for nid, n in nodes.items():
    if not n["pruned"] or n["parent"] is None:
        continue
    px, py = positions[n["parent"]]
    cx, cy = positions[nid]
    mark_x = px + (cx - px) * 0.18
    mark_y = py + (cy - py) * 0.18

    fig.add_annotation(
        x=mark_x, y=mark_y, text="//", showarrow=False, font={"size": 24, "color": "#CC0000", "family": "Arial Black"}
    )

# Draw nodes with hover tooltips
node_size = 48
for nid, n in nodes.items():
    nx, ny = positions[nid]
    node_color = (
        pruned_color
        if n["pruned"]
        else (decision_color if n["type"] == "decision" else chance_color if n["type"] == "chance" else terminal_color)
    )
    node_opacity = 0.65 if n["pruned"] else 1.0

    if n["type"] == "decision":
        symbol = "square"
    elif n["type"] == "chance":
        symbol = "circle"
    else:
        symbol = "triangle-right"

    # Rich hover template for each node
    hover_parts = [f"<b>{nid}</b> — {n['type'].title()} Node"]
    if n["emv"] is not None:
        hover_parts.append(f"EMV: <b>${n['emv']:,}</b>")
    if n["payoff"] is not None:
        hover_parts.append(f"Payoff: <b>${n['payoff']:+,}</b>")
    if n["prob"] is not None:
        hover_parts.append(f"Probability: {n['prob']:.0%}")
    if n["label"]:
        hover_parts.append(f"Branch: {n['label']}")
    if n["pruned"]:
        hover_parts.append("<i>Pruned (suboptimal path)</i>")
    else:
        if n["type"] != "terminal" or not n["pruned"]:
            hover_parts.append("<i>Optimal path</i>" if not n["pruned"] else "")
    hover_text = "<br>".join(p for p in hover_parts if p)

    fig.add_trace(
        go.Scatter(
            x=[nx],
            y=[ny],
            mode="markers",
            marker={
                "size": node_size,
                "color": node_color,
                "symbol": symbol,
                "line": {"color": "white", "width": 2.5},
                "opacity": node_opacity,
            },
            hoverinfo="skip",
            hoverlabel={"bgcolor": node_color, "font_size": 14, "font_color": "white"},
            showlegend=False,
        )
    )

    # EMV inside decision/chance nodes - larger text, dark text on pruned nodes
    if n["emv"] is not None:
        emv_color = "#333333" if n["pruned"] else "white"
        fig.add_annotation(
            x=nx, y=ny, text=f"<b>${n['emv']}</b>", showarrow=False, font={"size": 16, "color": emv_color}
        )

    # Payoff at terminal nodes
    if n["payoff"] is not None:
        display_color = pruned_color if n["pruned"] else "#2B2B2B"
        payoff_size = 17
        fig.add_annotation(
            x=nx,
            y=ny,
            text=f"<b>${n['payoff']:+,}</b>",
            showarrow=False,
            font={"size": payoff_size, "color": display_color},
            xshift=55,
        )

# Legend entries for node types
for name, color, symbol in [
    ("Decision Node", decision_color, "square"),
    ("Chance Node", chance_color, "circle"),
    ("Terminal Node", terminal_color, "triangle-right"),
]:
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            marker={"size": 16, "color": color, "symbol": symbol, "line": {"color": "white", "width": 1}},
            name=name,
            showlegend=True,
        )
    )

fig.add_trace(
    go.Scatter(
        x=[None],
        y=[None],
        mode="lines",
        line={"color": pruned_color, "width": 3, "dash": "dash"},
        name="Pruned Branch",
        showlegend=True,
    )
)

# Style
fig.update_layout(
    title={
        "text": "Product Launch Decision · tree-decision · plotly · pyplots.ai",
        "font": {"size": 28, "color": "#2B2B2B", "family": "Arial, sans-serif"},
        "x": 0.5,
        "xanchor": "center",
        "y": 0.96,
    },
    template="plotly_white",
    width=1600,
    height=900,
    xaxis={"showgrid": False, "zeroline": False, "showticklabels": False, "range": [-0.08, 0.95]},
    yaxis={"showgrid": False, "zeroline": False, "showticklabels": False, "range": [-0.02, 1.06]},
    legend={
        "font": {"size": 16},
        "x": 0.01,
        "y": 0.01,
        "xanchor": "left",
        "yanchor": "bottom",
        "bgcolor": "rgba(255,255,255,0.9)",
        "bordercolor": "#CCCCCC",
        "borderwidth": 1,
    },
    margin={"l": 40, "r": 60, "t": 80, "b": 30},
    plot_bgcolor=bg_color,
    paper_bgcolor="white",
    hoverlabel={"font_size": 14},
)

# Save static PNG
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Enable hover tooltips for interactive HTML export
# Trace order: edges (one per child node), then node markers (one per node), then 4 legend traces
# Enable hover on edge traces
edge_idx = 0
for _nid, n in nodes.items():
    if n["parent"] is None:
        continue
    edge_hover = f"<b>{n['label'] or ''}</b>"
    if n["prob"] is not None:
        edge_hover += f"<br>Probability: {n['prob']:.0%}"
    if n["payoff"] is not None:
        edge_hover += f"<br>Payoff: ${n['payoff']:+,}"
    if n["pruned"]:
        edge_hover += "<br><i>Pruned (suboptimal)</i>"
    fig.data[edge_idx].hoverinfo = "text"
    fig.data[edge_idx].hovertext = [edge_hover, edge_hover]
    edge_idx += 1

# Enable hover on node traces
num_edges = sum(1 for n in nodes.values() if n["parent"] is not None)
node_idx = num_edges
for nid, n in nodes.items():
    parts = [f"<b>{nid}</b> — {n['type'].title()} Node"]
    if n["emv"] is not None:
        parts.append(f"EMV: <b>${n['emv']:,}</b>")
    if n["payoff"] is not None:
        parts.append(f"Payoff: <b>${n['payoff']:+,}</b>")
    if n["prob"] is not None:
        parts.append(f"Probability: {n['prob']:.0%}")
    if n["label"]:
        parts.append(f"Branch: {n['label']}")
    if n["pruned"]:
        parts.append("<i>Pruned (suboptimal path)</i>")
    elif n["type"] != "terminal":
        parts.append("<i>Optimal path</i>")
    node_color = (
        pruned_color
        if n["pruned"]
        else (decision_color if n["type"] == "decision" else chance_color if n["type"] == "chance" else terminal_color)
    )
    fig.data[node_idx].hoverinfo = "text"
    fig.data[node_idx].hovertext = ["<br>".join(parts)]
    fig.data[node_idx].hoverlabel = {"bgcolor": node_color, "font_size": 14, "font_color": "white"}
    node_idx += 1

fig.write_html("plot.html", include_plotlyjs="cdn")
