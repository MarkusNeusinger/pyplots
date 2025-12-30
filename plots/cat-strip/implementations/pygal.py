"""pyplots.ai
cat-strip: Categorical Strip Plot
Library: pygal | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Performance scores across different departments
np.random.seed(42)
categories = ["Sales", "Engineering", "Marketing", "Support"]
n_per_category = 25

# Generate realistic performance scores for each department
data = {
    "Sales": np.random.normal(75, 12, n_per_category),
    "Engineering": np.random.normal(82, 8, n_per_category),
    "Marketing": np.random.normal(70, 15, n_per_category),
    "Support": np.random.normal(78, 10, n_per_category),
}

# Clip to realistic range (0-100)
for cat in data:
    data[cat] = np.clip(data[cat], 40, 100)

# Create jittered x-positions for strip plot effect
jitter_width = 0.3
points_by_category = {}
for i, cat in enumerate(categories):
    x_jitter = np.random.uniform(-jitter_width, jitter_width, n_per_category)
    x_positions = i + x_jitter
    points_by_category[cat] = list(zip(x_positions, data[cat], strict=False))

# Custom style for large canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=("#306998", "#FFD43B", "#4CAF50", "#E91E63"),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
    tooltip_font_size=36,
)

# Create custom x-label formatter to show category names
x_label_map = {0: "Sales", 1: "Engineering", 2: "Marketing", 3: "Support"}

# Create XY chart (scatter plot)
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="cat-strip · pygal · pyplots.ai",
    x_title="Department",
    y_title="Performance Score",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=4,
    stroke=False,
    dots_size=12,
    show_x_guides=False,
    show_y_guides=True,
    x_label_rotation=0,
    range=(35, 105),
    xrange=(-0.5, 3.5),
    explicit_size=True,
    print_values=False,
    x_value_formatter=lambda x: x_label_map.get(int(round(x)), ""),
)

# Add data for each category as separate series
for cat in categories:
    chart.add(cat, points_by_category[cat])

# Set x-axis labels at category positions (integers that will be formatted)
chart.x_labels = [0, 1, 2, 3]
chart.x_labels_major = [0, 1, 2, 3]

# Render to PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
