"""
bubble-packed: Basic Packed Bubble Chart
Library: bokeh
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
# r = sqrt(value) * scaling factor
max_radius = 400  # max radius in pixels for display
radii = np.sqrt(values) / np.sqrt(max(values)) * max_radius


# Circle packing simulation - position circles without overlap
def pack_circles(radii, center=(2400, 1350), iterations=500):
    """Simple force-directed packing algorithm."""
    n = len(radii)
    # Start with random positions near center
    np.random.seed(42)
    x = center[0] + (np.random.rand(n) - 0.5) * 1000
    y = center[1] + (np.random.rand(n) - 0.5) * 600

    for _ in range(iterations):
        # Pull toward center
        for i in range(n):
            dx = center[0] - x[i]
            dy = center[1] - y[i]
            dist = np.sqrt(dx**2 + dy**2) + 0.01
            x[i] += dx * 0.01
            y[i] += dy * 0.01

        # Push apart overlapping circles
        for i in range(n):
            for j in range(i + 1, n):
                dx = x[j] - x[i]
                dy = y[j] - y[i]
                dist = np.sqrt(dx**2 + dy**2) + 0.01
                min_dist = radii[i] + radii[j] + 10  # 10px padding

                if dist < min_dist:
                    overlap = (min_dist - dist) / 2
                    x[i] -= dx / dist * overlap
                    y[i] -= dy / dist * overlap
                    x[j] += dx / dist * overlap
                    y[j] += dy / dist * overlap

    return x, y


# Pack circles
x_pos, y_pos = pack_circles(radii)

# Create color palette - using Python Blue as base with variations
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
    data={
        "x": x_pos,
        "y": y_pos,
        "radius": radii,
        "category": categories,
        "value": values,
        "color": colors,
        "label": [f"{c}\n${v}M" for c, v in zip(categories, values, strict=True)],
    }
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
# Filter labels for bubbles large enough to show text
label_source = ColumnDataSource(
    data={
        "x": [x_pos[i] for i in range(len(values)) if radii[i] > 120],
        "y": [y_pos[i] for i in range(len(values)) if radii[i] > 120],
        "text": [categories[i] for i in range(len(values)) if radii[i] > 120],
        "value_text": [f"${values[i]}M" for i in range(len(values)) if radii[i] > 120],
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
