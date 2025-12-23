""" pyplots.ai
ridgeline-basic: Basic Ridgeline Plot
Library: pygal 3.1.0 | Python 3.13.11
Quality: 87/100 | Created: 2025-12-23
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Monthly temperature distributions for a city
np.random.seed(42)

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Generate temperature data with seasonal variation
base_temps = [2, 4, 8, 13, 18, 22, 25, 24, 19, 13, 7, 3]
month_data = []
for base in base_temps:
    temps = np.random.normal(base, 3, 100)
    month_data.append(temps)

# Common x range for all distributions
x_range = np.linspace(-10, 40, 150)

# Compute KDE for each month (inline, no functions)
kde_data = []
for temps in month_data:
    n = len(temps)
    bandwidth = n ** (-1 / 5) * np.std(temps)
    density = np.zeros_like(x_range)
    for xi in temps:
        density += np.exp(-0.5 * ((x_range - xi) / bandwidth) ** 2)
    density /= n * bandwidth * np.sqrt(2 * np.pi)
    kde_data.append(density)

# Normalize all densities
max_density = max(d.max() for d in kde_data)
kde_data = [d / max_density for d in kde_data]

# Color gradient with improved distinction between winter months
# Using more varied blue tones and adding purple/teal for better differentiation
colors = [
    "#2563eb",  # Jan - bright blue
    "#7c3aed",  # Feb - purple (distinct from blues)
    "#0891b2",  # Mar - teal/cyan
    "#10b981",  # Apr - emerald green (spring)
    "#84cc16",  # May - lime green
    "#eab308",  # Jun - yellow
    "#f97316",  # Jul - orange (peak summer)
    "#eab308",  # Aug - yellow
    "#84cc16",  # Sep - lime green
    "#10b981",  # Oct - emerald green
    "#0891b2",  # Nov - teal/cyan
    "#2563eb",  # Dec - bright blue
]

# Custom style for 4800x2700 px canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=tuple(colors),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=36,
    value_font_size=36,
    opacity=0.85,
    opacity_hover=0.95,
)

# Ridge parameters
ridge_height = 2.5  # Height scale for density curves
ridge_spacing = 1.8  # Vertical spacing between ridges (controls overlap)

# Create Y-axis labels at ridge baseline positions (months as labels, not numbers)
y_labels = []
for i, month in enumerate(reversed(months)):
    y_labels.append({"value": i * ridge_spacing + ridge_height * 0.3, "label": month})

# Create XY chart with month labels on Y-axis, no legend (spec requires Y-axis labels)
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="Monthly Temperature Distribution · ridgeline-basic · pygal · pyplots.ai",
    x_title="Temperature (°C)",
    y_title="Month",
    show_legend=False,  # Remove redundant legend; Y-axis shows month labels
    stroke=True,
    fill=True,
    dots_size=0,
    show_x_guides=True,
    show_y_guides=False,
    range=(-0.5, len(months) * ridge_spacing + ridge_height),
    xrange=(-10, 40),
    stroke_style={"width": 2},
    y_labels=y_labels,
    y_labels_major_every=1,
)

# Add ridges from back (Dec) to front (Jan) for proper layering
for i, (month, density) in enumerate(reversed(list(zip(months, kde_data, strict=True)))):
    # Baseline y-position for this ridge
    baseline = i * ridge_spacing

    # Scale density to ridge height
    scaled_density = density * ridge_height

    # Create closed polygon: bottom edge (baseline) + top edge (density curve) + close
    bottom_edge = [(float(x), float(baseline)) for x in x_range]
    top_edge = [(float(x), float(baseline + d)) for x, d in zip(x_range[::-1], scaled_density[::-1], strict=True)]
    polygon = bottom_edge + top_edge + [bottom_edge[0]]

    chart.add(month, polygon)

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
