"""pyplots.ai
facet-grid: Faceted Grid Plot
Library: bokeh | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import numpy as np
import pandas as pd
from bokeh.io import export_png
from bokeh.layouts import column, gridplot
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure


# Data - Product performance across regions and seasons
np.random.seed(42)

regions = ["North", "South", "East"]
seasons = ["Spring", "Summer", "Fall", "Winter"]

data = []
for region in regions:
    for season in seasons:
        n_points = 25
        # Base values vary by region
        base_x = {"North": 20, "South": 30, "East": 25}[region]
        base_y = {"North": 50, "South": 70, "East": 60}[region]

        # Seasonal adjustments
        season_adj = {"Spring": 1.0, "Summer": 1.3, "Fall": 0.9, "Winter": 0.7}[season]

        x = np.random.normal(base_x, 5, n_points)
        y = base_y * season_adj + x * 0.8 + np.random.normal(0, 8, n_points)

        for xi, yi in zip(x, y, strict=True):
            data.append({"marketing_spend": xi, "sales": yi, "region": region, "season": season})

df = pd.DataFrame(data)

# Colors for each region
colors = {"North": "#306998", "South": "#FFD43B", "East": "#4ECDC4"}

# Create grid of plots (rows=seasons, cols=regions)
plots = []

for season in seasons:
    row_plots = []
    for region in regions:
        subset = df[(df["region"] == region) & (df["season"] == season)]
        source = ColumnDataSource(data={"x": subset["marketing_spend"], "y": subset["sales"]})

        # Create figure for each cell
        p = figure(width=1500, height=600, x_range=(5, 50), y_range=(20, 130), tools="")

        # Add scatter points
        p.scatter(
            x="x", y="y", source=source, size=18, color=colors[region], alpha=0.7, line_color="#333333", line_width=1
        )

        # Add facet label in top-left corner
        p.text(
            x=[8],
            y=[122],
            text=[f"{region} · {season}"],
            text_font_size="18pt",
            text_color="#333333",
            text_font_style="bold",
        )

        # Style axes
        p.xaxis.axis_label = "Marketing Spend ($K)" if season == seasons[-1] else ""
        p.yaxis.axis_label = "Sales ($K)" if region == regions[0] else ""
        p.xaxis.axis_label_text_font_size = "20pt"
        p.yaxis.axis_label_text_font_size = "20pt"
        p.xaxis.major_label_text_font_size = "16pt"
        p.yaxis.major_label_text_font_size = "16pt"

        # Grid styling
        p.xgrid.grid_line_alpha = 0.3
        p.ygrid.grid_line_alpha = 0.3
        p.xgrid.grid_line_dash = "dashed"
        p.ygrid.grid_line_dash = "dashed"

        # Background
        p.background_fill_color = "#fafafa"

        row_plots.append(p)
    plots.append(row_plots)

# Create gridplot layout
grid = gridplot(plots, toolbar_location=None, merge_tools=False)

# Add overall title by creating a title figure
title_fig = figure(width=4500, height=200, tools="", x_range=(0, 1), y_range=(0, 1))
title_fig.text(
    x=[0.5],
    y=[0.5],
    text=["facet-grid · bokeh · pyplots.ai"],
    text_font_size="32pt",
    text_align="center",
    text_baseline="middle",
    text_color="#333333",
)
title_fig.xaxis.visible = False
title_fig.yaxis.visible = False
title_fig.xgrid.visible = False
title_fig.ygrid.visible = False
title_fig.outline_line_color = None
title_fig.background_fill_color = None
title_fig.border_fill_color = None

# Combine title and grid using column layout
final_layout = column(title_fig, grid)

# Save
export_png(final_layout, filename="plot.png")
