"""pyplots.ai
density-basic: Basic Density Plot
Library: pygal | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - simulated test scores showing slightly left-skewed distribution
np.random.seed(42)
values = np.concatenate(
    [
        np.random.normal(75, 8, 200),  # Main cluster around 75
        np.random.normal(60, 5, 50),  # Smaller cluster showing slight left skew
    ]
)


# Compute KDE using Gaussian kernel
x_range = np.linspace(values.min() - 10, values.max() + 10, 200)
n = len(values)
bandwidth = n ** (-1 / 5) * np.std(values)  # Scott's rule
density = np.zeros_like(x_range)
for xi in values:
    density += np.exp(-0.5 * ((x_range - xi) / bandwidth) ** 2)
density /= n * bandwidth * np.sqrt(2 * np.pi)

# Custom style for 4800x2700 px (scaled 3x from template for large canvas)
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333",
    foreground_strong="#333",
    foreground_subtle="#666",
    colors=("#306998",),
    title_font_size=56,
    label_font_size=42,
    major_label_font_size=36,
    legend_font_size=36,
    value_font_size=32,
)

# Create XY chart for continuous density curve
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="density-basic · pygal · pyplots.ai",
    x_title="Test Score (points)",
    y_title="Probability Density",
    show_dots=False,
    stroke_style={"width": 3},
    fill=True,
    show_legend=False,
    show_y_guides=True,
    show_x_guides=False,
)

# Add density curve data as XY points
xy_data = [(float(x), float(y)) for x, y in zip(x_range, density, strict=True)]
chart.add("Density", xy_data)

# Add rug plot as small vertical marks along x-axis (sampled for clarity)
rug_height = max(density) * 0.02  # Small height for rug marks
rug_sample = values[::5]  # Sample every 5th point to avoid clutter
rug_data = []
for xi in rug_sample:
    rug_data.append((float(xi), 0))
    rug_data.append((float(xi), float(rug_height)))
    rug_data.append((float(xi), 0))

# Add rug marks as a separate series with thinner stroke
chart.add("Observations", rug_data, stroke_style={"width": 1}, show_dots=False, fill=False)

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
