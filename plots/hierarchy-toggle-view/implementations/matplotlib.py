""" pyplots.ai
hierarchy-toggle-view: Interactive Treemap-Sunburst Toggle View
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 91/100 | Created: 2026-01-11
"""

import matplotlib.patches as mpatches
import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
import numpy as np


# Data: Company departments with sub-units (hierarchical structure)
# Format: (id, parent, label, value)
hierarchy_data = [
    ("root", None, "Company", 0),
    ("eng", "root", "Eng", 0),  # Shortened to fit inner ring
    ("sales", "root", "Sales", 0),
    ("ops", "root", "Ops", 0),  # Shortened to avoid truncation in sunburst
    ("hr", "root", "HR", 0),
    # Engineering sub-departments
    ("frontend", "eng", "Frontend", 45),
    ("backend", "eng", "Backend", 55),
    ("devops", "eng", "DevOps", 30),
    ("qa", "eng", "QA", 25),
    # Sales sub-departments
    ("domestic", "sales", "Domestic", 40),
    ("international", "sales", "Intl", 50),  # Shortened for outer ring
    ("partnerships", "sales", "Partners", 25),  # Shortened for outer ring
    # Operations sub-departments
    ("logistics", "ops", "Logist.", 35),  # Shortened for outer ring
    ("facilities", "ops", "Facil.", 20),  # Shortened for outer ring
    ("it_support", "ops", "IT", 25),  # Shortened for outer ring
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

# Create figure with gridspec for toggle control area
fig = plt.figure(figsize=(16, 9))

# Create grid: toggle control on top, two views below
gs = fig.add_gridspec(2, 2, height_ratios=[0.12, 0.88], hspace=0.1, wspace=0.1)
ax_toggle = fig.add_subplot(gs[0, :])  # Toggle control spans both columns
ax1 = fig.add_subplot(gs[1, 0])  # Treemap
ax2 = fig.add_subplot(gs[1, 1])  # Sunburst

# ============ TOGGLE CONTROL ============
ax_toggle.set_xlim(0, 1)
ax_toggle.set_ylim(0, 1)
ax_toggle.axis("off")

# Draw toggle switch shadow (drop shadow effect using multiple patches)
toggle_shadow = mpatches.FancyBboxPatch(
    (0.352, 0.22), 0.30, 0.5, boxstyle="round,pad=0.02", facecolor="#00000022", edgecolor="none"
)
ax_toggle.add_patch(toggle_shadow)

# Draw toggle switch background
toggle_bg = mpatches.FancyBboxPatch(
    (0.35, 0.25), 0.30, 0.5, boxstyle="round,pad=0.02", facecolor="#E8E8E8", edgecolor="#CCCCCC", linewidth=2
)
ax_toggle.add_patch(toggle_bg)

# Draw toggle buttons (Treemap selected with glow effect, Sunburst unselected)
# Selected button glow
btn_glow = mpatches.FancyBboxPatch(
    (0.355, 0.28), 0.14, 0.44, boxstyle="round,pad=0.01", facecolor="#30699833", edgecolor="none"
)
ax_toggle.add_patch(btn_glow)

btn_treemap = mpatches.FancyBboxPatch(
    (0.36, 0.30), 0.13, 0.40, boxstyle="round,pad=0.01", facecolor="#306998", edgecolor="#1d4a6e", linewidth=2
)
ax_toggle.add_patch(btn_treemap)
treemap_text = ax_toggle.text(
    0.425, 0.50, "Treemap", ha="center", va="center", fontsize=14, fontweight="bold", color="white"
)
treemap_text.set_path_effects([path_effects.withStroke(linewidth=2, foreground="#1d4a6e")])

btn_sunburst = mpatches.FancyBboxPatch(
    (0.51, 0.30), 0.13, 0.40, boxstyle="round,pad=0.01", facecolor="white", edgecolor="#BBBBBB", linewidth=2
)
ax_toggle.add_patch(btn_sunburst)
ax_toggle.text(0.575, 0.50, "Sunburst", ha="center", va="center", fontsize=14, fontweight="bold", color="#666666")

# Toggle label with subtle styling
toggle_label = ax_toggle.text(
    0.5, 0.90, "Toggle View:", ha="center", va="center", fontsize=16, fontweight="bold", color="#333333"
)
toggle_label.set_path_effects([path_effects.withStroke(linewidth=1, foreground="#FFFFFF")])

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
            text_color = "white" if color in ["#306998", "#2E8B57"] else "black"
            outline_color = "#00000066" if text_color == "white" else "#FFFFFF66"
            label = ax1.text(
                current_x + dept_width / 2 - 0.0025,
                current_y + item_height / 2 - 0.0025,
                f"{n['label']}\n({n['value']})",
                ha="center",
                va="center",
                fontsize=14,
                fontweight="bold",
                color=text_color,
            )
            label.set_path_effects([path_effects.withStroke(linewidth=2, foreground=outline_color)])

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

# Draw sunburst as concentric pie charts (increased radius for better canvas utilization)
# Inner ring (departments)
wedges1, _ = ax2.pie(
    inner_sizes,
    radius=0.62,
    colors=inner_colors,
    wedgeprops={"width": 0.32, "edgecolor": "white", "linewidth": 2.5},
    startangle=90,
)

# Add department labels on inner ring with path effects for better readability
for i, wedge in enumerate(wedges1):
    angle = (wedge.theta2 + wedge.theta1) / 2
    x = 0.46 * np.cos(np.radians(angle))
    y = 0.46 * np.sin(np.radians(angle))
    text_color = "white" if dept_order[i] in ["eng", "ops"] else "black"
    outline_color = "#00000088" if text_color == "white" else "#FFFFFF88"
    inner_label = ax2.text(
        x, y, dept_labels[i], ha="center", va="center", fontsize=17, fontweight="bold", color=text_color
    )
    inner_label.set_path_effects([path_effects.withStroke(linewidth=3, foreground=outline_color)])

# Outer ring (sub-departments)
wedges2, _ = ax2.pie(
    outer_sizes,
    radius=0.98,
    colors=outer_colors,
    wedgeprops={"width": 0.36, "edgecolor": "white", "linewidth": 2},
    startangle=90,
)

# Add sub-department labels on outer ring with smart positioning and path effects
for i, wedge in enumerate(wedges2):
    angle_span = wedge.theta2 - wedge.theta1
    if angle_span > 15:  # Only label larger segments to avoid overlap
        angle = (wedge.theta2 + wedge.theta1) / 2
        # Adjust radius based on segment size
        label_radius = 0.80 if angle_span > 25 else 0.78
        x = label_radius * np.cos(np.radians(angle))
        y = label_radius * np.sin(np.radians(angle))
        # Determine text color based on background
        bg_color = outer_colors[i]
        text_color = "white" if bg_color in ["#306998", "#2E8B57"] else "black"
        outline_color = "#00000066" if text_color == "white" else "#FFFFFF66"
        # Use horizontal labels for larger segments, rotated for smaller ones
        if angle_span >= 28:
            outer_label = ax2.text(
                x, y, outer_labels[i], ha="center", va="center", fontsize=12, fontweight="bold", color=text_color
            )
        else:
            # Ensure text is always readable (not upside down) with radial rotation
            if 90 < angle <= 270:
                rotation = angle + 90  # Right side up on left half
            else:
                rotation = angle - 90  # Right side up on right half
            outer_label = ax2.text(
                x,
                y,
                outer_labels[i],
                ha="center",
                va="center",
                fontsize=10,
                fontweight="bold",
                color=text_color,
                rotation=rotation,
                rotation_mode="anchor",
            )
        outer_label.set_path_effects([path_effects.withStroke(linewidth=2, foreground=outline_color)])

ax2.set_title("Sunburst View", fontsize=22, fontweight="bold", pad=15)

# Main title at the very top
fig.suptitle("hierarchy-toggle-view · matplotlib · pyplots.ai", fontsize=26, fontweight="bold", y=0.99)

# Legend for departments - use full names for legend
legend_labels = {"eng": "Engineering", "sales": "Sales", "ops": "Operations", "hr": "HR"}
legend_patches = [mpatches.Patch(color=dept_colors[d], label=legend_labels[d]) for d in dept_order]
fig.legend(handles=legend_patches, loc="lower center", ncol=4, fontsize=14, frameon=True, bbox_to_anchor=(0.5, 0.01))

plt.subplots_adjust(left=0.02, right=0.98, top=0.92, bottom=0.08)
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
