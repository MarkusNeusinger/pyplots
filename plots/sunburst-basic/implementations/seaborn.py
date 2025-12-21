""" pyplots.ai
sunburst-basic: Basic Sunburst Chart
Library: seaborn 0.13.2 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-14
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.patches import Wedge


# Set seaborn style for clean aesthetics
sns.set_style("whitegrid")

# Hierarchical data - Company budget breakdown
# Level 1: Main departments
# Level 2: Sub-departments/teams
# Level 3: Projects/activities
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

# Create color palette for each main department (level 1)
dept_palette = {
    "Engineering": "#306998",  # Python Blue
    "Marketing": "#FFD43B",  # Python Yellow
    "Sales": "#4ECDC4",  # Teal
    "Operations": "#FF6B6B",  # Coral
}

# Build mapping from team to department
parent_to_dept = {team: dept for dept, teams in hierarchy.items() for team in teams}

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Ring 1 (innermost): Departments - radius 0.4, width 0.25
level1_colors = [dept_palette[dept] for dept in level1_labels]
total1 = sum(level1_values)
angles1 = [v / total1 * 360 for v in level1_values]
ring1_info = []
start_angle = 90

for angle, label, color in zip(angles1, level1_labels, level1_colors, strict=True):
    wedge = Wedge(
        (0, 0), 0.4, start_angle - angle, start_angle, width=0.25, facecolor=color, edgecolor="white", linewidth=2
    )
    ax.add_patch(wedge)
    ring1_info.append((start_angle - angle / 2, 0.4 - 0.125, label, angle))
    start_angle -= angle

# Ring 2 (middle): Teams - radius 0.7, width 0.25
level2_colors = []
for parent in level2_parents:
    base_color = dept_palette[parent]
    rgb = plt.matplotlib.colors.to_rgb(base_color)
    level2_colors.append(tuple(min(1, c * 1.2) for c in rgb))

total2 = sum(level2_values)
angles2 = [v / total2 * 360 for v in level2_values]
ring2_info = []
start_angle = 90

for angle, label, color in zip(angles2, level2_labels, level2_colors, strict=True):
    wedge = Wedge(
        (0, 0), 0.7, start_angle - angle, start_angle, width=0.25, facecolor=color, edgecolor="white", linewidth=2
    )
    ax.add_patch(wedge)
    ring2_info.append((start_angle - angle / 2, 0.7 - 0.125, label, angle))
    start_angle -= angle

# Ring 3 (outermost): Projects - radius 1.0, width 0.25
level3_colors = []
for parent in level3_parents:
    dept = parent_to_dept[parent]
    base_color = dept_palette[dept]
    rgb = plt.matplotlib.colors.to_rgb(base_color)
    level3_colors.append(tuple(min(1, c * 1.4) for c in rgb))

total3 = sum(level3_values)
angles3 = [v / total3 * 360 for v in level3_values]
ring3_info = []
start_angle = 90

for angle, label, color in zip(angles3, level3_labels, level3_colors, strict=True):
    wedge = Wedge(
        (0, 0), 1.0, start_angle - angle, start_angle, width=0.25, facecolor=color, edgecolor="white", linewidth=2
    )
    ax.add_patch(wedge)
    ring3_info.append((start_angle - angle / 2, 1.0 - 0.125, label, angle))
    start_angle -= angle

# Add labels for level 1 (innermost ring) - all labeled
for angle, r, label, _span in ring1_info:
    angle_rad = np.radians(angle)
    x = r * np.cos(angle_rad) * 0.85
    y = r * np.sin(angle_rad) * 0.85
    ax.text(x, y, label, ha="center", va="center", fontsize=14, fontweight="bold", color="white")

# Add labels for level 2 (middle ring) - only for larger segments
for angle, r, label, span in ring2_info:
    if span > 20:  # Only label segments > 20 degrees
        angle_rad = np.radians(angle)
        x = (r + 0.12) * np.cos(angle_rad)
        y = (r + 0.12) * np.sin(angle_rad)
        rotation = angle - 90 if -90 <= angle <= 90 else angle + 90
        ax.text(x, y, label, ha="center", va="center", fontsize=11, rotation=rotation, color="#333333")

# Add labels for level 3 (outer ring) - only for largest segments
for angle, r, label, span in ring3_info:
    if span > 15:  # Only label segments > 15 degrees
        angle_rad = np.radians(angle)
        x = (r + 0.12) * np.cos(angle_rad)
        y = (r + 0.12) * np.sin(angle_rad)
        rotation = angle - 90 if -90 <= angle <= 90 else angle + 90
        ax.text(x, y, label, ha="center", va="center", fontsize=9, rotation=rotation, color="#555555")

# Set equal aspect ratio and limits
ax.set_aspect("equal")
ax.set_xlim(-1.4, 1.4)
ax.set_ylim(-1.2, 1.2)

# Remove axes
ax.axis("off")

# Title
ax.set_title("Company Budget · sunburst-basic · seaborn · pyplots.ai", fontsize=24, fontweight="bold", pad=20)

# Legend for main departments
legend_handles = [
    plt.Rectangle((0, 0), 1, 1, facecolor=dept_palette[dept], edgecolor="white", linewidth=2) for dept in level1_labels
]
ax.legend(
    legend_handles,
    [f"{dept}: ${val}K" for dept, val in zip(level1_labels, level1_values, strict=True)],
    loc="center left",
    bbox_to_anchor=(1.05, 0.5),
    fontsize=14,
    title="Departments",
    title_fontsize=16,
    framealpha=0.9,
)

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
