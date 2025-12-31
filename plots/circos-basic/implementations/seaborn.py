"""pyplots.ai
circos-basic: Circos Plot
Library: seaborn | Python 3.13
Quality: pending | Created: 2025-12-31
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Set seaborn theme for consistent styling
sns.set_theme(style="white", context="talk", font_scale=1.1)

# Data: Regional trade flows (10 regions with trade connections)
np.random.seed(42)

# Define segments (regions) with their sizes (trade volume)
segments = [
    "North America",
    "Europe",
    "East Asia",
    "Southeast Asia",
    "South Asia",
    "Middle East",
    "Africa",
    "South America",
    "Oceania",
    "Central Asia",
]
n_segments = len(segments)

# Segment sizes represent total trade volume
segment_sizes = np.array([250, 320, 280, 150, 120, 100, 80, 90, 60, 50])

# Create connection data (source, target, value)
connections = [
    (0, 1, 85),  # North America - Europe
    (0, 2, 120),  # North America - East Asia
    (1, 2, 95),  # Europe - East Asia
    (1, 5, 60),  # Europe - Middle East
    (2, 3, 70),  # East Asia - Southeast Asia
    (2, 4, 45),  # East Asia - South Asia
    (3, 4, 35),  # Southeast Asia - South Asia
    (1, 6, 40),  # Europe - Africa
    (0, 7, 55),  # North America - South America
    (2, 8, 50),  # East Asia - Oceania
    (5, 4, 30),  # Middle East - South Asia
    (5, 6, 25),  # Middle East - Africa
    (1, 9, 20),  # Europe - Central Asia
    (2, 9, 28),  # East Asia - Central Asia
    (0, 3, 38),  # North America - Southeast Asia
]

# Create color palette using seaborn
colors = sns.color_palette("husl", n_colors=n_segments)

# Create square figure for circular symmetry
fig, ax = plt.subplots(figsize=(12, 12))
ax.set_aspect("equal")
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)

# Calculate segment positions (angles)
total_size = segment_sizes.sum()
gap_fraction = 0.02  # Gap between segments
total_gap = gap_fraction * n_segments
available_angle = 2 * np.pi * (1 - total_gap / (2 * np.pi))

angles = []
current_angle = np.pi / 2  # Start from top

for size in segment_sizes:
    segment_angle = (size / total_size) * available_angle
    start_angle = current_angle
    end_angle = current_angle - segment_angle
    angles.append((start_angle, end_angle))
    current_angle = end_angle - gap_fraction

# Draw outer ring segments
outer_radius = 1.0
ring_width = 0.12

for i, (start, end) in enumerate(angles):
    # Create wedge for segment
    theta = np.linspace(end, start, 50)
    inner = outer_radius - ring_width

    # Outer arc
    x_outer = outer_radius * np.cos(theta)
    y_outer = outer_radius * np.sin(theta)

    # Inner arc (reversed)
    x_inner = inner * np.cos(theta[::-1])
    y_inner = inner * np.sin(theta[::-1])

    # Combine to form wedge
    x = np.concatenate([x_outer, x_inner])
    y = np.concatenate([y_outer, y_inner])

    ax.fill(x, y, color=colors[i], alpha=0.85, edgecolor="white", linewidth=1.5)

    # Add segment label
    mid_angle = (start + end) / 2
    label_radius = outer_radius + 0.12
    label_x = label_radius * np.cos(mid_angle)
    label_y = label_radius * np.sin(mid_angle)

    # Rotate text based on position - ensure text is always readable (not upside down)
    rotation_deg = np.degrees(mid_angle)

    # Normalize angle to 0-360 range
    norm_angle = rotation_deg % 360

    # For angles on the left side (90-270), flip the text
    if 90 < norm_angle < 270:
        rotation = rotation_deg + 180
        ha = "right"
    else:
        rotation = rotation_deg
        ha = "left"

    ax.text(
        label_x,
        label_y,
        segments[i],
        ha=ha,
        va="center",
        fontsize=14,
        fontweight="bold",
        rotation=rotation,
        rotation_mode="anchor",
    )

# Draw inner data track (trade volume as bar heights)
inner_track_outer = outer_radius - ring_width - 0.03
inner_track_inner = inner_track_outer - 0.15

for i, (start, end) in enumerate(angles):
    # Normalize height based on segment size
    height_fraction = segment_sizes[i] / segment_sizes.max()
    track_height = (inner_track_outer - inner_track_inner) * height_fraction

    theta = np.linspace(end, start, 30)
    inner = inner_track_outer - track_height

    x_outer = inner_track_outer * np.cos(theta)
    y_outer = inner_track_outer * np.sin(theta)
    x_inner = inner * np.cos(theta[::-1])
    y_inner = inner * np.sin(theta[::-1])

    x = np.concatenate([x_outer, x_inner])
    y = np.concatenate([y_outer, y_inner])

    ax.fill(x, y, color=colors[i], alpha=0.5, edgecolor="none")

# Draw ribbons (connections between segments)
ribbon_radius = inner_track_inner - 0.05


def bezier_ribbon(start_angle1, end_angle1, start_angle2, end_angle2, radius, color, alpha=0.4):
    """Draw a ribbon connecting two segments using bezier curves"""
    # Control point at center
    ctrl_radius = radius * 0.1

    # Points for the ribbon
    n_points = 50

    # First edge of ribbon
    t = np.linspace(0, 1, n_points)

    # Start and end points for first arc of source
    p0 = np.array([radius * np.cos(start_angle1), radius * np.sin(start_angle1)])
    p3 = np.array([radius * np.cos(start_angle2), radius * np.sin(start_angle2)])

    # Control points toward center
    p1 = ctrl_radius * np.array([np.cos(start_angle1), np.sin(start_angle1)])
    p2 = ctrl_radius * np.array([np.cos(start_angle2), np.sin(start_angle2)])

    # Cubic bezier
    curve1 = (
        (1 - t)[:, None] ** 3 * p0
        + 3 * (1 - t)[:, None] ** 2 * t[:, None] * p1
        + 3 * (1 - t)[:, None] * t[:, None] ** 2 * p2
        + t[:, None] ** 3 * p3
    )

    # Second edge of ribbon
    p0 = np.array([radius * np.cos(end_angle1), radius * np.sin(end_angle1)])
    p3 = np.array([radius * np.cos(end_angle2), radius * np.sin(end_angle2)])
    p1 = ctrl_radius * np.array([np.cos(end_angle1), np.sin(end_angle1)])
    p2 = ctrl_radius * np.array([np.cos(end_angle2), np.sin(end_angle2)])

    curve2 = (
        (1 - t)[:, None] ** 3 * p0
        + 3 * (1 - t)[:, None] ** 2 * t[:, None] * p1
        + 3 * (1 - t)[:, None] * t[:, None] ** 2 * p2
        + t[:, None] ** 3 * p3
    )

    # Arc at source segment
    arc1_angles = np.linspace(start_angle1, end_angle1, 10)
    arc1 = radius * np.column_stack([np.cos(arc1_angles), np.sin(arc1_angles)])

    # Arc at target segment
    arc2_angles = np.linspace(end_angle2, start_angle2, 10)
    arc2 = radius * np.column_stack([np.cos(arc2_angles), np.sin(arc2_angles)])

    # Combine all points
    vertices = np.vstack([arc1, curve1, arc2, curve2[::-1]])

    polygon = plt.Polygon(vertices, facecolor=color, edgecolor="none", alpha=alpha, zorder=1)
    ax.add_patch(polygon)


# Draw each connection as a ribbon
max_value = max(c[2] for c in connections)

for source, target, value in connections:
    # Calculate ribbon width based on value
    width_fraction = value / max_value * 0.6 + 0.1

    # Get segment angles
    start1, end1 = angles[source]
    start2, end2 = angles[target]

    # Calculate ribbon endpoints within segments
    seg1_span = (start1 - end1) * width_fraction * 0.4
    seg2_span = (start2 - end2) * width_fraction * 0.4

    # Center the ribbon in the segment
    mid1 = (start1 + end1) / 2
    mid2 = (start2 + end2) / 2

    ribbon_start1 = mid1 + seg1_span / 2
    ribbon_end1 = mid1 - seg1_span / 2
    ribbon_start2 = mid2 + seg2_span / 2
    ribbon_end2 = mid2 - seg2_span / 2

    # Use source color for ribbon
    bezier_ribbon(ribbon_start1, ribbon_end1, ribbon_start2, ribbon_end2, ribbon_radius, colors[source], alpha=0.5)

# Remove axes for clean circular display
ax.set_xlim(-1.6, 1.6)
ax.set_ylim(-1.6, 1.6)
ax.axis("off")

# Title
ax.set_title("Global Trade Flows · circos-basic · seaborn · pyplots.ai", fontsize=24, fontweight="bold", pad=20)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
