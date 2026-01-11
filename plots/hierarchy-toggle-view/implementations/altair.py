""" pyplots.ai
hierarchy-toggle-view: Interactive Treemap-Sunburst Toggle View
Library: altair 6.0.0 | Python 3.13.11
Quality: 75/100 | Created: 2026-01-11
"""

import altair as alt
import numpy as np
import pandas as pd


# Data - Company structure with departments and teams (25 nodes, 3 levels)
np.random.seed(42)

hierarchy_data = [
    # Root
    {"id": "Company", "parent": "", "label": "TechCorp Inc.", "value": 0},
    # Level 1 - Departments
    {"id": "Engineering", "parent": "Company", "label": "Engineering", "value": 0},
    {"id": "Sales", "parent": "Company", "label": "Sales", "value": 0},
    {"id": "Marketing", "parent": "Company", "label": "Marketing", "value": 0},
    {"id": "Operations", "parent": "Company", "label": "Operations", "value": 0},
    # Level 2 - Engineering Teams
    {"id": "Frontend", "parent": "Engineering", "label": "Frontend", "value": 45},
    {"id": "Backend", "parent": "Engineering", "label": "Backend", "value": 52},
    {"id": "DevOps", "parent": "Engineering", "label": "DevOps", "value": 28},
    {"id": "QA", "parent": "Engineering", "label": "QA", "value": 22},
    {"id": "DataScience", "parent": "Engineering", "label": "Data Science", "value": 35},
    # Level 2 - Sales Teams
    {"id": "Enterprise", "parent": "Sales", "label": "Enterprise", "value": 38},
    {"id": "SMB", "parent": "Sales", "label": "SMB", "value": 25},
    {"id": "Partnerships", "parent": "Sales", "label": "Partnerships", "value": 18},
    # Level 2 - Marketing Teams
    {"id": "Digital", "parent": "Marketing", "label": "Digital", "value": 20},
    {"id": "Content", "parent": "Marketing", "label": "Content", "value": 15},
    {"id": "Events", "parent": "Marketing", "label": "Events", "value": 12},
    {"id": "Brand", "parent": "Marketing", "label": "Brand", "value": 10},
    # Level 2 - Operations Teams
    {"id": "HR", "parent": "Operations", "label": "HR", "value": 18},
    {"id": "Finance", "parent": "Operations", "label": "Finance", "value": 22},
    {"id": "Legal", "parent": "Operations", "label": "Legal", "value": 8},
    {"id": "Facilities", "parent": "Operations", "label": "Facilities", "value": 12},
]

df = pd.DataFrame(hierarchy_data)

# Calculate parent values (sum of children)
parent_ids = df[df["parent"] != ""]["parent"].unique()
for _ in range(5):  # Iterate to propagate values up the hierarchy
    for parent_id in parent_ids:
        children = df[df["parent"] == parent_id]
        if len(children) > 0 and all(children["value"] > 0):
            df.loc[df["id"] == parent_id, "value"] = children["value"].sum()

# Assign department colors based on parent chain
dept_mapping = {"Engineering": "Engineering", "Sales": "Sales", "Marketing": "Marketing", "Operations": "Operations"}
for dept in dept_mapping:
    df.loc[df["parent"] == dept, "department"] = dept
df.loc[df["id"].isin(dept_mapping.keys()), "department"] = df.loc[df["id"].isin(dept_mapping.keys()), "id"]
df["department"] = df["department"].fillna("Company")

# Get leaf nodes (nodes that are not parents)
all_parent_ids = set(df["parent"].unique())
leaf_mask = ~df["id"].isin(all_parent_ids - {""})
leaf_df = df[leaf_mask & (df["value"] > 0)].copy()

# Build treemap rectangles using slice-and-dice algorithm
treemap_records = []
values = leaf_df["value"].tolist()
ids = leaf_df["id"].tolist()
labels = leaf_df["label"].tolist()
depts = leaf_df["department"].tolist()
total_value = sum(values)

# Sort by value descending for better layout
sorted_data = sorted(zip(values, ids, labels, depts, strict=True), reverse=True)
values = [v for v, nid, lbl, d in sorted_data]
ids = [nid for v, nid, lbl, d in sorted_data]
labels = [lbl for v, nid, lbl, d in sorted_data]
depts = [d for v, nid, lbl, d in sorted_data]

# Simple row-based layout
x, y = 0, 0
row_height = 25
col_x = 0
row_items = []
row_value = 0
target_row_value = total_value / 4  # 4 rows

for i, (val, node_id, lbl, dept) in enumerate(zip(values, ids, labels, depts, strict=True)):
    width = 100 * (val / total_value) * 4 if total_value > 0 else 10
    if col_x + width > 100 or i == len(values) - 1:
        # Finalize row
        if i == len(values) - 1:
            row_items.append((val, node_id, lbl, dept, width))
        actual_row_width = sum(w for v, ni, lb, d, w in row_items)
        scale = 100 / actual_row_width if actual_row_width > 0 else 1
        rx = 0
        for v, ni, lb, d, w in row_items:
            scaled_w = w * scale
            treemap_records.append(
                {
                    "id": ni,
                    "label": lb,
                    "value": v,
                    "department": d,
                    "x": rx,
                    "y": y,
                    "x2": rx + scaled_w,
                    "y2": y + row_height,
                    "cx": rx + scaled_w / 2,
                    "cy": y + row_height / 2,
                }
            )
            rx += scaled_w
        y += row_height
        row_items = [(val, node_id, lbl, dept, width)] if i < len(values) - 1 else []
        col_x = width if i < len(values) - 1 else 0
    else:
        row_items.append((val, node_id, lbl, dept, width))
        col_x += width

treemap_df = pd.DataFrame(treemap_records)

# Build sunburst data from hierarchy
sunburst_records = []
departments = ["Engineering", "Sales", "Marketing", "Operations"]
dept_values = {d: df[df["id"] == d]["value"].values[0] for d in departments}
total_company = sum(dept_values.values())

# Level 1 - Department arcs
start_angle = 0
for dept in departments:
    dept_angle = 360 * (dept_values[dept] / total_company)
    end_angle = start_angle + dept_angle
    sunburst_records.append(
        {
            "id": dept,
            "label": dept,
            "value": dept_values[dept],
            "department": dept,
            "startAngle": start_angle,
            "endAngle": end_angle,
            "innerRadius": 40,
            "outerRadius": 70,
            "depth": 1,
        }
    )
    # Level 2 - Team arcs within department
    teams = df[df["parent"] == dept]
    dept_start = start_angle
    for _, team in teams.iterrows():
        team_angle = dept_angle * (team["value"] / dept_values[dept]) if dept_values[dept] > 0 else 0
        team_end = dept_start + team_angle
        sunburst_records.append(
            {
                "id": team["id"],
                "label": team["label"],
                "value": team["value"],
                "department": dept,
                "startAngle": dept_start,
                "endAngle": team_end,
                "innerRadius": 70,
                "outerRadius": 100,
                "depth": 2,
            }
        )
        dept_start = team_end
    start_angle = end_angle

sunburst_df = pd.DataFrame(sunburst_records)
sunburst_df["startAngle_rad"] = np.radians(sunburst_df["startAngle"] - 90)
sunburst_df["endAngle_rad"] = np.radians(sunburst_df["endAngle"] - 90)

# Color scale
dept_domain = ["Engineering", "Sales", "Marketing", "Operations"]
dept_range = ["#306998", "#FFD43B", "#E74C3C", "#27AE60"]

# Treemap chart
treemap_rects = (
    alt.Chart(treemap_df)
    .mark_rect(stroke="white", strokeWidth=3)
    .encode(
        x=alt.X("x:Q", scale=alt.Scale(domain=[0, 100]), axis=None),
        y=alt.Y("y:Q", scale=alt.Scale(domain=[0, 100]), axis=None),
        x2="x2:Q",
        y2="y2:Q",
        color=alt.Color(
            "department:N",
            scale=alt.Scale(domain=dept_domain, range=dept_range),
            legend=alt.Legend(title="Department", titleFontSize=20, labelFontSize=18, orient="right"),
        ),
        tooltip=[
            alt.Tooltip("label:N", title="Team"),
            alt.Tooltip("value:Q", title="Headcount"),
            alt.Tooltip("department:N", title="Department"),
        ],
    )
)

treemap_labels = (
    alt.Chart(treemap_df)
    .mark_text(fontSize=14, fontWeight="bold", color="white", baseline="middle", align="center")
    .encode(
        x=alt.X("cx:Q", scale=alt.Scale(domain=[0, 100])),
        y=alt.Y("cy:Q", scale=alt.Scale(domain=[0, 100])),
        text="label:N",
    )
)

treemap_chart = (treemap_rects + treemap_labels).properties(
    width=1200, height=800, title=alt.Title("Treemap View - Team Sizes by Department", fontSize=22, anchor="middle")
)

# Sunburst chart
sunburst_chart = (
    alt.Chart(sunburst_df)
    .mark_arc(stroke="white", strokeWidth=2)
    .encode(
        theta=alt.Theta("endAngle_rad:Q", scale=alt.Scale(domain=[-np.pi, np.pi])),
        theta2="startAngle_rad:Q",
        radius=alt.Radius("outerRadius:Q", scale=alt.Scale(domain=[0, 120], range=[0, 350])),
        radius2="innerRadius:Q",
        color=alt.Color("department:N", scale=alt.Scale(domain=dept_domain, range=dept_range), legend=None),
        tooltip=[
            alt.Tooltip("label:N", title="Team"),
            alt.Tooltip("value:Q", title="Headcount"),
            alt.Tooltip("department:N", title="Department"),
        ],
    )
    .properties(
        width=800, height=800, title=alt.Title("Sunburst View - Hierarchical Structure", fontSize=22, anchor="middle")
    )
)

# Combine both views side by side
combined_chart = (
    alt.hconcat(treemap_chart, sunburst_chart, spacing=100)
    .resolve_scale(color="shared")
    .properties(
        title=alt.Title(
            "hierarchy-toggle-view · altair · pyplots.ai",
            fontSize=28,
            anchor="middle",
            offset=20,
            subtitle="Company Organization: Treemap (Size Comparison) vs Sunburst (Hierarchy)",
            subtitleFontSize=18,
        )
    )
    .configure_view(strokeWidth=0)
    .configure_legend(titleFontSize=20, labelFontSize=18, symbolSize=200)
)

# Save outputs
combined_chart.save("plot.png", scale_factor=3.0)
combined_chart.save("plot.html")
