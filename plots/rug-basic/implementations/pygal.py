""" pyplots.ai
rug-basic: Basic Rug Plot
Library: pygal 3.1.0 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-17
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

# Custom style for 4800x2700 px canvas
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
    opacity=0.6,
    opacity_hover=0.9,
)

# Create XY chart for rug plot
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="rug-basic · pygal · pyplots.ai",
    x_title="Response Time (ms)",
    y_title="",
    show_legend=False,
    show_dots=False,
    stroke=True,
    stroke_style={"width": 3},
    show_x_guides=False,  # Disable x guides to avoid visual clutter with tick marks
    show_y_guides=False,
    show_y_labels=False,  # Hide y-axis labels since they're not meaningful for rug
)

# Create rug plot by adding each tick as a separate vertical line
# This creates the distinctive tick mark appearance of a rug plot
# Traditional rug plots have short ticks at the bottom of the plot area
tick_height = 0.12  # Short tick marks (12% of plot height)

# Add invisible anchor points to set y-axis range (pygal auto-scales to data)
# Use two vertical invisible lines at the edges to set the range without diagonal line
x_min, x_max = float(values.min()), float(values.max())
chart.add("", [(x_min, 0), (x_min, 1.0)], stroke_style={"width": 0}, show_dots=False)
chart.add("", [(x_max, 0), (x_max, 1.0)], stroke_style={"width": 0}, show_dots=False)

# Add rug ticks
for val in values:
    x = float(val)
    # Each tick is a short vertical line segment from bottom
    chart.add("", [(x, 0), (x, tick_height)], stroke_style={"width": 4})

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
