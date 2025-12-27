""" pyplots.ai
scatter-size-mapped: Bubble Chart
Library: bokeh 3.8.1 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-27
"""

import numpy as np
from bokeh.io import export_png
from bokeh.models import ColumnDataSource, Legend, LegendItem
from bokeh.palettes import Category10
from bokeh.plotting import figure, output_file, save


# Data - Country economic indicators
np.random.seed(42)

# Regions and their characteristics
regions = ["Americas", "Europe", "Asia", "Africa", "Oceania"]
region_data = {
    "Americas": {"gdp_range": (15000, 65000), "life_range": (70, 82), "pop_range": (5e6, 350e6), "n": 8},
    "Europe": {"gdp_range": (25000, 75000), "life_range": (76, 84), "pop_range": (5e6, 85e6), "n": 10},
    "Asia": {"gdp_range": (3000, 55000), "life_range": (65, 85), "pop_range": (10e6, 1400e6), "n": 12},
    "Africa": {"gdp_range": (1000, 15000), "life_range": (55, 75), "pop_range": (10e6, 220e6), "n": 8},
    "Oceania": {"gdp_range": (30000, 60000), "life_range": (78, 84), "pop_range": (5e6, 30e6), "n": 4},
}

gdp_per_capita = []
life_expectancy = []
population = []
region_list = []

for region, params in region_data.items():
    n = params["n"]
    gdp_min, gdp_max = params["gdp_range"]
    life_min, life_max = params["life_range"]
    pop_min, pop_max = params["pop_range"]

    gdp_per_capita.extend(np.random.uniform(gdp_min, gdp_max, n))
    life_expectancy.extend(np.random.uniform(life_min, life_max, n))
    population.extend(np.random.uniform(pop_min, pop_max, n))
    region_list.extend([region] * n)

gdp_per_capita = np.array(gdp_per_capita)
life_expectancy = np.array(life_expectancy)
population = np.array(population)

# Scale bubble sizes using log scale for better visibility
# Map to range suitable for bokeh's size parameter (10-80)
pop_log = np.log10(population)
pop_normalized = (pop_log - pop_log.min()) / (pop_log.max() - pop_log.min())
bubble_sizes = 15 + pop_normalized * 65  # Range: 15-80

# Create ColumnDataSource
source = ColumnDataSource(
    data={
        "gdp": gdp_per_capita,
        "life": life_expectancy,
        "pop": population,
        "size": bubble_sizes,
        "region": region_list,
    }
)

# Create figure
p = figure(
    width=4800,
    height=2700,
    title="scatter-size-mapped · bokeh · pyplots.ai",
    x_axis_label="GDP per Capita (USD)",
    y_axis_label="Life Expectancy (years)",
)

# Color palette for regions
colors = Category10[5]

# Plot each region separately for legend
renderers = []
for i, region in enumerate(regions):
    mask = [r == region for r in region_list]
    region_source = ColumnDataSource(
        data={
            "gdp": gdp_per_capita[mask],
            "life": life_expectancy[mask],
            "size": bubble_sizes[mask],
            "pop": population[mask],
        }
    )
    r = p.scatter(
        x="gdp",
        y="life",
        size="size",
        source=region_source,
        fill_color=colors[i],
        line_color="white",
        line_width=2,
        fill_alpha=0.6,
    )
    renderers.append((region, [r]))

# Add legend
legend = Legend(items=[LegendItem(label=name, renderers=rends) for name, rends in renderers])
legend.location = "top_left"
legend.label_text_font_size = "22pt"
legend.glyph_height = 40
legend.glyph_width = 40
legend.spacing = 15
legend.padding = 20
legend.background_fill_alpha = 0.85
legend.border_line_width = 2
legend.border_line_color = "#cccccc"
p.add_layout(legend)

# Style adjustments for large canvas
p.title.text_font_size = "32pt"
p.title.text_font_style = "bold"
p.xaxis.axis_label_text_font_size = "24pt"
p.yaxis.axis_label_text_font_size = "24pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.major_label_text_font_size = "18pt"

# Grid styling
p.xgrid.grid_line_alpha = 0.3
p.ygrid.grid_line_alpha = 0.3
p.xgrid.grid_line_dash = [6, 4]
p.ygrid.grid_line_dash = [6, 4]

# Background
p.background_fill_color = "#fafafa"

# Axis formatting
p.xaxis.formatter.use_scientific = False
p.xaxis[0].ticker.desired_num_ticks = 10

# Add outline
p.outline_line_color = "#cccccc"
p.outline_line_width = 2

# Save PNG
export_png(p, filename="plot.png")

# Save HTML (interactive version)
output_file("plot.html", title="scatter-size-mapped · bokeh · pyplots.ai")
save(p)
