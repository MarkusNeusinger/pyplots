"""pyplots.ai
area-stock-range: Stock Area Chart with Range Selector
Library: bokeh | Python 3.13
Quality: pending | Created: 2026-01-11
"""

import numpy as np
import pandas as pd
from bokeh.io import export_png, save
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, RangeTool
from bokeh.plotting import figure
from bokeh.resources import CDN


# Data - Generate realistic stock price data over 3 years
np.random.seed(42)
n_days = 756  # ~3 years of trading days
dates = pd.date_range(start="2023-01-03", periods=n_days, freq="B")

# Generate realistic stock price movement using geometric Brownian motion
initial_price = 150.0
daily_returns = np.random.normal(0.0003, 0.015, n_days)  # ~7.5% annual return, 24% volatility
price_multipliers = np.exp(np.cumsum(daily_returns))
prices = initial_price * price_multipliers

# Add some trend changes and volatility clusters
trend_boost = np.sin(np.linspace(0, 4 * np.pi, n_days)) * 0.15
volatility_cluster = np.exp(-((np.arange(n_days) - 400) ** 2) / 20000) * 0.1
prices = prices * (1 + trend_boost + volatility_cluster)

source = ColumnDataSource(data={"date": dates, "price": prices})

# Main figure - Area chart with range selector
p = figure(
    width=4800,
    height=2200,
    title="area-stock-range · bokeh · pyplots.ai",
    x_axis_type="datetime",
    x_axis_label="Date",
    y_axis_label="Price (USD)",
    x_range=(dates[500], dates[-1]),  # Initial view: last ~256 trading days
    tools="xpan,xwheel_zoom,reset,save",
    active_scroll="xwheel_zoom",
)

# Area fill - semi-transparent with Python Blue
p.varea(x="date", y1=0, y2="price", source=source, fill_color="#306998", fill_alpha=0.4)

# Solid line on top
p.line(x="date", y="price", source=source, line_color="#306998", line_width=3)

# Style main chart
p.title.text_font_size = "28pt"
p.xaxis.axis_label_text_font_size = "22pt"
p.yaxis.axis_label_text_font_size = "22pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.major_label_text_font_size = "18pt"
p.grid.grid_line_alpha = 0.3
p.grid.grid_line_dash = "dashed"

# Range selector - mini chart at bottom
select = figure(
    width=4800,
    height=500,
    x_axis_type="datetime",
    y_axis_type=None,
    tools="",
    toolbar_location=None,
    x_axis_label="Drag to select date range",
)

# Fill area in range selector
select.varea(x="date", y1=0, y2="price", source=source, fill_color="#306998", fill_alpha=0.3)

# Line in range selector
select.line(x="date", y="price", source=source, line_color="#306998", line_width=2)

# Range tool overlay
range_tool = RangeTool(x_range=p.x_range)
range_tool.overlay.fill_color = "#FFD43B"
range_tool.overlay.fill_alpha = 0.3

select.add_tools(range_tool)
select.xaxis.major_label_text_font_size = "16pt"
select.xaxis.axis_label_text_font_size = "18pt"
select.grid.grid_line_alpha = 0.2

# Combine layouts
layout = column(p, select)

# Save output
export_png(layout, filename="plot.png")
save(layout, filename="plot.html", resources=CDN, title="area-stock-range · bokeh · pyplots.ai")
