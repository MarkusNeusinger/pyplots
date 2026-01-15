""" pyplots.ai
gantt-dependencies: Gantt Chart with Dependencies
Library: matplotlib 3.10.8 | Python 3.13.11
Quality: 91/100 | Created: 2026-01-15
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyArrowPatch


# Data - Software development project with phases and dependencies
np.random.seed(42)

tasks_data = {
    "task": [
        # Requirements Phase
        "Requirements Phase",
        "Gather Requirements",
        "Document Specs",
        "Review Requirements",
        # Design Phase
        "Design Phase",
        "System Architecture",
        "Database Design",
        "UI/UX Design",
        "Design Review",
        # Development Phase
        "Development Phase",
        "Backend Development",
        "Frontend Development",
        "API Integration",
        "Code Review",
        # Testing Phase
        "Testing Phase",
        "Unit Testing",
        "Integration Testing",
        "User Acceptance Testing",
    ],
    "start": [
        # Requirements Phase
        pd.Timestamp("2024-01-01"),
        pd.Timestamp("2024-01-01"),
        pd.Timestamp("2024-01-08"),
        pd.Timestamp("2024-01-15"),
        # Design Phase
        pd.Timestamp("2024-01-22"),
        pd.Timestamp("2024-01-22"),
        pd.Timestamp("2024-01-29"),
        pd.Timestamp("2024-01-29"),
        pd.Timestamp("2024-02-12"),
        # Development Phase
        pd.Timestamp("2024-02-19"),
        pd.Timestamp("2024-02-19"),
        pd.Timestamp("2024-02-26"),
        pd.Timestamp("2024-03-11"),
        pd.Timestamp("2024-03-25"),
        # Testing Phase
        pd.Timestamp("2024-04-01"),
        pd.Timestamp("2024-04-01"),
        pd.Timestamp("2024-04-08"),
        pd.Timestamp("2024-04-15"),
    ],
    "end": [
        # Requirements Phase
        pd.Timestamp("2024-01-19"),
        pd.Timestamp("2024-01-07"),
        pd.Timestamp("2024-01-14"),
        pd.Timestamp("2024-01-19"),
        # Design Phase
        pd.Timestamp("2024-02-16"),
        pd.Timestamp("2024-02-02"),
        pd.Timestamp("2024-02-09"),
        pd.Timestamp("2024-02-09"),
        pd.Timestamp("2024-02-16"),
        # Development Phase
        pd.Timestamp("2024-03-29"),
        pd.Timestamp("2024-03-08"),
        pd.Timestamp("2024-03-15"),
        pd.Timestamp("2024-03-22"),
        pd.Timestamp("2024-03-29"),
        # Testing Phase
        pd.Timestamp("2024-04-26"),
        pd.Timestamp("2024-04-07"),
        pd.Timestamp("2024-04-14"),
        pd.Timestamp("2024-04-26"),
    ],
    "group": [
        # Requirements Phase
        None,
        "Requirements Phase",
        "Requirements Phase",
        "Requirements Phase",
        # Design Phase
        None,
        "Design Phase",
        "Design Phase",
        "Design Phase",
        "Design Phase",
        # Development Phase
        None,
        "Development Phase",
        "Development Phase",
        "Development Phase",
        "Development Phase",
        # Testing Phase
        None,
        "Testing Phase",
        "Testing Phase",
        "Testing Phase",
    ],
    "depends_on": [
        # Requirements Phase
        [],
        [],
        ["Gather Requirements"],
        ["Document Specs"],
        # Design Phase
        ["Requirements Phase"],
        [],
        ["System Architecture"],
        ["System Architecture"],
        ["Database Design", "UI/UX Design"],
        # Development Phase
        ["Design Phase"],
        [],
        ["Backend Development"],
        ["Backend Development", "Frontend Development"],
        ["API Integration"],
        # Testing Phase
        ["Development Phase"],
        [],
        ["Unit Testing"],
        ["Integration Testing"],
    ],
}

df = pd.DataFrame(tasks_data)

# Calculate durations in days
df["duration"] = (df["end"] - df["start"]).dt.days

# Create task index mapping for y-position
task_to_idx = {task: i for i, task in enumerate(df["task"])}

# Define colors for each phase
phase_colors = {
    "Requirements Phase": "#306998",  # Python Blue
    "Design Phase": "#FFD43B",  # Python Yellow
    "Development Phase": "#4CAF50",  # Green
    "Testing Phase": "#E91E63",  # Pink
}

# Create figure
fig, ax = plt.subplots(figsize=(16, 9))

# Plot bars
bar_height = 0.6
group_bar_height = 0.4

for _idx, row in df.iterrows():
    task = row["task"]
    start = row["start"]
    duration = row["duration"]
    group = row["group"]
    y_pos = len(df) - 1 - task_to_idx[task]

    # Determine if this is a group header (phase summary)
    is_group = group is None and task in phase_colors

    if is_group:
        # Group header bar - darker color, smaller height
        color = phase_colors[task]
        ax.barh(
            y_pos, duration, left=start, height=group_bar_height, color=color, alpha=0.9, edgecolor="black", linewidth=2
        )
    else:
        # Regular task bar
        if group and group in phase_colors:
            color = phase_colors[group]
        else:
            color = "#306998"
        ax.barh(y_pos, duration, left=start, height=bar_height, color=color, alpha=0.7, edgecolor="black", linewidth=1)

# Draw dependency arrows
arrow_style = "Simple, head_width=8, head_length=6"

for _idx, row in df.iterrows():
    task = row["task"]
    depends = row["depends_on"]
    y_pos = len(df) - 1 - task_to_idx[task]
    task_start = row["start"]

    for dep in depends:
        if dep in task_to_idx:
            dep_idx = task_to_idx[dep]
            dep_y_pos = len(df) - 1 - dep_idx
            dep_row = df[df["task"] == dep].iloc[0]
            dep_end = dep_row["end"]

            # Calculate arrow positions
            # Arrow starts from end of dependency task
            start_x = dep_end
            start_y = dep_y_pos

            # Arrow ends at start of current task
            end_x = task_start
            end_y = y_pos

            # Draw connecting arrow with curved path
            arrow = FancyArrowPatch(
                (start_x, start_y),
                (end_x, end_y),
                arrowstyle="->",
                color="#555555",
                linewidth=2,
                connectionstyle="arc3,rad=0.15",
                alpha=0.7,
                mutation_scale=15,
            )
            ax.add_patch(arrow)

# Format y-axis with task names
task_labels = df["task"].tolist()[::-1]  # Reverse to match bar positions
y_positions = range(len(task_labels))

# Style task labels - indent child tasks
styled_labels = []
for label in task_labels:
    row = df[df["task"] == label].iloc[0]
    if row["group"] is not None:
        styled_labels.append(f"    {label}")  # Indent child tasks
    else:
        styled_labels.append(label)

ax.set_yticks(y_positions)
ax.set_yticklabels(styled_labels, fontsize=14)

# Format x-axis with dates
ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%b %d"))
ax.xaxis.set_major_locator(plt.matplotlib.dates.WeekdayLocator(interval=2))
plt.xticks(rotation=45, ha="right", fontsize=14)

# Labels and title
ax.set_xlabel("Timeline", fontsize=20)
ax.set_ylabel("Tasks", fontsize=20)
ax.set_title("gantt-dependencies · matplotlib · pyplots.ai", fontsize=24)

# Grid - subtle vertical lines for timeline
ax.grid(True, axis="x", alpha=0.3, linestyle="--")
ax.set_axisbelow(True)

# Create legend for phases
legend_patches = [mpatches.Patch(color=color, alpha=0.7, label=phase) for phase, color in phase_colors.items()]
legend_patches.append(mpatches.FancyArrow(0, 0, 1, 0, color="#555555", width=0.1, label="Dependency"))
ax.legend(
    handles=legend_patches[:4],  # Just phase colors
    loc="upper right",
    fontsize=14,
    framealpha=0.9,
)

# Add dependency arrow to legend manually via annotation
ax.annotate("→ Dependency", xy=(0.88, 0.72), xycoords="axes fraction", fontsize=14, color="#555555")

# Adjust layout
ax.set_xlim(df["start"].min() - pd.Timedelta(days=3), df["end"].max() + pd.Timedelta(days=3))

plt.tight_layout()
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
