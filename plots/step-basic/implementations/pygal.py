"""
step-basic: Basic Step Plot
Library: pygal
"""

import pygal
from pygal.style import Style


# Data - Monthly cumulative sales (in thousands)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
cumulative_sales = [45, 92, 128, 165, 198, 256, 312, 378, 425, 489, 562, 635]

# Create step data by duplicating points for stair-step effect (post-style)
# Each value extends horizontally until the next month
step_x_labels = []
step_values = []

for i, (month, value) in enumerate(zip(months, cumulative_sales, strict=True)):
    step_x_labels.append(month)
    # Use dict with 'value' key to control dot visibility
    step_values.append({"value": value, "node": {"r": 10}})
    # Add intermediate point at same Y before next X (except for last point)
    if i < len(months) - 1:
        step_x_labels.append("")  # Empty label for intermediate point
        # Hide dot for intermediate points
        step_values.append({"value": value, "node": {"r": 0}})

# Custom style for 4800x2700 canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333",
    foreground_strong="#333",
    foreground_subtle="#666",
    colors=("#306998",),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
)

# Create line chart configured for step visualization
chart = pygal.Line(
    width=4800,
    height=2700,
    title="step-basic \u00b7 pygal \u00b7 pyplots.ai",
    x_title="Month",
    y_title="Cumulative Sales ($K)",
    style=custom_style,
    show_dots=True,
    dots_size=10,
    stroke_style={"width": 6},
    show_y_guides=True,
    show_x_guides=False,
    x_label_rotation=0,
    legend_at_bottom=True,
    truncate_legend=-1,
)

# Add data
chart.x_labels = step_x_labels
chart.add("Cumulative Sales", step_values)

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
