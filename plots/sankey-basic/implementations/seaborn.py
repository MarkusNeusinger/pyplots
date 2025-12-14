"""
sankey-basic: Basic Sankey Diagram
Library: seaborn
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.path import Path


# Apply seaborn styling for consistent aesthetics
sns.set_theme(style="white")

# Data: Energy flow from sources to end uses (in TWh)
flows = [
    ("Coal", "Residential", 5),
    ("Coal", "Commercial", 8),
    ("Coal", "Industrial", 35),
    ("Coal", "Transport", 2),
    ("Natural Gas", "Residential", 25),
    ("Natural Gas", "Commercial", 18),
    ("Natural Gas", "Industrial", 20),
    ("Natural Gas", "Transport", 5),
    ("Nuclear", "Residential", 12),
    ("Nuclear", "Commercial", 10),
    ("Nuclear", "Industrial", 8),
    ("Nuclear", "Transport", 0),
    ("Renewables", "Residential", 8),
    ("Renewables", "Commercial", 6),
    ("Renewables", "Industrial", 5),
    ("Renewables", "Transport", 3),
]

# Filter out zero flows
flows = [(s, t, v) for s, t, v in flows if v > 0]

# Get unique sources and targets
sources = ["Coal", "Natural Gas", "Nuclear", "Renewables"]
targets = ["Residential", "Commercial", "Industrial", "Transport"]

# Calculate totals for node heights
source_totals = {s: sum(v for src, _, v in flows if src == s) for s in sources}
target_totals = {t: sum(v for _, tgt, v in flows if tgt == t) for t in targets}

# Colors using seaborn color palette
source_colors = sns.color_palette("husl", len(sources))
source_color_map = dict(zip(sources, source_colors, strict=True))

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Layout parameters
left_x = 0.1
right_x = 0.9
node_width = 0.03
gap = 0.02

# Calculate total height and scale
total_flow = sum(v for _, _, v in flows)
plot_height = 0.75
scale = plot_height / max(sum(source_totals.values()), sum(target_totals.values()))

# Position source nodes (left side)
source_positions = {}
current_y = 0.9
for source in sources:
    height = source_totals[source] * scale
    source_positions[source] = {
        "x": left_x,
        "y_top": current_y,
        "y_bottom": current_y - height,
        "height": height,
        "flow_y": current_y,  # Track where next flow starts
    }
    current_y -= height + gap

# Position target nodes (right side)
target_positions = {}
current_y = 0.9
for target in targets:
    height = target_totals[target] * scale
    target_positions[target] = {
        "x": right_x,
        "y_top": current_y,
        "y_bottom": current_y - height,
        "height": height,
        "flow_y": current_y,  # Track where next flow starts
    }
    current_y -= height + gap


def draw_flow(ax, x0, y0_top, y0_bottom, x1, y1_top, y1_bottom, color, alpha=0.5):
    """Draw a curved flow between two vertical segments using Bezier curves."""
    # Control points for smooth curves
    mid_x = (x0 + x1) / 2

    # Create path for the flow band
    verts = [
        (x0, y0_top),  # Start top-left
        (mid_x, y0_top),  # Control point 1
        (mid_x, y1_top),  # Control point 2
        (x1, y1_top),  # End top-right
        (x1, y1_bottom),  # End bottom-right
        (mid_x, y1_bottom),  # Control point 3
        (mid_x, y0_bottom),  # Control point 4
        (x0, y0_bottom),  # End bottom-left
        (x0, y0_top),  # Close path
    ]

    codes = [
        Path.MOVETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.LINETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CLOSEPOLY,
    ]

    path = Path(verts, codes)
    patch = mpatches.PathPatch(path, facecolor=color, edgecolor="none", alpha=alpha)
    ax.add_patch(patch)


# Draw flows
for source, target, value in flows:
    flow_height = value * scale
    color = source_color_map[source]

    # Get current flow positions
    src = source_positions[source]
    tgt = target_positions[target]

    # Calculate flow band positions
    src_y_top = src["flow_y"]
    src_y_bottom = src_y_top - flow_height
    tgt_y_top = tgt["flow_y"]
    tgt_y_bottom = tgt_y_top - flow_height

    # Draw the flow
    draw_flow(ax, src["x"] + node_width, src_y_top, src_y_bottom, tgt["x"], tgt_y_top, tgt_y_bottom, color, alpha=0.6)

    # Update flow tracking
    source_positions[source]["flow_y"] = src_y_bottom
    target_positions[target]["flow_y"] = tgt_y_bottom

# Draw source nodes (rectangles on left)
for source in sources:
    pos = source_positions[source]
    rect = mpatches.Rectangle(
        (pos["x"], pos["y_bottom"]),
        node_width,
        pos["height"],
        facecolor=source_color_map[source],
        edgecolor="white",
        linewidth=2,
    )
    ax.add_patch(rect)

    # Add label
    ax.text(
        pos["x"] - 0.02,
        (pos["y_top"] + pos["y_bottom"]) / 2,
        f"{source}\n({source_totals[source]} TWh)",
        ha="right",
        va="center",
        fontsize=14,
        fontweight="bold",
    )

# Draw target nodes (rectangles on right)
for target in targets:
    pos = target_positions[target]
    # Use a neutral color for targets
    rect = mpatches.Rectangle(
        (pos["x"], pos["y_bottom"]), node_width, pos["height"], facecolor="#306998", edgecolor="white", linewidth=2
    )
    ax.add_patch(rect)

    # Add label
    ax.text(
        pos["x"] + node_width + 0.02,
        (pos["y_top"] + pos["y_bottom"]) / 2,
        f"{target}\n({target_totals[target]} TWh)",
        ha="left",
        va="center",
        fontsize=14,
        fontweight="bold",
    )

# Style the plot
ax.set_xlim(-0.05, 1.05)
ax.set_ylim(0, 1)
ax.set_aspect("equal")
ax.axis("off")

# Title
ax.set_title("Energy Flow Distribution · sankey-basic · seaborn · pyplots.ai", fontsize=24, fontweight="bold", pad=20)

# Add legend for source colors
legend_handles = [mpatches.Patch(color=source_color_map[s], label=s, alpha=0.8) for s in sources]
ax.legend(handles=legend_handles, loc="lower center", ncol=4, fontsize=12, frameon=False, bbox_to_anchor=(0.5, -0.02))

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
