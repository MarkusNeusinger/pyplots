""" pyplots.ai
bubble-packed: Basic Packed Bubble Chart
Library: bokeh 3.8.1 | Python 3.13.11
Quality: 91/100 | Created: 2025-12-23
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import ColumnDataSource, LabelSet
from bokeh.plotting import figure


# Data - department budgets (in millions)
np.random.seed(42)
categories = [
    "Engineering",
    "Marketing",
    "Sales",
    "Operations",
    "HR",
    "Finance",
    "R&D",
    "Legal",
    "IT",
    "Customer Support",
    "Product",
    "Design",
    "QA",
    "Data Science",
    "Security",
]
values = [45, 32, 38, 25, 12, 18, 42, 8, 22, 15, 28, 14, 10, 20, 6]

# Calculate radii from values (scale by area for accurate perception)
max_radius = 400
radii = np.sqrt(values) / np.sqrt(max(values)) * max_radius

# Circle packing simulation - position circles without overlap
n = len(radii)
center_x, center_y = 2400, 1350

# Start with random positions near center
x_pos = center_x + (np.random.rand(n) - 0.5) * 1000
y_pos = center_y + (np.random.rand(n) - 0.5) * 600

# Force-directed packing iterations
for _ in range(500):
    # Pull toward center
    for i in range(n):
        dx = center_x - x_pos[i]
        dy = center_y - y_pos[i]
        x_pos[i] += dx * 0.01
        y_pos[i] += dy * 0.01

    # Push apart overlapping circles
    for i in range(n):
        for j in range(i + 1, n):
            dx = x_pos[j] - x_pos[i]
            dy = y_pos[j] - y_pos[i]
            dist = np.sqrt(dx**2 + dy**2) + 0.01
            min_dist = radii[i] + radii[j] + 10  # 10px padding

            if dist < min_dist:
                overlap = (min_dist - dist) / 2
                x_pos[i] -= dx / dist * overlap
                y_pos[i] -= dy / dist * overlap
                x_pos[j] += dx / dist * overlap
                y_pos[j] += dy / dist * overlap

# Create color palette - using Python Blue and Yellow with variations
colors = [
    "#306998",
    "#FFD43B",
    "#4B8BBE",
    "#FFE873",
    "#3776AB",
    "#FFD43B",
    "#306998",
    "#4B8BBE",
    "#FFE873",
    "#3776AB",
    "#306998",
    "#FFD43B",
    "#4B8BBE",
    "#FFE873",
    "#3776AB",
]

# Prepare data source
source = ColumnDataSource(
    data={"x": x_pos, "y": y_pos, "radius": radii, "category": categories, "value": values, "color": colors}
)

# Create figure
p = figure(
    width=4800,
    height=2700,
    title="Department Budgets · bubble-packed · bokeh · pyplots.ai",
    x_range=(0, 4800),
    y_range=(0, 2700),
    tools="hover",
    tooltips=[("Department", "@category"), ("Budget", "$@value M")],
)

# Draw circles
p.circle(
    x="x", y="y", radius="radius", source=source, fill_color="color", fill_alpha=0.85, line_color="white", line_width=3
)

# Add labels to circles (only for larger circles)
large_indices = [i for i in range(len(values)) if radii[i] > 120]
label_source = ColumnDataSource(
    data={
        "x": [x_pos[i] for i in large_indices],
        "y": [y_pos[i] for i in large_indices],
        "text": [categories[i] for i in large_indices],
        "value_text": [f"${values[i]}M" for i in large_indices],
    }
)

labels = LabelSet(
    x="x",
    y="y",
    text="text",
    source=label_source,
    text_align="center",
    text_baseline="middle",
    text_font_size="24pt",
    text_color="white",
    text_font_style="bold",
    y_offset=15,
)
p.add_layout(labels)

value_labels = LabelSet(
    x="x",
    y="y",
    text="value_text",
    source=label_source,
    text_align="center",
    text_baseline="middle",
    text_font_size="20pt",
    text_color="white",
    y_offset=-20,
)
p.add_layout(value_labels)

# Style the plot
p.title.text_font_size = "36pt"
p.title.align = "center"

# Hide axes - packed bubble charts don't use positional axes
p.xaxis.visible = False
p.yaxis.visible = False
p.xgrid.visible = False
p.ygrid.visible = False

# Clean background
p.background_fill_color = "#f8f9fa"
p.border_fill_color = "#f8f9fa"
p.outline_line_color = None

# Save as PNG and HTML
export_png(p, filename="plot.png")
output_file("plot.html", title="Packed Bubble Chart")
save(p)
