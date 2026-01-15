""" pyplots.ai
gantt-dependencies: Gantt Chart with Dependencies
Library: bokeh 3.8.2 | Python 3.13.11
Quality: 85/100 | Created: 2026-01-15
"""

import pandas as pd
from bokeh.io import export_png
from bokeh.models import ColumnDataSource, LabelSet, Legend, LegendItem
from bokeh.plotting import figure, output_file, save


# Data - Software development project with dependencies
tasks_data = [
    # Requirements Phase
    {
        "task": "Requirements Gathering",
        "start": "2026-01-06",
        "end": "2026-01-10",
        "group": "Requirements",
        "depends_on": [],
    },
    {
        "task": "Stakeholder Review",
        "start": "2026-01-13",
        "end": "2026-01-15",
        "group": "Requirements",
        "depends_on": ["Requirements Gathering"],
    },
    {
        "task": "Requirements Sign-off",
        "start": "2026-01-16",
        "end": "2026-01-17",
        "group": "Requirements",
        "depends_on": ["Stakeholder Review"],
    },
    # Design Phase
    {
        "task": "System Architecture",
        "start": "2026-01-20",
        "end": "2026-01-24",
        "group": "Design",
        "depends_on": ["Requirements Sign-off"],
    },
    {
        "task": "Database Design",
        "start": "2026-01-27",
        "end": "2026-01-30",
        "group": "Design",
        "depends_on": ["System Architecture"],
    },
    {
        "task": "UI/UX Design",
        "start": "2026-01-27",
        "end": "2026-01-31",
        "group": "Design",
        "depends_on": ["System Architecture"],
    },
    # Development Phase
    {
        "task": "Backend Core",
        "start": "2026-02-03",
        "end": "2026-02-14",
        "group": "Development",
        "depends_on": ["Database Design"],
    },
    {
        "task": "Frontend Core",
        "start": "2026-02-03",
        "end": "2026-02-12",
        "group": "Development",
        "depends_on": ["UI/UX Design"],
    },
    {
        "task": "API Integration",
        "start": "2026-02-17",
        "end": "2026-02-21",
        "group": "Development",
        "depends_on": ["Backend Core", "Frontend Core"],
    },
    # Testing Phase
    {
        "task": "Unit Testing",
        "start": "2026-02-17",
        "end": "2026-02-21",
        "group": "Testing",
        "depends_on": ["Backend Core"],
    },
    {
        "task": "Integration Testing",
        "start": "2026-02-24",
        "end": "2026-02-28",
        "group": "Testing",
        "depends_on": ["API Integration", "Unit Testing"],
    },
    {
        "task": "User Acceptance",
        "start": "2026-03-03",
        "end": "2026-03-07",
        "group": "Testing",
        "depends_on": ["Integration Testing"],
    },
]

# Convert to DataFrame
df = pd.DataFrame(tasks_data)
df["start"] = pd.to_datetime(df["start"])
df["end"] = pd.to_datetime(df["end"])

# Create task lookup for dependencies
task_lookup = {row["task"]: idx for idx, row in df.iterrows()}

# Define groups and colors
groups = ["Requirements", "Design", "Development", "Testing"]
group_colors = {"Requirements": "#306998", "Design": "#FFD43B", "Development": "#4CAF50", "Testing": "#E91E63"}

# Calculate group spans
group_spans = {}
for group in groups:
    group_df = df[df["group"] == group]
    group_spans[group] = {"start": group_df["start"].min(), "end": group_df["end"].max()}

# Build y-positions using numeric indices
y_positions = {}
y_labels = []
current_y = 0

for group in groups:
    # Group header
    y_positions[f"__group__{group}"] = current_y
    y_labels.append((current_y, group))
    current_y += 1
    # Tasks in this group (indented)
    group_tasks = df[df["group"] == group]["task"].tolist()
    for task in group_tasks:
        y_positions[task] = current_y
        y_labels.append((current_y, f"    {task}"))
        current_y += 1

max_y = current_y

# Create figure with numeric y-axis
p = figure(
    width=4800,
    height=2700,
    x_axis_type="datetime",
    y_range=(max_y + 0.5, -0.5),
    title="gantt-dependencies · bokeh · pyplots.ai",
    x_axis_label="Timeline",
    tools="",
)

# Style
p.title.text_font_size = "32pt"
p.xaxis.axis_label_text_font_size = "24pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.visible = False
p.xgrid.grid_line_alpha = 0.3
p.ygrid.grid_line_alpha = 0.0

# Draw group span bars (lighter background)
group_renderers = {}
for group in groups:
    span = group_spans[group]
    y = y_positions[f"__group__{group}"]
    source = ColumnDataSource(data={"y": [y], "left": [span["start"]], "right": [span["end"]], "height": [0.7]})
    r = p.hbar(y="y", left="left", right="right", height="height", color=group_colors[group], alpha=0.35, source=source)
    group_renderers[group] = r

# Draw task bars
for _, row in df.iterrows():
    y = y_positions[row["task"]]
    source = ColumnDataSource(data={"y": [y], "left": [row["start"]], "right": [row["end"]], "height": [0.55]})
    p.hbar(
        y="y", left="left", right="right", height="height", color=group_colors[row["group"]], alpha=0.9, source=source
    )

# Draw dependency arrows using multi_line with arrowheads
arrow_xs = []
arrow_ys = []
arrowhead_xs = []
arrowhead_ys = []

for _, row in df.iterrows():
    task_name = row["task"]
    task_y = y_positions[task_name]
    task_start = row["start"].value / 1e6  # Convert to ms for plotting

    for dep_name in row["depends_on"]:
        if dep_name in task_lookup:
            dep_row = df.iloc[task_lookup[dep_name]]
            dep_end = dep_row["end"].value / 1e6
            dep_y = y_positions[dep_name]

            # Create connector path: horizontal from dep end, then vertical, then horizontal to task start
            mid_x = (dep_end + task_start) / 2

            # Simple path: end of dep -> down/up -> start of task
            if abs(task_y - dep_y) < 0.1:
                # Same row (shouldn't happen, but handle it)
                arrow_xs.append([dep_end, task_start])
                arrow_ys.append([dep_y, task_y])
            else:
                # Multi-segment path
                arrow_xs.append([dep_end, mid_x, mid_x, task_start])
                arrow_ys.append([dep_y, dep_y, task_y, task_y])

            # Arrowhead (small triangle pointing right)
            arrow_size = 3 * 24 * 60 * 60 * 1000  # 3 days in ms for arrowhead
            arrowhead_xs.append([task_start - arrow_size, task_start, task_start - arrow_size])
            arrowhead_ys.append([task_y - 0.15, task_y, task_y + 0.15])

# Draw dependency lines
if arrow_xs:
    p.multi_line(xs=arrow_xs, ys=arrow_ys, line_color="#555555", line_width=2.5, line_alpha=0.7)

# Draw arrowheads
if arrowhead_xs:
    p.patches(
        xs=arrowhead_xs, ys=arrowhead_ys, fill_color="#555555", fill_alpha=0.8, line_color="#555555", line_width=1
    )

# Add y-axis labels manually
label_source = ColumnDataSource(
    data={
        "y": [y for y, _ in y_labels],
        "text": [label for _, label in y_labels],
        "x": [df["start"].min() - pd.Timedelta(days=1)] * len(y_labels),
    }
)
labels = LabelSet(
    x="x",
    y="y",
    text="text",
    source=label_source,
    text_font_size="16pt",
    text_align="right",
    x_offset=-10,
    y_offset=0,
    text_baseline="middle",
)
p.add_layout(labels)

# Adjust x range to make room for labels
x_min = df["start"].min() - pd.Timedelta(days=12)
x_max = df["end"].max() + pd.Timedelta(days=3)
p.x_range.start = x_min
p.x_range.end = x_max

# Add legend
legend_items = []
for group in groups:
    legend_items.append(LegendItem(label=group, renderers=[group_renderers[group]]))

legend = Legend(items=legend_items, location="top_right", label_text_font_size="18pt", spacing=10, padding=15)
p.add_layout(legend, "right")

# Remove toolbar
p.toolbar_location = None

# Save PNG
export_png(p, filename="plot.png")

# Save HTML (interactive)
output_file("plot.html", title="gantt-dependencies · bokeh · pyplots.ai")
save(p)
