""" pyplots.ai
circlepacking-basic: Circle Packing Chart
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 72/100 | Created: 2025-12-30
"""

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Set seaborn style
sns.set_theme(style="white")

# Data - Hierarchical structure for product categories (sales in thousands)
np.random.seed(42)

# Build hierarchical data: root -> categories -> subcategories
hierarchy = {
    "root": {"parent": None, "value": 0, "label": "", "depth": 0},
    "electronics": {"parent": "root", "value": 0, "label": "Electronics", "depth": 1},
    "clothing": {"parent": "root", "value": 0, "label": "Clothing", "depth": 1},
    "home": {"parent": "root", "value": 0, "label": "Home", "depth": 1},
    "sports": {"parent": "root", "value": 0, "label": "Sports", "depth": 1},
    # Electronics subcategories
    "phones": {"parent": "electronics", "value": 450, "label": "Phones", "depth": 2},
    "laptops": {"parent": "electronics", "value": 380, "label": "Laptops", "depth": 2},
    "tablets": {"parent": "electronics", "value": 220, "label": "Tablets", "depth": 2},
    # Clothing subcategories
    "shirts": {"parent": "clothing", "value": 320, "label": "Shirts", "depth": 2},
    "pants": {"parent": "clothing", "value": 280, "label": "Pants", "depth": 2},
    "shoes": {"parent": "clothing", "value": 350, "label": "Shoes", "depth": 2},
    # Home subcategories
    "furniture": {"parent": "home", "value": 400, "label": "Furniture", "depth": 2},
    "kitchen": {"parent": "home", "value": 280, "label": "Kitchen", "depth": 2},
    # Sports subcategories
    "fitness": {"parent": "sports", "value": 220, "label": "Fitness", "depth": 2},
    "outdoor": {"parent": "sports", "value": 180, "label": "Outdoor", "depth": 2},
}


def get_children(node_id, hierarchy):
    """Get all children of a node."""
    return [k for k, v in hierarchy.items() if v["parent"] == node_id]


def calculate_total_value(node_id, hierarchy):
    """Calculate total value including all descendants."""
    children = get_children(node_id, hierarchy)
    if not children:
        return hierarchy[node_id]["value"]
    return sum(calculate_total_value(c, hierarchy) for c in children)


# Color palette using seaborn
colors = sns.color_palette(["#306998", "#FFD43B", "#4ECDC4"], n_colors=3)

# Create figure
fig, ax = plt.subplots(figsize=(12, 12))

# Define positions for categories in a circular arrangement
categories = get_children("root", hierarchy)
cat_values = [calculate_total_value(c, hierarchy) for c in categories]

# Position categories in quadrants with appropriate spacing
cat_positions = {
    "electronics": (0.35, 0.35),
    "clothing": (-0.35, 0.35),
    "home": (-0.35, -0.35),
    "sports": (0.35, -0.35),
}

# Calculate radius scaling based on value
max_cat_value = max(cat_values)
cat_radii = {}
for cat_id in categories:
    val = calculate_total_value(cat_id, hierarchy)
    cat_radii[cat_id] = 0.32 * np.sqrt(val / max_cat_value) + 0.08

# Draw root circle (background)
root_circle = patches.Circle((0, 0), 0.95, facecolor=colors[0], edgecolor="white", linewidth=4, alpha=0.9)
ax.add_patch(root_circle)

# Draw category and subcategory circles
all_circles = []

for cat_id in categories:
    pos = cat_positions[cat_id]
    r = cat_radii[cat_id]

    # Draw category circle
    cat_circle = patches.Circle(pos, r, facecolor=colors[1], edgecolor="white", linewidth=3, alpha=0.95)
    ax.add_patch(cat_circle)
    all_circles.append({"pos": pos, "r": r, "label": hierarchy[cat_id]["label"], "depth": 1})

    # Get subcategories
    subcats = get_children(cat_id, hierarchy)
    if subcats:
        sub_values = [hierarchy[s]["value"] for s in subcats]
        max_sub_val = max(sub_values)
        n_subs = len(subcats)

        # Position subcategories within parent
        for i, sub_id in enumerate(subcats):
            sub_val = hierarchy[sub_id]["value"]
            sub_r = r * 0.35 * np.sqrt(sub_val / max_sub_val) + 0.03

            # Arrange in a circle within the parent
            angle = 2 * np.pi * i / n_subs + np.pi / 4
            dist = r * 0.5
            sub_x = pos[0] + dist * np.cos(angle)
            sub_y = pos[1] + dist * np.sin(angle)

            # Draw subcategory circle
            sub_circle = patches.Circle(
                (sub_x, sub_y), sub_r, facecolor=colors[2], edgecolor="white", linewidth=2, alpha=0.95
            )
            ax.add_patch(sub_circle)
            all_circles.append({"pos": (sub_x, sub_y), "r": sub_r, "label": hierarchy[sub_id]["label"], "depth": 2})

# Add subcategory labels first (depth 2)
for circle in all_circles:
    if circle["depth"] == 2:
        fontsize = max(10, min(14, int(circle["r"] * 100)))
        ax.text(
            circle["pos"][0],
            circle["pos"][1],
            circle["label"],
            ha="center",
            va="center",
            fontsize=fontsize,
            fontweight="bold",
            color="#1a1a1a",
        )

# Add category labels (depth 1) - placed at center of category circle
for circle in all_circles:
    if circle["depth"] == 1:
        ax.text(
            circle["pos"][0],
            circle["pos"][1],
            circle["label"],
            ha="center",
            va="center",
            fontsize=14,
            fontweight="bold",
            color="#333333",
            bbox={"boxstyle": "round,pad=0.2", "facecolor": "white", "edgecolor": "none", "alpha": 0.8},
        )

# Style
ax.set_xlim(-1.15, 1.15)
ax.set_ylim(-1.15, 1.15)
ax.set_aspect("equal")
ax.axis("off")

# Title
ax.set_title("circlepacking-basic · seaborn · pyplots.ai", fontsize=28, fontweight="bold", pad=25, color="#333333")

# Add legend for depth levels
legend_elements = [
    patches.Patch(facecolor=colors[0], edgecolor="white", label="Root (All Products)"),
    patches.Patch(facecolor=colors[1], edgecolor="white", label="Categories"),
    patches.Patch(facecolor=colors[2], edgecolor="white", label="Subcategories"),
]
ax.legend(
    handles=legend_elements,
    loc="upper right",
    fontsize=14,
    framealpha=0.95,
    title="Hierarchy Level",
    title_fontsize=16,
    bbox_to_anchor=(1.0, 0.98),
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
