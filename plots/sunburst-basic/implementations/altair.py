""" pyplots.ai
sunburst-basic: Basic Sunburst Chart
Library: altair 6.0.0 | Python 3.13.11
Quality: 90/100 | Created: 2025-12-14
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Company budget breakdown by department, team, and project
# Hierarchical structure: Department > Team > Project
data = [
    # Engineering Department
    {"level_1": "Engineering", "level_2": "Backend", "level_3": "API", "value": 180},
    {"level_1": "Engineering", "level_2": "Backend", "level_3": "Database", "value": 120},
    {"level_1": "Engineering", "level_2": "Frontend", "level_3": "Web App", "value": 150},
    {"level_1": "Engineering", "level_2": "Frontend", "level_3": "Mobile", "value": 100},
    {"level_1": "Engineering", "level_2": "DevOps", "level_3": "Cloud", "value": 90},
    {"level_1": "Engineering", "level_2": "DevOps", "level_3": "CI/CD", "value": 60},
    # Marketing Department
    {"level_1": "Marketing", "level_2": "Digital", "level_3": "SEO", "value": 80},
    {"level_1": "Marketing", "level_2": "Digital", "level_3": "Social", "value": 70},
    {"level_1": "Marketing", "level_2": "Content", "level_3": "Blog", "value": 50},
    {"level_1": "Marketing", "level_2": "Content", "level_3": "Video", "value": 60},
    # Operations Department
    {"level_1": "Operations", "level_2": "Support", "level_3": "Tier 1", "value": 70},
    {"level_1": "Operations", "level_2": "Support", "level_3": "Tier 2", "value": 50},
    {"level_1": "Operations", "level_2": "HR", "level_3": "Recruiting", "value": 60},
    {"level_1": "Operations", "level_2": "HR", "level_3": "Training", "value": 40},
    # Sales Department
    {"level_1": "Sales", "level_2": "Enterprise", "level_3": "APAC", "value": 100},
    {"level_1": "Sales", "level_2": "Enterprise", "level_3": "EMEA", "value": 85},
    {"level_1": "Sales", "level_2": "SMB", "level_3": "Direct", "value": 65},
    {"level_1": "Sales", "level_2": "SMB", "level_3": "Partners", "value": 45},
]

df = pd.DataFrame(data)

# Calculate totals for each level
total_value = df["value"].sum()

# Level 1 (innermost ring): Department totals
level1_totals = df.groupby("level_1")["value"].sum().reset_index()
level1_totals.columns = ["name", "value"]
level1_totals["level"] = 1
level1_totals = level1_totals.sort_values("value", ascending=False).reset_index(drop=True)

# Level 2 (middle ring): Team totals
level2_totals = df.groupby(["level_1", "level_2"])["value"].sum().reset_index()
level2_totals.columns = ["parent", "name", "value"]
level2_totals["level"] = 2

# Level 3 (outer ring): Project values
level3_totals = df.copy()
level3_totals["parent_l1"] = level3_totals["level_1"]
level3_totals["parent_l2"] = level3_totals["level_2"]
level3_totals["name"] = level3_totals["level_3"]
level3_totals["level"] = 3

# Color palette - use Python Blue as primary, with related colors for sub-categories
level1_colors = {"Engineering": "#306998", "Marketing": "#FFD43B", "Operations": "#4ECDC4", "Sales": "#FF6B6B"}


# Generate lighter shades for level 2 and 3
def lighten_color(hex_color, factor=0.3):
    """Lighten a hex color by mixing with white."""
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    return f"#{r:02x}{g:02x}{b:02x}"


# Calculate angular positions for each segment
# Angles in Altair arc mark are in radians, starting from 12 o'clock going clockwise


def calculate_angles(df_level, parent_angles=None, parent_col=None):
    """Calculate start and end angles for each segment."""
    if parent_angles is None:
        # Root level - distribute across full circle
        total = df_level["value"].sum()
        angles = []
        current_angle = 0
        for _, row in df_level.iterrows():
            fraction = row["value"] / total
            start = current_angle
            end = current_angle + fraction * 2 * np.pi
            angles.append({"start": start, "end": end})
            current_angle = end
        return angles
    else:
        # Child level - distribute within parent's angular range
        angles = []
        for _, row in df_level.iterrows():
            parent_name = row[parent_col]
            parent_data = parent_angles[parent_name]
            parent_start = parent_data["start"]
            parent_end = parent_data["end"]
            parent_total = parent_data["total"]

            # Calculate this segment's fraction of parent
            fraction = row["value"] / parent_total
            segment_angle = (parent_end - parent_start) * fraction

            # Find cumulative angle within parent
            cumulative = parent_data.get("cumulative", parent_start)
            start = cumulative
            end = cumulative + segment_angle

            parent_data["cumulative"] = end
            angles.append({"start": start, "end": end})
        return angles


# Build level 1 angles
level1_angles = calculate_angles(level1_totals)
level1_totals["theta"] = [a["start"] for a in level1_angles]
level1_totals["theta2"] = [a["end"] for a in level1_angles]

# Create parent angle lookup for level 2
parent_angles_l1 = {}
for _, row in level1_totals.iterrows():
    parent_angles_l1[row["name"]] = {
        "start": row["theta"],
        "end": row["theta2"],
        "total": row["value"],
        "cumulative": row["theta"],
    }

# Sort level2 by parent then by value for consistent ordering
level2_totals = level2_totals.sort_values(["parent", "value"], ascending=[True, False]).reset_index(drop=True)

# Build level 2 angles
level2_angles_list = []
for _, row in level2_totals.iterrows():
    parent_name = row["parent"]
    parent_data = parent_angles_l1[parent_name]
    parent_start = parent_data["start"]
    parent_end = parent_data["end"]
    parent_total = parent_data["total"]

    fraction = row["value"] / parent_total
    segment_angle = (parent_end - parent_start) * fraction
    cumulative = parent_data.get("cumulative", parent_start)

    level2_angles_list.append({"start": cumulative, "end": cumulative + segment_angle})
    parent_data["cumulative"] = cumulative + segment_angle

level2_totals["theta"] = [a["start"] for a in level2_angles_list]
level2_totals["theta2"] = [a["end"] for a in level2_angles_list]

# Create parent angle lookup for level 3
parent_angles_l2 = {}
for _, row in level2_totals.iterrows():
    key = f"{row['parent']}|{row['name']}"
    parent_angles_l2[key] = {
        "start": row["theta"],
        "end": row["theta2"],
        "total": row["value"],
        "cumulative": row["theta"],
    }

# Sort level3 for consistent ordering
level3_totals = level3_totals.sort_values(["level_1", "level_2", "value"], ascending=[True, True, False]).reset_index(
    drop=True
)

# Build level 3 angles
level3_angles_list = []
for _, row in level3_totals.iterrows():
    key = f"{row['level_1']}|{row['level_2']}"
    parent_data = parent_angles_l2[key]
    parent_start = parent_data["start"]
    parent_end = parent_data["end"]
    parent_total = parent_data["total"]

    fraction = row["value"] / parent_total
    segment_angle = (parent_end - parent_start) * fraction
    cumulative = parent_data.get("cumulative", parent_start)

    level3_angles_list.append({"start": cumulative, "end": cumulative + segment_angle})
    parent_data["cumulative"] = cumulative + segment_angle

level3_totals["theta"] = [a["start"] for a in level3_angles_list]
level3_totals["theta2"] = [a["end"] for a in level3_angles_list]

# Assign colors based on parent
level1_totals["color"] = level1_totals["name"].map(level1_colors)
level2_totals["color"] = level2_totals["parent"].map(level1_colors).apply(lambda c: lighten_color(c, 0.25))
level3_totals["color"] = level3_totals["level_1"].map(level1_colors).apply(lambda c: lighten_color(c, 0.5))

# Ring radii
inner_r1, outer_r1 = 80, 160  # Level 1 (innermost)
inner_r2, outer_r2 = 165, 245  # Level 2 (middle)
inner_r3, outer_r3 = 250, 330  # Level 3 (outermost)

# Create arc charts for each level
# Level 1 - innermost ring (Departments)
chart_l1 = (
    alt.Chart(level1_totals)
    .mark_arc(innerRadius=inner_r1, outerRadius=outer_r1, stroke="#ffffff", strokeWidth=2)
    .encode(
        theta=alt.Theta("theta:Q", scale=alt.Scale(domain=[0, 2 * np.pi])),
        theta2="theta2:Q",
        color=alt.Color("color:N", scale=None, legend=None),
        tooltip=[alt.Tooltip("name:N", title="Department"), alt.Tooltip("value:Q", title="Budget ($K)")],
    )
)

# Level 2 - middle ring (Teams)
chart_l2 = (
    alt.Chart(level2_totals)
    .mark_arc(innerRadius=inner_r2, outerRadius=outer_r2, stroke="#ffffff", strokeWidth=1.5)
    .encode(
        theta=alt.Theta("theta:Q", scale=alt.Scale(domain=[0, 2 * np.pi])),
        theta2="theta2:Q",
        color=alt.Color("color:N", scale=None, legend=None),
        tooltip=[
            alt.Tooltip("parent:N", title="Department"),
            alt.Tooltip("name:N", title="Team"),
            alt.Tooltip("value:Q", title="Budget ($K)"),
        ],
    )
)

# Level 3 - outer ring (Projects)
chart_l3 = (
    alt.Chart(level3_totals)
    .mark_arc(innerRadius=inner_r3, outerRadius=outer_r3, stroke="#ffffff", strokeWidth=1)
    .encode(
        theta=alt.Theta("theta:Q", scale=alt.Scale(domain=[0, 2 * np.pi])),
        theta2="theta2:Q",
        color=alt.Color("color:N", scale=None, legend=None),
        tooltip=[
            alt.Tooltip("level_1:N", title="Department"),
            alt.Tooltip("level_2:N", title="Team"),
            alt.Tooltip("name:N", title="Project"),
            alt.Tooltip("value:Q", title="Budget ($K)"),
        ],
    )
)

# Add labels for level 1 segments (department names)
# Calculate label positions at middle of each arc segment
level1_totals["label_angle"] = (level1_totals["theta"] + level1_totals["theta2"]) / 2
level1_totals["label_radius"] = (inner_r1 + outer_r1) / 2
level1_totals["label_x"] = level1_totals["label_radius"] * np.sin(level1_totals["label_angle"])
level1_totals["label_y"] = -level1_totals["label_radius"] * np.cos(level1_totals["label_angle"])

text_l1 = (
    alt.Chart(level1_totals)
    .mark_text(fontSize=16, fontWeight="bold", color="#ffffff")
    .encode(
        x=alt.X("label_x:Q", scale=alt.Scale(domain=[-400, 400]), axis=None),
        y=alt.Y("label_y:Q", scale=alt.Scale(domain=[-400, 400]), axis=None),
        text="name:N",
    )
)

# Create a custom legend
legend_data = pd.DataFrame(
    [
        {"label": "Engineering", "color": level1_colors["Engineering"], "order": 1},
        {"label": "Marketing", "color": level1_colors["Marketing"], "order": 2},
        {"label": "Operations", "color": level1_colors["Operations"], "order": 3},
        {"label": "Sales", "color": level1_colors["Sales"], "order": 4},
    ]
)

# Combine all layers
chart = (
    alt.layer(chart_l1, chart_l2, chart_l3, text_l1)
    .properties(
        width=800,
        height=800,
        title=alt.Title(text="sunburst-basic · altair · pyplots.ai", fontSize=28, anchor="middle"),
    )
    .configure_view(strokeWidth=0)
)

# Save outputs
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
