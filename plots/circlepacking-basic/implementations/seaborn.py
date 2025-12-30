"""pyplots.ai
circlepacking-basic: Circle Packing Chart
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 72/100 | Created: 2025-12-30
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


# Set seaborn style
sns.set_theme(style="white")

np.random.seed(42)

# Build hierarchical data: root -> categories -> subcategories (sales in thousands)
# Flat data structure - no helper functions
data = [
    # Root level
    {"id": "root", "parent": None, "value": 0, "label": "", "depth": 0},
    # Category level
    {"id": "electronics", "parent": "root", "value": 0, "label": "Electronics", "depth": 1},
    {"id": "clothing", "parent": "root", "value": 0, "label": "Clothing", "depth": 1},
    {"id": "home", "parent": "root", "value": 0, "label": "Home", "depth": 1},
    {"id": "sports", "parent": "root", "value": 0, "label": "Sports", "depth": 1},
    # Subcategory level - Electronics
    {"id": "phones", "parent": "electronics", "value": 450, "label": "Phones", "depth": 2},
    {"id": "laptops", "parent": "electronics", "value": 380, "label": "Laptops", "depth": 2},
    {"id": "tablets", "parent": "electronics", "value": 220, "label": "Tablets", "depth": 2},
    # Subcategory level - Clothing
    {"id": "shirts", "parent": "clothing", "value": 320, "label": "Shirts", "depth": 2},
    {"id": "pants", "parent": "clothing", "value": 280, "label": "Pants", "depth": 2},
    {"id": "shoes", "parent": "clothing", "value": 350, "label": "Shoes", "depth": 2},
    # Subcategory level - Home
    {"id": "furniture", "parent": "home", "value": 400, "label": "Furniture", "depth": 2},
    {"id": "kitchen", "parent": "home", "value": 280, "label": "Kitchen", "depth": 2},
    # Subcategory level - Sports
    {"id": "fitness", "parent": "sports", "value": 220, "label": "Fitness", "depth": 2},
    {"id": "outdoor", "parent": "sports", "value": 180, "label": "Outdoor", "depth": 2},
]

# Calculate total values for categories (sum of their subcategories)
cat_totals = {}
for node in data:
    if node["depth"] == 2:
        parent = node["parent"]
        cat_totals[parent] = cat_totals.get(parent, 0) + node["value"]

for node in data:
    if node["depth"] == 1:
        node["value"] = cat_totals.get(node["id"], 0)

# Total for root
root_total = sum(cat_totals.values())
for node in data:
    if node["depth"] == 0:
        node["value"] = root_total

# Category positions in quadrants - spread out to minimize category overlap
cat_positions = {
    "electronics": (0.45, 0.40),
    "clothing": (-0.45, 0.40),
    "home": (-0.45, -0.42),
    "sports": (0.45, -0.42),
}

# Calculate radii proportional to value (using area scaling)
# Make category circles larger to properly contain subcategories
max_cat_value = max(cat_totals.values())
cat_radii = {}
for cat_id, total in cat_totals.items():
    cat_radii[cat_id] = 0.38 * np.sqrt(total / max_cat_value) + 0.10

# Build circle data for plotting
circles = []

# Root circle - large enough to contain all categories
circles.append({"x": 0, "y": 0, "size": 0.95, "depth": 0, "label": ""})

# Category circles
for node in data:
    if node["depth"] == 1:
        cat_id = node["id"]
        pos = cat_positions[cat_id]
        r = cat_radii[cat_id]
        circles.append({"x": pos[0], "y": pos[1], "size": r, "depth": 1, "label": node["label"]})

# Subcategory circles - positioned INSIDE their parent circles with strict containment
for node in data:
    if node["depth"] == 2:
        parent_id = node["parent"]
        parent_pos = cat_positions[parent_id]
        parent_r = cat_radii[parent_id]

        # Get siblings for positioning
        siblings = [n for n in data if n["parent"] == parent_id and n["depth"] == 2]
        idx = next(i for i, s in enumerate(siblings) if s["id"] == node["id"])
        n_siblings = len(siblings)

        # Calculate subcircle radius - much smaller relative to parent
        max_sub_value = max(s["value"] for s in siblings)
        # Make subcircles smaller - max radius is 1/4 of parent
        sub_r = parent_r * 0.22 * np.sqrt(node["value"] / max_sub_value) + 0.015

        # Position inside parent with strict containment
        angle = 2 * np.pi * idx / n_siblings + np.pi / 4
        # Distance from parent center - strictly ensure subcircle stays inside
        # Use parent_r * 0.55 as max distance, and subtract subcircle radius
        max_allowed_dist = parent_r - sub_r - 0.03  # Generous margin
        dist = min(parent_r * 0.55, max_allowed_dist)

        sub_x = parent_pos[0] + dist * np.cos(angle)
        sub_y = parent_pos[1] + dist * np.sin(angle)

        circles.append({"x": sub_x, "y": sub_y, "size": sub_r, "depth": 2, "label": node["label"]})

# Convert to DataFrame for seaborn
df = pd.DataFrame(circles)

# Map depth to hierarchy level names for hue
depth_names = {0: "Root (All Products)", 1: "Categories", 2: "Subcategories"}
df["level"] = df["depth"].map(depth_names)

# Create figure - square for circle packing
fig, ax = plt.subplots(figsize=(12, 12))

# Color palette using seaborn
palette = {"Root (All Products)": "#306998", "Categories": "#FFD43B", "Subcategories": "#4ECDC4"}

# Calculate marker sizes in points^2 that map correctly to data coordinates
# With figsize=(12,12) and xlim/ylim=[-1.15, 1.15], the data range is 2.3 units
# Figure is 12*72 = 864 points per axis (at 72 dpi for display)
# But for savefig at dpi=300, it's 12*300 = 3600 pixels
# In data coords: 1 unit = 864 points / 2.3 ≈ 375 points
# Marker area s = (diameter in points)^2
# diameter in points = radius in data * 2 * (points per data unit)
# For 300 dpi output and tight display, use actual fig transform
# Simplified: s = (radius * scale_factor)^2 where scale_factor maps data to display

# Scale factor: data coord to marker size
# Marker s parameter is in points^2 (1 point = 1/72 inch)
# At figsize 12 inches and xlim 2.3 data units: 1 data unit ≈ 12/2.3 = 5.2 inches = 375 points
# But scatter 's' is area, so we need diameter^2
# For a circle with radius r in data units, marker diameter should be 2r * 375 points
# s = (2r * 375)^2 = (750r)^2

scale = 750  # points per data unit for diameter
df["marker_size"] = (df["size"] * scale) ** 2

# Plot each level separately to control z-order (largest first)
for depth in [0, 1, 2]:
    level_df = df[df["depth"] == depth]
    sns.scatterplot(
        data=level_df,
        x="x",
        y="y",
        size="marker_size",
        sizes=(level_df["marker_size"].min(), level_df["marker_size"].max()),
        hue="level",
        palette=palette,
        alpha=0.9,
        edgecolor="white",
        linewidth=3 if depth < 2 else 2,
        legend=False,
        ax=ax,
    )

# Add labels for subcategories
for _, row in df[df["depth"] == 2].iterrows():
    fontsize = max(10, min(14, int(row["size"] * 80)))
    ax.text(
        row["x"],
        row["y"],
        row["label"],
        ha="center",
        va="center",
        fontsize=fontsize,
        fontweight="bold",
        color="#1a1a1a",
    )

# Add labels for categories with background box - positioned below center to avoid subcircle overlap
for _, row in df[df["depth"] == 1].iterrows():
    # Position label toward the outside of the root circle
    label_offset_y = -0.18 if row["y"] > 0 else 0.18
    ax.text(
        row["x"],
        row["y"] + label_offset_y,
        row["label"],
        ha="center",
        va="center",
        fontsize=16,
        fontweight="bold",
        color="#333333",
        bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )

# Style
ax.set_xlim(-1.15, 1.15)
ax.set_ylim(-1.15, 1.15)
ax.set_aspect("equal")
ax.axis("off")

# Title
ax.set_title("circlepacking-basic · seaborn · pyplots.ai", fontsize=28, fontweight="bold", pad=25, color="#333333")

# Add legend for hierarchy levels
legend_elements = [
    mpatches.Patch(facecolor="#306998", edgecolor="white", label="Root (All Products)"),
    mpatches.Patch(facecolor="#FFD43B", edgecolor="white", label="Categories"),
    mpatches.Patch(facecolor="#4ECDC4", edgecolor="white", label="Subcategories"),
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
