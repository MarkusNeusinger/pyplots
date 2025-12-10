"""
radar-basic: Basic Radar Chart
Library: bokeh
"""

import numpy as np
from bokeh.io import export_png, output_file, save
from bokeh.models import ColumnDataSource, LabelSet, Legend, LegendItem
from bokeh.plotting import figure


# Data - Performance metrics for two athletes
categories = ["Speed", "Power", "Accuracy", "Stamina", "Technique"]
athlete_a = [85, 70, 90, 65, 80]
athlete_b = [70, 85, 75, 80, 70]

# Number of variables
n_vars = len(categories)

# Compute angles for each axis (starting from top, going clockwise)
angles = np.linspace(0, 2 * np.pi, n_vars, endpoint=False)
# Rotate so first category is at the top
angles = angles + np.pi / 2


# Convert polar to Cartesian coordinates
def polar_to_cartesian(values, angles):
    x = np.array(values) * np.cos(angles)
    y = np.array(values) * np.sin(angles)
    return x, y


# Close the polygons by appending first point
angles_closed = np.append(angles, angles[0])
athlete_a_closed = athlete_a + [athlete_a[0]]
athlete_b_closed = athlete_b + [athlete_b[0]]

# Convert to Cartesian
x_a, y_a = polar_to_cartesian(athlete_a_closed, angles_closed)
x_b, y_b = polar_to_cartesian(athlete_b_closed, angles_closed)

# Axis endpoints (at value 100)
x_axes, y_axes = polar_to_cartesian([100] * n_vars, angles)

# Category label positions (slightly beyond 100)
x_labels, y_labels = polar_to_cartesian([110] * n_vars, angles)

# Create figure
p = figure(
    width=4800,
    height=2700,
    title="Athlete Performance Comparison",
    x_range=(-150, 180),
    y_range=(-130, 150),
    tools="",
    toolbar_location=None,
)

# Color palette from style guide
color_a = "#306998"  # Python Blue
color_b = "#DC2626"  # Signal Red

# Draw grid circles
for r in [20, 40, 60, 80, 100]:
    circle_angles = np.linspace(0, 2 * np.pi, 100)
    cx = r * np.cos(circle_angles)
    cy = r * np.sin(circle_angles)
    p.line(cx, cy, line_color="gray", line_alpha=0.3, line_width=1)

# Draw axis lines from center to each category
for i in range(n_vars):
    p.line([0, x_axes[i]], [0, y_axes[i]], line_color="gray", line_alpha=0.5, line_width=1)

# Plot Athlete A polygon
source_a = ColumnDataSource(data={"x": x_a, "y": y_a})
line_a = p.line("x", "y", source=source_a, line_color=color_a, line_width=3)
p.patch(x_a, y_a, fill_color=color_a, fill_alpha=0.25, line_alpha=0)
p.scatter(x_a[:-1], y_a[:-1], size=12, color=color_a)

# Plot Athlete B polygon
source_b = ColumnDataSource(data={"x": x_b, "y": y_b})
line_b = p.line("x", "y", source=source_b, line_color=color_b, line_width=3)
p.patch(x_b, y_b, fill_color=color_b, fill_alpha=0.25, line_alpha=0)
p.scatter(x_b[:-1], y_b[:-1], size=12, color=color_b)

# Add category labels
label_source = ColumnDataSource(data={"x": x_labels, "y": y_labels, "text": categories})
labels = LabelSet(
    x="x", y="y", text="text", source=label_source, text_font_size="20pt", text_align="center", text_baseline="middle"
)
p.add_layout(labels)

# Add value labels for grid circles
for r in [20, 40, 60, 80, 100]:
    p.text([5], [r], text=[str(r)], text_font_size="14pt", text_color="gray", text_baseline="middle")

# Create legend
legend = Legend(
    items=[LegendItem(label="Athlete A", renderers=[line_a]), LegendItem(label="Athlete B", renderers=[line_b])],
    location="top_right",
    label_text_font_size="16pt",
)
p.add_layout(legend, "right")

# Styling
p.title.text_font_size = "24pt"
p.title.align = "center"
p.xaxis.visible = False
p.yaxis.visible = False
p.xgrid.visible = False
p.ygrid.visible = False
p.outline_line_color = None
p.background_fill_color = "white"

# Save outputs
export_png(p, filename="plot.png")
output_file("plot.html", title="Basic Radar Chart")
save(p)
