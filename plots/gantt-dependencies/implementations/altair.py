""" pyplots.ai
gantt-dependencies: Gantt Chart with Dependencies
Library: altair 6.0.0 | Python 3.13.11
Quality: 91/100 | Created: 2026-01-15
"""

import altair as alt
import pandas as pd


# Data - Software Development Project with Dependencies
tasks_data = [
    # Requirements Phase
    {
        "task": "Requirements Gathering",
        "start": "2024-01-01",
        "end": "2024-01-15",
        "group": "Requirements",
        "depends_on": None,
        "task_id": "REQ1",
    },
    {
        "task": "Requirements Review",
        "start": "2024-01-16",
        "end": "2024-01-22",
        "group": "Requirements",
        "depends_on": "REQ1",
        "task_id": "REQ2",
    },
    # Design Phase
    {
        "task": "System Architecture",
        "start": "2024-01-23",
        "end": "2024-02-05",
        "group": "Design",
        "depends_on": "REQ2",
        "task_id": "DES1",
    },
    {
        "task": "Database Design",
        "start": "2024-02-06",
        "end": "2024-02-15",
        "group": "Design",
        "depends_on": "DES1",
        "task_id": "DES2",
    },
    {
        "task": "UI/UX Design",
        "start": "2024-02-06",
        "end": "2024-02-20",
        "group": "Design",
        "depends_on": "DES1",
        "task_id": "DES3",
    },
    # Development Phase
    {
        "task": "Backend Development",
        "start": "2024-02-16",
        "end": "2024-03-20",
        "group": "Development",
        "depends_on": "DES2",
        "task_id": "DEV1",
    },
    {
        "task": "Frontend Development",
        "start": "2024-02-21",
        "end": "2024-03-25",
        "group": "Development",
        "depends_on": "DES3",
        "task_id": "DEV2",
    },
    {
        "task": "API Integration",
        "start": "2024-03-21",
        "end": "2024-04-05",
        "group": "Development",
        "depends_on": "DEV1",
        "task_id": "DEV3",
    },
    # Testing Phase
    {
        "task": "Unit Testing",
        "start": "2024-03-26",
        "end": "2024-04-10",
        "group": "Testing",
        "depends_on": "DEV2",
        "task_id": "TST1",
    },
    {
        "task": "Integration Testing",
        "start": "2024-04-06",
        "end": "2024-04-20",
        "group": "Testing",
        "depends_on": "DEV3",
        "task_id": "TST2",
    },
    {
        "task": "User Acceptance Testing",
        "start": "2024-04-21",
        "end": "2024-05-05",
        "group": "Testing",
        "depends_on": "TST2",
        "task_id": "TST3",
    },
    # Deployment Phase
    {
        "task": "Deployment Prep",
        "start": "2024-05-06",
        "end": "2024-05-12",
        "group": "Deployment",
        "depends_on": "TST3",
        "task_id": "DPL1",
    },
    {
        "task": "Production Deploy",
        "start": "2024-05-13",
        "end": "2024-05-15",
        "group": "Deployment",
        "depends_on": "DPL1",
        "task_id": "DPL2",
    },
]

df = pd.DataFrame(tasks_data)
df["start"] = pd.to_datetime(df["start"])
df["end"] = pd.to_datetime(df["end"])

# Create task lookup for dependency arrows
task_lookup = {row["task_id"]: row for _, row in df.iterrows()}

# Define colors for groups
group_colors = {
    "Requirements": "#306998",
    "Design": "#FFD43B",
    "Development": "#4B8BBE",
    "Testing": "#646464",
    "Deployment": "#FFE873",
}

# Build ordered list with y positions
group_order = ["Requirements", "Design", "Development", "Testing", "Deployment"]
rows = []
y_pos = 0
task_to_y = {}

for grp in group_order:
    # Group header
    grp_df = df[df["group"] == grp]
    rows.append(
        {
            "task": f"▸ {grp}",
            "start": grp_df["start"].min(),
            "end": grp_df["end"].max(),
            "group": grp,
            "is_group": True,
            "color": "#2C3E50",
            "y_pos": y_pos,
        }
    )
    task_to_y[f"▸ {grp}"] = y_pos
    y_pos += 1

    # Tasks in this group
    for _, row in grp_df.iterrows():
        display_task = f"  {row['task']}"
        rows.append(
            {
                "task": display_task,
                "start": row["start"],
                "end": row["end"],
                "group": grp,
                "is_group": False,
                "color": group_colors[grp],
                "y_pos": y_pos,
            }
        )
        task_to_y[display_task] = y_pos
        y_pos += 1

combined_df = pd.DataFrame(rows)
max_y = y_pos - 1

# Reverse y for proper display (top to bottom)
combined_df["y_display"] = max_y - combined_df["y_pos"]

# Add y bounds for rect marks
combined_df["y_min"] = combined_df["y_display"] - 0.35
combined_df["y_max"] = combined_df["y_display"] + 0.35

# Thinner bounds for group bars
combined_df.loc[combined_df["is_group"], "y_min"] = combined_df.loc[combined_df["is_group"], "y_display"] - 0.2
combined_df.loc[combined_df["is_group"], "y_max"] = combined_df.loc[combined_df["is_group"], "y_display"] + 0.2

# Build dependency data with y positions
dep_data = []
for _, row in df.iterrows():
    if row["depends_on"] and row["depends_on"] in task_lookup:
        pred = task_lookup[row["depends_on"]]
        from_task = f"  {pred['task']}"
        to_task = f"  {row['task']}"
        dep_data.append(
            {
                "from_x": pred["end"],
                "to_x": row["start"],
                "from_y": max_y - task_to_y[from_task],
                "to_y": max_y - task_to_y[to_task],
            }
        )
dep_df = pd.DataFrame(dep_data) if dep_data else pd.DataFrame()

# Shared scales
y_scale = alt.Scale(domain=[-0.5, max_y + 0.5])

# Task bars using rect
task_df = combined_df[~combined_df["is_group"]]
task_bars = (
    alt.Chart(task_df)
    .mark_rect(cornerRadius=4)
    .encode(
        x=alt.X("start:T", title="Timeline", axis=alt.Axis(format="%b %d", labelFontSize=16, titleFontSize=20)),
        x2=alt.X2("end:T"),
        y=alt.Y("y_min:Q", scale=y_scale, axis=None),
        y2=alt.Y2("y_max:Q"),
        color=alt.Color("color:N", scale=None),
        tooltip=[
            "task:N",
            alt.Tooltip("start:T", format="%Y-%m-%d"),
            alt.Tooltip("end:T", format="%Y-%m-%d"),
            "group:N",
        ],
    )
)

# Group bars using rect (thinner, dark)
group_df = combined_df[combined_df["is_group"]]
group_bars = (
    alt.Chart(group_df)
    .mark_rect(cornerRadius=3, opacity=0.75)
    .encode(
        x=alt.X("start:T"),
        x2=alt.X2("end:T"),
        y=alt.Y("y_min:Q", scale=y_scale, axis=None),
        y2=alt.Y2("y_max:Q"),
        color=alt.value("#2C3E50"),
        tooltip=["task:N", alt.Tooltip("start:T", format="%Y-%m-%d"), alt.Tooltip("end:T", format="%Y-%m-%d")],
    )
)

# Y-axis labels - groups (position at leftmost point of chart)
group_label_data = combined_df[combined_df["is_group"]][["task", "y_display", "start"]].copy()
group_labels = (
    alt.Chart(group_label_data)
    .mark_text(align="right", dx=-15, fontSize=15, fontWeight="bold")
    .encode(x=alt.value(0), y=alt.Y("y_display:Q", scale=y_scale), text="task:N")
)

# Y-axis labels - tasks (position at leftmost point of chart)
task_label_data = combined_df[~combined_df["is_group"]][["task", "y_display", "start"]].copy()
task_labels = (
    alt.Chart(task_label_data)
    .mark_text(align="right", dx=-15, fontSize=14)
    .encode(x=alt.value(0), y=alt.Y("y_display:Q", scale=y_scale), text="task:N")
)

# Dependency arrows
if not dep_df.empty:
    dep_rules = (
        alt.Chart(dep_df)
        .mark_rule(strokeWidth=2.5, opacity=0.65, color="#E74C3C", strokeDash=[6, 3])
        .encode(x=alt.X("from_x:T"), x2=alt.X2("to_x:T"), y=alt.Y("from_y:Q", scale=y_scale), y2=alt.Y2("to_y:Q"))
    )

    arrow_points = (
        alt.Chart(dep_df)
        .mark_point(shape="triangle-right", size=100, filled=True, color="#E74C3C", opacity=0.8)
        .encode(x=alt.X("to_x:T"), y=alt.Y("to_y:Q", scale=y_scale))
    )
else:
    dep_rules = alt.Chart(pd.DataFrame()).mark_rule()
    arrow_points = alt.Chart(pd.DataFrame()).mark_point()

# Create legend
legend_data = pd.DataFrame(
    [
        {"phase": "Requirements", "color": "#306998", "x": 0},
        {"phase": "Design", "color": "#FFD43B", "x": 1},
        {"phase": "Development", "color": "#4B8BBE", "x": 2},
        {"phase": "Testing", "color": "#646464", "x": 3},
        {"phase": "Deployment", "color": "#FFE873", "x": 4},
        {"phase": "Dependencies", "color": "#E74C3C", "x": 5},
    ]
)

legend_marks = (
    alt.Chart(legend_data)
    .mark_rect(width=20, height=16, cornerRadius=3)
    .encode(x=alt.X("x:O", title=None, axis=None), color=alt.Color("color:N", scale=None))
)

legend_labels = alt.Chart(legend_data).mark_text(dy=22, fontSize=13).encode(x="x:O", text="phase:N")

legend = alt.layer(legend_marks, legend_labels).properties(width=450, height=45)

# Combine main chart layers
main_chart = (
    alt.layer(group_bars, task_bars, dep_rules, arrow_points, group_labels, task_labels)
    .properties(
        width=1400,
        height=700,
        title=alt.Title("gantt-dependencies · altair · pyplots.ai", fontSize=28, anchor="middle"),
    )
    .resolve_scale(x="shared", y="shared")
)

# Vertical concat with legend
final_chart = (
    alt.vconcat(main_chart, legend, spacing=20)
    .configure_axis(labelFontSize=14, titleFontSize=18, grid=True, gridOpacity=0.25, gridDash=[3, 3])
    .configure_view(strokeWidth=0)
)

# Save
final_chart.save("plot.png", scale_factor=3.0)
final_chart.save("plot.html")
