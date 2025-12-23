""" pyplots.ai
rug-basic: Basic Rug Plot
Library: pygal 3.1.0 | Python 3.13.11
Quality: 82/100 | Created: 2025-12-23
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Response times (in milliseconds) showing realistic clustering patterns
np.random.seed(42)
values = np.concatenate(
    [
        np.random.normal(150, 20, 60),  # Main cluster of typical responses
        np.random.normal(250, 30, 25),  # Slower responses
        np.random.normal(400, 15, 10),  # Occasional outliers
        np.random.uniform(50, 100, 5),  # Very fast responses
    ]
)
values = np.clip(values, 30, 500)  # Realistic bounds
values = np.sort(values)  # Sort for better visual ordering

# Custom style for 4800x2700 px canvas - no y-axis line
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998",),  # Python Blue
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
    opacity=0.85,
    opacity_hover=0.95,
)

# Create XY chart for rug plot - use horizontal layout to maximize vertical utilization
# Using a shorter y-range centered on the visual area fills the canvas better
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="rug-basic · pygal · pyplots.ai",
    x_title="Response Time (ms)",
    y_title=None,  # No y-axis title for rug plot
    show_legend=False,
    show_dots=False,
    stroke=True,
    stroke_style={"width": 12},  # Thicker strokes for better visibility in dense areas
    show_x_guides=False,
    show_y_guides=False,
    show_y_labels=False,  # Hide y-axis labels
    print_values=False,
    range=(-0.05, 0.55),  # Tighter y-range so ticks fill more vertical space
    margin=100,
    margin_top=150,
    margin_bottom=250,  # Room for x-axis labels
    margin_left=100,  # Minimal left margin since no y-axis needed
)

# Add invisible anchor points to set x-axis range with padding
x_min, x_max = float(values.min()), float(values.max())
x_padding = (x_max - x_min) * 0.05
chart.add("", [(x_min - x_padding, 0), (x_max + x_padding, 0)], stroke_style={"width": 0}, show_dots=False)

# Rug tick parameters - ticks go from y=0 up to y=0.5 (filling ~90% of visible y-range)
tick_top = 0.5

# Add rug ticks - each tick is a vertical line from the baseline
for val in values:
    x = float(val)
    chart.add("", [(x, 0), (x, tick_top)], stroke_style={"width": 12})

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
