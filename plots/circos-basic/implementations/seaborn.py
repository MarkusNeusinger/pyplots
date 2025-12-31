""" pyplots.ai
circos-basic: Circos Plot
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 78/100 | Created: 2025-12-31
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Set seaborn theme for consistent styling with larger fonts
sns.set_theme(style="white", context="poster", font_scale=1.3)

# Data: Regional trade flows (10 regions with trade connections)
np.random.seed(42)

# Define segments (regions) with their sizes (trade volume in billion USD)
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

# Segment sizes represent total trade volume (billion USD)
segment_sizes = np.array([250, 320, 280, 150, 120, 100, 80, 90, 60, 50])

# Create connection data (source, target, value in billion USD)
connections = [
    (0, 1, 85),
    (0, 2, 120),
    (1, 2, 95),
    (1, 5, 60),
    (2, 3, 70),
    (2, 4, 45),
    (3, 4, 35),
    (1, 6, 40),
    (0, 7, 55),
    (2, 8, 50),
    (5, 4, 30),
    (5, 6, 25),
    (1, 9, 20),
    (2, 9, 28),
    (0, 3, 38),
]

# Create color palette using seaborn's husl palette
colors = sns.color_palette("husl", n_colors=n_segments)

# Create square figure for circular symmetry (3600x3600 at 300 dpi = 12x12 inches)
fig, ax = plt.subplots(figsize=(12, 12))
ax.set_aspect("equal")

# Calculate segment positions (angles)
total_size = segment_sizes.sum()
gap_fraction = 0.02
total_gap = gap_fraction * n_segments
available_angle = 2 * np.pi * (1 - total_gap / (2 * np.pi))

angles = []
current_angle = np.pi / 2

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
    theta = np.linspace(end, start, 50)
    inner = outer_radius - ring_width
    x_outer = outer_radius * np.cos(theta)
    y_outer = outer_radius * np.sin(theta)
    x_inner = inner * np.cos(theta[::-1])
    y_inner = inner * np.sin(theta[::-1])
    x = np.concatenate([x_outer, x_inner])
    y = np.concatenate([y_outer, y_inner])
    ax.fill(x, y, color=colors[i], alpha=0.85, edgecolor="white", linewidth=2)

    # Add segment label with larger font
    mid_angle = (start + end) / 2
    label_radius = outer_radius + 0.14
    label_x = label_radius * np.cos(mid_angle)
    label_y = label_radius * np.sin(mid_angle)
    rotation_deg = np.degrees(mid_angle)
    norm_angle = rotation_deg % 360
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
        fontsize=18,
        fontweight="bold",
        rotation=rotation,
        rotation_mode="anchor",
    )

# Draw inner data track (trade volume as bar heights)
inner_track_outer = outer_radius - ring_width - 0.03
inner_track_inner = inner_track_outer - 0.15

for i, (start, end) in enumerate(angles):
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

# Draw ribbons (connections between segments) - inline bezier curve calculation
ribbon_radius = inner_track_inner - 0.05
max_value = max(c[2] for c in connections)
ctrl_radius = ribbon_radius * 0.1
n_points = 50
t = np.linspace(0, 1, n_points)

for source, target, value in connections:
    width_fraction = value / max_value * 0.6 + 0.1
    start1, end1 = angles[source]
    start2, end2 = angles[target]
    seg1_span = (start1 - end1) * width_fraction * 0.4
    seg2_span = (start2 - end2) * width_fraction * 0.4
    mid1 = (start1 + end1) / 2
    mid2 = (start2 + end2) / 2
    ribbon_start1 = mid1 + seg1_span / 2
    ribbon_end1 = mid1 - seg1_span / 2
    ribbon_start2 = mid2 + seg2_span / 2
    ribbon_end2 = mid2 - seg2_span / 2

    # First bezier curve
    p0 = np.array([ribbon_radius * np.cos(ribbon_start1), ribbon_radius * np.sin(ribbon_start1)])
    p3 = np.array([ribbon_radius * np.cos(ribbon_start2), ribbon_radius * np.sin(ribbon_start2)])
    p1 = ctrl_radius * np.array([np.cos(ribbon_start1), np.sin(ribbon_start1)])
    p2 = ctrl_radius * np.array([np.cos(ribbon_start2), np.sin(ribbon_start2)])
    curve1 = (
        (1 - t)[:, None] ** 3 * p0
        + 3 * (1 - t)[:, None] ** 2 * t[:, None] * p1
        + 3 * (1 - t)[:, None] * t[:, None] ** 2 * p2
        + t[:, None] ** 3 * p3
    )

    # Second bezier curve
    p0 = np.array([ribbon_radius * np.cos(ribbon_end1), ribbon_radius * np.sin(ribbon_end1)])
    p3 = np.array([ribbon_radius * np.cos(ribbon_end2), ribbon_radius * np.sin(ribbon_end2)])
    p1 = ctrl_radius * np.array([np.cos(ribbon_end1), np.sin(ribbon_end1)])
    p2 = ctrl_radius * np.array([np.cos(ribbon_end2), np.sin(ribbon_end2)])
    curve2 = (
        (1 - t)[:, None] ** 3 * p0
        + 3 * (1 - t)[:, None] ** 2 * t[:, None] * p1
        + 3 * (1 - t)[:, None] * t[:, None] ** 2 * p2
        + t[:, None] ** 3 * p3
    )

    # Arcs at source and target segments
    arc1_angles = np.linspace(ribbon_start1, ribbon_end1, 10)
    arc1 = ribbon_radius * np.column_stack([np.cos(arc1_angles), np.sin(arc1_angles)])
    arc2_angles = np.linspace(ribbon_end2, ribbon_start2, 10)
    arc2 = ribbon_radius * np.column_stack([np.cos(arc2_angles), np.sin(arc2_angles)])

    # Combine vertices and draw polygon
    vertices = np.vstack([arc1, curve1, arc2, curve2[::-1]])
    polygon = plt.Polygon(vertices, facecolor=colors[source], edgecolor="none", alpha=0.5, zorder=1)
    ax.add_patch(polygon)

# Configure axes
ax.set_xlim(-1.7, 1.7)
ax.set_ylim(-1.7, 1.7)
ax.axis("off")

# Title with larger font
ax.set_title(
    "circos-basic · seaborn · pyplots.ai\nGlobal Trade Flows Between Regions", fontsize=28, fontweight="bold", pad=25
)

# Add legend explaining the visualization
legend_elements = [
    mpatches.Patch(
        facecolor=sns.color_palette("husl", 1)[0], alpha=0.85, label="Outer ring: Region (arc size ∝ total trade)"
    ),
    mpatches.Patch(
        facecolor=sns.color_palette("husl", 1)[0], alpha=0.5, label="Inner track: Trade volume (bar height)"
    ),
    mpatches.Patch(facecolor=sns.color_palette("husl", 1)[0], alpha=0.5, label="Ribbons: Trade flow (width ∝ value)"),
]
ax.legend(handles=legend_elements, loc="lower center", bbox_to_anchor=(0.5, -0.08), ncol=1, fontsize=16, frameon=False)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
