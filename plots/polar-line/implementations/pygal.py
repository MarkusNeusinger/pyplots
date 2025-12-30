"""pyplots.ai
polar-line: Polar Line Plot
Library: pygal | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import pygal
from pygal.style import Style


# Custom style for large canvas (4800x2700)
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333",
    foreground_strong="#333",
    foreground_subtle="#666",
    colors=("#306998", "#FFD43B"),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=48,
    value_font_size=36,
    stroke_width=6,
    opacity=0.9,
    opacity_hover=1.0,
)

# Data - Monthly temperature variations (cyclical pattern)
# 12 months at 30-degree intervals
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Average high temperatures - Northern hemisphere pattern
avg_high = [5.2, 7.1, 12.3, 16.8, 21.5, 25.2, 28.1, 27.4, 23.2, 17.1, 10.8, 6.3]

# Average low temperatures
avg_low = [-2.1, -0.8, 3.2, 7.5, 12.1, 16.3, 19.2, 18.5, 14.1, 8.3, 3.1, -0.5]

# Create polar/radar chart (pygal uses Radar for polar-style plots)
chart = pygal.Radar(
    width=4800,
    height=2700,
    style=custom_style,
    title="polar-line · pygal · pyplots.ai",
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=32,
    dots_size=12,
    fill=False,
    show_dots=True,
    range=(-5, 35),
    truncate_legend=-1,
    margin=60,
)

# X-axis labels (months around the circle)
chart.x_labels = months

# Add temperature series
chart.add("Avg High Temp", avg_high)
chart.add("Avg Low Temp", avg_low)

# Render to PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
