"""pyplots.ai
linked-views-selection: Multiple Linked Views with Selection Sync
Library: pygal | Python 3.13
Quality: pending | Created: 2026-01-08
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Simulated multivariate dataset with 3 clusters
np.random.seed(42)

# Generate clustered data
categories = ["Cluster A", "Cluster B", "Cluster C"]
n_per_cluster = 50

# Cluster centers and spreads
centers_x = [2.0, 5.5, 4.0]
centers_y = [3.0, 6.0, 2.0]
centers_val = [25, 45, 35]

x_data = []
y_data = []
value_data = []
cat_data = []

for i, cat in enumerate(categories):
    x_data.extend(np.random.normal(centers_x[i], 0.8, n_per_cluster))
    y_data.extend(np.random.normal(centers_y[i], 0.7, n_per_cluster))
    value_data.extend(np.random.normal(centers_val[i], 6, n_per_cluster))
    cat_data.extend([cat] * n_per_cluster)

x_data = np.array(x_data)
y_data = np.array(y_data)
value_data = np.array(value_data)
cat_data = np.array(cat_data)

# Simulate selection: Cluster B is selected
selected_category = "Cluster B"
selected_mask = cat_data == selected_category
n_selected = np.sum(selected_mask)
n_total = len(cat_data)

# Colors - order matters for pygal series assignment
color_selected = "#306998"  # Python Blue
color_unselected = "#CCCCCC"  # Gray
color_accent = "#FFD43B"  # Python Yellow

# Custom style for large canvas - unselected first (gray), then selected (blue)
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=(color_unselected, color_selected, color_accent),
    title_font_size=48,
    label_font_size=28,
    major_label_font_size=24,
    legend_font_size=28,
    value_font_size=22,
    stroke_width=3,
    opacity=0.85,
    opacity_hover=1.0,
)

# Create XY chart (scatter plot) showing linked selection concept
scatter_chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="linked-views-selection · pygal · pyplots.ai\nScatter Plot with Selection: {} of {} points (Cluster B highlighted)".format(
        n_selected, n_total
    ),
    x_title="X Coordinate",
    y_title="Y Coordinate",
    show_legend=True,
    legend_at_bottom=True,
    legend_box_size=24,
    dots_size=12,
    stroke=False,
    show_x_guides=True,
    show_y_guides=True,
)

# Add unselected points first (gray - from style colors[0])
unselected_points = [(x_data[i], y_data[i]) for i in range(len(x_data)) if not selected_mask[i]]
scatter_chart.add("Unselected (100 pts)", unselected_points, stroke=False)

# Add selected points (Python Blue - from style colors[1])
selected_points = [(x_data[i], y_data[i]) for i in range(len(x_data)) if selected_mask[i]]
scatter_chart.add("Selected: Cluster B (50 pts)", selected_points, stroke=False)

# Render scatter chart as the main plot
scatter_chart.render_to_png("plot.png")

# Also render HTML for interactivity (hover effects show data values)
scatter_chart.render_to_file("plot.html")
