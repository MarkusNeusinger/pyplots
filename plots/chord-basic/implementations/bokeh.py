"""
chord-basic: Basic Chord Diagram
Library: bokeh
"""

import numpy as np
from bokeh.io import export_png, save
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure


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

# Colors for each entity (colorblind-safe palette)
colors = ["#306998", "#FFD43B", "#E69F00", "#56B4E9", "#009E73", "#CC79A7"]

# Calculate total flows for each entity (sum of incoming and outgoing)
total_flows = flow_matrix.sum(axis=1) + flow_matrix.sum(axis=0)
total_all = total_flows.sum()

# Calculate arc angles for each entity
gap = 0.02 * 2 * np.pi  # Gap between arcs
total_gap = gap * n
available = 2 * np.pi - total_gap
arc_angles = (total_flows / total_all) * available

# Calculate start and end angles for each entity's arc
arc_starts = np.zeros(n)
arc_ends = np.zeros(n)
current_angle = 0
for i in range(n):
    arc_starts[i] = current_angle
    arc_ends[i] = current_angle + arc_angles[i]
    current_angle = arc_ends[i] + gap

# Calculate midpoint angles for each entity
arc_mids = (arc_starts + arc_ends) / 2

# Create figure
p = figure(
    width=4800,
    height=2700,
    title="chord-basic · bokeh · pyplots.ai",
    x_range=(-1.5, 1.5),
    y_range=(-1.1, 1.1),
    tools="hover,pan,wheel_zoom,reset",
    match_aspect=True,
)

# Remove axes and grid for cleaner look
p.axis.visible = False
p.grid.visible = False
p.outline_line_color = None

# Style title
p.title.text_font_size = "32pt"
p.title.align = "center"

# Draw outer arcs for each entity
outer_radius = 0.95
inner_radius = 0.88
arc_resolution = 50

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
label_radius = 1.08
for i in range(n):
    angle = arc_mids[i]
    x = label_radius * np.cos(angle)
    y = label_radius * np.sin(angle)

    # Adjust text angle for readability
    text_angle = angle
    if angle > np.pi / 2 and angle < 3 * np.pi / 2:
        text_angle = angle + np.pi
        anchor = "right"
    else:
        anchor = "left"

    # Center labels at top and bottom
    if abs(angle - np.pi / 2) < 0.3 or abs(angle - 3 * np.pi / 2) < 0.3:
        anchor = "center"

    p.text(
        x=[x],
        y=[y],
        text=[entities[i]],
        text_font_size="22pt",
        text_align=anchor,
        text_baseline="middle",
        text_color=colors[i],
        text_font_style="bold",
    )


# Function to create bezier curve points for chords
def bezier_chord(start_angle1, end_angle1, start_angle2, end_angle2, radius=0.85, n_points=50):
    """Create bezier curve points for a chord connecting two arcs."""
    # Start and end points on the inner circle
    x1_start = radius * np.cos(start_angle1)
    y1_start = radius * np.sin(start_angle1)
    x1_end = radius * np.cos(end_angle1)
    y1_end = radius * np.sin(end_angle1)

    x2_start = radius * np.cos(start_angle2)
    y2_start = radius * np.sin(start_angle2)
    x2_end = radius * np.cos(end_angle2)
    y2_end = radius * np.sin(end_angle2)

    # Bezier curve from arc1 to arc2
    t = np.linspace(0, 1, n_points)

    # First curve: end of arc1 to start of arc2 (through center)
    ctrl1 = np.array([0, 0])  # Control point at center
    curve1_x = (1 - t) ** 2 * x1_end + 2 * (1 - t) * t * ctrl1[0] + t**2 * x2_start
    curve1_y = (1 - t) ** 2 * y1_end + 2 * (1 - t) * t * ctrl1[1] + t**2 * y2_start

    # Arc along entity 2's segment
    theta2 = np.linspace(start_angle2, end_angle2, 10)
    arc2_x = radius * np.cos(theta2)
    arc2_y = radius * np.sin(theta2)

    # Second curve: end of arc2 to start of arc1 (through center)
    curve2_x = (1 - t) ** 2 * x2_end + 2 * (1 - t) * t * ctrl1[0] + t**2 * x1_start
    curve2_y = (1 - t) ** 2 * y2_end + 2 * (1 - t) * t * ctrl1[1] + t**2 * y1_start

    # Arc along entity 1's segment
    theta1 = np.linspace(start_angle1, end_angle1, 10)
    arc1_x = radius * np.cos(theta1)
    arc1_y = radius * np.sin(theta1)

    # Combine all points
    x = np.concatenate([arc1_x, curve1_x, arc2_x, curve2_x])
    y = np.concatenate([arc1_y, curve1_y, arc2_y, curve2_y])

    return x, y


# Track position within each entity's arc for chord placement
entity_positions = arc_starts.copy()

# Draw chords for each flow
chord_data = {"x": [], "y": [], "source_name": [], "target_name": [], "value": [], "color": []}

for i in range(n):
    for j in range(n):
        if i != j and flow_matrix[i, j] > 0:
            value = flow_matrix[i, j]
            # Calculate the angular width of this chord at each end
            chord_width_i = (value / total_flows[i]) * arc_angles[i]
            chord_width_j = (value / total_flows[j]) * arc_angles[j]

            # Get start/end angles for this chord at entity i
            start_i = entity_positions[i]
            end_i = start_i + chord_width_i
            entity_positions[i] = end_i

            # For the target, we need to track separately
            # Using a simple proportion of the arc for visual effect
            mid_j = arc_mids[j]
            start_j = mid_j - chord_width_j / 2
            end_j = mid_j + chord_width_j / 2

            # Create bezier chord
            x, y = bezier_chord(start_i, end_i, start_j, end_j, radius=inner_radius - 0.01)

            chord_data["x"].append(list(x))
            chord_data["y"].append(list(y))
            chord_data["source_name"].append(entities[i])
            chord_data["target_name"].append(entities[j])
            chord_data["value"].append(value)
            chord_data["color"].append(colors[i])

# Draw all chords
chord_source = ColumnDataSource(data=chord_data)
chords = p.patches(
    "x", "y", source=chord_source, fill_color="color", fill_alpha=0.5, line_color="color", line_alpha=0.7, line_width=1
)

# Add hover tool for chords
hover = p.select(type=HoverTool)
hover.tooltips = [("From", "@source_name"), ("To", "@target_name"), ("Flow", "@value million")]
hover.renderers = [chords]

# Add legend manually
legend_x = 1.15
legend_y = 0.8
for i, (entity, color) in enumerate(zip(entities, colors, strict=True)):
    y_pos = legend_y - i * 0.12
    # Draw color box
    p.rect(x=[legend_x], y=[y_pos], width=0.08, height=0.06, fill_color=color, line_color="white", line_width=1)
    # Draw label
    p.text(
        x=[legend_x + 0.08],
        y=[y_pos],
        text=[entity],
        text_font_size="18pt",
        text_baseline="middle",
        text_color="#333333",
    )

# Save as PNG and HTML
export_png(p, filename="plot.png")
save(p, filename="plot.html", title="chord-basic · bokeh · pyplots.ai")
