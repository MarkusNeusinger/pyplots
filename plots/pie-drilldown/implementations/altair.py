"""pyplots.ai
pie-drilldown: Drilldown Pie Chart with Click Navigation
Library: altair 6.0.0 | Python 3.13.11
Quality: 78/100 | Created: 2025-12-31
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

# Prepare Engineering sub-level data for drilldown display
eng_df = df[df["parent"] == "engineering"].copy()
eng_total = eng_df["value"].sum()
eng_df["percentage"] = eng_df["value"] / eng_total * 100
eng_df["pct_label"] = eng_df["percentage"].apply(lambda x: f"{x:.1f}%")

# Distinct color schemes - use clearly different colors
dept_colors = {"Engineering": "#306998", "Marketing": "#FFD43B", "Operations": "#2E8B57", "Human Resources": "#9B59B6"}

# Child colors - shades of blue for Engineering teams
team_colors = {"Frontend": "#5DA5DA", "Backend": "#306998", "DevOps": "#1E4D6B"}

# Selection parameter for click interactivity (highlights slice)
selection = alt.selection_point(fields=["name"], empty=False)

# Main pie chart (Level 1 - Departments)
main_pie = (
    alt.Chart(root_df)
    .mark_arc(innerRadius=100, outerRadius=350, stroke="#ffffff", strokeWidth=4, cursor="pointer")
    .encode(
        theta=alt.Theta("value:Q", stack=True),
        color=alt.Color(
            "name:N",
            scale=alt.Scale(domain=list(dept_colors.keys()), range=list(dept_colors.values())),
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
        opacity=alt.condition(selection, alt.value(1.0), alt.value(0.7)),
        tooltip=[
            alt.Tooltip("name:N", title="Department"),
            alt.Tooltip("value:Q", title="Budget ($)", format=",.0f"),
            alt.Tooltip("percentage:Q", title="Share (%)", format=".1f"),
        ],
    )
    .add_params(selection)
)

# Department name labels on slices
main_text = (
    alt.Chart(root_df)
    .mark_text(radius=250, fontSize=18, fontWeight="bold", align="center", baseline="middle")
    .encode(
        theta=alt.Theta("value:Q", stack=True),
        order=alt.Order("value:Q", sort="descending"),
        text=alt.Text("name:N"),
        color=alt.value("#ffffff"),
    )
)

# Percentage labels outside main pie
main_pct = (
    alt.Chart(root_df)
    .mark_text(radius=420, fontSize=16, align="center", baseline="middle")
    .encode(
        theta=alt.Theta("value:Q", stack=True),
        order=alt.Order("value:Q", sort="descending"),
        text=alt.Text("pct_label:N"),
        color=alt.value("#333333"),
    )
)

# Combine main pie layers
main_chart = main_pie + main_text + main_pct

# Drilldown pie chart (Level 2 - Engineering Teams)
drill_pie = (
    alt.Chart(eng_df)
    .mark_arc(innerRadius=80, outerRadius=280, stroke="#ffffff", strokeWidth=3)
    .encode(
        theta=alt.Theta("value:Q", stack=True),
        color=alt.Color(
            "name:N",
            scale=alt.Scale(domain=list(team_colors.keys()), range=list(team_colors.values())),
            legend=alt.Legend(
                title="Engineering Teams",
                titleFontSize=18,
                labelFontSize=16,
                orient="right",
                titlePadding=10,
                symbolSize=200,
                offset=10,
            ),
        ),
        order=alt.Order("value:Q", sort="descending"),
        tooltip=[
            alt.Tooltip("name:N", title="Team"),
            alt.Tooltip("value:Q", title="Budget ($)", format=",.0f"),
            alt.Tooltip("percentage:Q", title="Share (%)", format=".1f"),
        ],
    )
)

# Team name labels on drilldown slices
drill_text = (
    alt.Chart(eng_df)
    .mark_text(radius=190, fontSize=16, fontWeight="bold", align="center", baseline="middle")
    .encode(
        theta=alt.Theta("value:Q", stack=True),
        order=alt.Order("value:Q", sort="descending"),
        text=alt.Text("name:N"),
        color=alt.value("#ffffff"),
    )
)

# Percentage labels for drilldown
drill_pct = (
    alt.Chart(eng_df)
    .mark_text(radius=330, fontSize=14, align="center", baseline="middle")
    .encode(
        theta=alt.Theta("value:Q", stack=True),
        order=alt.Order("value:Q", sort="descending"),
        text=alt.Text("pct_label:N"),
        color=alt.value("#333333"),
    )
)

# Combine drilldown layers
drill_chart = drill_pie + drill_text + drill_pct

# Breadcrumb navigation text
breadcrumb_df = pd.DataFrame([{"text": "All  ›  Departments  ›  Engineering"}])
breadcrumb = (
    alt.Chart(breadcrumb_df)
    .mark_text(fontSize=22, align="center", fontWeight="bold", color="#306998")
    .encode(text="text:N")
    .properties(width=1200, height=50)
)

# Title configuration
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
instruction_df = pd.DataFrame(
    [{"text": "Click department slices to explore | Hover for details | Drilldown shows Engineering breakdown"}]
)
instruction = (
    alt.Chart(instruction_df)
    .mark_text(fontSize=16, color="#888888")
    .encode(text="text:N")
    .properties(width=1200, height=35)
)

# Combined layout: Main pie (left) + Drilldown pie (right)
combined_pies = alt.hconcat(
    main_chart.properties(width=650, height=700, title="All Departments"),
    drill_chart.properties(width=550, height=550, title="Engineering Breakdown ($1.76M)"),
    spacing=80,
)

# Final chart with breadcrumb and instructions
final_chart = (
    alt.vconcat(breadcrumb, combined_pies, instruction, spacing=15)
    .properties(title=title_text)
    .configure_view(strokeWidth=0)
    .configure_title(fontSize=32, subtitleFontSize=20)
    .configure_legend(titleFontSize=18, labelFontSize=16, symbolSize=200)
)

# Save outputs (target: 4800 x 2700 at scale 3 = 1600 x 900 base)
final_chart.save("plot.png", scale_factor=3.0)
final_chart.save("plot.html")
