"""pyplots.ai
cat-strip: Categorical Strip Plot
Library: pygal | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Plant growth experiment measurements
np.random.seed(42)

categories = ["Sunlight", "Partial Shade", "Full Shade", "Greenhouse"]
n_per_category = 15

data = {}
# Different growth patterns for each condition
data["Sunlight"] = np.random.normal(45, 8, n_per_category).tolist()
data["Partial Shade"] = np.random.normal(35, 6, n_per_category).tolist()
data["Full Shade"] = np.random.normal(22, 5, n_per_category).tolist()
data["Greenhouse"] = np.random.normal(55, 10, n_per_category).tolist()

# Custom style for pyplots
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#4ECDC4", "#E76F51"),
    title_font_size=48,
    label_font_size=32,
    major_label_font_size=28,
    legend_font_size=28,
    value_font_size=24,
    opacity=0.7,
    opacity_hover=0.9,
    stroke_width=2,
)

# Create XY chart for strip plot with jitter
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="cat-strip · pygal · pyplots.ai",
    x_title="Growth Condition",
    y_title="Plant Height (cm)",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=4,
    dots_size=12,
    stroke=False,
    show_x_guides=False,
    show_y_guides=True,
    x_label_rotation=0,
    truncate_label=-1,
    print_values=False,
)

# Add each category as a series with jittered x positions
for i, category in enumerate(categories):
    # Create jittered x positions around the category index
    jitter = np.random.uniform(-0.25, 0.25, len(data[category]))
    x_positions = i + 1 + jitter

    # Create (x, y) tuples for XY chart
    points = [(float(x), float(y)) for x, y in zip(x_positions, data[category], strict=True)]
    chart.add(category, points)

# Set x-axis labels at category positions
chart.x_labels = ["", "Sunlight", "Partial Shade", "Full Shade", "Greenhouse", ""]
chart.xrange = (0, 5)

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
