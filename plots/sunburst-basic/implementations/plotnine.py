"""
sunburst-basic: Basic Sunburst Chart
Library: plotnine

Note: plotnine (like ggplot2) does not have a native sunburst/pie geom.
This implementation uses matplotlib's Wedge patches directly to create
the sunburst visualization while following plotnine's minimal styling conventions.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Wedge


# Hierarchical data: Company budget breakdown (in thousands)
# Level 1: Departments, Level 2: Teams, Level 3: Projects
hierarchy = {
    "Engineering": {
        "Development": {"Frontend": 120, "Backend": 150, "Mobile": 80},
        "QA": {"Testing": 60, "Automation": 40},
        "DevOps": {"Infrastructure": 50, "Security": 30},
    },
    "Marketing": {"Digital": {"Social Media": 70, "SEO": 50, "Paid Ads": 90}, "Content": {"Blog": 30, "Video": 45}},
    "Sales": {"Direct": {"Enterprise": 100, "SMB": 60}, "Channel": {"Partners": 40, "Resellers": 35}},
    "Operations": {"Support": {"Customer Service": 55, "Technical": 45}, "Admin": {"Facilities": 30, "HR": 40}},
}

# Flatten hierarchy and calculate values for each level
level1_labels = []
level1_values = []
level2_labels = []
level2_values = []
level2_parents = []
level3_labels = []
level3_values = []
level3_parents = []

for dept, teams in hierarchy.items():
    dept_total = 0
    for team, projects in teams.items():
        team_total = sum(projects.values())
        dept_total += team_total
        level2_labels.append(team)
        level2_values.append(team_total)
        level2_parents.append(dept)
        for project, value in projects.items():
            level3_labels.append(project)
            level3_values.append(value)
            level3_parents.append(team)
    level1_labels.append(dept)
    level1_values.append(dept_total)

# Color palette using Python colors first, then colorblind-safe colors
dept_palette = {
    "Engineering": "#306998",  # Python Blue
    "Marketing": "#FFD43B",  # Python Yellow
    "Sales": "#4ECDC4",  # Teal
    "Operations": "#FF6B6B",  # Coral
}

# Build mapping from team to department
parent_to_dept = {team: dept for dept, teams in hierarchy.items() for team in teams}

# Create figure with plotnine-inspired minimal styling
fig, ax = plt.subplots(figsize=(16, 9))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

# Ring parameters
inner_radius = 0.25
ring_width = 0.22
gap = 0.03

# Ring 1 (innermost): Departments
level1_colors = [dept_palette[dept] for dept in level1_labels]
total1 = sum(level1_values)
angles1 = [v / total1 * 360 for v in level1_values]
ring1_info = []
start_angle = 90

for angle, label, color in zip(angles1, level1_labels, level1_colors, strict=True):
    wedge = Wedge(
        (0, 0),
        inner_radius + ring_width,
        start_angle - angle,
        start_angle,
        width=ring_width,
        facecolor=color,
        edgecolor="white",
        linewidth=2.5,
    )
    ax.add_patch(wedge)
    ring1_info.append((start_angle - angle / 2, inner_radius + ring_width / 2, label, angle))
    start_angle -= angle

# Ring 2 (middle): Teams - lighter shade of parent color
level2_colors = []
for parent in level2_parents:
    base_color = dept_palette[parent]
    rgb = plt.matplotlib.colors.to_rgb(base_color)
    level2_colors.append(tuple(min(1, c * 0.85 + 0.15) for c in rgb))

total2 = sum(level2_values)
angles2 = [v / total2 * 360 for v in level2_values]
ring2_info = []
start_angle = 90
ring2_radius = inner_radius + ring_width + gap + ring_width

for angle, label, color in zip(angles2, level2_labels, level2_colors, strict=True):
    wedge = Wedge(
        (0, 0),
        ring2_radius,
        start_angle - angle,
        start_angle,
        width=ring_width,
        facecolor=color,
        edgecolor="white",
        linewidth=2,
    )
    ax.add_patch(wedge)
    ring2_info.append((start_angle - angle / 2, ring2_radius - ring_width / 2, label, angle))
    start_angle -= angle

# Ring 3 (outermost): Projects - even lighter shade
level3_colors = []
for parent in level3_parents:
    dept = parent_to_dept[parent]
    base_color = dept_palette[dept]
    rgb = plt.matplotlib.colors.to_rgb(base_color)
    level3_colors.append(tuple(min(1, c * 0.7 + 0.3) for c in rgb))

total3 = sum(level3_values)
angles3 = [v / total3 * 360 for v in level3_values]
ring3_info = []
start_angle = 90
ring3_radius = ring2_radius + gap + ring_width

for angle, label, color in zip(angles3, level3_labels, level3_colors, strict=True):
    wedge = Wedge(
        (0, 0),
        ring3_radius,
        start_angle - angle,
        start_angle,
        width=ring_width,
        facecolor=color,
        edgecolor="white",
        linewidth=1.5,
    )
    ax.add_patch(wedge)
    ring3_info.append((start_angle - angle / 2, ring3_radius - ring_width / 2, label, angle))
    start_angle -= angle

# Add labels for level 1 (innermost ring)
for angle, r, label, _span in ring1_info:
    angle_rad = np.radians(angle)
    x = r * np.cos(angle_rad)
    y = r * np.sin(angle_rad)
    ax.text(x, y, label, ha="center", va="center", fontsize=14, fontweight="bold", color="white")

# Add labels for level 2 (middle ring) - only for larger segments
for angle, r, label, span in ring2_info:
    if span > 22:
        angle_rad = np.radians(angle)
        x = r * np.cos(angle_rad)
        y = r * np.sin(angle_rad)
        rotation = angle - 90 if -90 <= angle <= 90 else angle + 90
        ax.text(x, y, label, ha="center", va="center", fontsize=11, rotation=rotation, color="#333333")

# Add labels for level 3 (outer ring) - only for largest segments
for angle, r, label, span in ring3_info:
    if span > 18:
        angle_rad = np.radians(angle)
        x = r * np.cos(angle_rad)
        y = r * np.sin(angle_rad)
        rotation = angle - 90 if -90 <= angle <= 90 else angle + 90
        ax.text(x, y, label, ha="center", va="center", fontsize=9, rotation=rotation, color="#555555")

# Set equal aspect ratio and limits (extended xlim to prevent label clipping)
ax.set_aspect("equal")
ax.set_xlim(-1.3, 1.5)
ax.set_ylim(-1.15, 1.15)

# Remove axes (plotnine-minimal style)
ax.axis("off")

# Title with plotnine styling
ax.set_title(
    "Company Budget · sunburst-basic · plotnine · pyplots.ai",
    fontsize=24,
    fontweight="bold",
    pad=20,
    fontfamily="sans-serif",
)

# Legend for main departments
legend_handles = [
    plt.Rectangle((0, 0), 1, 1, facecolor=dept_palette[dept], edgecolor="white", linewidth=2) for dept in level1_labels
]
ax.legend(
    legend_handles,
    [f"{dept}: ${val}K" for dept, val in zip(level1_labels, level1_values, strict=True)],
    loc="center left",
    bbox_to_anchor=(1.02, 0.5),
    fontsize=14,
    title="Departments",
    title_fontsize=16,
    framealpha=0.95,
    edgecolor="#cccccc",
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
