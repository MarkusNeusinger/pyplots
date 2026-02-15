""" pyplots.ai
bubble-basic: Basic Bubble Chart
Library: pygal 3.1.0 | Python 3.14.3
Quality: 75/100 | Created: 2026-02-15
"""

import numpy as np
import pygal
from pygal.style import Style


# Data — City comparison: population density vs avg commute time, bubble = green space (%)
np.random.seed(42)
n_cities = 30

population_density = np.random.uniform(1000, 15000, n_cities)  # people per sq km
commute_time = 15 + population_density / 800 + np.random.normal(0, 3, n_cities)  # minutes
green_space_pct = np.clip(60 - population_density / 400 + np.random.normal(0, 8, n_cities), 5, 55)

# Normalize green space to bubble size range
gs_min, gs_max = green_space_pct.min(), green_space_pct.max()
bubble_size = 15 + (green_space_pct - gs_min) / (gs_max - gs_min) * 85

# Bin cities by green space coverage (pygal uses per-series dot sizes)
low_green = [
    (round(population_density[i], 1), round(commute_time[i], 1)) for i in range(n_cities) if bubble_size[i] < 45
]
mid_green = [
    (round(population_density[i], 1), round(commute_time[i], 1)) for i in range(n_cities) if 45 <= bubble_size[i] < 70
]
high_green = [
    (round(population_density[i], 1), round(commute_time[i], 1)) for i in range(n_cities) if bubble_size[i] >= 70
]

# Style
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#999999",
    colors=("#c44e52", "#dd8452", "#306998"),
    opacity=0.55,
    opacity_hover=0.8,
    title_font_size=28,
    label_font_size=22,
    major_label_font_size=18,
    legend_font_size=18,
    value_font_size=14,
    tooltip_font_size=14,
)

# Plot
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="bubble-basic \u00b7 pygal \u00b7 pyplots.ai",
    x_title="Population Density (people/km\u00b2)",
    y_title="Avg Commute Time (min)",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=3,
    stroke=False,
    dots_size=18,
    show_x_guides=True,
    show_y_guides=True,
)

chart.add("< 20% Green Space", low_green, dots_size=18)
chart.add("20-35% Green Space", mid_green, dots_size=32)
chart.add("> 35% Green Space", high_green, dots_size=48)

# Save
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
