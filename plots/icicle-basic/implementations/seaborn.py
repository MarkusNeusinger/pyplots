""" pyplots.ai
icicle-basic: Basic Icicle Chart
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 72/100 | Created: 2025-12-30
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import seaborn as sns


# Set seaborn style and context for consistent appearance
sns.set_style("whitegrid")
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

# Build tree structure
nodes = {}
for name, parent, value in hierarchy_data:
    nodes[name] = {"name": name, "parent": parent, "value": value, "children": []}

for name, parent, _value in hierarchy_data:
    if parent and parent in nodes:
        nodes[parent]["children"].append(name)


# Calculate hierarchy levels
def get_level(name, nodes):
    level = 0
    current = name
    while nodes[current]["parent"] is not None:
        level += 1
        current = nodes[current]["parent"]
    return level


max_level = max(get_level(name, nodes) for name in nodes)


# Calculate leaf values (sum of children or own value if leaf)
def calc_leaf_sum(name, nodes):
    children = nodes[name]["children"]
    if not children:
        return nodes[name]["value"]
    return sum(calc_leaf_sum(child, nodes) for child in children)


for name in nodes:
    nodes[name]["total"] = calc_leaf_sum(name, nodes)

# Get seaborn color palette
n_levels = max_level + 1
palette = sns.color_palette("Blues_r", n_colors=n_levels + 2)[1:-1]

# Create figure (16:9 aspect ratio for hierarchy)
fig, ax = plt.subplots(figsize=(16, 9))

# Calculate positions for icicle chart (horizontal, top-to-bottom)
rectangles = []


def layout_node(name, x_start, x_end, level, nodes, rectangles):
    """Recursively layout nodes as icicle rectangles."""
    node = nodes[name]
    width = x_end - x_start
    height = 1.0 / (max_level + 1)
    y = 1.0 - (level + 1) * height  # Top-to-bottom

    rectangles.append(
        {"name": name, "x": x_start, "y": y, "width": width, "height": height, "level": level, "value": node["total"]}
    )

    # Layout children proportionally
    children = node["children"]
    if children:
        total_child_value = sum(nodes[c]["total"] for c in children)
        current_x = x_start
        for child in children:
            child_fraction = nodes[child]["total"] / total_child_value
            child_width = width * child_fraction
            layout_node(child, current_x, current_x + child_width, level + 1, nodes, rectangles)
            current_x += child_width


# Start layout from root
layout_node("Root", 0, 1, 0, nodes, rectangles)

# Draw rectangles
for rect in rectangles:
    color = palette[rect["level"]]
    patch = mpatches.FancyBboxPatch(
        (rect["x"], rect["y"]),
        rect["width"],
        rect["height"] * 0.95,  # Small gap between levels
        boxstyle="round,pad=0,rounding_size=0.005",
        facecolor=color,
        edgecolor="white",
        linewidth=2,
    )
    ax.add_patch(patch)

    # Add labels for rectangles with sufficient width
    if rect["width"] > 0.05:
        label_x = rect["x"] + rect["width"] / 2
        label_y = rect["y"] + rect["height"] * 0.95 / 2

        # Adjust font size based on rectangle size
        fontsize = min(16, max(10, int(rect["width"] * 100)))

        # Determine text color based on background brightness
        text_color = "white" if rect["level"] < 2 else "#333333"

        display_text = rect["name"]
        if len(display_text) > 12 and rect["width"] < 0.15:
            display_text = display_text[:10] + "..."

        ax.text(
            label_x,
            label_y,
            display_text,
            ha="center",
            va="center",
            fontsize=fontsize,
            fontweight="bold",
            color=text_color,
        )

# Configure axes
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect("auto")
ax.axis("off")

# Title
ax.set_title("File System Structure · icicle-basic · seaborn · pyplots.ai", fontsize=24, fontweight="bold", pad=20)

# Add legend for hierarchy levels
legend_labels = ["Root", "Category", "Subcategory", "Files"][:n_levels]
legend_patches = [
    mpatches.Patch(facecolor=palette[i], edgecolor="white", label=legend_labels[i])
    for i in range(min(len(legend_labels), n_levels))
]
ax.legend(
    handles=legend_patches, loc="lower right", fontsize=14, framealpha=0.9, title="Hierarchy Level", title_fontsize=16
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
