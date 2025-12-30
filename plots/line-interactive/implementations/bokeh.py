""" pyplots.ai
line-interactive: Interactive Line Chart with Hover and Zoom
Library: bokeh 3.8.1 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-30
"""

import numpy as np
import pandas as pd
from bokeh.io import export_png
from bokeh.models import BoxZoomTool, ColumnDataSource, HoverTool, PanTool, ResetTool, WheelZoomTool
from bokeh.plotting import figure, output_file, save


# Data - Daily temperature readings for a year
np.random.seed(42)
dates = pd.date_range("2024-01-01", periods=365, freq="D")

# Simulate realistic temperature pattern with seasonal variation
day_of_year = np.arange(365)
seasonal = 15 * np.sin(2 * np.pi * (day_of_year - 80) / 365)  # Peak in summer
noise = np.random.normal(0, 3, 365)
temperature = 12 + seasonal + noise  # Base temp ~12°C

# Create DataFrame
df = pd.DataFrame({"date": dates, "temperature": temperature})

# Create ColumnDataSource with formatted date for hover
source = ColumnDataSource(
    data={
        "date": df["date"],
        "temperature": df["temperature"],
        "date_str": df["date"].dt.strftime("%Y-%m-%d"),
        "temp_str": [f"{t:.1f}" for t in df["temperature"]],
    }
)

# Create figure with 4800×2700 px dimensions
p = figure(
    width=4800,
    height=2700,
    title="line-interactive · bokeh · pyplots.ai",
    x_axis_label="Date",
    y_axis_label="Temperature (°C)",
    x_axis_type="datetime",
    tools="",  # Start with empty tools, add custom ones
    toolbar_location="right",
)

# Add interactive tools
wheel_zoom = WheelZoomTool()
pan = PanTool()
box_zoom = BoxZoomTool()
reset = ResetTool()

p.add_tools(wheel_zoom, pan, box_zoom, reset)
p.toolbar.active_scroll = wheel_zoom

# Add hover tool with detailed tooltip
hover = HoverTool(
    tooltips=[("Date", "@date_str"), ("Temperature", "@temp_str °C")], mode="vline", line_policy="nearest"
)
p.add_tools(hover)

# Plot line with Python Blue color
p.line(
    x="date",
    y="temperature",
    source=source,
    line_width=4,
    line_color="#306998",
    alpha=0.9,
    legend_label="Daily Temperature",
)

# Add circle markers at data points for hover interaction
p.scatter(
    x="date",
    y="temperature",
    source=source,
    size=10,
    fill_color="#306998",
    line_color="#FFD43B",
    line_width=2,
    alpha=0.8,
)

# Styling - Text sizes for large canvas
p.title.text_font_size = "36pt"
p.title.text_color = "#306998"
p.xaxis.axis_label_text_font_size = "28pt"
p.yaxis.axis_label_text_font_size = "28pt"
p.xaxis.major_label_text_font_size = "22pt"
p.yaxis.major_label_text_font_size = "22pt"

# Axis styling
p.xaxis.axis_line_width = 3
p.yaxis.axis_line_width = 3
p.xaxis.major_tick_line_width = 3
p.yaxis.major_tick_line_width = 3

# Grid styling - subtle
p.xgrid.grid_line_color = "#000000"
p.xgrid.grid_line_alpha = 0.2
p.xgrid.grid_line_dash = "dashed"
p.ygrid.grid_line_color = "#000000"
p.ygrid.grid_line_alpha = 0.2
p.ygrid.grid_line_dash = "dashed"

# Legend styling
p.legend.location = "top_left"
p.legend.label_text_font_size = "22pt"
p.legend.glyph_width = 50
p.legend.glyph_height = 50
p.legend.border_line_color = "#306998"
p.legend.border_line_width = 2
p.legend.background_fill_alpha = 0.8

# Background
p.background_fill_color = "#FAFAFA"
p.border_fill_color = "#FFFFFF"

# Toolbar styling
p.toolbar.logo = None

# Save as HTML for interactivity
output_file("plot.html", title="Interactive Line Chart")
save(p)

# Save as PNG for static preview
export_png(p, filename="plot.png")
