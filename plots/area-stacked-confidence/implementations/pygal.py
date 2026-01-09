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

# Product line A (Core) - steady growth with narrow confidence band
product_a = np.array([120.0, 125.0, 130.0, 140.0, 145.0, 150.0, 158.0, 165.0])
uncertainty_a = np.random.uniform(8, 12, n_points)

# Product line B (Growth) - moderate growth with medium uncertainty
product_b = np.array([80.0, 85.0, 88.0, 92.0, 95.0, 100.0, 105.0, 110.0])
uncertainty_b = np.random.uniform(6, 10, n_points)

# Product line C (New) - new product ramping up with higher uncertainty
product_c = np.array([30.0, 40.0, 55.0, 70.0, 85.0, 95.0, 105.0, 115.0])
uncertainty_c = np.random.uniform(12, 18, n_points)

# Calculate cumulative bounds for y-axis range
total_upper = product_a + product_b + product_c + uncertainty_a + uncertainty_b + uncertainty_c

# Style with distinct colors: light bands and darker centers for each product
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#222222",
    foreground_subtle="#555555",
    guide_stroke_color="#dddddd",
    colors=(
        "#ccdde8",  # A lower confidence band (very light blue)
        "#306998",  # A central value (blue)
        "#ccdde8",  # A upper confidence band (very light blue)
        "#f0e5cc",  # B lower confidence band (very light gold)
        "#c99000",  # B central value (gold)
        "#f0e5cc",  # B upper confidence band (very light gold)
        "#f0d0cc",  # C lower confidence band (very light red)
        "#c0392b",  # C central value (red)
        "#f0d0cc",  # C upper confidence band (very light red)
    ),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=44,
    legend_font_size=36,
    value_font_size=32,
    opacity="1",
    opacity_hover="1",
    font_family="sans-serif",
)

# Use StackedLine for proper stacking with visible confidence bands
chart = pygal.StackedLine(
    width=4800,
    height=2700,
    style=custom_style,
    title="area-stacked-confidence · pygal · pyplots.ai",
    x_title="Quarter",
    y_title="Revenue ($M)",
    fill=True,
    show_dots=False,
    show_x_guides=False,
    show_y_guides=True,
    legend_at_bottom=True,
    legend_box_size=28,
    truncate_legend=-1,
    margin=100,
    spacing=40,
    range=(0, float(total_upper.max() + 20)),
    stroke_style={"width": 0},
)

chart.x_labels = quarters

# Stack order: for each product, show lower_band, central_value, upper_band
# This creates visible confidence bands around each stacked area
# A: lower band height = uncertainty, central height = value - uncertainty, upper = uncertainty
chart.add("Core -90%", uncertainty_a.tolist())
chart.add("Core (A)", (product_a - uncertainty_a).tolist())
chart.add("Core +90%", uncertainty_a.tolist())

chart.add("Growth -90%", uncertainty_b.tolist())
chart.add("Growth (B)", (product_b - uncertainty_b).tolist())
chart.add("Growth +90%", uncertainty_b.tolist())

chart.add("New -90%", uncertainty_c.tolist())
chart.add("New (C)", (product_c - uncertainty_c).tolist())
chart.add("New +90%", uncertainty_c.tolist())

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
