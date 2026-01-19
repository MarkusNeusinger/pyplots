"""pyplots.ai
chart-export-menu: Chart with Built-in Export Menu
Library: bokeh | Python 3.13
Quality: pending | Created: 2025-01-19
"""

import numpy as np
import pandas as pd
from bokeh.io import export_png, save
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
from bokeh.resources import CDN


# Data - Monthly sales over 12 months
np.random.seed(42)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
sales = np.random.randint(50000, 150000, size=12)
sales_trend = sales + np.linspace(0, 30000, 12).astype(int)  # Upward trend

df = pd.DataFrame({"month": months, "sales": sales_trend})
source = ColumnDataSource(df)

# Create figure with export tools (Bokeh's built-in toolbar provides save/export functionality)
# The toolbar includes SaveTool which allows PNG/SVG export via right-click menu
p = figure(
    width=4800,
    height=2700,
    x_range=months,
    title="chart-export-menu · bokeh · pyplots.ai",
    x_axis_label="Month",
    y_axis_label="Sales ($)",
    tools="pan,box_zoom,wheel_zoom,save,reset",  # Save tool provides export menu
    toolbar_location="above",  # Toolbar at top for easy access
)

# Bar chart showing sales data
p.vbar(
    x="month",
    top="sales",
    source=source,
    width=0.7,
    fill_color="#306998",  # Python Blue
    line_color="#306998",
    fill_alpha=0.8,
)

# Add hover tool for interactivity
hover = HoverTool(tooltips=[("Month", "@month"), ("Sales", "$@sales{,}")], mode="vline")
p.add_tools(hover)

# Styling for 4800x2700 canvas
p.title.text_font_size = "32pt"
p.title.align = "center"
p.xaxis.axis_label_text_font_size = "24pt"
p.yaxis.axis_label_text_font_size = "24pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.major_label_text_font_size = "18pt"

# Grid styling
p.xgrid.visible = False
p.ygrid.grid_line_alpha = 0.3
p.ygrid.grid_line_dash = [4, 4]

# Axis styling
p.xaxis.major_tick_line_color = None
p.yaxis.major_tick_line_color = "#666666"
p.outline_line_color = None

# Y-axis formatting
p.yaxis.formatter.use_scientific = False
p.y_range.start = 0

# Toolbar styling (the export menu location)
p.toolbar.logo = None  # Remove bokeh logo for cleaner look

# Save static PNG for preview
export_png(p, filename="plot.png")

# Save interactive HTML with export menu functionality
# Users can click the save icon in the toolbar to export PNG/SVG
save(p, filename="plot.html", resources=CDN, title="Chart with Export Menu")
