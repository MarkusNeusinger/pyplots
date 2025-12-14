"""
chord-basic: Basic Chord Diagram
Library: matplotlib
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path


# Data: Migration flows between continents (in millions)
np.random.seed(42)
entities = ["Africa", "Asia", "Europe", "N. America", "S. America", "Oceania"]
n = len(entities)

# Flow matrix (row=source, col=target)
flow_matrix = np.array(
    [
        [0, 12, 8, 5, 2, 1],  # From Africa
        [8, 0, 15, 10, 3, 4],  # From Asia
        [3, 10, 0, 8, 4, 2],  # From Europe
        [2, 6, 12, 0, 7, 3],  # From N. America
        [1, 2, 5, 8, 0, 1],  # From S. America
        [0, 3, 2, 2, 1, 0],  # From Oceania
    ]
)

# Colors for each entity (colorblind-safe palette)
colors = ["#306998", "#FFD43B", "#4ECDC4", "#FF6B6B", "#95E1A3", "#DDA0DD"]

# Calculate totals for each entity (sum of outgoing + incoming)
totals = flow_matrix.sum(axis=1) + flow_matrix.sum(axis=0)
total_flow = totals.sum()

# Gap between entity arcs (in degrees)
gap = 3
total_gap = gap * n
available_degrees = 360 - total_gap

# Calculate arc spans for each entity
arc_spans = (totals / total_flow) * available_degrees

# Calculate start angles for each entity arc
start_angles = np.zeros(n)
current_angle = 90  # Start from top
for i in range(n):
    start_angles[i] = current_angle
    current_angle -= arc_spans[i] + gap

# Create figure
fig, ax = plt.subplots(figsize=(16, 9), subplot_kw={"aspect": "equal"})
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.3, 1.3)
ax.axis("off")

# Draw entity arcs on the outer ring
radius = 1.0
arc_width = 0.08

for i in range(n):
    theta1 = start_angles[i] - arc_spans[i]
    theta2 = start_angles[i]

    # Draw outer arc as a wedge
    wedge = mpatches.Wedge(
        (0, 0), radius, theta1, theta2, width=arc_width, facecolor=colors[i], edgecolor="white", linewidth=2
    )
    ax.add_patch(wedge)

    # Add entity label
    mid_angle = (theta1 + theta2) / 2
    label_radius = radius + 0.12
    label_x = label_radius * np.cos(np.radians(mid_angle))
    label_y = label_radius * np.sin(np.radians(mid_angle))

    # Rotate text to align with arc
    rotation = mid_angle
    if mid_angle > 90 or mid_angle < -90:
        rotation = mid_angle + 180
    if 90 < mid_angle < 270 or -270 < mid_angle < -90:
        ha = "right"
    else:
        ha = "left"
    if abs(mid_angle) < 10 or abs(mid_angle - 180) < 10 or abs(mid_angle + 180) < 10:
        ha = "center"

    ax.text(label_x, label_y, entities[i], fontsize=18, fontweight="bold", ha=ha, va="center", color=colors[i])


def draw_chord(ax, start1, end1, start2, end2, color, alpha=0.65):
    """Draw a chord between two arcs using Bezier curves."""
    inner_radius = radius - arc_width

    # Convert angles to radians
    s1, e1 = np.radians(start1), np.radians(end1)
    s2, e2 = np.radians(start2), np.radians(end2)

    # Create path points
    n_arc_points = 20

    # First arc (source)
    arc1_angles = np.linspace(s1, e1, n_arc_points)
    arc1_points = np.column_stack([inner_radius * np.cos(arc1_angles), inner_radius * np.sin(arc1_angles)])

    # Second arc (target)
    arc2_angles = np.linspace(s2, e2, n_arc_points)
    arc2_points = np.column_stack([inner_radius * np.cos(arc2_angles), inner_radius * np.sin(arc2_angles)])

    # Control points for Bezier curves (through center with some offset)
    ctrl_factor = 0.3

    # Build path: arc1 -> bezier to arc2 -> arc2 -> bezier back to arc1
    verts = []
    codes = []

    # Start at first point of arc1
    verts.append(arc1_points[0])
    codes.append(Path.MOVETO)

    # Arc1 points
    for pt in arc1_points[1:]:
        verts.append(pt)
        codes.append(Path.LINETO)

    # Bezier curve from end of arc1 to start of arc2
    ctrl1 = arc1_points[-1] * ctrl_factor
    ctrl2 = arc2_points[0] * ctrl_factor
    verts.extend([ctrl1, ctrl2, arc2_points[0]])
    codes.extend([Path.CURVE4, Path.CURVE4, Path.CURVE4])

    # Arc2 points
    for pt in arc2_points[1:]:
        verts.append(pt)
        codes.append(Path.LINETO)

    # Bezier curve from end of arc2 back to start of arc1
    ctrl3 = arc2_points[-1] * ctrl_factor
    ctrl4 = arc1_points[0] * ctrl_factor
    verts.extend([ctrl3, ctrl4, arc1_points[0]])
    codes.extend([Path.CURVE4, Path.CURVE4, Path.CURVE4])

    path = Path(verts, codes)
    patch = mpatches.PathPatch(path, facecolor=color, edgecolor="none", alpha=alpha)
    ax.add_patch(patch)


# Track position within each entity arc for placing chords
arc_positions = {}
for i in range(n):
    arc_positions[i] = {"out": start_angles[i], "in": start_angles[i]}

# Calculate the angular span each flow unit represents for each entity
unit_angles = arc_spans / totals

# Draw chords for each flow
for i in range(n):
    for j in range(n):
        if i != j and flow_matrix[i, j] > 0:
            flow = flow_matrix[i, j]

            # Calculate chord width at source (outgoing from entity i)
            source_span = flow * unit_angles[i]
            source_start = arc_positions[i]["out"] - source_span
            source_end = arc_positions[i]["out"]
            arc_positions[i]["out"] = source_start

            # Calculate chord width at target (incoming to entity j)
            target_span = flow * unit_angles[j]
            target_start = arc_positions[j]["in"] - target_span
            target_end = arc_positions[j]["in"]
            arc_positions[j]["in"] = target_start

            # Draw the chord (use source color)
            draw_chord(ax, source_start, source_end, target_start, target_end, colors[i])

# Title
ax.set_title(
    "Continental Migration Flows · chord-basic · matplotlib · pyplots.ai", fontsize=24, fontweight="bold", pad=20
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
