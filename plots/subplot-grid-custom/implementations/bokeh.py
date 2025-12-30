""" pyplots.ai
subplot-grid-custom: Custom Subplot Grid Layout
Library: bokeh 3.8.1 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-30
"""

import numpy as np
from bokeh.io import export_png
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Title
from bokeh.plotting import figure


# Data
np.random.seed(42)

# Main time series data (simulating daily stock prices)
n_days = 100
dates = np.arange(n_days)
prices = 100 + np.cumsum(np.random.randn(n_days) * 2)
volumes = np.random.uniform(1, 5, n_days) * 1e6
returns = np.diff(prices) / prices[:-1] * 100

# Additional data for supporting plots
categories = ["Product A", "Product B", "Product C", "Product D"]
sales = [45, 72, 38, 65]

scatter_x = np.random.randn(80)
scatter_y = scatter_x * 0.8 + np.random.randn(80) * 0.5

# Column data sources
price_source = ColumnDataSource(data={"x": dates, "y": prices})
bar_source = ColumnDataSource(data={"x": categories, "y": sales})
scatter_source = ColumnDataSource(data={"x": scatter_x, "y": scatter_y})

# Color palette
python_blue = "#306998"
python_yellow = "#FFD43B"
accent_green = "#2E8B57"
accent_red = "#CD5C5C"

# Plot 1: Main time series (large - spans conceptually 2 columns)
p1 = figure(
    width=3000,
    height=1400,
    title="Price Trend Over Time",
    x_axis_label="Day",
    y_axis_label="Price ($)",
    toolbar_location=None,
)
p1.line("x", "y", source=price_source, line_width=4, color=python_blue, alpha=0.9)
p1.scatter("x", "y", source=price_source, size=12, color=python_blue, alpha=0.6)
p1.title.text_font_size = "32pt"
p1.xaxis.axis_label_text_font_size = "24pt"
p1.yaxis.axis_label_text_font_size = "24pt"
p1.xaxis.major_label_text_font_size = "20pt"
p1.yaxis.major_label_text_font_size = "20pt"
p1.grid.grid_line_alpha = 0.3
p1.outline_line_color = "#cccccc"
p1.outline_line_width = 2

# Add main title above p1
main_title = Title(text="subplot-grid-custom · bokeh · pyplots.ai", text_font_size="36pt", align="center")
p1.add_layout(main_title, "above")

# Plot 2: Volume bar chart (right side panel)
p2 = figure(
    width=1600,
    height=1400,
    title="Daily Trading Volume",
    x_axis_label="Day",
    y_axis_label="Volume (millions)",
    toolbar_location=None,
)
p2.vbar(x=dates, top=volumes / 1e6, width=0.7, color=python_yellow, alpha=0.85)
p2.title.text_font_size = "32pt"
p2.xaxis.axis_label_text_font_size = "24pt"
p2.yaxis.axis_label_text_font_size = "24pt"
p2.xaxis.major_label_text_font_size = "20pt"
p2.yaxis.major_label_text_font_size = "20pt"
p2.grid.grid_line_alpha = 0.3
p2.outline_line_color = "#cccccc"
p2.outline_line_width = 2

# Plot 3: Returns histogram (bottom left)
hist, edges = np.histogram(returns, bins=20)
hist_source = ColumnDataSource(data={"top": hist, "left": edges[:-1], "right": edges[1:]})
p3 = figure(
    width=1500,
    height=1100,
    title="Returns Distribution",
    x_axis_label="Daily Return (%)",
    y_axis_label="Frequency",
    toolbar_location=None,
)
p3.quad(
    top="top",
    bottom=0,
    left="left",
    right="right",
    source=hist_source,
    fill_color=accent_green,
    line_color="white",
    line_width=2,
    alpha=0.85,
)
p3.title.text_font_size = "28pt"
p3.xaxis.axis_label_text_font_size = "22pt"
p3.yaxis.axis_label_text_font_size = "22pt"
p3.xaxis.major_label_text_font_size = "18pt"
p3.yaxis.major_label_text_font_size = "18pt"
p3.grid.grid_line_alpha = 0.3
p3.outline_line_color = "#cccccc"
p3.outline_line_width = 2

# Plot 4: Categorical bar chart (bottom center)
p4 = figure(
    width=1500,
    height=1100,
    x_range=categories,
    title="Sales by Product Category",
    x_axis_label="Product",
    y_axis_label="Units Sold",
    toolbar_location=None,
)
p4.vbar(x="x", top="y", source=bar_source, width=0.6, color=python_blue, alpha=0.85)
p4.title.text_font_size = "28pt"
p4.xaxis.axis_label_text_font_size = "22pt"
p4.yaxis.axis_label_text_font_size = "22pt"
p4.xaxis.major_label_text_font_size = "18pt"
p4.yaxis.major_label_text_font_size = "18pt"
p4.xaxis.major_label_orientation = 0.3
p4.grid.grid_line_alpha = 0.3
p4.outline_line_color = "#cccccc"
p4.outline_line_width = 2

# Plot 5: Scatter plot with correlation (bottom right)
p5 = figure(
    width=1600,
    height=1100,
    title="Variable Correlation Analysis",
    x_axis_label="X Variable",
    y_axis_label="Y Variable",
    toolbar_location=None,
)
p5.scatter("x", "y", source=scatter_source, size=18, color=accent_red, alpha=0.7)
p5.title.text_font_size = "28pt"
p5.xaxis.axis_label_text_font_size = "22pt"
p5.yaxis.axis_label_text_font_size = "22pt"
p5.xaxis.major_label_text_font_size = "18pt"
p5.yaxis.major_label_text_font_size = "18pt"
p5.grid.grid_line_alpha = 0.3
p5.outline_line_color = "#cccccc"
p5.outline_line_width = 2

# Custom grid layout demonstrating non-uniform cell sizes
# Row 1: Main time series (3000px) + Volume sidebar (1600px) = 4600px
# Row 2: Histogram (1500px) + Bar chart (1500px) + Scatter (1600px) = 4600px
# This creates a dashboard with varied cell sizes (colspan/rowspan concept)

top_row = row(p1, p2)
bottom_row = row(p3, p4, p5)
final_layout = column(top_row, bottom_row)

# Save
export_png(final_layout, filename="plot.png")
