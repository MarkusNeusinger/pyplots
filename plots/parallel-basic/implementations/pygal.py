"""
parallel-basic: Basic Parallel Coordinates Plot
Library: pygal
"""

import pygal
from pygal.style import Style


# Data - Iris dataset (same as other implementations)
# Using inline data for reproducibility and simplicity
iris_data = {
    "setosa": [
        [5.1, 3.5, 1.4, 0.2],
        [4.9, 3.0, 1.4, 0.2],
        [4.7, 3.2, 1.3, 0.2],
        [4.6, 3.1, 1.5, 0.2],
        [5.0, 3.6, 1.4, 0.2],
        [5.4, 3.9, 1.7, 0.4],
        [4.6, 3.4, 1.4, 0.3],
        [5.0, 3.4, 1.5, 0.2],
        [4.4, 2.9, 1.4, 0.2],
        [4.9, 3.1, 1.5, 0.1],
        [5.4, 3.7, 1.5, 0.2],
        [4.8, 3.4, 1.6, 0.2],
        [4.8, 3.0, 1.4, 0.1],
        [4.3, 3.0, 1.1, 0.1],
        [5.8, 4.0, 1.2, 0.2],
    ],
    "versicolor": [
        [7.0, 3.2, 4.7, 1.4],
        [6.4, 3.2, 4.5, 1.5],
        [6.9, 3.1, 4.9, 1.5],
        [5.5, 2.3, 4.0, 1.3],
        [6.5, 2.8, 4.6, 1.5],
        [5.7, 2.8, 4.5, 1.3],
        [6.3, 3.3, 4.7, 1.6],
        [4.9, 2.4, 3.3, 1.0],
        [6.6, 2.9, 4.6, 1.3],
        [5.2, 2.7, 3.9, 1.4],
        [5.0, 2.0, 3.5, 1.0],
        [5.9, 3.0, 4.2, 1.5],
        [6.0, 2.2, 4.0, 1.0],
        [6.1, 2.9, 4.7, 1.4],
        [5.6, 2.9, 3.6, 1.3],
    ],
    "virginica": [
        [6.3, 3.3, 6.0, 2.5],
        [5.8, 2.7, 5.1, 1.9],
        [7.1, 3.0, 5.9, 2.1],
        [6.3, 2.9, 5.6, 1.8],
        [6.5, 3.0, 5.8, 2.2],
        [7.6, 3.0, 6.6, 2.1],
        [4.9, 2.5, 4.5, 1.7],
        [7.3, 2.9, 6.3, 1.8],
        [6.7, 2.5, 5.8, 1.8],
        [7.2, 3.6, 6.1, 2.5],
        [6.5, 3.2, 5.1, 2.0],
        [6.4, 2.7, 5.3, 1.9],
        [6.8, 3.0, 5.5, 2.1],
        [5.7, 2.5, 5.0, 2.0],
        [5.8, 2.8, 5.1, 2.4],
    ],
}

# Compute min/max for normalization across all species
all_values = [[row[i] for species in iris_data.values() for row in species] for i in range(4)]
mins = [min(col) for col in all_values]
maxs = [max(col) for col in all_values]


# Normalize function
def normalize(value, col_idx):
    return (value - mins[col_idx]) / (maxs[col_idx] - mins[col_idx])


# Species colors - Python Blue, Yellow, and a complementary teal
species_colors = {"setosa": "#306998", "versicolor": "#FFD43B", "virginica": "#4ECDC4"}

# Build color list in exact order for each series added
# 3 species x 15 observations each = 45 colors
color_list = []
for species_name in iris_data:
    color = species_colors[species_name]
    color_list.extend([color] * len(iris_data[species_name]))

# Create custom style for 4800x2700 px output
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=tuple(color_list),
    title_font_size=56,
    label_font_size=40,
    major_label_font_size=36,
    legend_font_size=36,
    value_font_size=28,
    opacity=0.5,
    opacity_hover=0.9,
)

# Create line chart to simulate parallel coordinates
chart = pygal.Line(
    width=4800,
    height=2700,
    style=custom_style,
    title="parallel-basic · pygal · pyplots.ai",
    x_title="Dimensions",
    y_title="Normalized Value",
    show_dots=False,
    stroke_style={"width": 3},
    show_y_guides=True,
    show_x_guides=True,
    x_label_rotation=0,
    legend_at_bottom=True,
    legend_box_size=30,
    truncate_legend=-1,
    range=(0, 1),
    margin=50,
    spacing=30,
    show_legend=False,  # Disable default legend due to pygal limitation
)

# X-axis labels for dimensions
chart.x_labels = ["Sepal Length", "Sepal Width", "Petal Length", "Petal Width"]

# Add data for each species
for _species_name, rows in iris_data.items():
    for row in rows:
        normalized = [normalize(row[i], i) for i in range(4)]
        chart.add("", normalized, stroke_style={"width": 2})

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
