""" pyplots.ai
icicle-basic: Basic Icicle Chart
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 78/100 | Created: 2025-12-30
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.patches import Patch


# Set seaborn style for consistent appearance
sns.set_style("white")
sns.set_context("talk", font_scale=1.2)

# Hierarchical data: File system structure
# Format: (name, parent, value)
hierarchy_data = [
    ("Root", None, 1000),
    ("Documents", "Root", 350),
    ("Media", "Root", 450),
    ("Projects", "Root", 200),
    ("Reports", "Documents", 150),
    ("Presentations", "Documents", 120),
    ("Templates", "Documents", 80),
    ("Images", "Media", 200),
    ("Videos", "Media", 180),
    ("Audio", "Media", 70),
    ("Q1_Report.pdf", "Reports", 50),
    ("Q2_Report.pdf", "Reports", 60),
    ("Annual.pdf", "Reports", 40),
    ("Sales.pptx", "Presentations", 70),
    ("Training.pptx", "Presentations", 50),
    ("Photos", "Images", 120),
    ("Screenshots", "Images", 80),
    ("Tutorials", "Videos", 100),
    ("Recordings", "Videos", 80),
    ("Code", "Projects", 120),
    ("Designs", "Projects", 80),
]

# Build node dictionary
nodes = {}
for name, parent, value in hierarchy_data:
    nodes[name] = {"name": name, "parent": parent, "value": value, "children": []}

for name, parent, _value in hierarchy_data:
    if parent and parent in nodes:
        nodes[parent]["children"].append(name)

# Calculate levels inline (no helper functions - KISS principle)
levels = {}
for name in nodes:
    level = 0
    current = name
    while nodes[current]["parent"] is not None:
        level += 1
        current = nodes[current]["parent"]
    levels[name] = level

max_level = max(levels.values())

# Calculate totals inline (sum of children or own value if leaf)
totals = {}
sorted_nodes = sorted(nodes.keys(), key=lambda x: levels[x], reverse=True)
for name in sorted_nodes:
    children = nodes[name]["children"]
    if not children:
        totals[name] = nodes[name]["value"]
    else:
        totals[name] = sum(totals[child] for child in children)

# Calculate positions for icicle chart using stack-based iteration
rectangles = []
stack = [("Root", 0.0, 1.0, 0)]

while stack:
    name, x_start, x_end, level = stack.pop()
    width = x_end - x_start
    height = 1.0 / (max_level + 1)
    y = 1.0 - (level + 1) * height

    rectangles.append(
        {"name": name, "x": x_start, "y": y, "width": width, "height": height, "level": level, "value": totals[name]}
    )

    children = nodes[name]["children"]
    if children:
        total_child_value = sum(totals[c] for c in children)
        current_x = x_start
        for child in reversed(children):
            child_fraction = totals[child] / total_child_value
            child_width = width * child_fraction
            stack.append((child, current_x, current_x + child_width, level + 1))
            current_x += child_width

# Create heatmap matrix for icicle visualization using seaborn
# Grid resolution for the heatmap
grid_cols = 200
grid_rows = (max_level + 1) * 5  # 5 rows per level for visual clarity
heatmap_data = np.full((grid_rows, grid_cols), np.nan)
annotations = {}

# Fill heatmap grid based on rectangle positions
for rect in rectangles:
    col_start = int(rect["x"] * grid_cols)
    col_end = int((rect["x"] + rect["width"]) * grid_cols)
    row_start = int((1 - rect["y"] - rect["height"]) * grid_rows)
    row_end = int((1 - rect["y"]) * grid_rows)

    # Leave gaps between rectangles
    col_start = min(col_start + 1, col_end - 1) if col_end - col_start > 2 else col_start
    col_end = max(col_end - 1, col_start + 1) if col_end - col_start > 2 else col_end
    row_end = max(row_end - 1, row_start + 1)

    # Use level as value for coloring
    heatmap_data[row_start:row_end, col_start:col_end] = rect["level"]

    # Store annotation position for labels
    if rect["width"] > 0.035:
        annotations[rect["name"]] = {
            "col": (col_start + col_end) / 2,
            "row": (row_start + row_end) / 2,
            "width": col_end - col_start,
            "level": rect["level"],
        }

# Create figure with optimal size
fig, ax = plt.subplots(figsize=(16, 10))

# Use seaborn heatmap to create the icicle chart visualization
n_levels = max_level + 1
cmap = sns.color_palette("Blues_r", n_colors=n_levels + 2, as_cmap=False)
cmap_full = sns.blend_palette(cmap[1:-1], n_colors=n_levels, as_cmap=True)

sns.heatmap(
    heatmap_data,
    ax=ax,
    cmap=cmap_full,
    vmin=0,
    vmax=max_level,
    cbar=False,
    xticklabels=False,
    yticklabels=False,
    linewidths=0,
    square=False,
)

# Add text labels for larger rectangles
for name, pos in annotations.items():
    level = pos["level"]
    fontsize = 11 if level <= 1 else (10 if level == 2 else 9)
    text_color = "white" if level < 2 else "#2c3e50"

    display_text = name
    max_chars = max(8, int(pos["width"] / 8))
    if len(display_text) > max_chars:
        display_text = display_text[: max_chars - 2] + ".."

    ax.text(
        pos["col"],
        pos["row"],
        display_text,
        ha="center",
        va="center",
        fontsize=fontsize,
        fontweight="bold",
        color=text_color,
    )

# Configure axes
ax.set_xlim(0, grid_cols)
ax.set_ylim(grid_rows, 0)
ax.axis("off")

# Title with correct format: spec-id first
ax.set_title("icicle-basic · File System Structure · seaborn · pyplots.ai", fontsize=24, fontweight="bold", pad=20)

# Add legend for hierarchy levels
palette = sns.color_palette("Blues_r", n_colors=n_levels + 2)[1:-1]
legend_labels = ["Root", "Category", "Subcategory", "Files"][:n_levels]
legend_patches = [
    Patch(facecolor=palette[i], edgecolor="white", linewidth=1.5, label=legend_labels[i]) for i in range(n_levels)
]
ax.legend(
    handles=legend_patches,
    loc="lower right",
    fontsize=14,
    framealpha=0.95,
    title="Hierarchy Level",
    title_fontsize=16,
    edgecolor="#cccccc",
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
