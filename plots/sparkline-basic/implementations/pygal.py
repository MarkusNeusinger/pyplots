""" pyplots.ai
sparkline-basic: Basic Sparkline
Library: pygal 3.1.0 | Python 3.13.11
Quality: 85/100 | Created: 2025-12-23
"""

import pygal
from pygal.style import Style


# Data - simulated daily sales trend with realistic variation
# 30 data points representing a month of daily sales with growth AND decline periods
values = [
    65,
    72,
    78,
    85,
    82,
    88,
    95,
    92,
    86,
    79,
    72,
    68,
    62,
    58,
    55,
    52,
    48,
    45,
    51,
    58,
    65,
    73,
    82,
    89,
    96,
    102,
    98,
    105,
    110,
    108,
]

# Find min/max indices for highlighting
min_val = min(values)
max_val = max(values)
min_idx = values.index(min_val)
max_idx = values.index(max_val)

# Custom style for sparkline - minimal and clean
# Colors: main line (blue), min point (yellow), max point (yellow)
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333",
    foreground_strong="#333",
    foreground_subtle="#666",
    colors=("#306998", "#FFD43B", "#FFD43B"),  # Main line, min highlight, max highlight
    title_font_size=72,
    label_font_size=1,
    major_label_font_size=1,
    legend_font_size=1,
    value_font_size=1,
    stroke_width=8,  # Slightly thicker line for visibility at large canvas
    opacity=1.0,
    opacity_hover=1.0,
)

# Create sparkline chart - pure visualization without chrome
chart = pygal.Line(
    width=4800,
    height=2700,
    style=custom_style,
    show_x_labels=False,  # No X axis labels for sparkline
    show_y_labels=False,  # No Y axis labels for sparkline
    show_x_guides=False,  # No vertical gridlines
    show_y_guides=False,  # No horizontal gridlines
    show_legend=False,  # No legend - sparklines are pure visualization
    show_dots=True,  # Enable dots globally for highlight points
    dots_size=6,  # Base dot size
    fill=True,  # Area fill under line
    interpolate="cubic",  # Smooth line for clean appearance
    margin=100,
    title="sparkline-basic · pygal · pyplots.ai",
)

# Add main sparkline data
chart.add("", values)

# Add separate series for min point highlight (larger yellow dot)
min_series = [None] * len(values)
min_series[min_idx] = min_val
chart.add("", min_series, stroke=False, show_dots=True, dots_size=30)

# Add separate series for max point highlight (larger yellow dot)
max_series = [None] * len(values)
max_series[max_idx] = max_val
chart.add("", max_series, stroke=False, show_dots=True, dots_size=30)

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
