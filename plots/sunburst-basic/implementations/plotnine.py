"""
sunburst-basic: Basic Sunburst Chart
Library: plotnine

Note: plotnine doesn't support coord_polar for sunburst charts.
Using matplotlib directly with plotnine-style aesthetics.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Wedge


# Data - Organizational budget hierarchy (3 levels)
data = pd.DataFrame(
    {
        "level_1": [
            "Engineering",
            "Engineering",
            "Engineering",
            "Engineering",
            "Engineering",
            "Marketing",
            "Marketing",
            "Marketing",
            "Sales",
            "Sales",
            "Sales",
            "Sales",
            "Operations",
            "Operations",
            "Operations",
        ],
        "level_2": [
            "Product",
            "Product",
            "Infrastructure",
            "Infrastructure",
            "QA",
            "Digital",
            "Digital",
            "Events",
            "Direct",
            "Direct",
            "Channel",
            "Support",
            "Logistics",
            "Logistics",
            "Facilities",
        ],
        "level_3": [
            "Frontend",
            "Backend",
            "Cloud",
            "Security",
            "Testing",
            "Social",
            "SEO",
            "Conferences",
            "Enterprise",
            "SMB",
            "Partners",
            "Customer Success",
            "Shipping",
            "Warehouse",
            "Maintenance",
        ],
        "value": [180, 220, 150, 100, 80, 120, 80, 60, 200, 150, 120, 80, 90, 70, 50],
    }
)

# Aggregate values for level_1 and level_2
level1_agg = data.groupby("level_1")["value"].sum().reset_index()
level2_agg = data.groupby(["level_1", "level_2"])["value"].sum().reset_index()

# Sort consistently to maintain hierarchy alignment
level1_agg = level1_agg.sort_values("level_1").reset_index(drop=True)
level1_order = level1_agg["level_1"].tolist()

# Color palette - base colors for level 1 categories
base_colors = {"Engineering": "#306998", "Marketing": "#FFD43B", "Sales": "#4ECDC4", "Operations": "#E76F51"}


def lighten_color(hex_color, factor=0.3):
    """Lighten a hex color by a factor."""
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    return f"#{r:02x}{g:02x}{b:02x}"


# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Ring radii (inner radius, outer radius for each level)
inner_ring = (0.3, 0.5)  # Level 1 (innermost)
middle_ring = (0.55, 0.75)  # Level 2
outer_ring = (0.8, 1.0)  # Level 3 (outermost)

total = data["value"].sum()

# Calculate angles for each level
# Level 1 - inner ring
level1_angles = []
start_angle = 90  # Start from top
for _, row in level1_agg.iterrows():
    extent = 360 * row["value"] / total
    level1_angles.append({"label": row["level_1"], "start": start_angle, "extent": extent})
    start_angle += extent

# Draw Level 1 (inner ring)
for angle_info in level1_angles:
    label = angle_info["label"]
    color = base_colors[label]
    wedge = Wedge(
        center=(0, 0),
        r=inner_ring[1],
        theta1=angle_info["start"],
        theta2=angle_info["start"] + angle_info["extent"],
        width=inner_ring[1] - inner_ring[0],
        facecolor=color,
        edgecolor="white",
        linewidth=2,
    )
    ax.add_patch(wedge)

    # Add label in center of wedge
    mid_angle = np.radians(angle_info["start"] + angle_info["extent"] / 2)
    mid_radius = (inner_ring[0] + inner_ring[1]) / 2
    x = mid_radius * np.cos(mid_angle)
    y = mid_radius * np.sin(mid_angle)
    if angle_info["extent"] > 30:  # Only label if segment is large enough
        ax.text(x, y, label, ha="center", va="center", fontsize=12, fontweight="bold", color="white", rotation=0)

# Level 2 - middle ring
level2_angles = []
start_angle = 90
for l1 in level1_order:
    l1_data = level2_agg[level2_agg["level_1"] == l1].sort_values("level_2")
    for _, row in l1_data.iterrows():
        extent = 360 * row["value"] / total
        level2_angles.append(
            {"label": row["level_2"], "level_1": row["level_1"], "start": start_angle, "extent": extent}
        )
        start_angle += extent

# Draw Level 2 (middle ring)
for angle_info in level2_angles:
    label = angle_info["label"]
    parent = angle_info["level_1"]
    color = lighten_color(base_colors[parent], 0.25)
    wedge = Wedge(
        center=(0, 0),
        r=middle_ring[1],
        theta1=angle_info["start"],
        theta2=angle_info["start"] + angle_info["extent"],
        width=middle_ring[1] - middle_ring[0],
        facecolor=color,
        edgecolor="white",
        linewidth=1.5,
    )
    ax.add_patch(wedge)

    # Add label
    mid_angle = np.radians(angle_info["start"] + angle_info["extent"] / 2)
    mid_radius = (middle_ring[0] + middle_ring[1]) / 2
    x = mid_radius * np.cos(mid_angle)
    y = mid_radius * np.sin(mid_angle)
    if angle_info["extent"] > 15:
        ax.text(x, y, label, ha="center", va="center", fontsize=10, fontweight="bold", color="#333333")

# Level 3 - outer ring
level3_angles = []
start_angle = 90
for l1 in level1_order:
    l2_in_l1 = level2_agg[level2_agg["level_1"] == l1]["level_2"].tolist()
    l2_in_l1.sort()
    for l2 in l2_in_l1:
        l3_data = data[(data["level_1"] == l1) & (data["level_2"] == l2)]
        for _, row in l3_data.iterrows():
            extent = 360 * row["value"] / total
            level3_angles.append(
                {
                    "label": row["level_3"],
                    "level_1": row["level_1"],
                    "level_2": row["level_2"],
                    "start": start_angle,
                    "extent": extent,
                    "value": row["value"],
                }
            )
            start_angle += extent

# Draw Level 3 (outer ring)
for angle_info in level3_angles:
    label = angle_info["label"]
    parent = angle_info["level_1"]
    color = lighten_color(base_colors[parent], 0.5)
    wedge = Wedge(
        center=(0, 0),
        r=outer_ring[1],
        theta1=angle_info["start"],
        theta2=angle_info["start"] + angle_info["extent"],
        width=outer_ring[1] - outer_ring[0],
        facecolor=color,
        edgecolor="white",
        linewidth=1,
    )
    ax.add_patch(wedge)

    # Add label for larger segments
    mid_angle = np.radians(angle_info["start"] + angle_info["extent"] / 2)
    mid_radius = (outer_ring[0] + outer_ring[1]) / 2
    x = mid_radius * np.cos(mid_angle)
    y = mid_radius * np.sin(mid_angle)
    if angle_info["extent"] > 10:
        # Rotate text for readability
        rotation = angle_info["start"] + angle_info["extent"] / 2 - 90
        if 90 < (angle_info["start"] + angle_info["extent"] / 2) % 360 < 270:
            rotation += 180
        ax.text(x, y, label, ha="center", va="center", fontsize=9, color="#333333", rotation=rotation)

# Add center circle (white) for visual appeal
center_circle = plt.Circle((0, 0), inner_ring[0], fc="white", ec="white")
ax.add_patch(center_circle)

# Add legend
legend_elements = [plt.Rectangle((0, 0), 1, 1, facecolor=color, edgecolor="white") for color in base_colors.values()]
ax.legend(
    legend_elements,
    base_colors.keys(),
    loc="center left",
    bbox_to_anchor=(1.02, 0.5),
    fontsize=16,
    title="Department",
    title_fontsize=18,
    frameon=False,
)

# Styling
ax.set_xlim(-1.3, 1.6)
ax.set_ylim(-1.2, 1.2)
ax.set_aspect("equal")
ax.axis("off")

# Title in pyplots format
ax.set_title(
    "Budget Hierarchy \u00b7 sunburst-basic \u00b7 plotnine \u00b7 pyplots.ai", fontsize=26, fontweight="bold", pad=25
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight", facecolor="white")
