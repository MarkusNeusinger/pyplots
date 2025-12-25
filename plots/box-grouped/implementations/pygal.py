"""pyplots.ai
box-grouped: Grouped Box Plot
Library: pygal | Python 3.13
Quality: pending | Created: 2025-12-25
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Employee performance scores across departments and experience levels
np.random.seed(42)

categories = ["Engineering", "Marketing", "Sales"]
subcategories = ["Junior", "Senior", "Lead"]

# Generate performance distributions with realistic differences
data = {}
# Engineering: Higher scores overall, tight distributions
data[("Engineering", "Junior")] = np.random.normal(72, 8, 50)
data[("Engineering", "Senior")] = np.random.normal(82, 6, 50)
data[("Engineering", "Lead")] = np.random.normal(88, 5, 50)

# Marketing: More variability
data[("Marketing", "Junior")] = np.random.normal(68, 12, 50)
data[("Marketing", "Senior")] = np.random.normal(76, 10, 50)
data[("Marketing", "Lead")] = np.random.normal(84, 8, 50)

# Sales: Widest distributions with outliers
data[("Sales", "Junior")] = np.random.normal(65, 15, 50)
data[("Sales", "Senior")] = np.random.normal(78, 12, 50)
data[("Sales", "Lead")] = np.random.normal(85, 10, 50)

# Add outliers to show box plot features
data[("Engineering", "Junior")] = np.append(data[("Engineering", "Junior")], [45, 95])
data[("Sales", "Senior")] = np.append(data[("Sales", "Senior")], [40, 105])
data[("Marketing", "Lead")] = np.append(data[("Marketing", "Lead")], [60, 100])

# Subcategory colors (colorblind-safe palette)
subcategory_colors = ["#306998", "#FFD43B", "#4CAF50"]  # Blue, Yellow, Green

# Build color list: repeat pattern for each category group
colors_list = subcategory_colors * len(categories)

# Custom style for large canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=tuple(colors_list),
    title_font_size=64,
    label_font_size=36,
    major_label_font_size=32,
    legend_font_size=40,
    value_font_size=28,
)

# Create box chart - use series names to show grouping
chart = pygal.Box(
    width=4800,
    height=2700,
    style=custom_style,
    title="box-grouped · pygal · pyplots.ai",
    x_title="Department / Experience Level",
    y_title="Performance Score (0-100)",
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=32,
    show_y_guides=True,
    show_x_guides=False,
    margin=60,
    box_mode="tukey",
    x_label_rotation=0,
)

# Add data series with descriptive labels showing category and subcategory
# This makes the grouping structure clear through naming
for category in categories:
    for subcategory in subcategories:
        label = f"{category} - {subcategory}"
        chart.add(label, data[(category, subcategory)].tolist())

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
