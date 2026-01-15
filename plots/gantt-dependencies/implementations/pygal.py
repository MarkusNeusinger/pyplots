""" pyplots.ai
gantt-dependencies: Gantt Chart with Dependencies
Library: pygal 3.1.0 | Python 3.13.11
Quality: 91/100 | Created: 2026-01-15
"""

from datetime import date

import cairosvg
import pygal
from pygal.style import Style


# Custom style for large canvas (4800x2700)
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#4ECDC4", "#E74C3C", "#9B59B6"),
    title_font_size=60,
    label_font_size=26,
    major_label_font_size=26,
    legend_font_size=28,
    value_font_size=24,
    tooltip_font_size=24,
)

# Software Development Project with Dependencies
# Each tuple: (task_id, task_name, category, start_date, end_date, depends_on_ids)
tasks = [
    # Requirements Phase
    (1, "Requirements Gathering", "Requirements", date(2025, 1, 6), date(2025, 1, 17), []),
    (2, "Stakeholder Interviews", "Requirements", date(2025, 1, 13), date(2025, 1, 24), [1]),
    (3, "Requirements Document", "Requirements", date(2025, 1, 27), date(2025, 2, 7), [2]),
    # Design Phase
    (4, "Architecture Design", "Design", date(2025, 2, 3), date(2025, 2, 14), [3]),
    (5, "UI/UX Design", "Design", date(2025, 2, 3), date(2025, 2, 21), [3]),
    (6, "Database Schema", "Design", date(2025, 2, 17), date(2025, 2, 28), [4]),
    (7, "API Specification", "Design", date(2025, 2, 24), date(2025, 3, 7), [4]),
    # Development Phase
    (8, "Backend Development", "Development", date(2025, 3, 3), date(2025, 3, 28), [6, 7]),
    (9, "Frontend Development", "Development", date(2025, 3, 10), date(2025, 4, 4), [5, 7]),
    (10, "Integration", "Development", date(2025, 3, 31), date(2025, 4, 11), [8, 9]),
    # Testing Phase
    (11, "Unit Testing", "Testing", date(2025, 3, 17), date(2025, 4, 4), [8]),
    (12, "Integration Testing", "Testing", date(2025, 4, 7), date(2025, 4, 18), [10]),
    (13, "User Acceptance Testing", "Testing", date(2025, 4, 14), date(2025, 4, 25), [12]),
    # Deployment Phase
    (14, "Deployment Prep", "Deployment", date(2025, 4, 21), date(2025, 4, 28), [12]),
    (15, "Production Deployment", "Deployment", date(2025, 4, 28), date(2025, 5, 2), [13, 14]),
    (16, "Post-Launch Support", "Deployment", date(2025, 5, 5), date(2025, 5, 16), [15]),
]

# Create lookup for task by id
task_by_id = {t[0]: t for t in tasks}

# Reference date for day calculations
reference_date = date(2025, 1, 1)

# Category colors
category_colors = {
    "Requirements": "#306998",
    "Design": "#FFD43B",
    "Development": "#4ECDC4",
    "Testing": "#E74C3C",
    "Deployment": "#9B59B6",
}

# Calculate date range
all_dates = []
for _, _, _, start, end, _ in tasks:
    all_dates.extend([start, end])
min_date = min(all_dates)
max_date = max(all_dates)

# X-axis range in days
start_day = (min_date - reference_date).days - 5
end_day = (max_date - reference_date).days + 5
day_range = end_day - start_day

# Task labels for y-axis
task_labels = [t[1] for t in tasks]
num_tasks = len(tasks)

# Create pygal HorizontalBar chart as base structure
chart = pygal.HorizontalBar(
    width=4800,
    height=2700,
    style=custom_style,
    title="Software Project Timeline · gantt-dependencies · pygal · pyplots.ai",
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=24,
    print_values=False,
    show_y_guides=False,
    show_x_guides=False,
    show_x_labels=False,
    margin=60,
    spacing=15,
    range=(0, 100),
)

# Set task names as y-axis labels
chart.x_labels = task_labels

# Add placeholder series for legend (one per category)
categories_in_order = ["Requirements", "Design", "Development", "Testing", "Deployment"]
for cat in categories_in_order:
    chart.add(cat, [None] * num_tasks)

# Render base SVG
svg_string = chart.render().decode("utf-8")

# Pygal coordinates (from typical SVG: plot area dimensions)
PLOT_ORIGIN_X = 520
PLOT_ORIGIN_Y = 140
PLOT_WIDTH = 4200
PLOT_HEIGHT = 2340

PLOT_LEFT = PLOT_ORIGIN_X
PLOT_TOP = PLOT_ORIGIN_Y

row_height = PLOT_HEIGHT / num_tasks
bar_height = row_height * 0.50

# Store bar positions for drawing dependencies
bar_positions = {}

# Build custom Gantt bar rectangles
bar_elements = []

for i, (task_id, task_name, category, start, end, deps) in enumerate(tasks):
    start_day_val = (start - reference_date).days
    end_day_val = (end - reference_date).days

    # Convert days to x position
    x_start = PLOT_LEFT + ((start_day_val - start_day) / day_range) * PLOT_WIDTH
    x_end = PLOT_LEFT + ((end_day_val - start_day) / day_range) * PLOT_WIDTH
    width = x_end - x_start

    # Y position (pygal HorizontalBar has first item at bottom, so reverse index)
    reversed_i = num_tasks - 1 - i
    y_center = PLOT_TOP + (reversed_i + 0.5) * row_height
    y_top = y_center - bar_height / 2

    # Store position for dependency arrows
    bar_positions[task_id] = {"x_start": x_start, "x_end": x_end, "y_center": y_center}

    color = category_colors[category]
    duration = (end - start).days

    # Dependency info for tooltip
    dep_names = [task_by_id[d][1] for d in deps] if deps else []
    dep_text = f"&#10;Depends on: {', '.join(dep_names)}" if dep_names else ""

    bar_elements.append(
        f'<rect x="{x_start:.1f}" y="{y_top:.1f}" width="{width:.1f}" '
        f'height="{bar_height:.1f}" fill="{color}" rx="6" ry="6" opacity="0.9">'
        f"<title>{task_name}&#10;{start.strftime('%b %d')} - {end.strftime('%b %d')} "
        f"({duration} days){dep_text}</title></rect>"
    )

# Draw dependency arrows
arrow_elements = []
arrow_color = "#666666"

for task_id, _task_name, _category, _start, _end, deps in tasks:
    if not deps:
        continue

    target_pos = bar_positions[task_id]

    for dep_id in deps:
        source_pos = bar_positions[dep_id]

        # Arrow from end of source task to start of target task
        x1 = source_pos["x_end"]
        y1 = source_pos["y_center"]
        x2 = target_pos["x_start"]
        y2 = target_pos["y_center"]

        # Create a path with a slight curve for better visibility
        # Use a simple elbow connector: horizontal then vertical
        mid_x = x1 + (x2 - x1) * 0.5

        if abs(y1 - y2) < 5:
            # Same row - straight line
            path = f"M {x1:.1f},{y1:.1f} L {x2:.1f},{y2:.1f}"
        else:
            # Different rows - elbow connector
            path = f"M {x1:.1f},{y1:.1f} L {mid_x:.1f},{y1:.1f} L {mid_x:.1f},{y2:.1f} L {x2:.1f},{y2:.1f}"

        # Draw the path
        arrow_elements.append(
            f'<path d="{path}" stroke="{arrow_color}" stroke-width="2" '
            f'fill="none" opacity="0.6" marker-end="url(#arrowhead)"/>'
        )

# Define arrowhead marker
arrowhead_def = """
<defs>
  <marker id="arrowhead" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">
    <polygon points="0 0, 10 4, 0 8" fill="#666666" opacity="0.8"/>
  </marker>
</defs>
"""

# Add month markers and labels
month_markers = []
for month in range(1, 6):
    month_date = date(2025, month, 1)
    day_val = (month_date - reference_date).days
    if start_day <= day_val <= end_day:
        x_pos = PLOT_LEFT + ((day_val - start_day) / day_range) * PLOT_WIDTH
        month_name = month_date.strftime("%b")
        # Vertical guide line
        month_markers.append(
            f'<line x1="{x_pos:.1f}" y1="{PLOT_TOP}" x2="{x_pos:.1f}" '
            f'y2="{PLOT_TOP + PLOT_HEIGHT}" stroke="#cccccc" stroke-width="2" '
            f'stroke-dasharray="8,4"/>'
        )
        # Month label
        month_markers.append(
            f'<text x="{x_pos:.1f}" y="{PLOT_TOP + PLOT_HEIGHT + 45}" '
            f'font-family="Consolas, monospace" font-size="28" fill="#333" '
            f'text-anchor="middle">{month_name} 2025</text>'
        )

# X-axis title
month_markers.append(
    f'<text x="{PLOT_LEFT + PLOT_WIDTH / 2}" y="{PLOT_TOP + PLOT_HEIGHT + 95}" '
    f'font-family="Consolas, monospace" font-size="32" fill="#333" '
    f'text-anchor="middle">Project Timeline</text>'
)

# Add legend note for dependencies
legend_note = (
    f'<text x="{PLOT_LEFT + PLOT_WIDTH - 100}" y="{PLOT_TOP - 20}" '
    f'font-family="Consolas, monospace" font-size="24" fill="#666666" '
    f'text-anchor="end">→ indicates task dependencies</text>'
)

# Inject custom elements before </svg>
# Add arrowhead definition right after opening svg tag
svg_output = svg_string.replace("<svg ", f"<svg {arrowhead_def[7:-8]} ", 1)
# Actually, let's insert defs properly
svg_output = svg_string.replace("</svg>", f"{arrowhead_def}\n</svg>")

all_elements = "\n".join(month_markers + bar_elements + arrow_elements + [legend_note])
svg_output = svg_output.replace("</svg>", f"{all_elements}\n</svg>")

# Remove "No data" text that appears from empty series
svg_output = svg_output.replace(">No data<", "><")

# Save outputs
with open("plot.html", "w") as f:
    f.write(svg_output)

cairosvg.svg2png(bytestring=svg_output.encode(), write_to="plot.png")
