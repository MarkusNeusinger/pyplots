""" pyplots.ai
circlepacking-basic: Circle Packing Chart
Library: altair 6.0.0 | Python 3.13.11
Quality: 55/100 | Created: 2025-12-30
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Company budget allocation by department and team (values in $K)
np.random.seed(42)

# Leaf nodes (teams) with their budgets
teams = [
    # Engineering Department
    {"id": "eng-backend", "parent": "Engineering", "label": "Backend", "value": 180},
    {"id": "eng-frontend", "parent": "Engineering", "label": "Frontend", "value": 150},
    {"id": "eng-devops", "parent": "Engineering", "label": "DevOps", "value": 90},
    {"id": "eng-mobile", "parent": "Engineering", "label": "Mobile", "value": 120},
    # Marketing Department
    {"id": "mkt-digital", "parent": "Marketing", "label": "Digital", "value": 100},
    {"id": "mkt-content", "parent": "Marketing", "label": "Content", "value": 80},
    {"id": "mkt-brand", "parent": "Marketing", "label": "Brand", "value": 60},
    # Operations Department
    {"id": "ops-support", "parent": "Operations", "label": "Support", "value": 70},
    {"id": "ops-hr", "parent": "Operations", "label": "HR", "value": 50},
    {"id": "ops-admin", "parent": "Operations", "label": "Admin", "value": 40},
    # Sales Department
    {"id": "sales-enterprise", "parent": "Sales", "label": "Enterprise", "value": 130},
    {"id": "sales-smb", "parent": "Sales", "label": "SMB", "value": 85},
    {"id": "sales-partners", "parent": "Sales", "label": "Partners", "value": 55},
]

# Calculate department totals
dept_totals = {}
for t in teams:
    dept_totals[t["parent"]] = dept_totals.get(t["parent"], 0) + t["value"]

# Department positions in a 2x2 grid (well-separated to avoid overlap)
dept_positions = {
    "Engineering": (-200, 150),  # Top-left (largest)
    "Sales": (200, 150),  # Top-right
    "Marketing": (-180, -180),  # Bottom-left
    "Operations": (180, -180),  # Bottom-right (smallest)
}

# Color palette - different color for each department (colorblind-safe)
dept_colors = {
    "Engineering": "#306998",  # Blue
    "Sales": "#2ca02c",  # Green
    "Marketing": "#9467bd",  # Purple
    "Operations": "#ff7f0e",  # Orange
}

# Scale value to radius (sqrt for area-proportional sizing)
max_value = max(t["value"] for t in teams)
min_radius = 30
max_radius = 70


# Pack children within a department using simple circular arrangement
# This keeps all children inside the parent circle without overlap
circles_data = []
root_radius = 500  # Outer company circle

# Add root circle (Company)
company_total = sum(t["value"] for t in teams)
circles_data.append(
    {
        "x": 0,
        "y": 0,
        "radius": root_radius,
        "label": "Company",
        "value": company_total,
        "depth": 0,
        "color": "#1a3d5c",
        "department": "Company",
    }
)

# Process each department
for dept, (dept_x, dept_y) in dept_positions.items():
    dept_teams = [t for t in teams if t["parent"] == dept]
    dept_value = dept_totals[dept]

    # Calculate team radii
    team_radii = []
    for t in dept_teams:
        r = min_radius + (max_radius - min_radius) * np.sqrt(t["value"] / max_value)
        team_radii.append(r)

    # Calculate department radius to contain all teams
    # Use a simple arrangement: place teams in a circle around department center
    n_teams = len(dept_teams)

    if n_teams == 1:
        # Single team - place at center
        positions = [(0, 0)]
        inner_radius = team_radii[0]
    else:
        # Multiple teams - arrange in a circle
        # Calculate the radius of the arrangement circle
        max_team_r = max(team_radii)
        sum_diameters = sum(2 * r for r in team_radii)
        # Circumference should fit all teams with gaps
        arrangement_radius = max(sum_diameters / (2 * np.pi) + max_team_r * 0.3, max_team_r * 1.5)

        positions = []
        angle_offset = np.pi / 2  # Start from top
        for i in range(n_teams):
            angle = angle_offset + 2 * np.pi * i / n_teams
            px = arrangement_radius * np.cos(angle)
            py = arrangement_radius * np.sin(angle)
            positions.append((px, py))

        inner_radius = arrangement_radius + max_team_r

    # Department circle radius with padding
    dept_radius = inner_radius + 25

    # Add department circle
    circles_data.append(
        {
            "x": dept_x,
            "y": dept_y,
            "radius": dept_radius,
            "label": dept,
            "value": dept_value,
            "depth": 1,
            "color": dept_colors[dept],
            "department": dept,
        }
    )

    # Add team circles
    for i, t in enumerate(dept_teams):
        tx, ty = positions[i]
        team_r = team_radii[i]
        circles_data.append(
            {
                "x": dept_x + tx,
                "y": dept_y + ty,
                "radius": team_r,
                "label": t["label"],
                "value": t["value"],
                "depth": 2,
                "color": dept_colors[dept],
                "department": dept,
            }
        )

# Create DataFrame
df = pd.DataFrame(circles_data)

# Create display text
df["display_value"] = df["value"].apply(lambda v: f"${v}K")
df["display_text"] = df.apply(
    lambda r: f"{r['label']}\n{r['display_value']}" if r["depth"] == 2 else r["label"], axis=1
)

# Separate by depth for layered rendering
df_root = df[df["depth"] == 0].copy()
df_depts = df[df["depth"] == 1].copy()
df_teams = df[df["depth"] == 2].copy()

# Calculate size scale (radius squared for area encoding)
size_domain = [df["radius"].min(), df["radius"].max()]
size_range = [df["radius"].min() ** 2 * 3, df["radius"].max() ** 2 * 3]

# Shared scales for consistent positioning
x_scale = alt.Scale(domain=[-600, 600])
y_scale = alt.Scale(domain=[-500, 500])
size_scale = alt.Scale(domain=size_domain, range=size_range)

# Root circle layer (outermost - Company)
root_layer = (
    alt.Chart(df_root)
    .mark_circle(opacity=0.15, stroke="#1a3d5c", strokeWidth=3)
    .encode(
        x=alt.X("x:Q", axis=None, scale=x_scale),
        y=alt.Y("y:Q", axis=None, scale=y_scale),
        size=alt.Size("radius:Q", scale=size_scale, legend=None),
        color=alt.value("#1a3d5c"),
        tooltip=[alt.Tooltip("label:N", title="Name"), alt.Tooltip("display_value:N", title="Budget")],
    )
)

# Department circles layer
dept_layer = (
    alt.Chart(df_depts)
    .mark_circle(opacity=0.35, stroke="white", strokeWidth=2)
    .encode(
        x=alt.X("x:Q", axis=None, scale=x_scale),
        y=alt.Y("y:Q", axis=None, scale=y_scale),
        size=alt.Size("radius:Q", scale=size_scale, legend=None),
        color=alt.Color("color:N", scale=None),
        tooltip=[alt.Tooltip("label:N", title="Department"), alt.Tooltip("display_value:N", title="Budget")],
    )
)

# Team circles layer
team_layer = (
    alt.Chart(df_teams)
    .mark_circle(opacity=0.85, stroke="white", strokeWidth=2)
    .encode(
        x=alt.X("x:Q", axis=None, scale=x_scale),
        y=alt.Y("y:Q", axis=None, scale=y_scale),
        size=alt.Size("radius:Q", scale=size_scale, legend=None),
        color=alt.Color("color:N", scale=None),
        tooltip=[
            alt.Tooltip("label:N", title="Team"),
            alt.Tooltip("department:N", title="Department"),
            alt.Tooltip("display_value:N", title="Budget"),
        ],
    )
)

# Department labels
dept_label_layer = (
    alt.Chart(df_depts)
    .mark_text(color="white", fontWeight="bold", fontSize=18, dy=-60)
    .encode(x=alt.X("x:Q", axis=None, scale=x_scale), y=alt.Y("y:Q", axis=None, scale=y_scale), text="label:N")
)

# Team labels
team_label_layer = (
    alt.Chart(df_teams)
    .mark_text(color="white", fontWeight="bold", fontSize=12, lineBreak="\n")
    .encode(x=alt.X("x:Q", axis=None, scale=x_scale), y=alt.Y("y:Q", axis=None, scale=y_scale), text="display_text:N")
)

# Legend data
legend_df = pd.DataFrame(
    [
        {"department": dept, "color": color, "x": 450, "y": 380 - i * 50}
        for i, (dept, color) in enumerate(dept_colors.items())
    ]
)

# Legend circles
legend_circles = (
    alt.Chart(legend_df)
    .mark_circle(size=400, opacity=0.85)
    .encode(
        x=alt.X("x:Q", axis=None, scale=x_scale),
        y=alt.Y("y:Q", axis=None, scale=y_scale),
        color=alt.Color("color:N", scale=None),
    )
)

# Legend text
legend_text = (
    alt.Chart(legend_df)
    .mark_text(align="left", dx=20, fontSize=14, fontWeight="bold")
    .encode(x=alt.X("x:Q", axis=None, scale=x_scale), y=alt.Y("y:Q", axis=None, scale=y_scale), text="department:N")
)

# Combine all layers
chart = (
    alt.layer(root_layer, dept_layer, team_layer, dept_label_layer, team_label_layer, legend_circles, legend_text)
    .properties(
        width=1200,
        height=1200,
        title=alt.Title("circlepacking-basic · altair · pyplots.ai", fontSize=28, fontWeight="bold", anchor="middle"),
    )
    .configure_view(strokeWidth=0)
)

# Save outputs (3600x3600 px with scale_factor=3.0)
chart.save("plot.png", scale_factor=3.0)
chart.save("plot.html")
