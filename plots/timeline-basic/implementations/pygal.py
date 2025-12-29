""" pyplots.ai
timeline-basic: Event Timeline
Library: pygal 3.1.0 | Python 3.13.11
Quality: 88/100 | Created: 2025-12-29
"""

from datetime import date

import cairosvg
import pygal
from pygal.style import Style


# Data - Software project milestones
events = [
    (date(2024, 1, 15), "Project Kickoff", "Planning"),
    (date(2024, 2, 10), "Requirements Complete", "Planning"),
    (date(2024, 3, 20), "Architecture Design", "Design"),
    (date(2024, 4, 25), "Development Start", "Development"),
    (date(2024, 6, 15), "Alpha Release", "Development"),
    (date(2024, 8, 1), "Beta Release", "Testing"),
    (date(2024, 9, 10), "User Acceptance", "Testing"),
    (date(2024, 10, 20), "Production Launch", "Deployment"),
]

# Sort events by date
events = sorted(events, key=lambda x: x[0])

# Category colors
category_colors = {
    "Planning": "#306998",
    "Design": "#FFD43B",
    "Development": "#4ECDC4",
    "Testing": "#FF6B6B",
    "Deployment": "#45B7D1",
}

# Custom style for large canvas (4800x2700)
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#4ECDC4", "#FF6B6B", "#45B7D1"),
    title_font_size=60,
    label_font_size=28,
    major_label_font_size=28,
    legend_font_size=32,
    value_font_size=24,
    tooltip_font_size=24,
)

# Use a Line chart as base (will be heavily customized)
chart = pygal.Line(
    width=4800,
    height=2700,
    style=custom_style,
    title="Software Project Milestones · timeline-basic · pygal · pyplots.ai",
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=28,
    show_x_labels=False,
    show_y_labels=False,
    show_dots=False,
    show_x_guides=False,
    show_y_guides=False,
    margin=80,
    range=(-2, 2),
)

# Add empty series for legend (one per category)
for category in ["Planning", "Design", "Development", "Testing", "Deployment"]:
    chart.add(category, [None])

# Render base SVG
svg_string = chart.render().decode("utf-8")

# Plot coordinates (based on pygal defaults for 4800x2700)
PLOT_LEFT = 100
PLOT_TOP = 200
PLOT_WIDTH = 4600
PLOT_HEIGHT = 2100
TIMELINE_Y = PLOT_TOP + PLOT_HEIGHT * 0.5  # Middle of plot area

# Date range
reference_date = date(2024, 1, 1)
min_date = min(e[0] for e in events)
max_date = max(e[0] for e in events)
start_day = (min_date - reference_date).days - 20
end_day = (max_date - reference_date).days + 20
day_range = end_day - start_day

# Build custom timeline elements
timeline_elements = []

# Main timeline axis line
timeline_elements.append(
    f'<line x1="{PLOT_LEFT}" y1="{TIMELINE_Y}" x2="{PLOT_LEFT + PLOT_WIDTH}" '
    f'y2="{TIMELINE_Y}" stroke="#333333" stroke-width="6"/>'
)

# Arrow at the end
arrow_size = 20
timeline_elements.append(
    f'<polygon points="{PLOT_LEFT + PLOT_WIDTH},{TIMELINE_Y} '
    f"{PLOT_LEFT + PLOT_WIDTH - arrow_size},{TIMELINE_Y - arrow_size / 2} "
    f'{PLOT_LEFT + PLOT_WIDTH - arrow_size},{TIMELINE_Y + arrow_size / 2}" '
    f'fill="#333333"/>'
)

# Add month markers along the timeline
for month in range(1, 12):
    month_date = date(2024, month, 1)
    day_val = (month_date - reference_date).days
    if start_day <= day_val <= end_day:
        x_pos = PLOT_LEFT + ((day_val - start_day) / day_range) * PLOT_WIDTH
        month_name = month_date.strftime("%b")
        # Tick mark
        timeline_elements.append(
            f'<line x1="{x_pos:.1f}" y1="{TIMELINE_Y - 15}" x2="{x_pos:.1f}" '
            f'y2="{TIMELINE_Y + 15}" stroke="#999999" stroke-width="3"/>'
        )
        # Month label
        timeline_elements.append(
            f'<text x="{x_pos:.1f}" y="{TIMELINE_Y + 60}" '
            f'font-family="Consolas, sans-serif" font-size="32" fill="#666666" '
            f'text-anchor="middle">{month_name}</text>'
        )

# Year label
timeline_elements.append(
    f'<text x="{PLOT_LEFT + PLOT_WIDTH / 2}" y="{TIMELINE_Y + 110}" '
    f'font-family="Consolas, sans-serif" font-size="36" fill="#333333" '
    f'text-anchor="middle" font-weight="bold">2024</text>'
)

# Add event markers and labels
marker_radius = 20
label_offset_above = -80
label_offset_below = 140

for i, (event_date, event_name, category) in enumerate(events):
    day_val = (event_date - reference_date).days
    x_pos = PLOT_LEFT + ((day_val - start_day) / day_range) * PLOT_WIDTH
    color = category_colors[category]

    # Alternate label positions above/below
    is_above = i % 2 == 0
    label_y = TIMELINE_Y + (label_offset_above if is_above else label_offset_below)
    connector_y1 = TIMELINE_Y + (-marker_radius - 5 if is_above else marker_radius + 5)
    connector_y2 = TIMELINE_Y + (label_offset_above + 30 if is_above else label_offset_below - 45)

    # Event marker (circle)
    timeline_elements.append(
        f'<circle cx="{x_pos:.1f}" cy="{TIMELINE_Y}" r="{marker_radius}" '
        f'fill="{color}" stroke="white" stroke-width="4">'
        f"<title>{event_name}&#10;{event_date.strftime('%B %d, %Y')}&#10;"
        f"Category: {category}</title></circle>"
    )

    # Connector line from marker to label
    timeline_elements.append(
        f'<line x1="{x_pos:.1f}" y1="{connector_y1:.1f}" x2="{x_pos:.1f}" '
        f'y2="{connector_y2:.1f}" stroke="{color}" stroke-width="3" stroke-dasharray="6,4"/>'
    )

    # Event name label (multiline for long names)
    words = event_name.split()
    if len(words) > 2:
        line1 = " ".join(words[:2])
        line2 = " ".join(words[2:])
        timeline_elements.append(
            f'<text x="{x_pos:.1f}" y="{label_y:.1f}" '
            f'font-family="Consolas, sans-serif" font-size="36" fill="#333333" '
            f'text-anchor="middle" font-weight="bold">{line1}</text>'
        )
        timeline_elements.append(
            f'<text x="{x_pos:.1f}" y="{label_y + 40:.1f}" '
            f'font-family="Consolas, sans-serif" font-size="36" fill="#333333" '
            f'text-anchor="middle" font-weight="bold">{line2}</text>'
        )
    else:
        timeline_elements.append(
            f'<text x="{x_pos:.1f}" y="{label_y:.1f}" '
            f'font-family="Consolas, sans-serif" font-size="36" fill="#333333" '
            f'text-anchor="middle" font-weight="bold">{event_name}</text>'
        )

    # Date label
    date_label_y = label_y + (40 if len(words) <= 2 else 80)
    timeline_elements.append(
        f'<text x="{x_pos:.1f}" y="{date_label_y:.1f}" '
        f'font-family="Consolas, sans-serif" font-size="28" fill="#666666" '
        f'text-anchor="middle">{event_date.strftime("%b %d")}</text>'
    )

# Inject custom elements before </svg>
all_elements = "\n".join(timeline_elements)
svg_output = svg_string.replace("</svg>", f"{all_elements}\n</svg>")

# Remove "No data" text that appears from empty series
svg_output = svg_output.replace(">No data<", "><")

# Save outputs
with open("plot.html", "w") as f:
    f.write(svg_output)

cairosvg.svg2png(bytestring=svg_output.encode(), write_to="plot.png")
