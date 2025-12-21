""" pyplots.ai
polar-basic: Basic Polar Chart
Library: pygal 3.1.0 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-14
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Hourly temperature readings in a 24-hour cycle
np.random.seed(42)
hours = np.arange(24)
base_temp = 15 + 8 * np.sin((hours - 6) * np.pi / 12)  # Peak at noon (hour 12)
temp = base_temp + np.random.randn(24) * 1.5  # Add slight noise

# Custom style for 4800x2700 px canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998",),  # Python Blue
    title_font_size=72,
    label_font_size=42,
    major_label_font_size=36,
    legend_font_size=42,
    tooltip_font_size=36,
    value_font_size=28,
    opacity=0.3,
    opacity_hover=0.6,
)

# Create Radar chart (pygal's polar-like visualization)
# Radar naturally positions data points around a circle
chart = pygal.Radar(
    width=4800,
    height=2700,
    style=custom_style,
    title="Hourly Temperature (°C) · polar-basic · pygal · pyplots.ai",
    show_legend=False,
    fill=True,
    dots_size=10,
    stroke_style={"width": 4},
    show_y_guides=True,
    inner_radius=0,
)

# X-axis labels as hours (angular positions)
chart.x_labels = [f"{h:02d}:00" for h in hours]

# Add temperature data (radius values at each angular position)
chart.add("Temperature", [float(t) for t in temp])

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
