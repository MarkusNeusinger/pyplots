"""
scatter-color-groups: Scatter Plot with Color Groups
Library: pygal
"""

import numpy as np
import pygal
from pygal.style import Style


# Generate iris-like sample data
np.random.seed(42)

# Setosa cluster (short sepal length, wide sepal width)
setosa_x = np.random.normal(5.0, 0.35, 50)
setosa_y = np.random.normal(3.4, 0.38, 50)

# Versicolor cluster (medium sepal length, medium sepal width)
versicolor_x = np.random.normal(5.9, 0.52, 50)
versicolor_y = np.random.normal(2.8, 0.31, 50)

# Virginica cluster (long sepal length, medium-wide sepal width)
virginica_x = np.random.normal(6.6, 0.64, 50)
virginica_y = np.random.normal(3.0, 0.32, 50)

groups = {
    "Setosa": list(zip(setosa_x, setosa_y, strict=True)),
    "Versicolor": list(zip(versicolor_x, versicolor_y, strict=True)),
    "Virginica": list(zip(virginica_x, virginica_y, strict=True)),
}

# Style (using PyPlots.ai palette)
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#DC2626", "#059669", "#8B5CF6", "#F97316"),
    title_font_size=40,
    legend_font_size=32,
    label_font_size=32,
    major_label_font_size=32,
)

# Create XY scatter chart
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="Iris Sepal Dimensions by Species",
    x_title="Sepal Length (cm)",
    y_title="Sepal Width (cm)",
    stroke=False,
    show_x_guides=True,
    show_y_guides=True,
    dots_size=8,
)

# Add data by group
for group_name, points in groups.items():
    chart.add(group_name, points)

# Save
chart.render_to_png("plot.png")
