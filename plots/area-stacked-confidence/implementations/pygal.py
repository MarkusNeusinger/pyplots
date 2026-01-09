"""pyplots.ai
area-stacked-confidence: Stacked Area Chart with Confidence Bands
Library: pygal | Python 3.13
Quality: pending | Created: 2026-01-09
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Quarterly revenue forecasts by product line with confidence intervals
np.random.seed(42)
quarters = ["Q1'24", "Q2'24", "Q3'24", "Q4'24", "Q1'25", "Q2'25", "Q3'25", "Q4'25"]
n_points = len(quarters)

# Product line A (Core) - steady growth with narrow confidence band
product_a = np.array([120.0, 125.0, 130.0, 140.0, 145.0, 150.0, 158.0, 165.0])
product_a_uncertainty = np.random.uniform(8, 12, n_points)

# Product line B (Growth) - moderate growth with medium uncertainty
product_b = np.array([80.0, 85.0, 88.0, 92.0, 95.0, 100.0, 105.0, 110.0])
product_b_uncertainty = np.random.uniform(6, 10, n_points)

# Product line C (New) - new product ramping up with higher uncertainty
product_c = np.array([30.0, 40.0, 55.0, 70.0, 85.0, 95.0, 105.0, 115.0])
product_c_uncertainty = np.random.uniform(12, 18, n_points)

# Custom style for large canvas with enhanced visibility
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#222222",
    foreground_subtle="#555555",
    colors=(
        "#2a5278",  # Product A - dark blue
        "#306998",  # Product A band - Python Blue
        "#5a8ab8",  # Product A band - light blue
        "#c99c00",  # Product B band - dark yellow
        "#FFD43B",  # Product B - Python Yellow
        "#ffe880",  # Product B band - light yellow
        "#b03225",  # Product C band - dark red
        "#E74C3C",  # Product C - red
        "#f2a9a3",  # Product C band - light red
    ),
    title_font_size=72,
    label_font_size=42,
    major_label_font_size=38,
    legend_font_size=36,
    value_font_size=28,
    opacity=0.70,
    opacity_hover=0.90,
    transition="200ms",
    font_family="sans-serif",
)

# Create stacked line chart
chart = pygal.StackedLine(
    width=4800,
    height=2700,
    style=custom_style,
    title="area-stacked-confidence · pygal · pyplots.ai",
    x_title="Quarter",
    y_title="Revenue ($M)",
    fill=True,
    show_dots=True,
    dots_size=10,
    stroke_style={"width": 4},
    show_x_guides=False,
    show_y_guides=True,
    x_label_rotation=0,
    legend_at_bottom=True,
    legend_box_size=32,
    margin=100,
    spacing=50,
    truncate_legend=-1,
    show_legend=True,
)

# Set x-axis labels
chart.x_labels = quarters

# Add series in stacking order (bottom to top)
# Each product has: lower band, central value, upper band
# This creates a visual confidence band effect around each stacked area

# Product A (bottom layer) with 90% confidence band
chart.add("A (+90% CI)", (product_a_uncertainty * 0.5).tolist())
chart.add("Product A (Core)", product_a.tolist())
chart.add("A (-90% CI)", (product_a_uncertainty * 0.5).tolist())

# Product B (middle layer) with 90% confidence band
chart.add("B (+90% CI)", (product_b_uncertainty * 0.5).tolist())
chart.add("Product B (Growth)", product_b.tolist())
chart.add("B (-90% CI)", (product_b_uncertainty * 0.5).tolist())

# Product C (top layer) with 90% confidence band
chart.add("C (+90% CI)", (product_c_uncertainty * 0.5).tolist())
chart.add("Product C (New)", product_c.tolist())
chart.add("C (-90% CI)", (product_c_uncertainty * 0.5).tolist())

# Save as PNG and HTML
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
