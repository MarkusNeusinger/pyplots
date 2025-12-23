""" pyplots.ai
chord-basic: Basic Chord Diagram
Library: bokeh 3.8.1 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-23
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure


output_file("plot.html", title="chord-basic · bokeh · pyplots.ai")

# Data - Migration flows between continents (in millions)
entities = ["Africa", "Asia", "Europe", "N. America", "S. America", "Oceania"]
n = len(entities)

# Flow matrix (rows = source, cols = target)
np.random.seed(42)
flow_matrix = np.array(
    [
        [0, 8, 12, 3, 2, 1],  # Africa to others
        [5, 0, 15, 10, 2, 4],  # Asia to others
        [3, 10, 0, 8, 4, 2],  # Europe to others
        [2, 6, 12, 0, 8, 1],  # N. America to others
        [4, 3, 7, 12, 0, 1],  # S. America to others
        [1, 5, 3, 2, 1, 0],  # Oceania to others
    ]
)

# Colors for each entity (colorblind-safe palette starting with Python colors)
colors = ["#306998", "#FFD43B", "#E69F00", "#56B4E9", "#009E73", "#CC79A7"]

# Calculate total flows for each entity (sum of incoming and outgoing)
total_flows = flow_matrix.sum(axis=1) + flow_matrix.sum(axis=0)
total_all = total_flows.sum()

# Calculate arc angles for each entity
gap = 0.03 * 2 * np.pi  # Gap between arcs
total_gap = gap * n
available = 2 * np.pi - total_gap
arc_angles = (total_flows / total_all) * available

# Calculate start and end angles for each entity's arc (start from top)
arc_starts = np.zeros(n)
arc_ends = np.zeros(n)
current_angle = np.pi / 2  # Start from top
for i in range(n):
    arc_starts[i] = current_angle
    arc_ends[i] = current_angle + arc_angles[i]
    current_angle = arc_ends[i] + gap

# Calculate midpoint angles for each entity
arc_mids = (arc_starts + arc_ends) / 2

# Create square figure for better chord diagram proportions
p = figure(
    width=3600,
    height=3600,
    title="chord-basic · bokeh · pyplots.ai",
    x_range=(-1.5, 2.0),
    y_range=(-1.5, 1.5),
    tools="hover,pan,wheel_zoom,reset",
)

# Remove axes and grid for cleaner look
p.axis.visible = False
p.grid.visible = False
p.outline_line_color = None

# Style title
p.title.text_font_size = "36pt"
p.title.align = "center"

# Draw outer arcs for each entity
outer_radius = 0.95
inner_radius = 0.87
arc_resolution = 60

for i in range(n):
    # Create arc points
    theta = np.linspace(arc_starts[i], arc_ends[i], arc_resolution)

    # Outer arc
    x_outer = outer_radius * np.cos(theta)
    y_outer = outer_radius * np.sin(theta)

    # Inner arc (reversed)
    x_inner = inner_radius * np.cos(theta[::-1])
    y_inner = inner_radius * np.sin(theta[::-1])

    # Combine to form closed polygon
    x_arc = np.concatenate([x_outer, x_inner])
    y_arc = np.concatenate([y_outer, y_inner])

    source = ColumnDataSource(
        data={"x": [list(x_arc)], "y": [list(y_arc)], "entity": [entities[i]], "total": [total_flows[i]]}
    )

    p.patches("x", "y", source=source, fill_color=colors[i], fill_alpha=0.9, line_color="white", line_width=2)

# Add entity labels outside the arcs
label_radius = 1.12
for i in range(n):
    angle = arc_mids[i]
    x = label_radius * np.cos(angle)
    y = label_radius * np.sin(angle)

    # Determine text alignment based on angle
    angle_deg = np.degrees(angle) % 360
    if angle_deg > 80 and angle_deg < 100:
        anchor = "center"
    elif angle_deg > 260 and angle_deg < 280:
        anchor = "center"
    elif angle_deg > 90 and angle_deg < 270:
        anchor = "right"
    else:
        anchor = "left"

    p.text(
        x=[x],
        y=[y],
        text=[entities[i]],
        text_font_size="26pt",
        text_align=anchor,
        text_baseline="middle",
        text_color=colors[i],
        text_font_style="bold",
    )


# Create bezier curve points for chords
def bezier_chord(start1, end1, start2, end2, radius=0.85, n_points=40):
    """Create bezier curve points for a chord connecting two arcs."""
    # Points on the inner circle for each arc
    x1_start = radius * np.cos(start1)
    y1_start = radius * np.sin(start1)
    x1_end = radius * np.cos(end1)
    y1_end = radius * np.sin(end1)

    x2_start = radius * np.cos(start2)
    y2_start = radius * np.sin(start2)
    x2_end = radius * np.cos(end2)
    y2_end = radius * np.sin(end2)

    # Bezier curves through center
    t = np.linspace(0, 1, n_points)
    ctrl = np.array([0, 0])

    # First curve: end of arc1 to start of arc2
    curve1_x = (1 - t) ** 2 * x1_end + 2 * (1 - t) * t * ctrl[0] + t**2 * x2_start
    curve1_y = (1 - t) ** 2 * y1_end + 2 * (1 - t) * t * ctrl[1] + t**2 * y2_start

    # Arc along entity 2
    theta2 = np.linspace(start2, end2, 15)
    arc2_x = radius * np.cos(theta2)
    arc2_y = radius * np.sin(theta2)

    # Second curve: end of arc2 to start of arc1
    curve2_x = (1 - t) ** 2 * x2_end + 2 * (1 - t) * t * ctrl[0] + t**2 * x1_start
    curve2_y = (1 - t) ** 2 * y2_end + 2 * (1 - t) * t * ctrl[1] + t**2 * y1_start

    # Arc along entity 1
    theta1 = np.linspace(start1, end1, 15)
    arc1_x = radius * np.cos(theta1)
    arc1_y = radius * np.sin(theta1)

    # Combine all points
    x = np.concatenate([arc1_x, curve1_x, arc2_x, curve2_x])
    y = np.concatenate([arc1_y, curve1_y, arc2_y, curve2_y])

    return x, y


# Track position within each entity's arc for chord placement
entity_out_pos = arc_starts.copy()  # Track outgoing chord positions
entity_in_pos = {}  # Track incoming chord positions
for i in range(n):
    entity_in_pos[i] = arc_ends[i]  # Start from end for incoming

# Draw chords for each flow
chord_data = {"x": [], "y": [], "source_name": [], "target_name": [], "value": [], "color": []}

for i in range(n):
    for j in range(i + 1, n):  # Only process each pair once
        # Combined bidirectional flow for visual clarity
        val_ij = flow_matrix[i, j]
        val_ji = flow_matrix[j, i]

        if val_ij > 0 or val_ji > 0:
            total_flow = val_ij + val_ji

            # Calculate chord width at each end based on total bidirectional flow
            chord_width_i = (total_flow / total_flows[i]) * arc_angles[i]
            chord_width_j = (total_flow / total_flows[j]) * arc_angles[j]

            # Get positions for this chord at entity i
            start_i = entity_out_pos[i]
            end_i = start_i + chord_width_i
            entity_out_pos[i] = end_i

            # Get positions for this chord at entity j
            start_j = entity_out_pos[j]
            end_j = start_j + chord_width_j
            entity_out_pos[j] = end_j

            # Create bezier chord
            x, y = bezier_chord(start_i, end_i, start_j, end_j, radius=inner_radius - 0.02)

            # Use gradient color - blend source and target colors for bidirectional
            chord_data["x"].append(list(x))
            chord_data["y"].append(list(y))
            chord_data["source_name"].append(entities[i])
            chord_data["target_name"].append(entities[j])
            chord_data["value"].append(total_flow)
            # Color by entity with larger outgoing flow
            chord_data["color"].append(colors[i] if val_ij >= val_ji else colors[j])

# Draw all chords
chord_source = ColumnDataSource(data=chord_data)
chords = p.patches(
    "x",
    "y",
    source=chord_source,
    fill_color="color",
    fill_alpha=0.55,
    line_color="color",
    line_alpha=0.75,
    line_width=1.5,
)

# Configure hover tool for chords
hover = p.select(type=HoverTool)
hover.tooltips = [("From", "@source_name"), ("To", "@target_name"), ("Total Flow", "@value million")]
hover.renderers = [chords]

# Add legend (positioned to avoid label overlap)
legend_x = 1.35
legend_y = 0.6
p.text(
    x=[legend_x - 0.02],
    y=[legend_y + 0.15],
    text=["Migration Flows"],
    text_font_size="22pt",
    text_font_style="bold",
    text_color="#333333",
)

for i, (entity, color) in enumerate(zip(entities, colors, strict=True)):
    y_pos = legend_y - i * 0.14
    # Draw color box
    p.rect(x=[legend_x], y=[y_pos], width=0.1, height=0.08, fill_color=color, line_color="white", line_width=2)
    # Draw label
    p.text(
        x=[legend_x + 0.1],
        y=[y_pos],
        text=[entity],
        text_font_size="20pt",
        text_baseline="middle",
        text_color="#333333",
    )

# Save as PNG and HTML
export_png(p, filename="plot.png")
save(p)
