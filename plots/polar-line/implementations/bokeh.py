"""pyplots.ai
polar-line: Polar Line Plot
Library: bokeh | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import numpy as np
from bokeh.io import export_png
from bokeh.models import ColumnDataSource, LabelSet
from bokeh.plotting import figure


# Data: Average temperature by month (cyclical pattern)
np.random.seed(42)
months = np.arange(12)
month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Two cities with different seasonal patterns
city_a_temps = np.array([2, 4, 10, 15, 20, 25, 28, 27, 22, 15, 8, 3])  # Northern climate
city_b_temps = np.array([28, 27, 24, 20, 15, 12, 10, 12, 16, 20, 24, 27])  # Southern climate

# Convert to polar coordinates (theta in radians)
theta = months * (2 * np.pi / 12)

# Close the loop by appending first point at the end
theta_closed = np.append(theta, theta[0])
city_a_closed = np.append(city_a_temps, city_a_temps[0])
city_b_closed = np.append(city_b_temps, city_b_temps[0])

# Convert polar to Cartesian coordinates
# Normalize radius to fit nicely in plot (scale temps to 0.3-1.0 range)
max_temp = max(city_a_temps.max(), city_b_temps.max())
min_temp = min(city_a_temps.min(), city_b_temps.min())


def polar_to_cartesian(theta, r, r_min, r_max, scale_min=0.3, scale_max=1.0):
    """Convert polar to Cartesian, scaling radius to desired range."""
    r_scaled = scale_min + (r - r_min) / (r_max - r_min) * (scale_max - scale_min)
    x = r_scaled * np.cos(theta)
    y = r_scaled * np.sin(theta)
    return x, y


x_a, y_a = polar_to_cartesian(theta_closed, city_a_closed, min_temp, max_temp)
x_b, y_b = polar_to_cartesian(theta_closed, city_b_closed, min_temp, max_temp)

# Create figure (square for polar plot)
p = figure(
    width=3600,
    height=3600,
    title="polar-line · bokeh · pyplots.ai",
    x_range=(-1.4, 1.4),
    y_range=(-1.4, 1.4),
    tools="",
    toolbar_location=None,
)

# Hide axes (polar plots don't use traditional axes)
p.axis.visible = False
p.grid.visible = False

# Draw concentric circles for reference (grid lines)
for r in [0.3, 0.5, 0.7, 0.9, 1.0]:
    circle_theta = np.linspace(0, 2 * np.pi, 100)
    circle_x = r * np.cos(circle_theta)
    circle_y = r * np.sin(circle_theta)
    p.line(circle_x, circle_y, line_color="gray", line_alpha=0.3, line_width=1)

# Draw radial lines for months
for i, name in enumerate(month_names):
    angle = i * (2 * np.pi / 12)
    x_end = 1.15 * np.cos(angle)
    y_end = 1.15 * np.sin(angle)
    p.line([0, x_end], [0, y_end], line_color="gray", line_alpha=0.3, line_width=1)

    # Add month labels
    label_x = 1.25 * np.cos(angle)
    label_y = 1.25 * np.sin(angle)
    source = ColumnDataSource(data={"x": [label_x], "y": [label_y], "text": [name]})
    labels = LabelSet(
        x="x",
        y="y",
        text="text",
        source=source,
        text_align="center",
        text_baseline="middle",
        text_font_size="22pt",
        text_color="#333333",
    )
    p.add_layout(labels)

# Add temperature labels on circles (positioned at top right for better visibility)
temp_labels = [f"{int(min_temp)}°C", "", f"{int((min_temp + max_temp) / 2)}°C", "", f"{int(max_temp)}°C"]
radii = [0.3, 0.5, 0.7, 0.9, 1.0]
label_angle = np.pi / 6  # 30 degrees (between Jan and Feb)
for r, label in zip(radii, temp_labels, strict=False):
    if label:
        lx = r * np.cos(label_angle) + 0.05
        ly = r * np.sin(label_angle) + 0.02
        source = ColumnDataSource(data={"x": [lx], "y": [ly], "text": [label]})
        labels = LabelSet(
            x="x",
            y="y",
            text="text",
            source=source,
            text_align="left",
            text_baseline="bottom",
            text_font_size="18pt",
            text_color="#444444",
        )
        p.add_layout(labels)

# Plot City A (Northern climate) - Python Blue
source_a = ColumnDataSource(data={"x": x_a, "y": y_a})
p.line(x="x", y="y", source=source_a, line_color="#306998", line_width=4, legend_label="Northern City")
p.scatter(x=x_a[:-1], y=y_a[:-1], size=18, color="#306998", alpha=0.9)

# Plot City B (Southern climate) - Python Yellow
source_b = ColumnDataSource(data={"x": x_b, "y": y_b})
p.line(x="x", y="y", source=source_b, line_color="#FFD43B", line_width=4, legend_label="Southern City")
p.scatter(x=x_b[:-1], y=y_b[:-1], size=18, color="#FFD43B", alpha=0.9)

# Style
p.title.text_font_size = "36pt"
p.title.align = "center"
p.background_fill_color = "white"
p.border_fill_color = "white"
p.outline_line_color = None

# Legend - position in top left area
p.legend.location = "top_left"
p.legend.label_text_font_size = "22pt"
p.legend.background_fill_alpha = 0.9
p.legend.border_line_color = "#cccccc"
p.legend.padding = 15
p.legend.spacing = 10
p.legend.glyph_width = 30
p.legend.glyph_height = 30

# Save
export_png(p, filename="plot.png")
