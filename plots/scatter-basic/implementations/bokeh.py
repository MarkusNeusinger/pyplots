""" pyplots.ai
scatter-basic: Basic Scatter Plot
Library: bokeh 3.8.2 | Python 3.14.2
Quality: /100 | Updated: 2026-02-10
"""

import numpy as np
from bokeh.io import export_png
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure, output_file, save
from bokeh.transform import factor_cmap


# Data - Coffee shop daily metrics: cups sold vs revenue across seasons
np.random.seed(42)
n = 120
seasons = np.random.choice(["Winter", "Spring", "Summer", "Autumn"], size=n, p=[0.28, 0.24, 0.24, 0.24])
base_cups = {"Winter": 180, "Spring": 140, "Summer": 110, "Autumn": 150}
cups_sold = np.array([base_cups[s] + np.random.normal(0, 30) for s in seasons]).clip(40, 300)
revenue = cups_sold * np.random.uniform(3.2, 4.8, n) + np.random.normal(0, 40, n)
revenue = revenue.clip(100, 1600)

source = ColumnDataSource(data={"cups": cups_sold, "revenue": revenue, "season": seasons})

season_list = ["Winter", "Spring", "Summer", "Autumn"]
palette = ["#306998", "#2CA02C", "#FFD43B", "#E25822"]

# Create figure
p = figure(width=4800, height=2700, title="scatter-basic \u00b7 bokeh \u00b7 pyplots.ai")
p.xaxis.axis_label = "Cups Sold per Day"
p.yaxis.axis_label = "Daily Revenue ($)"

# Plot scatter with season-based coloring
p.scatter(
    x="cups",
    y="revenue",
    source=source,
    size=30,
    alpha=0.75,
    color=factor_cmap("season", palette, season_list),
    legend_group="season",
)

# HoverTool for interactivity
hover = HoverTool(tooltips=[("Season", "@season"), ("Cups Sold", "@cups{0}"), ("Revenue", "$@revenue{0.00}")])
p.add_tools(hover)

# Title styling
p.title.text_font_size = "72pt"
p.title.text_color = "#2C3E50"

# Axis styling
p.xaxis.axis_label_text_font_size = "48pt"
p.yaxis.axis_label_text_font_size = "48pt"
p.xaxis.major_label_text_font_size = "36pt"
p.yaxis.major_label_text_font_size = "36pt"
p.xaxis.axis_label_text_color = "#34495E"
p.yaxis.axis_label_text_color = "#34495E"
p.xaxis.axis_line_width = 3
p.yaxis.axis_line_width = 3
p.xaxis.major_tick_line_width = 3
p.yaxis.major_tick_line_width = 3

# Grid
p.grid.grid_line_alpha = 0.3
p.grid.grid_line_width = 2
p.grid.grid_line_dash = [6, 4]

# Legend
p.legend.label_text_font_size = "36pt"
p.legend.glyph_width = 50
p.legend.glyph_height = 50
p.legend.spacing = 14
p.legend.padding = 20
p.legend.background_fill_alpha = 0.85
p.legend.border_line_alpha = 0.3
p.legend.location = "top_left"

# Background
p.background_fill_color = "#FAFBFC"
p.border_fill_color = "white"
p.outline_line_color = "#E0E0E0"
p.outline_line_width = 2

# Save
export_png(p, filename="plot.png")
output_file("plot.html")
save(p)
