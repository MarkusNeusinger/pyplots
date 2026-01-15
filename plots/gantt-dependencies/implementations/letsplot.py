""" pyplots.ai
gantt-dependencies: Gantt Chart with Dependencies
Library: letsplot 4.8.2 | Python 3.13.11
Quality: 88/100 | Created: 2026-01-15
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
        "depends_on": ["Gather Requirements"],
    },
    {
        "task": "Document Specs",
        "start": "2024-01-08",
        "end": "2024-01-15",
        "group": "Requirements",
        "depends_on": ["Stakeholder Interviews"],
    },
    # Design phase
    {
        "task": "Architecture Design",
        "start": "2024-01-15",
        "end": "2024-01-25",
        "group": "Design",
        "depends_on": ["Document Specs"],
    },
    {
        "task": "UI/UX Mockups",
        "start": "2024-01-18",
        "end": "2024-01-28",
        "group": "Design",
        "depends_on": ["Document Specs"],
    },
    {
        "task": "Database Schema",
        "start": "2024-01-22",
        "end": "2024-01-30",
        "group": "Design",
        "depends_on": ["Architecture Design"],
    },
    # Development phase
    {
        "task": "Backend API",
        "start": "2024-01-30",
        "end": "2024-02-20",
        "group": "Development",
        "depends_on": ["Database Schema", "Architecture Design"],
    },
    {
        "task": "Frontend Components",
        "start": "2024-01-30",
        "end": "2024-02-18",
        "group": "Development",
        "depends_on": ["UI/UX Mockups"],
    },
    {
        "task": "Integration",
        "start": "2024-02-18",
        "end": "2024-02-28",
        "group": "Development",
        "depends_on": ["Backend API", "Frontend Components"],
    },
    # Testing phase
    {
        "task": "Unit Testing",
        "start": "2024-02-15",
        "end": "2024-02-25",
        "group": "Testing",
        "depends_on": ["Backend API"],
    },
    {
        "task": "Integration Testing",
        "start": "2024-02-28",
        "end": "2024-03-08",
        "group": "Testing",
        "depends_on": ["Integration"],
    },
    {
        "task": "User Acceptance",
        "start": "2024-03-08",
        "end": "2024-03-15",
        "group": "Testing",
        "depends_on": ["Integration Testing"],
    },
]

df = pd.DataFrame(tasks_data)
df["start"] = pd.to_datetime(df["start"])
df["end"] = pd.to_datetime(df["end"])

# Create task order (grouped by phase, with group headers)
group_order = ["Requirements", "Design", "Development", "Testing"]
group_colors = {"Requirements": "#306998", "Design": "#FFD43B", "Development": "#2CA02C", "Testing": "#9467BD"}

# Build ordered task list with y positions
y_positions = {}
task_info = {}
y_pos = 0

for group in group_order:
    group_tasks = df[df["group"] == group]
    # Group header position
    y_positions[f"[{group}]"] = y_pos
    task_info[f"[{group}]"] = {
        "start": group_tasks["start"].min(),
        "end": group_tasks["end"].max(),
        "is_group": True,
        "group": group,
    }
    y_pos += 1
    # Individual tasks
    for _, row in group_tasks.iterrows():
        y_positions[row["task"]] = y_pos
        task_info[row["task"]] = {
            "start": row["start"],
            "end": row["end"],
            "is_group": False,
            "group": row["group"],
            "depends_on": row["depends_on"],
        }
        y_pos += 1

# Prepare data for plotting
plot_data = []
for task_name, y in y_positions.items():
    info = task_info[task_name]
    plot_data.append(
        {
            "task": task_name,
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

# Separate group headers and tasks
groups_df = plot_df[plot_df["is_group"]]
tasks_df = plot_df[~plot_df["is_group"]]

# Create dependency arrows data
arrows_data = []
for task_name, info in task_info.items():
    if not info["is_group"] and info.get("depends_on"):
        for dep in info["depends_on"]:
            if dep in task_info:
                dep_info = task_info[dep]
                # Arrow from end of dependency to start of task
                arrows_data.append(
                    {
                        "x": dep_info["end"].timestamp(),
                        "y": y_positions[dep],
                        "xend": info["start"].timestamp(),
                        "yend": y_positions[task_name],
                    }
                )

arrows_df = pd.DataFrame(arrows_data) if arrows_data else None

# Build the plot
plot = ggplot()

# Add group header bars (darker, full width)
plot = plot + geom_segment(
    aes(x="start_num", xend="end_num", y="y", yend="y"), data=groups_df, size=12, color="#1a365d", alpha=0.9
)

# Add task bars with color by group
for group in group_order:
    group_tasks = tasks_df[tasks_df["group"] == group]
    if not group_tasks.empty:
        plot = plot + geom_segment(
            aes(x="start_num", xend="end_num", y="y", yend="y"),
            data=group_tasks,
            size=8,
            color=group_colors[group],
            alpha=0.85,
        )

# Add dependency arrows
if arrows_df is not None and not arrows_df.empty:
    plot = plot + geom_segment(
        aes(x="x", xend="xend", y="y", yend="yend"),
        data=arrows_df,
        size=0.8,
        color="#666666",
        alpha=0.7,
        arrow=arrow(angle=20, length=8, type="closed"),
    )

# Add task labels on the right side of bars
all_labels = plot_df.copy()
all_labels["label_x"] = all_labels["end_num"] + (plot_df["end_num"].max() - plot_df["start_num"].min()) * 0.01
plot = plot + geom_text(aes(x="label_x", y="y", label="task"), data=all_labels, hjust=0, size=9, color="#333333")

# Create date axis breaks and labels
date_range = pd.date_range("2024-01-01", "2024-03-15", freq="2W")
date_breaks = [d.timestamp() for d in date_range]
date_labels = [d.strftime("%b %d") for d in date_range]

# Calculate x-axis limits with padding for labels
x_min = plot_df["start_num"].min()
x_max = plot_df["end_num"].max()
x_range = x_max - x_min
x_padding = x_range * 0.25  # 25% padding on right for labels

# Apply theme and formatting
plot = (
    plot
    + scale_x_continuous(breaks=date_breaks, labels=date_labels, limits=[x_min - x_range * 0.02, x_max + x_padding])
    + scale_y_continuous(breaks=[], labels=[])
    + labs(x="Timeline", y="", title="gantt-dependencies \u00b7 letsplot \u00b7 pyplots.ai")
    + theme_minimal()
    + theme(
        axis_title_x=element_text(size=20),
        axis_title_y=element_blank(),
        axis_text_x=element_text(size=16, angle=45),
        axis_text_y=element_blank(),
        plot_title=element_text(size=24),
        panel_grid_major_y=element_blank(),
        panel_grid_minor=element_blank(),
        panel_grid_major_x=element_line(color="#E5E5E5", size=0.5),
    )
    + ggsize(1600, 900)
)

# Save outputs
ggsave(plot, "plot.png", scale=3)
ggsave(plot, "plot.html")
