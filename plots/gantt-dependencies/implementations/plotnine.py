"""pyplots.ai
gantt-dependencies: Gantt Chart with Dependencies
Library: plotnine | Python 3.13
Quality: pending | Created: 2026-01-15
"""

from datetime import datetime

import pandas as pd
from plotnine import (
    aes,
    element_blank,
    element_line,
    element_text,
    geom_segment,
    ggplot,
    labs,
    scale_color_manual,
    scale_x_datetime,
    scale_y_continuous,
    theme,
    theme_minimal,
)


# Data - Software development project with dependencies
tasks_data = [
    # Requirements Phase
    {
        "task": "Gather Requirements",
        "start": datetime(2024, 1, 1),
        "end": datetime(2024, 1, 10),
        "group": "Requirements",
        "depends_on": [],
    },
    {
        "task": "Document Specs",
        "start": datetime(2024, 1, 8),
        "end": datetime(2024, 1, 15),
        "group": "Requirements",
        "depends_on": ["Gather Requirements"],
    },
    {
        "task": "Review & Approve",
        "start": datetime(2024, 1, 15),
        "end": datetime(2024, 1, 18),
        "group": "Requirements",
        "depends_on": ["Document Specs"],
    },
    # Design Phase
    {
        "task": "System Architecture",
        "start": datetime(2024, 1, 18),
        "end": datetime(2024, 1, 28),
        "group": "Design",
        "depends_on": ["Review & Approve"],
    },
    {
        "task": "Database Design",
        "start": datetime(2024, 1, 25),
        "end": datetime(2024, 2, 2),
        "group": "Design",
        "depends_on": ["System Architecture"],
    },
    {
        "task": "UI/UX Mockups",
        "start": datetime(2024, 1, 20),
        "end": datetime(2024, 2, 5),
        "group": "Design",
        "depends_on": ["Review & Approve"],
    },
    # Development Phase
    {
        "task": "Backend API",
        "start": datetime(2024, 2, 3),
        "end": datetime(2024, 2, 25),
        "group": "Development",
        "depends_on": ["Database Design"],
    },
    {
        "task": "Frontend Components",
        "start": datetime(2024, 2, 6),
        "end": datetime(2024, 2, 28),
        "group": "Development",
        "depends_on": ["UI/UX Mockups"],
    },
    {
        "task": "Integration",
        "start": datetime(2024, 2, 26),
        "end": datetime(2024, 3, 5),
        "group": "Development",
        "depends_on": ["Backend API", "Frontend Components"],
    },
    # Testing Phase
    {
        "task": "Unit Testing",
        "start": datetime(2024, 2, 20),
        "end": datetime(2024, 3, 2),
        "group": "Testing",
        "depends_on": ["Backend API"],
    },
    {
        "task": "Integration Testing",
        "start": datetime(2024, 3, 5),
        "end": datetime(2024, 3, 12),
        "group": "Testing",
        "depends_on": ["Integration"],
    },
    {
        "task": "User Acceptance",
        "start": datetime(2024, 3, 12),
        "end": datetime(2024, 3, 18),
        "group": "Testing",
        "depends_on": ["Integration Testing"],
    },
]

df = pd.DataFrame(tasks_data)

# Define group colors
group_colors = {"Requirements": "#306998", "Design": "#4B8BBE", "Development": "#FFD43B", "Testing": "#646464"}

# Create ordered task list with group headers (top to bottom)
group_order = ["Requirements", "Design", "Development", "Testing"]
task_display_order = []  # Top to bottom display order
task_labels = {}  # Map y position to label

y_pos = 0
group_positions = {}
task_positions = {}

for grp in group_order:
    # Group header
    group_label = f"▸ {grp}"
    task_display_order.append({"label": group_label, "y": y_pos, "is_group": True, "group": grp})
    group_positions[grp] = y_pos
    task_labels[y_pos] = group_label
    y_pos += 1

    # Tasks in this group
    group_tasks = df[df["group"] == grp]
    for _, task_row in group_tasks.iterrows():
        task_label = f"   {task_row['task']}"
        task_display_order.append(
            {
                "label": task_label,
                "y": y_pos,
                "is_group": False,
                "group": grp,
                "task": task_row["task"],
                "start": task_row["start"],
                "end": task_row["end"],
            }
        )
        task_positions[task_row["task"]] = y_pos
        task_labels[y_pos] = task_label
        y_pos += 1

# Calculate group aggregates
group_data = []
for grp in group_order:
    group_tasks = df[df["group"] == grp]
    group_data.append(
        {
            "y": group_positions[grp],
            "start": group_tasks["start"].min(),
            "end": group_tasks["end"].max(),
            "group": grp,
            "is_group": True,
        }
    )

# Create task data with y positions
task_data = []
for grp in group_order:
    group_tasks = df[df["group"] == grp]
    for _, task_row in group_tasks.iterrows():
        task_data.append(
            {
                "y": task_positions[task_row["task"]],
                "start": task_row["start"],
                "end": task_row["end"],
                "group": grp,
                "is_group": False,
            }
        )

# Create DataFrames for plotting
tasks_df = pd.DataFrame(task_data)
groups_df = pd.DataFrame(group_data)

# Build dependency arrows
arrows_data = []
for _, row in df.iterrows():
    if row["depends_on"]:
        for dep_name in row["depends_on"]:
            if dep_name in task_positions:
                dep_row = df[df["task"] == dep_name].iloc[0]
                arrows_data.append(
                    {
                        "x_start": dep_row["end"],
                        "x_end": row["start"],
                        "y_start": task_positions[dep_name],
                        "y_end": task_positions[row["task"]],
                    }
                )

arrows_df = pd.DataFrame(arrows_data) if arrows_data else None

# Create y-axis labels and breaks
y_breaks = list(task_labels.keys())
y_labels = [task_labels[y] for y in y_breaks]

# Build the plot
plot = (
    ggplot()
    # Task bars
    + geom_segment(
        data=tasks_df, mapping=aes(x="start", xend="end", y="y", yend="y", color="group"), size=10, lineend="butt"
    )
    # Group aggregate bars (thicker)
    + geom_segment(
        data=groups_df,
        mapping=aes(x="start", xend="end", y="y", yend="y", color="group"),
        size=14,
        lineend="butt",
        alpha=0.9,
    )
)

# Add dependency arrows
if arrows_df is not None and len(arrows_df) > 0:
    plot = plot + geom_segment(
        data=arrows_df,
        mapping=aes(x="x_start", xend="x_end", y="y_start", yend="y_end"),
        color="#555555",
        size=1,
        alpha=0.7,
    )

# Add scales, labels, and theme
plot = (
    plot
    + scale_color_manual(values=group_colors, name="Phase")
    + scale_y_continuous(
        breaks=y_breaks,
        labels=y_labels,
        trans="reverse",  # Reverse so first group is at top
    )
    + scale_x_datetime()
    + labs(title="gantt-dependencies · plotnine · pyplots.ai", x="Timeline", y="")
    + theme_minimal()
    + theme(
        figure_size=(16, 9),
        plot_title=element_text(size=24, weight="bold"),
        axis_title_x=element_text(size=18),
        axis_text_x=element_text(size=14, rotation=45, ha="right"),
        axis_text_y=element_text(size=12, ha="right"),
        legend_title=element_text(size=16),
        legend_text=element_text(size=14),
        legend_position="right",
        panel_grid_major_y=element_blank(),
        panel_grid_minor=element_blank(),
        panel_grid_major_x=element_line(color="#CCCCCC", size=0.5, alpha=0.3),
    )
)

# Save the plot
plot.save("plot.png", dpi=300, width=16, height=9, verbose=False)
