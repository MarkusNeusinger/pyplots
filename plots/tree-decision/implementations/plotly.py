""" pyplots.ai
tree-decision: Decision Tree Visualization with Probabilities
Library: plotly 6.6.0 | Python 3.14.3
Quality: 85/100 | Created: 2026-03-06
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

# Layout positions (x, y) - left-to-right tree
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

# Pre-build hover text for edges and nodes (used for both PNG annotations and HTML interactivity)
edge_hover_texts = {}
for nid, n in nodes.items():
    if n["parent"] is None:
        continue
    parts = [f"<b>{n['label'] or ''}</b>"]
    if n["prob"] is not None:
        parts.append(f"Probability: {n['prob']:.0%}")
    if n["payoff"] is not None:
        parts.append(f"Payoff: ${n['payoff']:+,}")
    if n["pruned"]:
        parts.append("<i>Pruned (suboptimal)</i>")
    edge_hover_texts[nid] = "<br>".join(parts)

node_hover_texts = {}
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
    node_hover_texts[nid] = "<br>".join(parts)

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

    # Branch label
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
        font={"size": 20, "color": text_color, "family": "Arial, sans-serif"},
        yshift=20,
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
        x=mark_x, y=mark_y, text="//", showarrow=False, font={"size": 26, "color": "#CC0000", "family": "Arial Black"}
    )

# Draw nodes using layout shapes for precise rendering + invisible scatter for hover
node_shapes = []
shape_size_x = 0.032
shape_size_y = 0.05

for nid, n in nodes.items():
    nx, ny = positions[nid]
    node_color = (
        pruned_color
        if n["pruned"]
        else (decision_color if n["type"] == "decision" else chance_color if n["type"] == "chance" else terminal_color)
    )
    node_opacity = 0.65 if n["pruned"] else 1.0

    if n["type"] == "decision":
        # Square shape via layout
        node_shapes.append(
            {
                "type": "rect",
                "x0": nx - shape_size_x,
                "y0": ny - shape_size_y,
                "x1": nx + shape_size_x,
                "y1": ny + shape_size_y,
                "fillcolor": node_color,
                "opacity": node_opacity,
                "line": {"color": "white", "width": 2.5},
                "xref": "x",
                "yref": "y",
            }
        )
    elif n["type"] == "chance":
        # Circle shape via layout
        node_shapes.append(
            {
                "type": "circle",
                "x0": nx - shape_size_x,
                "y0": ny - shape_size_y,
                "x1": nx + shape_size_x,
                "y1": ny + shape_size_y,
                "fillcolor": node_color,
                "opacity": node_opacity,
                "line": {"color": "white", "width": 2.5},
                "xref": "x",
                "yref": "y",
            }
        )
    else:
        # Terminal: use triangle-right marker (shapes don't support triangles)
        fig.add_trace(
            go.Scatter(
                x=[nx],
                y=[ny],
                mode="markers",
                marker={
                    "size": 52,
                    "color": node_color,
                    "symbol": "triangle-right",
                    "line": {"color": "white", "width": 2.5},
                    "opacity": node_opacity,
                },
                hoverinfo="skip",
                showlegend=False,
            )
        )

    # Invisible scatter trace for hover interactivity on all nodes
    fig.add_trace(
        go.Scatter(
            x=[nx],
            y=[ny],
            mode="markers",
            marker={"size": 50, "color": "rgba(0,0,0,0)", "symbol": "square"},
            hoverinfo="skip",
            hoverlabel={"bgcolor": node_color, "font_size": 15, "font_color": "white"},
            showlegend=False,
        )
    )

    # EMV inside decision/chance nodes
    if n["emv"] is not None:
        emv_color = "#333333" if n["pruned"] else "white"
        fig.add_annotation(
            x=nx,
            y=ny,
            text=f"<b>${n['emv']}</b>",
            showarrow=False,
            font={"size": 20, "color": emv_color, "family": "Arial, sans-serif"},
        )

    # Payoff at terminal nodes
    if n["payoff"] is not None:
        display_color = pruned_color if n["pruned"] else "#2B2B2B"
        fig.add_annotation(
            x=nx,
            y=ny,
            text=f"<b>${n['payoff']:+,}</b>",
            showarrow=False,
            font={"size": 20, "color": display_color, "family": "Arial, sans-serif"},
            xshift=58,
        )

# Legend entries
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
        "text": (
            "Product Launch Decision · tree-decision · plotly · pyplots.ai"
            "<br><sup style='color:#666; font-size:16px'>"
            "Optimal path maximizes EMV at $280K · Pruned branches marked with //</sup>"
        ),
        "font": {"size": 28, "color": "#2B2B2B", "family": "Arial, sans-serif"},
        "x": 0.5,
        "xanchor": "center",
        "y": 0.97,
    },
    template="plotly_white",
    width=1600,
    height=900,
    shapes=node_shapes,
    xaxis={"showgrid": False, "zeroline": False, "showticklabels": False, "range": [-0.08, 0.95]},
    yaxis={"showgrid": False, "zeroline": False, "showticklabels": False, "range": [-0.02, 1.06]},
    legend={
        "font": {"size": 17, "family": "Arial, sans-serif"},
        "x": 0.01,
        "y": 0.01,
        "xanchor": "left",
        "yanchor": "bottom",
        "bgcolor": "rgba(255,255,255,0.92)",
        "bordercolor": "#CCCCCC",
        "borderwidth": 1,
    },
    margin={"l": 40, "r": 60, "t": 100, "b": 30},
    plot_bgcolor=bg_color,
    paper_bgcolor="white",
    hoverlabel={"font_size": 15},
)

# Save static PNG
fig.write_image("plot.png", width=1600, height=900, scale=3)

# Enable hover tooltips for interactive HTML export using pre-built hover texts
edge_idx = 0
for nid, n in nodes.items():
    if n["parent"] is None:
        continue
    hover = edge_hover_texts[nid]
    fig.data[edge_idx].hoverinfo = "text"
    fig.data[edge_idx].hovertext = [hover, hover]
    edge_idx += 1

# Enable hover on invisible node traces
# Trace order after edges: terminal marker traces interleaved with invisible hover traces
# We need to find the invisible hover traces (the ones with rgba(0,0,0,0) markers)
for i in range(edge_idx, len(fig.data)):
    trace = fig.data[i]
    if trace.marker and trace.marker.color == "rgba(0,0,0,0)" and trace.x is not None and len(trace.x) == 1:
        # Find which node this trace belongs to by matching position
        tx, ty = trace.x[0], trace.y[0]
        for nid, (nx, ny) in positions.items():
            if abs(tx - nx) < 0.001 and abs(ty - ny) < 0.001:
                node_color = (
                    pruned_color
                    if nodes[nid]["pruned"]
                    else (
                        decision_color
                        if nodes[nid]["type"] == "decision"
                        else chance_color
                        if nodes[nid]["type"] == "chance"
                        else terminal_color
                    )
                )
                trace.hoverinfo = "text"
                trace.hovertext = [node_hover_texts[nid]]
                trace.hoverlabel = {"bgcolor": node_color, "font_size": 15, "font_color": "white"}
                break

fig.write_html("plot.html", include_plotlyjs="cdn")
