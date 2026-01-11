"""pyplots.ai
hierarchy-toggle-view: Interactive Treemap-Sunburst Toggle View
Library: matplotlib | Python 3.13
Quality: pending | Created: 2026-01-11
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np


# Data: Company departments with sub-units (hierarchical structure)
# Format: (id, parent, label, value)
hierarchy_data = [
    ("root", None, "Company", 0),
    ("eng", "root", "Engineering", 0),
    ("sales", "root", "Sales", 0),
    ("ops", "root", "Operations", 0),
    ("hr", "root", "HR", 0),
    # Engineering sub-departments
    ("frontend", "eng", "Frontend", 45),
    ("backend", "eng", "Backend", 55),
    ("devops", "eng", "DevOps", 30),
    ("qa", "eng", "QA", 25),
    # Sales sub-departments
    ("domestic", "sales", "Domestic", 40),
    ("international", "sales", "International", 50),
    ("partnerships", "sales", "Partnerships", 25),
    # Operations sub-departments
    ("logistics", "ops", "Logistics", 35),
    ("facilities", "ops", "Facilities", 20),
    ("it_support", "ops", "IT Support", 25),
    # HR sub-departments
    ("recruiting", "hr", "Recruiting", 30),
    ("training", "hr", "Training", 20),
    ("benefits", "hr", "Benefits", 15),
]

# Build hierarchy structure
nodes = {row[0]: {"parent": row[1], "label": row[2], "value": row[3]} for row in hierarchy_data}

# Calculate parent values as sum of children
for node_id, node in nodes.items():
    if node["value"] == 0:
        children_sum = sum(n["value"] for nid, n in nodes.items() if n["parent"] == node_id)
        node["value"] = children_sum

# Color palette for main departments (colorblind-safe)
dept_colors = {
    "eng": "#306998",  # Python Blue
    "sales": "#FFD43B",  # Python Yellow
    "ops": "#2E8B57",  # Sea Green
    "hr": "#E07B39",  # Burnt Orange
}

# Pre-compute node colors (children inherit parent department color)
node_colors = {}
for nid in nodes:
    if nid == "root":
        node_colors[nid] = "#CCCCCC"
    elif nid in dept_colors:
        node_colors[nid] = dept_colors[nid]
    else:
        parent = nodes[nid]["parent"]
        node_colors[nid] = dept_colors.get(parent, "#CCCCCC")

# Create figure with two subplots side by side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 9))

# ============ LEFT: TREEMAP ============
# Get leaf nodes (sub-departments)
leaf_nodes = [
    (nid, n) for nid, n in nodes.items() if n["value"] > 0 and n["parent"] != "root" and n["parent"] is not None
]
leaf_nodes = [(nid, n) for nid, n in leaf_nodes if nodes.get(n["parent"], {}).get("parent") == "root"]

# Group by parent department
dept_groups = {}
for nid, n in leaf_nodes:
    parent = n["parent"]
    if parent not in dept_groups:
        dept_groups[parent] = []
    dept_groups[parent].append((nid, n))

# Calculate total value for proportions
total_value = sum(n["value"] for _, n in leaf_nodes)

# Treemap layout using simple slice-and-dice
x_start = 0.05
y_start = 0.05
width = 0.9
height = 0.85

current_x = x_start
for _dept_id, items in dept_groups.items():
    dept_value = sum(n["value"] for _, n in items)
    dept_width = (dept_value / total_value) * width

    current_y = y_start
    for nid, n in items:
        item_height = (n["value"] / dept_value) * height
        color = node_colors[nid]

        rect = mpatches.FancyBboxPatch(
            (current_x, current_y),
            dept_width - 0.005,
            item_height - 0.005,
            boxstyle="round,pad=0.01",
            facecolor=color,
            edgecolor="white",
            linewidth=2,
        )
        ax1.add_patch(rect)

        # Add label if rectangle is large enough
        if dept_width > 0.1 and item_height > 0.08:
            ax1.text(
                current_x + dept_width / 2 - 0.0025,
                current_y + item_height / 2 - 0.0025,
                f"{n['label']}\n({n['value']})",
                ha="center",
                va="center",
                fontsize=14,
                fontweight="bold",
                color="white" if color in ["#306998", "#2E8B57"] else "black",
            )

        current_y += item_height

    current_x += dept_width

ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.set_aspect("equal")
ax1.axis("off")
ax1.set_title("Treemap View", fontsize=22, fontweight="bold", pad=15)

# ============ RIGHT: SUNBURST ============
# Prepare data for sunburst (two rings: departments and sub-departments)
dept_order = ["eng", "sales", "ops", "hr"]
dept_values = [nodes[d]["value"] for d in dept_order]
dept_labels = [nodes[d]["label"] for d in dept_order]
dept_cols = [dept_colors[d] for d in dept_order]

# Inner ring: departments
inner_sizes = dept_values
inner_colors = dept_cols

# Outer ring: sub-departments (in order)
outer_sizes = []
outer_colors = []
outer_labels = []
for dept_id in dept_order:
    children = [(nid, n) for nid, n in nodes.items() if n["parent"] == dept_id]
    for nid, n in children:
        outer_sizes.append(n["value"])
        outer_colors.append(node_colors[nid])
        outer_labels.append(n["label"])

# Draw sunburst as concentric pie charts
# Inner ring (departments)
wedges1, _ = ax2.pie(
    inner_sizes,
    radius=0.6,
    colors=inner_colors,
    wedgeprops={"width": 0.3, "edgecolor": "white", "linewidth": 2},
    startangle=90,
)

# Add department labels on inner ring
for i, wedge in enumerate(wedges1):
    angle = (wedge.theta2 + wedge.theta1) / 2
    x = 0.45 * np.cos(np.radians(angle))
    y = 0.45 * np.sin(np.radians(angle))
    color = "white" if dept_order[i] in ["eng", "ops"] else "black"
    ax2.text(x, y, dept_labels[i], ha="center", va="center", fontsize=13, fontweight="bold", color=color)

# Outer ring (sub-departments)
wedges2, _ = ax2.pie(
    outer_sizes,
    radius=0.95,
    colors=outer_colors,
    wedgeprops={"width": 0.35, "edgecolor": "white", "linewidth": 1.5},
    startangle=90,
)

# Add sub-department labels on outer ring (only for larger segments)
for i, wedge in enumerate(wedges2):
    angle_span = wedge.theta2 - wedge.theta1
    if angle_span > 15:  # Only label larger segments
        angle = (wedge.theta2 + wedge.theta1) / 2
        x = 0.77 * np.cos(np.radians(angle))
        y = 0.77 * np.sin(np.radians(angle))
        # Determine text color based on background
        bg_color = outer_colors[i]
        text_color = "white" if bg_color in ["#306998", "#2E8B57"] else "black"
        # Horizontal labels (no rotation) for better readability
        ax2.text(x, y, outer_labels[i], ha="center", va="center", fontsize=10, fontweight="bold", color=text_color)

ax2.set_title("Sunburst View", fontsize=22, fontweight="bold", pad=15)

# Main title
fig.suptitle("hierarchy-toggle-view · matplotlib · pyplots.ai", fontsize=26, fontweight="bold", y=0.98)

# Legend for departments
legend_patches = [mpatches.Patch(color=dept_colors[d], label=nodes[d]["label"]) for d in dept_order]
fig.legend(handles=legend_patches, loc="lower center", ncol=4, fontsize=14, frameon=True, bbox_to_anchor=(0.5, 0.02))

plt.tight_layout(rect=[0, 0.08, 1, 0.95])
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
