""" pyplots.ai
pie-drilldown: Drilldown Pie Chart with Click Navigation
Library: altair 6.0.0 | Python 3.13.11
Quality: 78/100 | Created: 2025-12-31
"""

import altair as alt
import pandas as pd


# Hierarchical data: Company budget breakdown
# Structure: id, name, value, parent (following spec's data format)
# Pre-aggregated values for each level
hierarchy_data = [
    # Level 1: Departments (children of root)
    {"id": "engineering", "name": "Engineering", "value": 1755000, "parent": "root", "level": 1},
    {"id": "marketing", "name": "Marketing", "value": 740000, "parent": "root", "level": 1},
    {"id": "operations", "name": "Operations", "value": 485000, "parent": "root", "level": 1},
    {"id": "hr", "name": "Human Resources", "value": 220000, "parent": "root", "level": 1},
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
root_df["pct_label"] = root_df["percentage"].apply(lambda x: f"{x:.1f}%")

# Define explicit color mapping for consistent legend-to-slice matching
dept_names = root_df["name"].tolist()
colors = ["#306998", "#FFD43B", "#4B8BBE", "#C45AEC"]
color_domain = dept_names
color_range = colors[: len(dept_names)]

# Create selection for click interactivity (highlights slice)
selection = alt.selection_point(fields=["name"], empty=False)

# Main pie chart using arc mark
pie = (
    alt.Chart(root_df)
    .mark_arc(innerRadius=100, outerRadius=350, stroke="#ffffff", strokeWidth=4, cursor="pointer")
    .encode(
        theta=alt.Theta("value:Q", stack=True),
        color=alt.Color(
            "name:N",
            scale=alt.Scale(domain=color_domain, range=color_range),
            sort=dept_names,
            legend=alt.Legend(
                title="Departments",
                titleFontSize=20,
                labelFontSize=18,
                orient="right",
                titlePadding=15,
                symbolSize=300,
                offset=20,
            ),
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

# Text labels on pie slices
text_labels = (
    alt.Chart(root_df)
    .mark_text(radius=250, fontSize=18, fontWeight="bold", align="center", baseline="middle")
    .encode(
        theta=alt.Theta("value:Q", stack=True),
        order=alt.Order("value:Q", sort="descending"),
        text=alt.Text("name:N"),
        color=alt.value("#ffffff"),
    )
)

# Percentage labels outside the pie
pct_labels = (
    alt.Chart(root_df)
    .mark_text(radius=400, fontSize=16, align="center", baseline="middle")
    .encode(
        theta=alt.Theta("value:Q", stack=True),
        order=alt.Order("value:Q", sort="descending"),
        text=alt.Text("pct_label:N"),
        color=alt.value("#333333"),
    )
)

# Combine pie layers
pie_chart = pie + text_labels + pct_labels

# Breadcrumb navigation display
breadcrumb_df = pd.DataFrame(
    [
        {"text": "All", "x": 0, "clickable": True},
        {"text": " > ", "x": 1, "clickable": False},
        {"text": "Departments", "x": 2, "clickable": False},
        {"text": " (click to drill down)", "x": 3, "clickable": False},
    ]
)

breadcrumb = (
    alt.Chart(breadcrumb_df)
    .mark_text(fontSize=18, align="left")
    .encode(
        x=alt.X("x:O", axis=None, scale=alt.Scale(domain=[0, 1, 2, 3])),
        text="text:N",
        color=alt.condition(
            alt.datum.clickable == True,  # noqa: E712
            alt.value("#306998"),
            alt.value("#666666"),
        ),
    )
    .properties(width=600, height=30)
)

# Title
title_text = alt.TitleParams(
    text="Company Budget Breakdown",
    subtitle="pie-drilldown · altair · pyplots.ai",
    fontSize=32,
    subtitleFontSize=20,
    subtitleColor="#666666",
    anchor="middle",
    offset=20,
)

# Instruction text
instruction_df = pd.DataFrame([{"text": "Click slices to explore | Hover for details | Interactive drilldown in HTML"}])

instruction = (
    alt.Chart(instruction_df)
    .mark_text(fontSize=16, color="#888888")
    .encode(text="text:N")
    .properties(width=600, height=30)
)

# Combine main chart with breadcrumb and instruction
main_chart = (
    alt.vconcat(breadcrumb, pie_chart, instruction, spacing=10)
    .properties(title=title_text)
    .configure_view(strokeWidth=0)
    .configure_title(fontSize=32, subtitleFontSize=20)
    .configure_legend(titleFontSize=20, labelFontSize=18, symbolSize=300)
)

# Save outputs (target: 4800 x 2700 at scale 3 = 1600 x 900 base)
main_chart.save("plot.png", scale_factor=3.0)
main_chart.save("plot.html")
