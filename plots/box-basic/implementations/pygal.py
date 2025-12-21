""" pyplots.ai
box-basic: Basic Box Plot
Library: pygal 3.1.0 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-14
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Generate distributions for different departments
np.random.seed(42)
categories = ["Engineering", "Marketing", "Sales", "Operations", "HR"]
data = {
    "Engineering": np.random.normal(85000, 15000, 100),
    "Marketing": np.random.normal(72000, 12000, 100),
    "Sales": np.random.normal(68000, 18000, 100),
    "Operations": np.random.normal(62000, 10000, 100),
    "HR": np.random.normal(58000, 8000, 100),
}

# Custom style using PyPlots colors
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#4CAF50", "#FF5722", "#9C27B0"),
    title_font_size=60,
    label_font_size=40,
    major_label_font_size=36,
    legend_font_size=36,
    value_font_size=32,
)

# Create box chart
chart = pygal.Box(
    width=4800,
    height=2700,
    style=custom_style,
    title="box-basic · pygal · pyplots.ai",
    x_title="Department",
    y_title="Salary ($)",
    show_legend=True,
    legend_at_bottom=True,
    show_y_guides=True,
    show_x_guides=False,
    margin=50,
)

# Add data for each category
for category in categories:
    chart.add(category, data[category].tolist())

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
