""" pyplots.ai
pie-drilldown: Drilldown Pie Chart with Click Navigation
Library: altair 6.0.0 | Python 3.13.11
Quality: 84/100 | Created: 2025-12-31
"""

import altair as alt
import pandas as pd


# Hierarchical data: Company budget breakdown
# Structure: id, name, value, parent (following spec's data format)
hierarchy_data = [
    # Level 1: Departments (children of root)
    {"id": "engineering", "name": "Engineering", "value": 1755000, "parent": "root", "level": 1},
    {"id": "marketing", "name": "Marketing", "value": 740000, "parent": "root", "level": 1},
    {"id": "operations", "name": "Operations", "value": 485000, "parent": "root", "level": 1},
    {"id": "hr", "name": "HR", "value": 220000, "parent": "root", "level": 1},
    # Level 2: Engineering Teams
    {"id": "eng_frontend", "name": "Frontend", "value": 510000, "parent": "engineering", "level": 2},
    {"id": "eng_backend", "name": "Backend", "value": 745000, "parent": "engineering", "level": 2},
    {"id": "eng_devops", "name": "DevOps", "value": 500000, "parent": "engineering", "level": 2},
    # Level 2: Marketing Teams
    {"id": "mkt_digital", "name": "Digital", "value": 295000, "parent": "marketing", "level": 2},
    {"id": "mkt_content", "name": "Content", "value": 245000, "parent": "marketing", "level": 2},
    {"id": "mkt_events", "name": "Events", "value": 200000, "parent": "marketing", "level": 2},
    # Level 2: Operations Teams
    {"id": "ops_facilities", "name": "Facilities", "value": 325000, "parent": "operations", "level": 2},
    {"id": "ops_it", "name": "IT Support", "value": 160000, "parent": "operations", "level": 2},
    # Level 2: HR Teams
    {"id": "hr_recruit", "name": "Recruiting", "value": 120000, "parent": "hr", "level": 2},
    {"id": "hr_training", "name": "Training", "value": 100000, "parent": "hr", "level": 2},
]

df = pd.DataFrame(hierarchy_data)

# Get root level data (departments) for main pie chart
root_df = df[df["parent"] == "root"].copy()
root_df["percentage"] = root_df["value"] / root_df["value"].sum() * 100
root_df["pct_label"] = root_df.apply(
    lambda r: f"{r['name']}\n${r['value'] / 1e6:.2f}M ({r['percentage']:.1f}%)", axis=1
)

# Prepare sub-level data for all departments
eng_df = df[df["parent"] == "engineering"].copy()
eng_df["percentage"] = eng_df["value"] / eng_df["value"].sum() * 100
eng_df["label"] = eng_df.apply(lambda r: f"{r['name']}: ${r['value'] / 1e3:.0f}K ({r['percentage']:.1f}%)", axis=1)

mkt_df = df[df["parent"] == "marketing"].copy()
mkt_df["percentage"] = mkt_df["value"] / mkt_df["value"].sum() * 100
mkt_df["label"] = mkt_df.apply(lambda r: f"{r['name']}: ${r['value'] / 1e3:.0f}K ({r['percentage']:.1f}%)", axis=1)

ops_df = df[df["parent"] == "operations"].copy()
ops_df["percentage"] = ops_df["value"] / ops_df["value"].sum() * 100
ops_df["label"] = ops_df.apply(lambda r: f"{r['name']}: ${r['value'] / 1e3:.0f}K ({r['percentage']:.1f}%)", axis=1)

hr_df = df[df["parent"] == "hr"].copy()
hr_df["percentage"] = hr_df["value"] / hr_df["value"].sum() * 100
hr_df["label"] = hr_df.apply(lambda r: f"{r['name']}: ${r['value'] / 1e3:.0f}K ({r['percentage']:.1f}%)", axis=1)

# Color scheme - main departments with distinct colors
dept_colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#9467bd"]

# Team colors - shades for each department's drilldown
eng_colors = ["#4a90d9", "#1f77b4", "#15537a"]
mkt_colors = ["#ffaa4a", "#ff7f0e", "#cc6600"]
ops_colors = ["#4dbd4d", "#2ca02c"]
hr_colors = ["#b38fc5", "#9467bd"]

# Selection parameter for click interactivity
selection = alt.selection_point(fields=["name"], empty=False, name="dept_select")

# Main pie chart (Level 1 - Departments) - central position
main_pie = (
    alt.Chart(root_df)
    .mark_arc(innerRadius=120, outerRadius=280, stroke="#ffffff", strokeWidth=4, cursor="pointer")
    .encode(
        theta=alt.Theta("value:Q", stack=True),
        color=alt.Color(
            "name:N",
            scale=alt.Scale(domain=["Engineering", "Marketing", "Operations", "HR"], range=dept_colors),
            legend=None,
        ),
        order=alt.Order("value:Q", sort="descending"),
        opacity=alt.condition(selection, alt.value(1.0), alt.value(0.75)),
        tooltip=[
            alt.Tooltip("name:N", title="Department"),
            alt.Tooltip("value:Q", title="Budget ($)", format=",.0f"),
            alt.Tooltip("percentage:Q", title="Share (%)", format=".1f"),
        ],
    )
    .add_params(selection)
)

# Department labels outside main pie
main_labels = (
    alt.Chart(root_df)
    .mark_text(radius=350, fontSize=18, fontWeight="bold", align="center", baseline="middle", lineBreak="\n")
    .encode(
        theta=alt.Theta("value:Q", stack=True),
        order=alt.Order("value:Q", sort="descending"),
        text=alt.Text("pct_label:N"),
        color=alt.value("#333333"),
    )
)

# Center text showing total
center_df = pd.DataFrame([{"text": "Total Budget", "subtext": "$3.20M"}])
center_label = (
    alt.Chart(center_df).mark_text(fontSize=20, fontWeight="bold", color="#333333", dy=-12).encode(text="text:N")
)
center_value = (
    alt.Chart(center_df).mark_text(fontSize=28, fontWeight="bold", color="#1f77b4", dy=18).encode(text="subtext:N")
)

main_chart = (main_pie + main_labels + center_label + center_value).properties(width=500, height=500)


# Helper function to create drilldown pie
def create_drilldown(data, colors, title, parent_color):
    pie = (
        alt.Chart(data)
        .mark_arc(innerRadius=50, outerRadius=140, stroke="#ffffff", strokeWidth=2)
        .encode(
            theta=alt.Theta("value:Q", stack=True),
            color=alt.Color("name:N", scale=alt.Scale(domain=data["name"].tolist(), range=colors), legend=None),
            order=alt.Order("value:Q", sort="descending"),
            tooltip=[
                alt.Tooltip("name:N", title="Team"),
                alt.Tooltip("value:Q", title="Budget ($)", format=",.0f"),
                alt.Tooltip("percentage:Q", title="Share (%)", format=".1f"),
            ],
        )
    )

    labels = (
        alt.Chart(data)
        .mark_text(radius=175, fontSize=14, align="center", baseline="middle")
        .encode(
            theta=alt.Theta("value:Q", stack=True),
            order=alt.Order("value:Q", sort="descending"),
            text=alt.Text("label:N"),
            color=alt.value("#333333"),
        )
    )

    title_df = pd.DataFrame([{"title": title}])
    title_text = (
        alt.Chart(title_df)
        .mark_text(fontSize=16, fontWeight="bold", color=parent_color, dy=-180)
        .encode(text="title:N")
    )

    return (pie + labels + title_text).properties(width=320, height=350)


# Create drilldown charts for each department
eng_chart = create_drilldown(eng_df, eng_colors, "⬆ Engineering ($1.76M)", "#1f77b4")
mkt_chart = create_drilldown(mkt_df, mkt_colors, "⬆ Marketing ($740K)", "#ff7f0e")
ops_chart = create_drilldown(ops_df, ops_colors, "⬆ Operations ($485K)", "#2ca02c")
hr_chart = create_drilldown(hr_df, hr_colors, "⬆ HR ($220K)", "#9467bd")

# Arrange drilldowns in a 2x2 grid around the main chart
top_drilldowns = alt.hconcat(eng_chart, mkt_chart, spacing=60)
bottom_drilldowns = alt.hconcat(ops_chart, hr_chart, spacing=60)

# Breadcrumb navigation
breadcrumb_df = pd.DataFrame([{"text": "📊 All Departments  ›  Click any slice to explore team breakdown"}])
breadcrumb = (
    alt.Chart(breadcrumb_df)
    .mark_text(fontSize=20, align="center", fontWeight="bold", color="#555555")
    .encode(text="text:N")
    .properties(width=1400, height=40)
)

# Title configuration
title_text = alt.TitleParams(
    text="Company Budget Breakdown with Drilldown Navigation",
    subtitle="pie-drilldown · altair · pyplots.ai",
    fontSize=32,
    subtitleFontSize=20,
    subtitleColor="#666666",
    anchor="middle",
    offset=25,
)

# Instruction text
instruction_df = pd.DataFrame(
    [
        {
            "text": "Interactive: Click department slices to highlight | Hover for budget details | Arrows (⬆) show parent relationship"
        }
    ]
)
instruction = (
    alt.Chart(instruction_df)
    .mark_text(fontSize=16, color="#888888")
    .encode(text="text:N")
    .properties(width=1400, height=30)
)

# Layout: Main pie in center with drilldowns on sides
left_drilldowns = alt.vconcat(eng_chart, ops_chart, spacing=30)
right_drilldowns = alt.vconcat(mkt_chart, hr_chart, spacing=30)

main_with_drilldowns = alt.hconcat(left_drilldowns, main_chart, right_drilldowns, spacing=40)

# Final chart composition
final_chart = (
    alt.vconcat(breadcrumb, main_with_drilldowns, instruction, spacing=20)
    .properties(title=title_text)
    .configure_view(strokeWidth=0)
    .configure_title(fontSize=32, subtitleFontSize=20)
)

# Save outputs (target: 4800 x 2700 at scale 3 = 1600 x 900 base)
final_chart.save("plot.png", scale_factor=3.0)
final_chart.save("plot.html")
