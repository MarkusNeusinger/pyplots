"""pyplots.ai
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

# Bin into 5 tiers for pygal (requires per-series dots_size)
tier_edges = [0.0] + list(np.quantile(bubble_norm, [0.2, 0.4, 0.6, 0.8])) + [1.01]
tier_sizes = [20, 30, 40, 52, 64]
tier_labels = ["Green Space ≤15%", "Green Space ~22%", "Green Space ~30%", "Green Space ~38%", "Green Space ≥45%"]

# Colorblind-safe sequential palette (deep purple → teal → gold)
tier_colors = ["#7b2d8e", "#306998", "#2a9d8f", "#8ab17d", "#e9c46a"]

bins = {t: [] for t in range(5)}
for i in range(n_cities):
    for t in range(5):
        if tier_edges[t] <= bubble_norm[i] < tier_edges[t + 1]:
            bins[t].append(
                {
                    "value": (round(float(population_density[i]), 1), round(float(commute_time[i]), 1)),
                    "label": f"Density: {population_density[i]:,.0f}/km² | Commute: {commute_time[i]:.1f} min | Green: {green_space_pct[i]:.0f}%",
                }
            )
            break

# Style — refined palette on clean white background
custom_style = Style(
    background="white",
    plot_background="#f8f8f8",
    foreground="#2d2d2d",
    foreground_strong="#2d2d2d",
    foreground_subtle="#d8d8d8",
    colors=tuple(tier_colors),
    opacity=0.6,
    opacity_hover=0.9,
    title_font_size=32,
    label_font_size=22,
    major_label_font_size=20,
    legend_font_size=20,
    value_font_size=14,
    tooltip_font_size=18,
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
    legend_at_bottom_columns=5,
    legend_box_size=24,
    stroke=False,
    dots_size=20,
    show_x_guides=True,
    show_y_guides=True,
    x_value_formatter=lambda x: f"{x:,.0f}",
    value_formatter=lambda x: f"{x:.1f}",
    margin_top=30,
    margin_bottom=60,
    tooltip_border_radius=6,
    tooltip_fancy_mode=True,
    print_values=False,
)

# Add each tier as its own series — all 5 tiers labeled in legend
for t in range(5):
    chart.add(tier_labels[t], bins[t], dots_size=tier_sizes[t])

# Save
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
