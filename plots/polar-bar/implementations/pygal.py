"""pyplots.ai
polar-bar: Polar Bar Chart (Wind Rose)
Library: pygal | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import pygal
from pygal.style import Style


# Data - Wind direction frequency (cumulative for stacking effect)
directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

# Wind speed data - showing dominant westerly/northwesterly winds pattern
strong_winds = [2, 1, 2, 1, 2, 3, 4, 3]  # 25+ km/h (innermost)
moderate_winds = [6, 4, 5, 3, 5, 9, 14, 11]  # 15-25 km/h (cumulative)
light_winds = [15, 10, 10, 6, 10, 18, 26, 24]  # 5-15 km/h (cumulative)
calm_winds = [22, 14, 13, 8, 14, 24, 36, 34]  # 0-5 km/h (outermost)

# Custom style for large canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#2E5A88", "#306998", "#5B9BD5", "#A6CEE3"),  # Blue gradient
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
    width=3600,
    height=3600,
    style=custom_style,
    title="polar-bar · pygal · pyplots.ai",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=4,
    fill=True,
    show_dots=False,
    range=(0, 40),
    inner_radius=0.05,
    margin=100,
    spacing=50,
)

# X-axis labels (compass directions)
chart.x_labels = directions

# Add wind speed categories (outer to inner for proper layering)
chart.add("Calm (0-5 km/h)", calm_winds)
chart.add("Light (5-15 km/h)", light_winds)
chart.add("Moderate (15-25 km/h)", moderate_winds)
chart.add("Strong (25+ km/h)", strong_winds)

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
