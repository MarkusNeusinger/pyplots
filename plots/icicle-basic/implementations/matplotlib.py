"""pyplots.ai
icicle-basic: Basic Icicle Chart
Library: matplotlib | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import matplotlib.patches as patches
import matplotlib.pyplot as plt


# Data: File system structure with folders and files
# Format: (name, parent, value)
hierarchy_data = [
    ("Root", None, 0),
    ("Documents", "Root", 0),
    ("Pictures", "Root", 0),
    ("Music", "Root", 0),
    ("Reports", "Documents", 0),
    ("Letters", "Documents", 0),
    ("Spreadsheets", "Documents", 0),
    ("Photos", "Pictures", 200),
    ("Screenshots", "Pictures", 50),
    ("Icons", "Pictures", 30),
    ("Albums", "Music", 180),
    ("Playlists", "Music", 40),
    ("Podcasts", "Music", 90),
    ("Q1_Report", "Reports", 45),
    ("Q2_Report", "Reports", 55),
    ("Q3_Report", "Reports", 50),
    ("Cover_Letter", "Letters", 25),
    ("Resume", "Letters", 35),
    ("Thank_You", "Letters", 20),
    ("Budget", "Spreadsheets", 60),
    ("Forecast", "Spreadsheets", 40),
    ("Analysis", "Spreadsheets", 20),
]

# Build tree structure
nodes = {}
children = {}

for name, parent, value in hierarchy_data:
    nodes[name] = {"name": name, "parent": parent, "value": value}
    if parent is not None:
        if parent not in children:
            children[parent] = []
        children[parent].append(name)


# Calculate total value for each node (sum of children if internal node)
def get_total_value(node_name):
    if node_name not in children:
        return nodes[node_name]["value"]
    total = sum(get_total_value(child) for child in children[node_name])
    return total


# Calculate positions for icicle chart (top-to-bottom layout)
def calculate_positions(node_name, x_start, x_end, depth, positions):
    total_value = get_total_value(node_name)
    positions[node_name] = {"x_start": x_start, "x_end": x_end, "depth": depth, "value": total_value}

    if node_name in children:
        current_x = x_start
        for child in children[node_name]:
            child_value = get_total_value(child)
            child_width = (child_value / total_value) * (x_end - x_start)
            calculate_positions(child, current_x, current_x + child_width, depth + 1, positions)
            current_x += child_width


positions = {}
calculate_positions("Root", 0, 1, 0, positions)

# Find max depth
max_depth = max(pos["depth"] for pos in positions.values())

# Color palette by depth level (colorblind-safe)
depth_colors = [
    "#306998",  # Python Blue - Level 0
    "#FFD43B",  # Python Yellow - Level 1
    "#4ECDC4",  # Teal - Level 2
    "#FF6B6B",  # Coral - Level 3
    "#95E1D3",  # Light teal - Level 4
]

# Create plot
fig, ax = plt.subplots(figsize=(16, 9))

# Draw rectangles
row_height = 1.0 / (max_depth + 1)

for node_name, pos in positions.items():
    depth = pos["depth"]
    x_start = pos["x_start"]
    x_end = pos["x_end"]
    width = x_end - x_start

    # Y position (top-to-bottom: depth 0 at top)
    y_start = 1.0 - (depth + 1) * row_height

    # Get color based on depth
    color = depth_colors[depth % len(depth_colors)]

    # Draw rectangle
    rect = patches.Rectangle(
        (x_start, y_start),
        width,
        row_height * 0.95,  # Small gap between rows
        linewidth=2,
        edgecolor="white",
        facecolor=color,
        alpha=0.85,
    )
    ax.add_patch(rect)

    # Add label if rectangle is wide enough
    if width > 0.04:
        label = node_name
        if len(label) > 10 and width < 0.10:
            label = label[:8] + ".."

        # Calculate font size based on width
        fontsize = min(18, max(11, int(width * 140)))

        ax.text(
            x_start + width / 2,
            y_start + row_height * 0.95 / 2,
            label,
            ha="center",
            va="center",
            fontsize=fontsize,
            fontweight="bold",
            color="white" if depth != 1 else "black",
        )

# Configure axes
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect("auto")

# Add depth level labels on the right
for depth in range(max_depth + 1):
    y_pos = 1.0 - (depth + 0.5) * row_height
    level_label = ["Root", "Category", "Subcategory", "Files", ""][depth]
    ax.text(1.02, y_pos, level_label, fontsize=14, va="center", color="#333333")

# Remove axes for cleaner look
ax.axis("off")

# Add title
ax.set_title("File System Structure · icicle-basic · matplotlib · pyplots.ai", fontsize=24, fontweight="bold", pad=20)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
