""" pyplots.ai
band-basic: Basic Band Plot
Library: pygal 3.1.0 | Python 3.13.11
Quality: 88/100 | Created: 2025-12-23
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Time series with 95% confidence interval
np.random.seed(42)
x = np.linspace(0, 10, 50)
# Central trend line (quadratic curve)
y_center = 2 + 0.5 * x + 0.1 * x**2 + np.random.randn(50) * 0.3
# Smooth the center line
y_center = np.convolve(y_center, np.ones(3) / 3, mode="same")
# Confidence interval widens with x (increasing uncertainty)
uncertainty = 0.5 + 0.15 * x
y_lower = y_center - uncertainty
y_upper = y_center + uncertainty

# Custom style for 4800x2700 canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    guide_stroke_color="#888888",  # Darker grid lines for better visibility
    colors=("#306998", "#FFD43B"),  # Blue for band, Yellow for center line
    opacity=".65",  # Higher opacity for clearly visible band
    opacity_hover=".75",
    stroke_width=5,  # Thicker lines for better visibility
    title_font_size=60,
    label_font_size=42,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
)

# Create XY chart for precise coordinate control
chart = pygal.XY(
    style=custom_style,
    width=4800,
    height=2700,
    title="95% Confidence Interval · band-basic · pygal · pyplots.ai",
    x_title="Time (s)",
    y_title="Measurement Value",
    show_dots=False,
    show_x_guides=True,
    show_y_guides=True,
    fill=True,
    stroke=True,
    legend_at_bottom=True,
    truncate_legend=-1,
)

# Create band as a closed polygon: upper boundary forward, then lower backward
# Using fill only (no stroke) to avoid visual artifacts at polygon edges
band_polygon = []
# Upper boundary (forward)
for xi, yi in zip(x, y_upper, strict=True):
    band_polygon.append((float(xi), float(yi)))
# Lower boundary (backward to close the polygon smoothly)
for xi, yi in zip(reversed(x), reversed(y_lower), strict=True):
    band_polygon.append((float(xi), float(yi)))

chart.add("Confidence Band", band_polygon, stroke=False)

# Add center line (no fill, just stroke) - using a contrasting color
center_data = [(float(xi), float(yi)) for xi, yi in zip(x, y_center, strict=True)]
chart.add("Central Trend", center_data, fill=False, stroke=True, dots_size=0, stroke_style={"width": 6})

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
