"""pyplots.ai
chord-basic: Basic Chord Diagram
Library: plotly | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import numpy as np
import plotly.graph_objects as go


# Data: Migration flows between 6 continents (bidirectional)
continents = ["Africa", "Asia", "Europe", "N. America", "S. America", "Oceania"]
n = len(continents)

# Flow matrix (row = source, col = target) - realistic migration patterns
np.random.seed(42)
flow_matrix = np.array(
    [
        [0, 15, 25, 10, 5, 3],  # Africa to others
        [12, 0, 30, 20, 8, 15],  # Asia to others
        [20, 35, 0, 25, 12, 10],  # Europe to others
        [8, 18, 22, 0, 15, 5],  # N. America to others
        [6, 10, 18, 20, 0, 4],  # S. America to others
        [2, 12, 8, 6, 3, 0],  # Oceania to others
    ]
)

# Colors for each continent (Python Blue first, then colorblind-safe palette)
colors = ["#306998", "#FFD43B", "#2E8B57", "#DC143C", "#9370DB", "#FF8C00"]

# Calculate totals for each continent
totals = flow_matrix.sum(axis=0) + flow_matrix.sum(axis=1)
total_flow = flow_matrix.sum()

# Calculate arc positions around the circle
gap = 0.02
arc_starts = []
arc_ends = []
current_pos = 0
for _, total in enumerate(totals):
    arc_starts.append(current_pos)
    arc_ends.append(current_pos + (total / total_flow) * (1 - n * gap))
    current_pos = arc_ends[-1] + gap

# Create figure
fig = go.Figure()

# Draw outer arcs for each continent
for i in range(n):
    # Generate arc points (outer)
    angles_outer = np.linspace(2 * np.pi * arc_starts[i] - np.pi / 2, 2 * np.pi * arc_ends[i] - np.pi / 2, 100)
    x_outer = 1.0 * np.cos(angles_outer)
    y_outer = 1.0 * np.sin(angles_outer)

    # Generate arc points (inner, reversed)
    angles_inner = np.linspace(2 * np.pi * arc_ends[i] - np.pi / 2, 2 * np.pi * arc_starts[i] - np.pi / 2, 100)
    x_inner = 0.95 * np.cos(angles_inner)
    y_inner = 0.95 * np.sin(angles_inner)

    fig.add_trace(
        go.Scatter(
            x=np.concatenate([x_outer, x_inner]),
            y=np.concatenate([y_outer, y_inner]),
            fill="toself",
            fillcolor=colors[i],
            line=dict(color="white", width=1),
            hoverinfo="text",
            text=f"{continents[i]}<br>Total flow: {totals[i]}",
            name=continents[i],
            showlegend=True,
        )
    )

# Draw chords between continents
shapes = []
for i in range(n):
    src_pos = arc_starts[i]
    for j in range(n):
        if i != j and flow_matrix[i, j] > 0:
            flow = flow_matrix[i, j]
            chord_width = (flow / total_flow) * (1 - n * gap)

            # Calculate target position offset
            tgt_base = arc_starts[j]
            tgt_offset = sum(
                (flow_matrix[k, j] / total_flow) * (1 - n * gap) for k in range(i) if flow_matrix[k, j] > 0
            )

            # Calculate chord endpoints (source)
            src_angle1 = 2 * np.pi * src_pos - np.pi / 2
            src_angle2 = 2 * np.pi * (src_pos + chord_width) - np.pi / 2
            x1 = 0.95 * np.cos(src_angle1)
            y1 = 0.95 * np.sin(src_angle1)
            x2 = 0.95 * np.cos(src_angle2)
            y2 = 0.95 * np.sin(src_angle2)

            # Calculate chord endpoints (target)
            tgt_start = tgt_base + tgt_offset
            tgt_end = tgt_start + chord_width
            tgt_angle1 = 2 * np.pi * tgt_start - np.pi / 2
            tgt_angle2 = 2 * np.pi * tgt_end - np.pi / 2
            x3 = 0.95 * np.cos(tgt_angle1)
            y3 = 0.95 * np.sin(tgt_angle1)
            x4 = 0.95 * np.cos(tgt_angle2)
            y4 = 0.95 * np.sin(tgt_angle2)

            # SVG path with quadratic bezier curves through center
            path = (
                f"M {x1},{y1} Q 0,0 {x3},{y3} A 0.95,0.95 0 0,1 {x4},{y4} Q 0,0 {x2},{y2} A 0.95,0.95 0 0,1 {x1},{y1} Z"
            )

            shapes.append(
                dict(type="path", path=path, fillcolor=colors[i], opacity=0.6, line=dict(color=colors[i], width=0.5))
            )

            src_pos += chord_width

# Add continent labels around the perimeter
for i in range(n):
    mid_pos = (arc_starts[i] + arc_ends[i]) / 2
    angle = 2 * np.pi * mid_pos - np.pi / 2
    label_radius = 1.12

    # Rotate text for readability
    text_angle_deg = np.degrees(angle)
    if 90 < text_angle_deg < 270 or -270 < text_angle_deg < -90:
        text_angle_deg += 180
    rotation = -text_angle_deg + 90 if -90 < np.degrees(angle) < 90 else -text_angle_deg - 90

    fig.add_annotation(
        x=label_radius * np.cos(angle),
        y=label_radius * np.sin(angle),
        text=f"<b>{continents[i]}</b>",
        font=dict(size=18, color=colors[i]),
        showarrow=False,
        textangle=rotation,
    )

# Layout
fig.update_layout(
    title=dict(
        text="Migration Flows Between Continents · chord-basic · plotly · pyplots.ai",
        font=dict(size=28),
        x=0.5,
        xanchor="center",
    ),
    shapes=shapes,
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.4, 1.4]),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.4, 1.4], scaleanchor="x"),
    template="plotly_white",
    showlegend=True,
    legend=dict(font=dict(size=16), x=1.02, y=0.5, yanchor="middle"),
    margin=dict(l=50, r=150, t=100, b=50),
    plot_bgcolor="white",
    paper_bgcolor="white",
)

# Save outputs
fig.write_image("plot.png", width=1600, height=900, scale=3)
fig.write_html("plot.html", include_plotlyjs="cdn")
