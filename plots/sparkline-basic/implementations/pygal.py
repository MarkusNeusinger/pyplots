""" pyplots.ai
sparkline-basic: Basic Sparkline
Library: pygal 3.1.0 | Python 3.13.11
Quality: 72/100 | Created: 2025-12-23
"""

import pygal
from pygal.style import Style


# Data - simulated daily sales trend with realistic variation
# 30 data points showing balanced growth and decline periods (not predominantly upward)
# Pattern: start mid-range, rise, decline to minimum, recover to max, decline again
values = [
    75,
    82,
    88,
    95,
    100,
    97,
    90,
    82,
    75,
    68,
    58,
    50,
    45,
    42,
    48,
    55,
    65,
    78,
    88,
    98,
    105,
    108,
    102,
    95,
    88,
    82,
    78,
    75,
    72,
    70,
]

# Find min/max indices for highlighting
min_val = min(values)
max_val = max(values)
min_idx = values.index(min_val)
max_idx = values.index(max_val)

# Custom style for sparkline - minimal and clean
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="transparent",
    foreground_strong="transparent",
    foreground_subtle="transparent",
    colors=("#306998",),  # Blue for main line
    title_font_size=72,
    label_font_size=1,
    major_label_font_size=1,
    legend_font_size=1,
    value_font_size=1,
    tooltip_font_size=1,
    stroke_width=8,  # Thicker line for visibility at large canvas
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
    show_dots=False,  # No dots on main line
    fill=True,  # Area fill under line
    interpolate="cubic",  # Smooth line for clean appearance
    margin=100,
    title="sparkline-basic · pygal · pyplots.ai",
)

# Create data with highlighted min/max points using dictionary format
# This allows per-point styling with 'node' style overrides
data_with_highlights = []
for i, val in enumerate(values):
    if i == min_idx:
        # Min point - red highlight for minimum value
        data_with_highlights.append({"value": val, "node": {"r": 25}, "color": "#E53935"})
    elif i == max_idx:
        # Max point - green highlight for maximum value
        data_with_highlights.append({"value": val, "node": {"r": 25}, "color": "#43A047"})
    else:
        # Regular points - no visible dots
        data_with_highlights.append({"value": val, "node": {"r": 0}})

# Add sparkline data with highlighted points
chart.add(None, data_with_highlights, show_dots=True)

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
