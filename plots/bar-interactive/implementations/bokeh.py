"""pyplots.ai
bar-interactive: Interactive Bar Chart with Hover and Click
Library: bokeh | Python 3.13
Quality: pending | Created: 2025-01-07
"""

import numpy as np
from bokeh.io import export_png
from bokeh.models import ColumnDataSource, CustomJS, HoverTool, TapTool
from bokeh.plotting import figure, output_file, save


# Data - Product sales with additional context
np.random.seed(42)
categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys", "Food & Beverages"]
values = np.array([156000, 98000, 87000, 72000, 45000, 63000, 112000])
percentages = (values / values.sum() * 100).round(1)
units_sold = np.array([3200, 4900, 2100, 1800, 8900, 3100, 5600])

# Colors for bars (hover state will be different)
base_color = "#306998"
hover_color = "#FFD43B"
colors = [base_color] * len(categories)

# Create ColumnDataSource
source = ColumnDataSource(
    data={
        "category": categories,
        "value": values,
        "percentage": percentages,
        "units": units_sold,
        "color": colors,
        "hover_color": [hover_color] * len(categories),
    }
)

# Create figure with categorical x-axis
p = figure(
    x_range=categories,
    width=4800,
    height=2700,
    title="bar-interactive · bokeh · pyplots.ai",
    toolbar_location="above",
    tools="pan,wheel_zoom,box_zoom,reset,save",
)

# Create bars
bars = p.vbar(
    x="category",
    top="value",
    width=0.7,
    source=source,
    fill_color="color",
    line_color="#1a3d5c",
    line_width=2,
    fill_alpha=0.85,
    hover_fill_color="hover_color",
    hover_fill_alpha=1.0,
    hover_line_color="#b38f00",
)

# Add hover tool with custom tooltip
hover = HoverTool(
    renderers=[bars],
    tooltips=[
        ("Category", "@category"),
        ("Revenue", "$@value{0,0}"),
        ("Share", "@percentage%"),
        ("Units Sold", "@units{0,0}"),
    ],
    mode="vline",
)
p.add_tools(hover)

# Add tap tool for click interaction (with console callback for demo)
tap_callback = CustomJS(
    args={"source": source},
    code="""
    const indices = source.selected.indices;
    if (indices.length > 0) {
        const category = source.data['category'][indices[0]];
        const value = source.data['value'][indices[0]];
        console.log('Clicked:', category, 'Revenue: $' + value.toLocaleString());
    }
""",
)
tap_tool = TapTool(callback=tap_callback)
p.add_tools(tap_tool)

# Styling - Title
p.title.text_font_size = "32pt"
p.title.text_font_style = "bold"
p.title.text_color = "#2c3e50"

# Styling - Axes
p.xaxis.axis_label = "Product Category"
p.yaxis.axis_label = "Revenue (USD)"
p.xaxis.axis_label_text_font_size = "24pt"
p.yaxis.axis_label_text_font_size = "24pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.major_label_text_font_size = "18pt"
p.xaxis.major_label_orientation = 0.4  # Slight angle for readability

# Styling - Grid
p.xgrid.grid_line_color = None
p.ygrid.grid_line_alpha = 0.3
p.ygrid.grid_line_dash = "dashed"

# Styling - Axis lines
p.xaxis.axis_line_width = 2
p.yaxis.axis_line_width = 2
p.xaxis.axis_line_color = "#2c3e50"
p.yaxis.axis_line_color = "#2c3e50"

# Format y-axis with thousands separator
p.yaxis.formatter.use_scientific = False

# Outline
p.outline_line_color = "#2c3e50"
p.outline_line_width = 2

# Background
p.background_fill_color = "#fafafa"
p.border_fill_color = "white"

# Save as PNG
export_png(p, filename="plot.png")

# Also save interactive HTML version
output_file("plot.html", title="Interactive Bar Chart")
save(p)
