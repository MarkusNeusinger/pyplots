""" pyplots.ai
chord-basic: Basic Chord Diagram
Library: plotly 6.5.0 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-14
"""

import numpy as np
import plotly.graph_objects as go


# Data: Migration flows between 6 continents (bidirectional)
continents = ["Africa", "Asia", "Europe", "N. America", "S. America", "Oceania"]
n = len(continents)

# Flow matrix (row = source, col = target)
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

# Colors for each continent (colorblind-safe)
colors = ["#306998", "#FFD43B", "#2E8B57", "#DC143C", "#9370DB", "#FF8C00"]

# Calculate totals for each continent
totals = flow_matrix.sum(axis=0) + flow_matrix.sum(axis=1)
total_flow = flow_matrix.sum()

# Calculate arc positions around the circle
gap = 0.02  # Gap between arcs
arc_starts = []
arc_ends = []
current_pos = 0
for i, total in enumerate(totals):
    arc_starts.append(current_pos)
    arc_ends.append(current_pos + (total / total_flow) * (1 - n * gap))
    current_pos = arc_ends[-1] + gap


def angle_from_pos(pos):
    """Convert position (0-1) to angle in radians."""
    return 2 * np.pi * pos - np.pi / 2


def get_arc_points(start_pos, end_pos, radius, n_points=50):
    """Generate points for an arc."""
    angles = np.linspace(angle_from_pos(start_pos), angle_from_pos(end_pos), n_points)
    x = radius * np.cos(angles)
    y = radius * np.sin(angles)
    return x, y


def get_chord_path(src_start, src_end, tgt_start, tgt_end, radius=0.95):
    """Generate SVG path for a chord."""
    # Source arc points
    src_angle1 = angle_from_pos(src_start)
    src_angle2 = angle_from_pos(src_end)
    x1, y1 = radius * np.cos(src_angle1), radius * np.sin(src_angle1)
    x2, y2 = radius * np.cos(src_angle2), radius * np.sin(src_angle2)

    # Target arc points
    tgt_angle1 = angle_from_pos(tgt_start)
    tgt_angle2 = angle_from_pos(tgt_end)
    x3, y3 = radius * np.cos(tgt_angle1), radius * np.sin(tgt_angle1)
    x4, y4 = radius * np.cos(tgt_angle2), radius * np.sin(tgt_angle2)

    # Create path with quadratic bezier curves through center
    path = f"M {x1},{y1} "
    path += f"Q 0,0 {x3},{y3} "
    path += f"A {radius},{radius} 0 0,1 {x4},{y4} "
    path += f"Q 0,0 {x2},{y2} "
    path += f"A {radius},{radius} 0 0,1 {x1},{y1} Z"

    return path


# Create figure
fig = go.Figure()

# Draw outer arcs for each continent
for i in range(n):
    x_arc, y_arc = get_arc_points(arc_starts[i], arc_ends[i], 1.0, 100)
    x_arc_inner, y_arc_inner = get_arc_points(arc_ends[i], arc_starts[i], 0.95, 100)

    x_shape = np.concatenate([x_arc, x_arc_inner])
    y_shape = np.concatenate([y_arc, y_arc_inner])

    fig.add_trace(
        go.Scatter(
            x=x_shape,
            y=y_shape,
            fill="toself",
            fillcolor=colors[i],
            line=dict(color="white", width=1),
            hoverinfo="text",
            text=f"{continents[i]}<br>Total flow: {totals[i]}",
            name=continents[i],
            showlegend=True,
        )
    )

# Draw chords
shapes = []
for i in range(n):
    src_pos = arc_starts[i]
    for j in range(n):
        if i != j and flow_matrix[i, j] > 0:
            # Calculate chord width based on flow
            flow = flow_matrix[i, j]
            chord_width_src = (flow / total_flow) * (1 - n * gap)
            chord_width_tgt = chord_width_src

            # Find position within target arc
            tgt_base = arc_starts[j]
            # Offset within target arc based on cumulative flows
            tgt_offset = 0
            for k in range(i):
                if flow_matrix[k, j] > 0:
                    tgt_offset += (flow_matrix[k, j] / total_flow) * (1 - n * gap)

            shapes.append(
                dict(
                    type="path",
                    path=get_chord_path(
                        src_pos,
                        src_pos + chord_width_src,
                        tgt_base + tgt_offset,
                        tgt_base + tgt_offset + chord_width_tgt,
                    ),
                    fillcolor=colors[i],
                    opacity=0.6,
                    line=dict(color=colors[i], width=0.5),
                )
            )

            src_pos += chord_width_src

# Add continent labels
for i in range(n):
    mid_pos = (arc_starts[i] + arc_ends[i]) / 2
    angle = angle_from_pos(mid_pos)
    label_radius = 1.12

    # Calculate text rotation
    text_angle = np.degrees(angle)
    if 90 < text_angle < 270 or -270 < text_angle < -90:
        text_angle += 180

    fig.add_annotation(
        x=label_radius * np.cos(angle),
        y=label_radius * np.sin(angle),
        text=f"<b>{continents[i]}</b>",
        font=dict(size=18, color=colors[i]),
        showarrow=False,
        textangle=-text_angle + 90 if -90 < np.degrees(angle) < 90 else -text_angle - 90,
    )

# Update layout
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
