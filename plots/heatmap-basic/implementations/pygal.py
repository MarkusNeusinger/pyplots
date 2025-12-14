"""
heatmap-basic: Basic Heatmap
Library: pygal
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - create a sample performance metrics matrix
np.random.seed(42)
rows = ["Product A", "Product B", "Product C", "Product D", "Product E", "Product F", "Product G", "Product H"]
cols = ["Q1", "Q2", "Q3", "Q4", "Jan", "Feb", "Mar", "Apr"]

# Generate performance data (values between 0 and 100)
data = np.random.randint(20, 100, size=(len(rows), len(cols)))

# Custom style for 4800x2700 px
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998",),  # Python Blue base color
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
    tooltip_font_size=36,
)

# Create Dot chart (pygal's heatmap equivalent)
chart = pygal.Dot(
    width=4800,
    height=2700,
    style=custom_style,
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=4,
    dots_size=40,
    show_x_guides=False,
    show_y_guides=False,
    x_label_rotation=0,
    print_values=True,
    print_values_position="center",
)

chart.title = "heatmap-basic \u00b7 pygal \u00b7 pyplots.ai"
chart.x_labels = cols
chart.x_title = "Time Period"
chart.y_title = "Product"

# Add data rows
for i, row_name in enumerate(rows):
    chart.add(row_name, data[i].tolist())

# Save as SVG and PNG
chart.render_to_file("plot.svg")
chart.render_to_png("plot.png")

# Also save HTML for interactivity
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>heatmap-basic - pygal</title>
    <style>
        body {{ margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #f5f5f5; }}
        .chart {{ max-width: 100%; height: auto; }}
    </style>
</head>
<body>
    <figure class="chart">
        {chart.render(is_unicode=True)}
    </figure>
</body>
</html>
"""

with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)
