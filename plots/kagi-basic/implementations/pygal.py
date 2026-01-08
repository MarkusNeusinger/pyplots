""" pyplots.ai
kagi-basic: Basic Kagi Chart
Library: pygal 3.1.0 | Python 3.13.11
Quality: 72/100 | Created: 2026-01-08
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Generate realistic stock price data
np.random.seed(42)
n_days = 250
returns = np.random.normal(0.001, 0.018, n_days)
prices = 100 * np.cumprod(1 + returns)

# Kagi chart parameters
reversal_pct = 0.04  # 4% reversal threshold

# Build Kagi chart turning points
kagi_points = [prices[0]]
direction = 0

for price in prices[1:]:
    last_price = kagi_points[-1]

    if direction == 0:
        if price >= last_price * (1 + reversal_pct):
            direction = 1
            kagi_points.append(price)
        elif price <= last_price * (1 - reversal_pct):
            direction = -1
            kagi_points.append(price)
    elif direction == 1:
        if price > last_price:
            kagi_points[-1] = price
        elif price <= last_price * (1 - reversal_pct):
            kagi_points.append(price)
            direction = -1
    else:
        if price < last_price:
            kagi_points[-1] = price
        elif price >= last_price * (1 + reversal_pct):
            kagi_points.append(price)
            direction = 1

# Determine yang/yin state for each segment
segments = []
is_yang = True
shoulder = kagi_points[0]
waist = kagi_points[0]

for i in range(len(kagi_points) - 1):
    y_start = kagi_points[i]
    y_end = kagi_points[i + 1]
    going_up = y_end > y_start

    if going_up and y_end > shoulder:
        is_yang = True
        shoulder = y_end
    elif not going_up and y_end < waist:
        is_yang = False
        waist = y_end

    segments.append((i, y_start, y_end, is_yang))

# Build color list matching segment order
segment_colors = []
for _, _, _, is_yang in segments:
    segment_colors.append("#16A34A" if is_yang else "#DC2626")

# Custom style
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    colors=tuple(segment_colors),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=40,
    legend_font_size=48,
    value_font_size=36,
    opacity=1.0,
    font_family="sans-serif",
)

# Create chart
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="kagi-basic \u00b7 pygal \u00b7 pyplots.ai",
    x_title="Kagi Line Index",
    y_title="Price ($)",
    show_dots=False,
    show_x_guides=False,
    show_y_guides=True,
    show_legend=False,
    margin=50,
    spacing=20,
    xrange=(0, len(segments) + 1),
)

# Add each segment as a separate series
for i, (x, y_start, y_end, is_yang) in enumerate(segments):
    path = []

    # Horizontal connector from previous point
    if i > 0:
        path.append((x - 1, y_start))
        path.append((x, y_start))

    # Vertical segment
    path.append((x, y_start))
    path.append((x, y_end))

    # Stroke width: thick for yang, thin for yin
    width = 10 if is_yang else 4
    chart.add("", path, stroke_style={"width": width}, show_dots=False)

# Save outputs
chart.render_to_png("plot.png")
chart.render_to_file("plot.html")
