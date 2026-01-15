"""pyplots.ai
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
        "dep_type": None,
    },
    {
        "task": "Stakeholder Interviews",
        "start": "2024-01-03",
        "end": "2024-01-10",
        "group": "Requirements",
        "depends_on": ["Gather Requirements"],
        "dep_type": "start-to-start",
    },
    {
        "task": "Document Specs",
        "start": "2024-01-08",
        "end": "2024-01-15",
        "group": "Requirements",
        "depends_on": ["Stakeholder Interviews"],
        "dep_type": "finish-to-start",
    },
    # Design phase
    {
        "task": "Architecture Design",
        "start": "2024-01-15",
        "end": "2024-01-25",
        "group": "Design",
        "depends_on": ["Document Specs"],
        "dep_type": "finish-to-start",
    },
    {
        "task": "UI/UX Mockups",
        "start": "2024-01-18",
        "end": "2024-01-28",
        "group": "Design",
        "depends_on": ["Document Specs"],
        "dep_type": "finish-to-start",
    },
    {
        "task": "Database Schema",
        "start": "2024-01-22",
        "end": "2024-01-30",
        "group": "Design",
        "depends_on": ["Architecture Design"],
        "dep_type": "start-to-start",
    },
    # Development phase
    {
        "task": "Backend API",
        "start": "2024-01-30",
        "end": "2024-02-20",
        "group": "Development",
        "depends_on": ["Database Schema", "Architecture Design"],
        "dep_type": "finish-to-start",
    },
    {
        "task": "Frontend Components",
        "start": "2024-01-30",
        "end": "2024-02-18",
        "group": "Development",
        "depends_on": ["UI/UX Mockups"],
        "dep_type": "finish-to-start",
    },
    {
        "task": "Integration",
        "start": "2024-02-18",
        "end": "2024-02-28",
        "group": "Development",
        "depends_on": ["Backend API", "Frontend Components"],
        "dep_type": "finish-to-finish",
    },
    # Testing phase
    {
        "task": "Unit Testing",
        "start": "2024-02-15",
        "end": "2024-02-25",
        "group": "Testing",
        "depends_on": ["Backend API"],
        "dep_type": "start-to-start",
    },
    {
        "task": "Integration Testing",
        "start": "2024-02-28",
        "end": "2024-03-08",
        "group": "Testing",
        "depends_on": ["Integration"],
        "dep_type": "finish-to-start",
    },
    {
        "task": "User Acceptance",
        "start": "2024-03-08",
        "end": "2024-03-15",
        "group": "Testing",
        "depends_on": ["Integration Testing"],
        "dep_type": "finish-to-start",
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
            "dep_type": row["dep_type"],
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

# Dependency type colors and styles
dep_colors = {
    "finish-to-start": "#E74C3C",  # Red - most common
    "start-to-start": "#3498DB",  # Blue
    "finish-to-finish": "#27AE60",  # Green
}

# Create dependency arrows data with different types
arrows_data = []
for task_name, info in task_info.items():
    if not info["is_group"] and info.get("depends_on"):
        dep_type = info.get("dep_type", "finish-to-start")
        for dep in info["depends_on"]:
            if dep in task_info:
                dep_info = task_info[dep]
                # Arrow coordinates depend on dependency type
                if dep_type == "start-to-start":
                    x_start = dep_info["start"].timestamp()
                    x_end = info["start"].timestamp()
                elif dep_type == "finish-to-finish":
                    x_start = dep_info["end"].timestamp()
                    x_end = info["end"].timestamp()
                else:  # finish-to-start (default)
                    x_start = dep_info["end"].timestamp()
                    x_end = info["start"].timestamp()
                arrows_data.append(
                    {
                        "x": x_start,
                        "y": y_positions[dep],
                        "xend": x_end,
                        "yend": y_positions[task_name],
                        "dep_type": dep_type if dep_type else "finish-to-start",
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

# Add dependency arrows with different colors per type
if arrows_df is not None and not arrows_df.empty:
    for dep_type, color in dep_colors.items():
        type_arrows = arrows_df[arrows_df["dep_type"] == dep_type]
        if not type_arrows.empty:
            plot = plot + geom_segment(
                aes(x="x", xend="xend", y="y", yend="yend"),
                data=type_arrows,
                size=1.2,
                color=color,
                alpha=0.85,
                arrow=arrow(angle=25, length=10, type="closed"),
            )

# Add task labels on the right side of bars
all_labels = plot_df.copy()
all_labels["label_x"] = all_labels["end_num"] + (plot_df["end_num"].max() - plot_df["start_num"].min()) * 0.01
plot = plot + geom_text(aes(x="label_x", y="y", label="task"), data=all_labels, hjust=0, size=11, color="#222222")

# Create date axis breaks and labels
date_range = pd.date_range("2024-01-01", "2024-03-15", freq="2W")
date_breaks = [d.timestamp() for d in date_range]
date_labels = [d.strftime("%b %d") for d in date_range]

# Calculate x-axis limits with padding for labels
x_min = plot_df["start_num"].min()
x_max = plot_df["end_num"].max()
x_range = x_max - x_min
x_padding = x_range * 0.30  # 30% padding on right for labels and legend

# Add legend for dependency types (positioned in lower right area)
legend_y_start = -0.5
legend_x = x_max + x_range * 0.12
legend_data = pd.DataFrame(
    [
        {
            "x": legend_x,
            "xend": legend_x + x_range * 0.06,
            "y": legend_y_start,
            "label": "Finish-to-Start",
            "color": "#E74C3C",
        },
        {
            "x": legend_x,
            "xend": legend_x + x_range * 0.06,
            "y": legend_y_start - 0.8,
            "label": "Start-to-Start",
            "color": "#3498DB",
        },
        {
            "x": legend_x,
            "xend": legend_x + x_range * 0.06,
            "y": legend_y_start - 1.6,
            "label": "Finish-to-Finish",
            "color": "#27AE60",
        },
    ]
)

# Add legend title
plot = plot + geom_text(
    aes(x="x", y="y", label="label"),
    data=pd.DataFrame([{"x": legend_x, "y": legend_y_start + 0.8, "label": "Dependencies:"}]),
    hjust=0,
    size=12,
    fontface="bold",
    color="#222222",
)

# Add legend items (arrows and labels)
for _, row in legend_data.iterrows():
    plot = plot + geom_segment(
        aes(x="x", xend="xend", y="y", yend="y"),
        data=pd.DataFrame([row]),
        size=1.2,
        color=row["color"],
        arrow=arrow(angle=25, length=10, type="closed"),
    )

plot = plot + geom_text(
    aes(x="xend", y="y", label="label"),
    data=legend_data.assign(xend=legend_data["xend"] + x_range * 0.01),
    hjust=0,
    size=10,
    color="#333333",
)

# Apply theme and formatting
plot = (
    plot
    + scale_x_continuous(breaks=date_breaks, labels=date_labels, limits=[x_min - x_range * 0.02, x_max + x_padding])
    + scale_y_continuous(breaks=[], labels=[], limits=[-2.5, y_pos + 0.5])
    + labs(x="Timeline", y="", title="gantt-dependencies \u00b7 letsplot \u00b7 pyplots.ai")
    + theme_minimal()
    + theme(
        axis_title_x=element_text(size=22),
        axis_title_y=element_blank(),
        axis_text_x=element_text(size=18, angle=45),
        axis_text_y=element_blank(),
        plot_title=element_text(size=28),
        panel_grid_major_y=element_blank(),
        panel_grid_minor=element_blank(),
        panel_grid_major_x=element_line(color="#E5E5E5", size=0.5),
    )
    + ggsize(1600, 900)
)

# Save outputs
ggsave(plot, "plot.png", scale=3)
ggsave(plot, "plot.html")
