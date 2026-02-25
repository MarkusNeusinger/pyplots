""" pyplots.ai
gantt-dependencies: Gantt Chart with Dependencies
Library: letsplot 4.8.2 | Python 3.14
Quality: 81/100 | Updated: 2026-02-25
"""

import pandas as pd
from lets_plot import *


LetsPlot.setup_html()

# Data - Software development project with phases and dependencies
tasks_data = [
    # Requirements phase
    {
        "task": "Gather Requirements",
        "start": "2024-01-01",
        "end": "2024-01-08",
        "group": "Requirements",
        "depends_on": [],
    },
    {
        "task": "Stakeholder Interviews",
        "start": "2024-01-03",
        "end": "2024-01-10",
        "group": "Requirements",
        "depends_on": [("Gather Requirements", "start-to-start")],
    },
    {
        "task": "Document Specs",
        "start": "2024-01-10",
        "end": "2024-01-17",
        "group": "Requirements",
        "depends_on": [("Stakeholder Interviews", "finish-to-start")],
    },
    # Design phase
    {
        "task": "Architecture Design",
        "start": "2024-01-17",
        "end": "2024-01-27",
        "group": "Design",
        "depends_on": [("Document Specs", "finish-to-start")],
    },
    {
        "task": "UI/UX Mockups",
        "start": "2024-01-20",
        "end": "2024-01-30",
        "group": "Design",
        "depends_on": [("Document Specs", "finish-to-start")],
    },
    {
        "task": "Database Schema",
        "start": "2024-01-22",
        "end": "2024-01-31",
        "group": "Design",
        "depends_on": [("Architecture Design", "start-to-start")],
    },
    # Development phase
    {
        "task": "Backend API",
        "start": "2024-01-31",
        "end": "2024-02-21",
        "group": "Development",
        "depends_on": [("Database Schema", "finish-to-start"), ("Architecture Design", "finish-to-start")],
    },
    {
        "task": "Frontend Components",
        "start": "2024-01-30",
        "end": "2024-02-18",
        "group": "Development",
        "depends_on": [("UI/UX Mockups", "finish-to-start")],
    },
    {
        "task": "Integration",
        "start": "2024-02-18",
        "end": "2024-02-28",
        "group": "Development",
        "depends_on": [("Backend API", "finish-to-finish"), ("Frontend Components", "finish-to-start")],
    },
    # Testing phase
    {
        "task": "Unit Testing",
        "start": "2024-02-10",
        "end": "2024-02-24",
        "group": "Testing",
        "depends_on": [("Backend API", "start-to-start")],
    },
    {
        "task": "Integration Testing",
        "start": "2024-02-28",
        "end": "2024-03-08",
        "group": "Testing",
        "depends_on": [("Integration", "finish-to-start")],
    },
    {
        "task": "User Acceptance",
        "start": "2024-03-08",
        "end": "2024-03-15",
        "group": "Testing",
        "depends_on": [("Integration Testing", "finish-to-start")],
    },
]

df = pd.DataFrame(tasks_data)
df["start"] = pd.to_datetime(df["start"])
df["end"] = pd.to_datetime(df["end"])

# Group ordering and colors
group_order = ["Requirements", "Design", "Development", "Testing"]
group_colors = {"Requirements": "#306998", "Design": "#E8A838", "Development": "#2CA02C", "Testing": "#9467BD"}

# Build y positions — assign in reading order top-to-bottom, then flip
y_positions = {}
task_info = {}
reading_order = []

for group in group_order:
    group_tasks = df[df["group"] == group]
    reading_order.append(group)
    task_info[group] = {
        "start": group_tasks["start"].min(),
        "end": group_tasks["end"].max(),
        "is_group": True,
        "group": group,
    }
    for _, row in group_tasks.sort_values("start").iterrows():
        reading_order.append(row["task"])
        task_info[row["task"]] = {
            "start": row["start"],
            "end": row["end"],
            "is_group": False,
            "group": row["group"],
            "depends_on": row["depends_on"],
        }

# Flip: first in reading order gets highest y (top of chart)
n = len(reading_order)
for i, name in enumerate(reading_order):
    y_positions[name] = n - 1 - i
y_pos = n

# Prepare plot dataframes
plot_data = []
for name, y in y_positions.items():
    info = task_info[name]
    plot_data.append(
        {
            "task": name,
            "y": y,
            "start": info["start"],
            "end": info["end"],
            "is_group": info["is_group"],
            "group": info["group"],
            "start_num": info["start"].timestamp(),
            "end_num": info["end"].timestamp(),
        }
    )

plot_df = pd.DataFrame(plot_data)
groups_df = plot_df[plot_df["is_group"]]
tasks_df = plot_df[~plot_df["is_group"]]

# Dependency arrow colors
dep_colors = {"finish-to-start": "#E74C3C", "start-to-start": "#3498DB", "finish-to-finish": "#27AE60"}

# Build arrow data
arrows_data = []
for task_name, info in task_info.items():
    if info["is_group"] or not info.get("depends_on"):
        continue
    for dep_name, dep_type in info["depends_on"]:
        if dep_name not in task_info:
            continue
        dep_info = task_info[dep_name]
        if dep_type == "start-to-start":
            x_from = dep_info["start"].timestamp()
            x_to = info["start"].timestamp()
        elif dep_type == "finish-to-finish":
            x_from = dep_info["end"].timestamp()
            x_to = info["end"].timestamp()
        else:
            x_from = dep_info["end"].timestamp()
            x_to = info["start"].timestamp()
        arrows_data.append(
            {
                "x": x_from,
                "y": y_positions[dep_name],
                "xend": x_to,
                "yend": y_positions[task_name],
                "dep_type": dep_type,
            }
        )

arrows_df = pd.DataFrame(arrows_data) if arrows_data else None

# Build plot
x_range = plot_df["end_num"].max() - plot_df["start_num"].min()
x_min = plot_df["start_num"].min()
x_max = plot_df["end_num"].max()

plot = ggplot()

# Alternating group background bands for visual separation
for group in group_order:
    group_y = y_positions[group]
    group_task_ys = [y_positions[t] for t, info in task_info.items() if info["group"] == group]
    y_lo = min(group_task_ys) - 0.45
    y_hi = max(group_task_ys) + 0.45
    band_color = "#F7F9FC" if group_order.index(group) % 2 == 0 else "#FFFFFF"
    band_df = pd.DataFrame(
        [{"xmin": x_min - x_range * 0.25, "xmax": x_max + x_range * 0.05, "ymin": y_lo, "ymax": y_hi}]
    )
    plot += geom_rect(aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax"), data=band_df, fill=band_color, alpha=0.8)

# Group header bars
plot += geom_segment(
    aes(x="start_num", xend="end_num", y="y", yend="y"), data=groups_df, size=14, color="#1a365d", alpha=0.95
)

# Task bars colored by group
for group in group_order:
    gdf = tasks_df[tasks_df["group"] == group]
    if not gdf.empty:
        plot += geom_segment(
            aes(x="start_num", xend="end_num", y="y", yend="y"), data=gdf, size=8, color=group_colors[group], alpha=0.85
        )

# Dependency arrows by type
if arrows_df is not None and not arrows_df.empty:
    for dep_type, color in dep_colors.items():
        type_df = arrows_df[arrows_df["dep_type"] == dep_type]
        if not type_df.empty:
            plot += geom_segment(
                aes(x="x", xend="xend", y="y", yend="yend"),
                data=type_df,
                size=1.2,
                color=color,
                alpha=0.85,
                arrow=arrow(angle=25, length=10, type="closed"),
            )

# Labels on the left side of bars for tasks, right for groups
label_offset = x_range * 0.008

group_labels = groups_df.copy()
group_labels["label_x"] = group_labels["end_num"] + label_offset

task_labels = tasks_df.copy()
task_labels["label_x"] = task_labels["start_num"] - label_offset

plot += geom_text(
    aes(x="label_x", y="y", label="task"), data=group_labels, hjust=0, size=12, fontface="bold", color="#1a365d"
)
plot += geom_text(aes(x="label_x", y="y", label="task"), data=task_labels, hjust=1, size=10, color="#333333")

# Date axis
date_range = pd.date_range("2024-01-01", "2024-03-18", freq="2W")
date_breaks = [d.timestamp() for d in date_range]
date_labels_fmt = [d.strftime("%b %d") for d in date_range]

# Legend for dependency types (bottom right)
legend_y = -2.0
legend_x = x_max - x_range * 0.15
legend_items = pd.DataFrame(
    [
        {
            "x": legend_x,
            "xend": legend_x + x_range * 0.05,
            "y": legend_y,
            "label": "Finish-to-Start",
            "color": "#E74C3C",
        },
        {
            "x": legend_x,
            "xend": legend_x + x_range * 0.05,
            "y": legend_y - 0.9,
            "label": "Start-to-Start",
            "color": "#3498DB",
        },
        {
            "x": legend_x,
            "xend": legend_x + x_range * 0.05,
            "y": legend_y - 1.8,
            "label": "Finish-to-Finish",
            "color": "#27AE60",
        },
    ]
)

plot += geom_text(
    aes(x="x", y="y", label="label"),
    data=pd.DataFrame([{"x": legend_x, "y": legend_y + 0.9, "label": "Dependencies:"}]),
    hjust=0,
    size=12,
    fontface="bold",
    color="#222222",
)

for _, row in legend_items.iterrows():
    plot += geom_segment(
        aes(x="x", xend="xend", y="y", yend="y"),
        data=pd.DataFrame([row]),
        size=1.2,
        color=row["color"],
        arrow=arrow(angle=25, length=10, type="closed"),
    )

plot += geom_text(
    aes(x="xend", y="y", label="label"),
    data=legend_items.assign(xend=legend_items["xend"] + x_range * 0.008),
    hjust=0,
    size=10,
    color="#333333",
)

# Theme and formatting
x_left_pad = x_range * 0.25
x_right_pad = x_range * 0.15

plot += scale_x_continuous(breaks=date_breaks, labels=date_labels_fmt, limits=[x_min - x_left_pad, x_max + x_right_pad])
plot += scale_y_continuous(breaks=[], labels=[], limits=[-5.0, y_pos + 0.5])
plot += labs(x="Timeline", y="", title="gantt-dependencies \u00b7 letsplot \u00b7 pyplots.ai")
plot += theme_minimal()
plot += theme(
    axis_title_x=element_text(size=22),
    axis_title_y=element_blank(),
    axis_text_x=element_text(size=18, angle=45),
    axis_text_y=element_blank(),
    plot_title=element_text(size=28),
    panel_grid_major_y=element_blank(),
    panel_grid_minor=element_blank(),
    panel_grid_major_x=element_line(color="#E0E4E8", size=0.5),
)
plot += ggsize(1600, 900)

# Save
ggsave(plot, "plot.png", scale=3)
ggsave(plot, "plot.html")
