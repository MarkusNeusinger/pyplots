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

# Custom style for 4800x2700 canvas - band color with transparency
band_style = Style(
    background="white",
    plot_background="white",
    foreground="#333",
    foreground_strong="#333",
    foreground_subtle="#666",
    colors=("white", "#306998"),  # Base (transparent), band color
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
    opacity=0.35,
    opacity_hover=0.5,
)

# Create stacked line chart to simulate band
# Band is created by stacking: lower (transparent) + band height = upper
chart = pygal.StackedLine(
    width=4800,
    height=2700,
    title="band-basic \u00b7 pygal \u00b7 pyplots.ai",
    x_title="Time (units)",
    y_title="Value",
    style=band_style,
    fill=True,
    show_dots=False,
    stroke_style={"width": 0},
    show_y_guides=True,
    show_x_guides=False,
    x_label_rotation=0,
    legend_at_bottom=True,
    truncate_legend=-1,
    range=(min(y_lower) - 5, max(y_upper) + 5),
    show_legend=True,
)

# Add x-axis labels (show every 10th for readability)
chart.x_labels = [str(int(v)) if v % 10 == 0 else "" for v in x]

# Add lower boundary as base (white fill blends with background)
chart.add(None, [float(v) for v in y_lower])

# Add band height (difference between upper and lower)
band_height = y_upper - y_lower
chart.add("95% Confidence Interval", [float(v) for v in band_height])

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
