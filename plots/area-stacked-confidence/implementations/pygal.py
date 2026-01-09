""" pyplots.ai
area-stacked-confidence: Stacked Area Chart with Confidence Bands
Library: pygal 3.1.0 | Python 3.13.11
Quality: 62/100 | Created: 2026-01-09
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Quarterly revenue forecasts by product line with 90% confidence intervals
np.random.seed(42)
quarters = ["Q1'24", "Q2'24", "Q3'24", "Q4'24", "Q1'25", "Q2'25", "Q3'25", "Q4'25"]
n_points = len(quarters)
x = np.arange(n_points)

# Product line A (Core) - steady growth with narrow confidence band
product_a = np.array([120.0, 125.0, 130.0, 140.0, 145.0, 150.0, 158.0, 165.0])
product_a_lower = product_a - np.random.uniform(8, 12, n_points)
product_a_upper = product_a + np.random.uniform(8, 12, n_points)

# Product line B (Growth) - moderate growth with medium uncertainty
product_b = np.array([80.0, 85.0, 88.0, 92.0, 95.0, 100.0, 105.0, 110.0])
product_b_lower = product_b - np.random.uniform(6, 10, n_points)
product_b_upper = product_b + np.random.uniform(6, 10, n_points)

# Product line C (New) - new product ramping up with higher uncertainty
product_c = np.array([30.0, 40.0, 55.0, 70.0, 85.0, 95.0, 105.0, 115.0])
product_c_lower = product_c - np.random.uniform(12, 18, n_points)
product_c_upper = product_c + np.random.uniform(12, 18, n_points)

# Calculate cumulative values for stacking (A at bottom, then B, then C on top)
# Central values
cum_a = product_a
cum_b = cum_a + product_b
cum_c = cum_b + product_c

# Lower and upper bounds (cumulative) - each band surrounds its own series
cum_a_lower = product_a_lower
cum_a_upper = product_a_upper
cum_b_lower = cum_a + product_b_lower
cum_b_upper = cum_a + product_b_upper
cum_c_lower = cum_b + product_c_lower
cum_c_upper = cum_b + product_c_upper

# Custom style for large canvas with good visibility
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#222222",
    foreground_subtle="#555555",
    guide_stroke_color="#cccccc",
    colors=(
        "rgba(48, 105, 152, 0.3)",  # Product A band (semi-transparent blue)
        "#306998",  # Product A center (solid blue)
        "rgba(230, 168, 0, 0.3)",  # Product B band (semi-transparent gold)
        "#c99000",  # Product B center (solid gold)
        "rgba(231, 76, 60, 0.3)",  # Product C band (semi-transparent red)
        "#c0392b",  # Product C center (solid red)
    ),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=44,
    legend_font_size=42,
    value_font_size=32,
    opacity="1",
    opacity_hover="1",
    font_family="sans-serif",
)

# Create XY chart for precise polygon control
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="area-stacked-confidence · pygal · pyplots.ai",
    x_title="Quarter",
    y_title="Revenue ($M)",
    show_dots=False,
    show_x_guides=False,
    show_y_guides=True,
    fill=True,
    legend_at_bottom=True,
    legend_box_size=36,
    truncate_legend=-1,
    margin=100,
    spacing=50,
    range=(0, float(cum_c_upper.max() + 30)),
    xrange=(-0.3, float(n_points - 0.7)),
)

# Custom x-labels (use numeric x values 0-7 but display quarter names)
chart.x_labels = [{"value": i, "label": q} for i, q in enumerate(quarters)]
chart.x_labels_major = [{"value": i, "label": q} for i, q in enumerate(quarters)]

# Build confidence band polygons (upper bound forward, lower bound backward to close)
# Product A band polygon
band_a = [(float(xi), float(yi)) for xi, yi in zip(x, cum_a_upper, strict=True)]
band_a += [(float(xi), float(yi)) for xi, yi in zip(reversed(x), reversed(cum_a_lower), strict=True)]

# Product B band polygon
band_b = [(float(xi), float(yi)) for xi, yi in zip(x, cum_b_upper, strict=True)]
band_b += [(float(xi), float(yi)) for xi, yi in zip(reversed(x), reversed(cum_b_lower), strict=True)]

# Product C band polygon
band_c = [(float(xi), float(yi)) for xi, yi in zip(x, cum_c_upper, strict=True)]
band_c += [(float(xi), float(yi)) for xi, yi in zip(reversed(x), reversed(cum_c_lower), strict=True)]

# Build central line data
line_a = [(float(xi), float(yi)) for xi, yi in zip(x, cum_a, strict=True)]
line_b = [(float(xi), float(yi)) for xi, yi in zip(x, cum_b, strict=True)]
line_c = [(float(xi), float(yi)) for xi, yi in zip(x, cum_c, strict=True)]

# Add layers from bottom to top (A, then B, then C)
# Each layer has: confidence band (filled polygon) + central line (stroke only)

# Product A (bottom layer)
chart.add("A: Core (90% CI)", band_a, stroke=False)
chart.add("A: Core", line_a, fill=False, stroke=True, stroke_style={"width": 5})

# Product B (middle layer)
chart.add("B: Growth (90% CI)", band_b, stroke=False)
chart.add("B: Growth", line_b, fill=False, stroke=True, stroke_style={"width": 5})

# Product C (top layer)
chart.add("C: New (90% CI)", band_c, stroke=False)
chart.add("C: New", line_c, fill=False, stroke=True, stroke_style={"width": 5})

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
