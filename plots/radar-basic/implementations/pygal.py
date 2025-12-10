"""
radar-basic: Basic Radar Chart
Library: pygal
"""

import pygal
from pygal.style import Style


# Data - Performance metrics for two athletes
categories = ["Speed", "Power", "Accuracy", "Stamina", "Technique"]
athlete_a = [85, 72, 90, 65, 78]
athlete_b = [70, 88, 75, 82, 85]

# Style using PyPlots palette
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B"),
    label_font_size=40,
    title_font_size=56,
    legend_font_size=40,
    value_font_size=32,
    opacity=0.7,
    opacity_hover=0.9,
)

# Create radar chart
chart = pygal.Radar(
    width=4800,
    height=2700,
    title="Athlete Performance Comparison",
    style=custom_style,
    show_legend=True,
    legend_at_bottom=False,
    fill=True,
    dots_size=8,
    show_dots=True,
    range=(0, 100),
)

# Set category labels
chart.x_labels = categories

# Add data series
chart.add("Athlete A", athlete_a)
chart.add("Athlete B", athlete_b)

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
