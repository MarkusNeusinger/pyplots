"""pyplots.ai
subplot-mosaic: Mosaic Subplot Layout with Varying Sizes
Library: bokeh | Python 3.13
Quality: pending | Created: 2025-12-31
"""

import numpy as np
from bokeh.io import export_png
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure


np.random.seed(42)

# Color palette (Python Blue and Yellow)
PYTHON_BLUE = "#306998"
PYTHON_YELLOW = "#FFD43B"

# Data for various subplots - Dashboard with business metrics

# A: Large overview time series (top left, spans 2 rows)
days = np.arange(1, 91)
revenue = 50000 + np.cumsum(np.random.randn(90) * 2000) + days * 300
source_a = ColumnDataSource(data={"day": days, "revenue": revenue})

# B: Scatter plot (top right)
products = np.random.rand(50) * 100
profit_margin = products * 0.3 + np.random.randn(50) * 5 + 10
source_b = ColumnDataSource(data={"products": products, "profit_margin": profit_margin})

# C: Bar chart - Categories (middle left)
categories = ["Electronics", "Clothing", "Food", "Books"]
sales = [45000, 32000, 28000, 18000]
source_c = ColumnDataSource(data={"category": categories, "sales": sales})

# D: Line chart - Monthly trend (bottom, spans full width)
months = np.arange(1, 13)
monthly_orders = [1200, 1400, 1100, 1600, 1800, 2100, 1900, 2200, 2400, 2100, 2300, 2800]
source_d = ColumnDataSource(data={"month": months, "orders": monthly_orders})

# E: Small metric - Conversion rate trend
weeks = np.arange(1, 13)
conversion = 3.2 + np.cumsum(np.random.randn(12) * 0.2)
source_e = ColumnDataSource(data={"week": weeks, "conversion": conversion})

# F: Small metric - Customer satisfaction
quarters = ["Q1", "Q2", "Q3", "Q4"]
satisfaction = [78, 82, 85, 88]
source_f = ColumnDataSource(data={"quarter": quarters, "satisfaction": satisfaction})

# A: Large Revenue Overview (spans 2 columns, taller)
p_a = figure(
    width=3200,
    height=1100,
    title="Quarterly Revenue Overview",
    x_axis_label="Day",
    y_axis_label="Revenue ($)",
    toolbar_location=None,
)
p_a.line("day", "revenue", source=source_a, line_width=4, color=PYTHON_BLUE)
p_a.scatter("day", "revenue", source=source_a, size=8, color=PYTHON_BLUE, alpha=0.6)
p_a.title.text_font_size = "28pt"
p_a.xaxis.axis_label_text_font_size = "20pt"
p_a.yaxis.axis_label_text_font_size = "20pt"
p_a.xaxis.major_label_text_font_size = "16pt"
p_a.yaxis.major_label_text_font_size = "16pt"
p_a.grid.grid_line_alpha = 0.3
p_a.grid.grid_line_dash = "dashed"

# B: Product Profitability Scatter
p_b = figure(
    width=1600,
    height=1100,
    title="Product Profitability",
    x_axis_label="Units Sold",
    y_axis_label="Profit Margin (%)",
    toolbar_location=None,
)
p_b.scatter(
    "products",
    "profit_margin",
    source=source_b,
    size=18,
    color=PYTHON_YELLOW,
    alpha=0.7,
    line_color=PYTHON_BLUE,
    line_width=2,
)
p_b.title.text_font_size = "24pt"
p_b.xaxis.axis_label_text_font_size = "18pt"
p_b.yaxis.axis_label_text_font_size = "18pt"
p_b.xaxis.major_label_text_font_size = "14pt"
p_b.yaxis.major_label_text_font_size = "14pt"
p_b.grid.grid_line_alpha = 0.3
p_b.grid.grid_line_dash = "dashed"

# C: Category Sales Bar Chart
p_c = figure(
    width=2400,
    height=900,
    x_range=categories,
    title="Sales by Category",
    x_axis_label="Category",
    y_axis_label="Sales ($)",
    toolbar_location=None,
)
p_c.vbar(
    x="category",
    top="sales",
    source=source_c,
    width=0.7,
    color=PYTHON_BLUE,
    alpha=0.85,
    line_color="white",
    line_width=2,
)
p_c.title.text_font_size = "24pt"
p_c.xaxis.axis_label_text_font_size = "18pt"
p_c.yaxis.axis_label_text_font_size = "18pt"
p_c.xaxis.major_label_text_font_size = "14pt"
p_c.yaxis.major_label_text_font_size = "14pt"
p_c.xaxis.major_label_orientation = 0.3
p_c.grid.grid_line_alpha = 0.3
p_c.grid.grid_line_dash = "dashed"

# E: Conversion Rate Mini Chart
p_e = figure(
    width=2400, height=450, title="Conversion Rate (%)", x_axis_label="Week", y_axis_label="Rate", toolbar_location=None
)
p_e.line("week", "conversion", source=source_e, line_width=4, color=PYTHON_BLUE)
p_e.scatter("week", "conversion", source=source_e, size=12, color=PYTHON_YELLOW)
p_e.title.text_font_size = "22pt"
p_e.xaxis.axis_label_text_font_size = "16pt"
p_e.yaxis.axis_label_text_font_size = "16pt"
p_e.xaxis.major_label_text_font_size = "14pt"
p_e.yaxis.major_label_text_font_size = "14pt"
p_e.grid.grid_line_alpha = 0.3
p_e.grid.grid_line_dash = "dashed"

# F: Customer Satisfaction Bar
p_f = figure(
    width=2400,
    height=450,
    x_range=quarters,
    title="Customer Satisfaction",
    x_axis_label="Quarter",
    y_axis_label="Score",
    toolbar_location=None,
)
p_f.vbar(
    x="quarter",
    top="satisfaction",
    source=source_f,
    width=0.6,
    color=PYTHON_YELLOW,
    alpha=0.9,
    line_color=PYTHON_BLUE,
    line_width=2,
)
p_f.title.text_font_size = "22pt"
p_f.xaxis.axis_label_text_font_size = "16pt"
p_f.yaxis.axis_label_text_font_size = "16pt"
p_f.xaxis.major_label_text_font_size = "14pt"
p_f.yaxis.major_label_text_font_size = "14pt"
p_f.grid.grid_line_alpha = 0.3
p_f.grid.grid_line_dash = "dashed"

# D: Monthly Orders Trend with main title (full width bottom)
p_d = figure(
    width=4800,
    height=700,
    title="subplot-mosaic · bokeh · pyplots.ai",
    x_axis_label="Month",
    y_axis_label="Orders",
    toolbar_location=None,
)
p_d.line("month", "orders", source=source_d, line_width=5, color=PYTHON_BLUE)
p_d.scatter("month", "orders", source=source_d, size=20, color=PYTHON_YELLOW, line_color=PYTHON_BLUE, line_width=3)
p_d.title.text_font_size = "32pt"
p_d.xaxis.axis_label_text_font_size = "22pt"
p_d.yaxis.axis_label_text_font_size = "22pt"
p_d.xaxis.major_label_text_font_size = "18pt"
p_d.yaxis.major_label_text_font_size = "18pt"
p_d.grid.grid_line_alpha = 0.3
p_d.grid.grid_line_dash = "dashed"

# Create mosaic layout: AAB / CEF / DDD pattern
# Row 1: A (large, spans 2 cols) + B on right
# Row 2: C left, E and F stacked on right
# Row 3: D spans full width

# Stack E and F vertically for middle right
right_stack = column(p_e, p_f)

# Row 1: Large A + B
row1 = row(p_a, p_b)

# Row 2: C + stacked (E, F)
row2 = row(p_c, right_stack)

# Full layout
layout = column(row1, row2, p_d)

export_png(layout, filename="plot.png")
