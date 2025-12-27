"""pyplots.ai
scatter-size-mapped: Bubble Chart
Library: pygal | Python 3.13
Quality: pending | Created: 2025-12-27
"""

import numpy as np
import pygal
from pygal.style import Style


# Data: Country economic indicators
np.random.seed(42)

# Generate 40 synthetic countries across different regions
n_countries = 40
regions = ["Europe", "Asia", "Americas", "Africa"]

# Assign regions with some variation
region_assignments = np.random.choice(regions, n_countries)

# GDP per capita (1,000 - 80,000)
gdp_per_capita = np.random.uniform(5000, 75000, n_countries)
# Adjust by region for realism
for i, region in enumerate(region_assignments):
    if region == "Europe":
        gdp_per_capita[i] = np.random.uniform(25000, 75000)
    elif region == "Asia":
        gdp_per_capita[i] = np.random.uniform(5000, 60000)
    elif region == "Americas":
        gdp_per_capita[i] = np.random.uniform(8000, 70000)
    else:  # Africa
        gdp_per_capita[i] = np.random.uniform(1000, 20000)

# Life expectancy (50-85) correlated with GDP
life_expectancy = 50 + 30 * (gdp_per_capita / 80000) + np.random.uniform(-5, 5, n_countries)
life_expectancy = np.clip(life_expectancy, 50, 85)

# Population (log scale, 1M - 1.4B)
population = 10 ** np.random.uniform(6, 9.2, n_countries)

# Create custom style
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#E74C3C", "#27AE60", "#9B59B6"),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=40,
    legend_font_size=40,
    value_font_size=36,
    opacity=0.6,
    opacity_hover=0.8,
)

# Create XY chart for scatter plot
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="scatter-size-mapped · pygal · pyplots.ai",
    x_title="GDP per Capita (USD)",
    y_title="Life Expectancy (years)",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=4,
    dots_size=15,
    show_x_guides=True,
    show_y_guides=True,
    stroke=False,
    explicit_size=True,
    truncate_legend=-1,
)

# Group data by region and add as series
# Pygal XY chart uses value dict with 'value' for coordinates
for region in regions:
    mask = region_assignments == region
    points = []
    for i in np.where(mask)[0]:
        # Scale population to reasonable dot size (log scale)
        # Population ranges from 1M to 1.4B, scale to 5-60 for visibility
        size = 5 + 55 * (np.log10(population[i]) - 6) / 3.2
        points.append({"value": (float(gdp_per_capita[i]), float(life_expectancy[i])), "node": {"r": size}})
    chart.add(region, points)

# Render to files
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
