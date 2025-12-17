"""
band-basic: Basic Band Plot
Library: pygal
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Time series with 95% confidence interval
np.random.seed(42)
x = np.arange(0, 50)

# Create central trend line (simulating a model prediction)
y_center = 50 + 0.8 * x + 5 * np.sin(x / 5)

# Create upper and lower bounds (confidence interval)
uncertainty = 3 + 0.5 * np.sqrt(x)  # Increasing uncertainty over time
y_upper = y_center + uncertainty
y_lower = y_center - uncertainty

# Custom style for 4800x2700 canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333",
    foreground_strong="#333",
    foreground_subtle="#666",
    # Colors: transparent base, band fill, center line
    colors=("rgba(255,255,255,0)", "#306998", "#FFD43B"),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
    opacity=0.35,
    opacity_hover=0.5,
)

# Create stacked line chart to simulate band with overlaid center line
# pygal doesn't have native band support, so we use stacking technique:
# 1. Transparent base at y_lower level
# 2. Band fill (y_upper - y_lower) stacked on top
# 3. Center line as non-stacked overlay (using secondary_fill approach)
chart = pygal.StackedLine(
    width=4800,
    height=2700,
    title="band-basic · pygal · pyplots.ai",
    x_title="Time (units)",
    y_title="Value",
    style=custom_style,
    fill=True,
    show_dots=False,
    show_y_guides=True,
    show_x_guides=False,
    x_label_rotation=0,
    legend_at_bottom=True,
    truncate_legend=-1,
    range=(min(y_lower) - 5, max(y_upper) + 5),
    show_legend=True,
)

# X-axis labels (show every 10th for readability)
chart.x_labels = [str(int(v)) if v % 10 == 0 else "" for v in x]

# Add lower boundary as transparent base (blends with white background)
chart.add(None, [float(v) for v in y_lower], fill=True, stroke=False)

# Add band height (stacks on top of base to reach y_upper)
band_height = y_upper - y_lower
chart.add("95% Confidence Interval", [float(v) for v in band_height], fill=True, stroke=False)

# Add central trend line (non-filled, visible stroke)
# Use allow_interruptions to ensure line draws on top of stacked areas
chart.add(
    "Central Trend",
    [{"value": float(v), "style": "stroke-width: 6"} for v in y_center],
    fill=False,
    stroke=True,
    show_dots=False,
    allow_interruptions=True,
)

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
