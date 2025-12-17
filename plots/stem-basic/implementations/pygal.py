"""
stem-basic: Basic Stem Plot
Library: pygal
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - discrete signal samples demonstrating impulse response
np.random.seed(42)
n_points = 30
x = np.arange(n_points)
# Create a decaying oscillation pattern (typical impulse response)
y = np.exp(-x / 8) * np.sin(x * 0.8) * 2 + np.random.randn(n_points) * 0.1

# Custom style for 4800×2700 px canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#306998"),  # Python Blue for stems and markers
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
)

# Create XY chart for stem plot
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="stem-basic · pygal · pyplots.ai",
    x_title="Sample Index",
    y_title="Amplitude",
    show_legend=False,
    show_dots=True,
    stroke=True,
    dots_size=12,
    stroke_style={"width": 4},
    show_x_guides=False,
    show_y_guides=True,
)

# Add each stem as a separate line from baseline to data point
# This creates the stem effect: vertical lines from y=0 to each data point
for i in range(n_points):
    xi = float(x[i])
    yi = float(y[i])
    # Each stem is a line from (x, 0) to (x, y)
    chart.add("", [(xi, 0), (xi, yi)], show_dots=True, dots_size=12, stroke_style={"width": 3})

# Add baseline at y=0
chart.add(
    "Baseline", [(float(x[0]), 0), (float(x[-1]), 0)], show_dots=False, stroke_style={"width": 2, "dasharray": "10, 5"}
)

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
