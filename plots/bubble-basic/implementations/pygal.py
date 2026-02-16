""" pyplots.ai
bubble-basic: Basic Bubble Chart
Library: pygal 3.1.0 | Python 3.14.3
Quality: 77/100 | Created: 2026-02-16
"""

import numpy as np
import pygal
from pygal.style import Style


# Data — City comparison: population density vs avg commute time, bubble = green space (%)
np.random.seed(42)
n_cities = 40

population_density = np.random.uniform(1500, 14000, n_cities)  # people per sq km
commute_time = 16 + population_density / 900 + np.random.normal(0, 2.5, n_cities)  # minutes
green_space_pct = np.clip(45 - population_density / 500 + np.random.normal(0, 12, n_cities), 5, 50)

# Normalize green space for bubble sizing (scaled by area)
gs_min, gs_max = green_space_pct.min(), green_space_pct.max()
bubble_norm = (green_space_pct - gs_min) / (gs_max - gs_min)  # 0..1

# Bin into 5 tiers using quantile edges for balanced groups (pygal requires per-series dots_size)
tier_edges = [0.0] + list(np.quantile(bubble_norm, [0.2, 0.4, 0.6, 0.8])) + [1.01]
tier_sizes = [14, 22, 32, 44, 58]
tier_labels = ["≤15%", None, "~30%", None, "≥45%"]  # Label representative tiers

# Colorblind-safe sequential palette (deep purple → teal → gold)
tier_colors = ["#7b2d8e", "#306998", "#2a9d8f", "#8ab17d", "#e9c46a"]

bins = {t: [] for t in range(5)}
for i in range(n_cities):
    for t in range(5):
        if tier_edges[t] <= bubble_norm[i] < tier_edges[t + 1]:
            bins[t].append((round(population_density[i], 1), round(commute_time[i], 1)))
            break

# Style — refined palette on clean white background
custom_style = Style(
    background="white",
    plot_background="#fafafa",
    foreground="#2d2d2d",
    foreground_strong="#2d2d2d",
    foreground_subtle="#d0d0d0",
    colors=tuple(tier_colors),
    opacity=0.6,
    opacity_hover=0.85,
    title_font_size=30,
    label_font_size=20,
    major_label_font_size=18,
    legend_font_size=22,
    value_font_size=14,
    tooltip_font_size=16,
)

# Plot
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="bubble-basic · pygal · pyplots.ai",
    x_title="Population Density (people/km²)",
    y_title="Avg Commute Time (min)",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=3,
    legend_box_size=20,
    stroke=False,
    dots_size=14,
    show_x_guides=True,
    show_y_guides=True,
    x_value_formatter=lambda x: f"{x:,.0f}",
    value_formatter=lambda x: f"{x:.1f}",
    margin_top=10,
    tooltip_border_radius=4,
    tooltip_fancy_mode=True,
)

# Add each tier — labeled tiers appear in legend, None-titled ones are hidden
for t in range(5):
    label = f"Green Space {tier_labels[t]}" if tier_labels[t] else None
    chart.add(label, bins[t], dots_size=tier_sizes[t])

# Save
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
