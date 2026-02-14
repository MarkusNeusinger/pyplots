""" pyplots.ai
box-basic: Basic Box Plot
Library: pygal 3.1.0 | Python 3.14
Quality: 80/100 | Created: 2025-12-23
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Generate salary distributions for different departments
np.random.seed(42)
categories = ["Engineering", "Marketing", "Sales", "Operations", "HR"]
data = {
    "Engineering": np.random.normal(85000, 15000, 100),
    "Marketing": np.random.normal(72000, 12000, 100),
    "Sales": np.random.normal(68000, 18000, 100),
    "Operations": np.random.normal(62000, 10000, 100),
    "HR": np.random.normal(58000, 8000, 100),
}

# Add outliers to demonstrate box plot features
data["Engineering"] = np.append(data["Engineering"], [130000, 135000, 40000])
data["Sales"] = np.append(data["Sales"], [120000, 25000])

# Custom style scaled for 4800x2700 canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#cccccc",
    colors=("#306998", "#E69F00", "#009E73", "#D55E00", "#8B5CF6"),
    title_font_size=72,
    label_font_size=44,
    major_label_font_size=40,
    legend_font_size=44,
    value_font_size=32,
    opacity=0.9,
    opacity_hover=1.0,
)

# Create box chart
chart = pygal.Box(
    width=4800,
    height=2700,
    style=custom_style,
    title="box-basic \u00b7 pygal \u00b7 pyplots.ai",
    x_title="Department",
    y_title="Salary ($)",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=5,
    legend_box_size=36,
    truncate_legend=-1,
    truncate_label=-1,
    show_y_guides=True,
    show_x_guides=False,
    margin=60,
    spacing=40,
    box_mode="tukey",
    dots_size=8,
)

# Add data for each category
for category in categories:
    chart.add(category, data[category].tolist())

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
