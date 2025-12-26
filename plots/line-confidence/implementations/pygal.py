"""pyplots.ai
line-confidence: Line Plot with Confidence Interval
Library: pygal 3.1.0 | Python 3.13.11
Quality: 55/100 | Created: 2025-12-26
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Model predictions with 95% confidence interval
np.random.seed(42)

# Time points (e.g., weeks)
x = np.linspace(0, 12, 50)

# Central prediction: exponential growth pattern (e.g., user growth model)
y_center = 1000 + 500 * (1 - np.exp(-0.3 * x)) + np.random.randn(50) * 20
# Smooth the center line
y_center = np.convolve(y_center, np.ones(5) / 5, mode="same")
y_center[0:2] = y_center[2]  # Fix edge effects from convolution
y_center[-2:] = y_center[-3]

# Confidence interval widens over time (increasing uncertainty in predictions)
uncertainty = 30 + 15 * x
y_lower = y_center - uncertainty
y_upper = y_center + uncertainty

# Custom style for 4800x2700 canvas
# Note: pygal doesn't support per-series opacity, so we use colors with alpha
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    guide_stroke_color="#888888",
    colors=(
        "rgba(48, 105, 152, 0.3)",  # Light blue with transparency for upper fill
        "white",  # White to mask lower portion
        "#306998",  # Solid blue for center line
    ),
    opacity="1",  # Full opacity - transparency handled in colors
    opacity_hover="1",
    stroke_width=5,
    title_font_size=60,
    label_font_size=42,
    major_label_font_size=42,
    legend_font_size=42,
    value_font_size=36,
)

# Create XY chart with fill enabled for layered band effect
chart = pygal.XY(
    style=custom_style,
    width=4800,
    height=2700,
    title="95% Confidence Interval · line-confidence · pygal · pyplots.ai",
    x_title="Time (weeks)",
    y_title="Predicted Users",
    show_dots=False,
    show_x_guides=True,
    show_y_guides=True,
    fill=True,
    stroke=False,
    legend_at_bottom=True,
    truncate_legend=-1,
)

# Prepare data as XY tuples
upper_data = [(float(xi), float(yi)) for xi, yi in zip(x, y_upper, strict=True)]
lower_data = [(float(xi), float(yi)) for xi, yi in zip(x, y_lower, strict=True)]
center_data = [(float(xi), float(yi)) for xi, yi in zip(x, y_center, strict=True)]

# Layer 1: Upper bound filled down to baseline (creates top of band)
chart.add("95% Confidence Interval", upper_data, show_dots=False)

# Layer 2: Lower bound filled with white to mask everything below lower bound
chart.add(None, lower_data, show_dots=False)  # None = no legend entry

# Layer 3: Center line with solid stroke on top
chart.add("Predicted Mean", center_data, fill=False, stroke=True, show_dots=False, stroke_style={"width": 6})

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
