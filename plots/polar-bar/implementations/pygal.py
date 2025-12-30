"""pyplots.ai
polar-bar: Polar Bar Chart (Wind Rose)
Library: pygal 3.1.0 | Python 3.13.11
Quality: 85/100 | Created: 2025-12-30
"""

import pygal
from pygal.style import Style


# Data - Wind direction frequency (actual values per category, not cumulative)
directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

# Wind speed data - actual frequency (%) per category per direction
# Showing dominant westerly/northwesterly winds pattern
calm_winds = [8, 5, 4, 3, 5, 7, 12, 11]  # 0-5 km/h
light_winds = [6, 4, 3, 2, 4, 7, 10, 9]  # 5-15 km/h
moderate_winds = [3, 2, 2, 1, 2, 4, 7, 6]  # 15-25 km/h
strong_winds = [2, 1, 1, 1, 1, 2, 4, 3]  # 25+ km/h

# Custom style for landscape canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#A6CEE3", "#5B9BD5", "#306998", "#2E5A88"),  # Light to dark blue
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=44,
    legend_font_size=40,
    value_font_size=36,
    stroke_width=1,
    opacity=0.85,
    opacity_hover=0.95,
)

# Create radar chart (polar visualization for wind rose)
chart = pygal.Radar(
    width=4800,
    height=2700,
    style=custom_style,
    title="Polar Bar Chart (Wind Rose) · polar-bar · pygal · pyplots.ai",
    x_title="Wind Frequency (%)",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=4,
    fill=True,
    show_dots=False,
    range=(0, 15),
    inner_radius=0.05,
    margin=100,
    spacing=50,
)

# X-axis labels (compass directions)
chart.x_labels = directions

# Add wind speed categories (innermost to outermost for proper stacking)
chart.add("Calm (0-5 km/h)", calm_winds)
chart.add("Light (5-15 km/h)", light_winds)
chart.add("Moderate (15-25 km/h)", moderate_winds)
chart.add("Strong (25+ km/h)", strong_winds)

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
