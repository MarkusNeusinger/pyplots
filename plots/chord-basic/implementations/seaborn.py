"""
chord-basic: Basic Chord Diagram
Library: seaborn
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path


# Data - Migration flows between continents (in millions)
continents = ["Africa", "Asia", "Europe", "N. America", "S. America", "Oceania"]
n = len(continents)

# Flow matrix (source rows -> target columns)
np.random.seed(42)
flows = np.array(
    [
        [0, 8, 12, 3, 2, 1],  # Africa to others
        [5, 0, 15, 10, 2, 4],  # Asia to others
        [3, 6, 0, 8, 4, 2],  # Europe to others
        [2, 4, 6, 0, 5, 1],  # N. America to others
        [1, 2, 5, 8, 0, 1],  # S. America to others
        [1, 3, 2, 2, 1, 0],  # Oceania to others
    ]
)

# Colors for each continent
colors = ["#306998", "#FFD43B", "#4CAF50", "#E91E63", "#9C27B0", "#FF9800"]

# Calculate arc sizes based on total flow (in + out)
total_flow = flows.sum(axis=1) + flows.sum(axis=0)
total = total_flow.sum()

# Gap between segments
gap = 0.02
available = 1 - n * gap
arc_sizes = (total_flow / total) * available

# Calculate start and end angles for each segment
angles = []
current = 0
for i in range(n):
    start = current
    end = current + arc_sizes[i] * 2 * np.pi
    angles.append((start, end))
    current = end + gap * 2 * np.pi

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))
ax.set_aspect("equal")

# Draw outer arcs for each continent
radius = 1.0
arc_width = 0.08

for i, (start, end) in enumerate(angles):
    theta = np.linspace(start, end, 50)
    # Outer arc
    x_outer = (radius + arc_width / 2) * np.cos(theta)
    y_outer = (radius + arc_width / 2) * np.sin(theta)
    x_inner = (radius - arc_width / 2) * np.cos(theta)
    y_inner = (radius - arc_width / 2) * np.sin(theta)

    # Create filled arc using fill_between approach
    verts = (
        list(zip(x_outer, y_outer, strict=True))
        + list(zip(x_inner[::-1], y_inner[::-1], strict=True))
        + [(x_outer[0], y_outer[0])]
    )
    codes = [Path.MOVETO] + [Path.LINETO] * (len(verts) - 2) + [Path.CLOSEPOLY]
    path = Path(verts, codes)
    patch = mpatches.PathPatch(path, facecolor=colors[i], edgecolor="white", linewidth=2)
    ax.add_patch(patch)

    # Add label
    mid_angle = (start + end) / 2
    label_r = radius + arc_width / 2 + 0.15
    x_label = label_r * np.cos(mid_angle)
    y_label = label_r * np.sin(mid_angle)

    # Rotate text to be readable
    rotation = np.degrees(mid_angle)
    if 90 < rotation < 270:
        rotation += 180
        ha = "right"
    else:
        ha = "left"

    ax.text(
        x_label,
        y_label,
        continents[i],
        fontsize=18,
        fontweight="bold",
        ha=ha,
        va="center",
        rotation=rotation,
        rotation_mode="anchor",
    )


# Draw chords between segments
def bezier_chord(start1, end1, start2, end2, color, alpha=0.6):
    """Draw a chord between two arc segments using bezier curves."""
    # Control point at center
    ctrl = (0, 0)

    # Points on first arc
    theta1_start = start1
    theta1_end = end1
    # Points on second arc
    theta2_start = start2
    theta2_end = end2

    r = radius - arc_width / 2 - 0.02

    # Build path for the chord
    n_pts = 20
    t1 = np.linspace(theta1_start, theta1_end, n_pts)
    t2 = np.linspace(theta2_end, theta2_start, n_pts)

    # First edge along arc 1
    x1 = r * np.cos(t1)
    y1 = r * np.sin(t1)

    # Bezier curve from arc1 end to arc2 start
    p0 = (r * np.cos(theta1_end), r * np.sin(theta1_end))
    p2 = (r * np.cos(theta2_end), r * np.sin(theta2_end))

    bez1_t = np.linspace(0, 1, n_pts)
    bez1_x = (1 - bez1_t) ** 2 * p0[0] + 2 * (1 - bez1_t) * bez1_t * ctrl[0] + bez1_t**2 * p2[0]
    bez1_y = (1 - bez1_t) ** 2 * p0[1] + 2 * (1 - bez1_t) * bez1_t * ctrl[1] + bez1_t**2 * p2[1]

    # Second edge along arc 2 (reversed)
    x2 = r * np.cos(t2)
    y2 = r * np.sin(t2)

    # Bezier curve from arc2 end to arc1 start
    p0b = (r * np.cos(theta2_start), r * np.sin(theta2_start))
    p2b = (r * np.cos(theta1_start), r * np.sin(theta1_start))

    bez2_x = (1 - bez1_t) ** 2 * p0b[0] + 2 * (1 - bez1_t) * bez1_t * ctrl[0] + bez1_t**2 * p2b[0]
    bez2_y = (1 - bez1_t) ** 2 * p0b[1] + 2 * (1 - bez1_t) * bez1_t * ctrl[1] + bez1_t**2 * p2b[1]

    # Combine all vertices
    all_x = np.concatenate([x1, bez1_x, x2, bez2_x])
    all_y = np.concatenate([y1, bez1_y, y2, bez2_y])

    verts = list(zip(all_x, all_y, strict=True)) + [(all_x[0], all_y[0])]
    codes = [Path.MOVETO] + [Path.LINETO] * (len(verts) - 2) + [Path.CLOSEPOLY]

    path = Path(verts, codes)
    patch = mpatches.PathPatch(path, facecolor=color, edgecolor="none", alpha=alpha)
    ax.add_patch(patch)


# Calculate sub-arc positions within each segment for chord connections
# For each segment, divide it proportionally based on flows
def get_sub_arc(segment_idx, partner_idx, is_outgoing):
    """Get the angular position for a chord endpoint within a segment."""
    start, end = angles[segment_idx]
    segment_span = end - start

    if is_outgoing:
        # Outgoing flows use first half of segment
        flow_values = flows[segment_idx, :]
    else:
        # Incoming flows use second half of segment
        flow_values = flows[:, segment_idx]

    total = flow_values.sum()
    if total == 0:
        return start, start

    # Calculate cumulative positions
    cumsum = np.cumsum(flow_values)
    if partner_idx == 0:
        prev_sum = 0
    else:
        prev_sum = cumsum[partner_idx - 1]
    curr_sum = cumsum[partner_idx]

    # Map to angular position within segment
    arc_start = start + (prev_sum / total) * segment_span
    arc_end = start + (curr_sum / total) * segment_span

    return arc_start, arc_end


# Draw all chords
for i in range(n):
    for j in range(n):
        if i != j and flows[i, j] > 0:
            # Get source arc position (outgoing from i)
            src_start, src_end = get_sub_arc(i, j, is_outgoing=True)
            # Get target arc position (incoming to j)
            tgt_start, tgt_end = get_sub_arc(j, i, is_outgoing=False)

            # Draw chord with source color
            bezier_chord(src_start, src_end, tgt_start, tgt_end, colors[i], alpha=0.5)

# Style
ax.set_xlim(-1.6, 1.6)
ax.set_ylim(-1.4, 1.4)
ax.axis("off")

# Title
ax.set_title("Global Migration Flows · chord-basic · seaborn · pyplots.ai", fontsize=24, fontweight="bold", pad=20)

# Legend
legend_handles = [mpatches.Patch(color=colors[i], label=continents[i]) for i in range(n)]
ax.legend(handles=legend_handles, loc="lower right", fontsize=14, framealpha=0.9, title="Continents", title_fontsize=16)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
