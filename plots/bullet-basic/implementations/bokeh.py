""" pyplots.ai
bullet-basic: Basic Bullet Chart
Library: bokeh 3.8.1 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-23
"""

from bokeh.io import export_png, output_file, save
from bokeh.models import Label
from bokeh.plotting import figure


# Data - Sales performance metrics with targets
metrics = [
    {"label": "Revenue", "actual": 275, "target": 250, "ranges": [150, 225, 300]},
    {"label": "Profit", "actual": 85, "target": 100, "ranges": [50, 75, 100]},
    {"label": "Orders", "actual": 320, "target": 350, "ranges": [200, 300, 400]},
    {"label": "Customers", "actual": 1450, "target": 1200, "ranges": [800, 1100, 1500]},
    {"label": "Satisfaction", "actual": 4.2, "target": 4.5, "ranges": [3.0, 4.0, 5.0]},
]

# Configuration
num_metrics = len(metrics)
bar_spacing = 1.5  # Space between each bullet row
bar_height = 0.8  # Maximum height of range bars

# Qualitative range colors (grayscale: poor, satisfactory, good - light to dark)
range_colors = ["#dddddd", "#aaaaaa", "#777777"]

# Create figure
p = figure(
    width=4800,
    height=2700,
    x_range=(0, 110),
    y_range=(-0.5, num_metrics * bar_spacing),
    title="bullet-basic · bokeh · pyplots.ai",
    x_axis_label="% of Target Range",
    toolbar_location=None,
)

# Remove y-axis ticks and gridlines
p.yaxis.visible = False
p.ygrid.grid_line_color = None
p.xgrid.grid_line_alpha = 0.3
p.xgrid.grid_line_dash = "dashed"

# Draw bullets for each metric
for i, metric in enumerate(metrics):
    y_pos = (num_metrics - 1 - i) * bar_spacing  # Reverse so first is at top
    actual = metric["actual"]
    target = metric["target"]
    ranges = metric["ranges"]
    max_range = ranges[-1]

    # Normalize values to percentage of max range
    norm_actual = (actual / max_range) * 100
    norm_target = (target / max_range) * 100
    norm_ranges = [(r / max_range) * 100 for r in ranges]

    # Draw qualitative ranges (background bands) - from outer to inner
    for j in range(len(norm_ranges) - 1, -1, -1):
        range_width = norm_ranges[j]
        height_factor = 1 - j * 0.25  # Decrease height for inner ranges
        h = bar_height * height_factor
        p.rect(x=range_width / 2, y=y_pos, width=range_width, height=h, color=range_colors[j], line_color=None)

    # Draw actual value bar (primary measure)
    actual_bar_height = bar_height * 0.35
    p.rect(x=norm_actual / 2, y=y_pos, width=norm_actual, height=actual_bar_height, color="#306998", line_color=None)

    # Draw target marker (thin black vertical line)
    target_marker_height = bar_height * 0.6
    p.rect(x=norm_target, y=y_pos, width=0.8, height=target_marker_height, color="#1a1a1a", line_color=None)

    # Add metric label on the left
    label = Label(
        x=-2,
        y=y_pos,
        text=metric["label"],
        text_font_size="28pt",
        text_color="#333333",
        text_align="right",
        text_baseline="middle",
        text_font_style="bold",
    )
    p.add_layout(label)

    # Add actual value text label on the right
    value_label = Label(
        x=norm_actual + 3,
        y=y_pos,
        text=str(metric["actual"]),
        text_font_size="24pt",
        text_color="#306998",
        text_align="left",
        text_baseline="middle",
        text_font_style="bold",
    )
    p.add_layout(value_label)

# Extend x_range to accommodate labels (but clip axis display)
p.x_range.start = -35
p.x_range.end = 115

# Styling - scaled for 4800x2700 canvas
p.title.text_font_size = "42pt"
p.title.text_color = "#333333"
p.title.align = "center"
p.xaxis.axis_label_text_font_size = "28pt"
p.xaxis.major_label_text_font_size = "22pt"

# Only show positive tick marks on x-axis
p.xaxis.ticker = [0, 20, 40, 60, 80, 100]

# Axis styling
p.xaxis.axis_line_color = "#666666"
p.outline_line_color = None

# Save as PNG
export_png(p, filename="plot.png")

# Save as HTML for interactivity
output_file("plot.html")
save(p)
