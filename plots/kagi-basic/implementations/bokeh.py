"""pyplots.ai
kagi-basic: Basic Kagi Chart
Library: bokeh | Python 3.13
Quality: pending | Created: 2025-01-08
"""

import numpy as np
from bokeh.io import export_png
from bokeh.plotting import figure, output_file, save


# Generate sample stock price data
np.random.seed(42)
n_days = 250  # ~1 year of trading days

# Simulate realistic stock price movements with trend
returns = np.random.normal(0.0005, 0.02, n_days)  # Daily returns
price = 100 * np.cumprod(1 + returns)

# Build Kagi chart data
reversal_pct = 0.04  # 4% reversal threshold

kagi_segments = []  # List of (x1, y1, x2, y2, is_yang, thickness)
direction = None  # 'up' or 'down'
last_price = price[0]
high = price[0]
low = price[0]
x_pos = 0

for i in range(1, len(price)):
    p = price[i]

    if direction is None:
        # Initialize direction
        change = (p - last_price) / last_price
        if change >= reversal_pct:
            direction = "up"
            is_yang = True
            kagi_segments.append((x_pos, last_price, x_pos, p, is_yang))
            high = p
            last_price = p
        elif change <= -reversal_pct:
            direction = "down"
            is_yang = False
            kagi_segments.append((x_pos, last_price, x_pos, p, is_yang))
            low = p
            last_price = p
    elif direction == "up":
        if p > high:
            # Continue uptrend
            if kagi_segments:
                seg = kagi_segments[-1]
                kagi_segments[-1] = (seg[0], seg[1], seg[2], p, seg[4])
            high = p
            last_price = p
        elif (high - p) / high >= reversal_pct:
            # Reversal to down
            x_pos += 1
            # Add horizontal connector
            kagi_segments.append(
                (x_pos - 1, last_price, x_pos, last_price, kagi_segments[-1][4] if kagi_segments else True)
            )
            # Check if breaking below previous low (transition to yin)
            is_yang = p >= low
            kagi_segments.append((x_pos, last_price, x_pos, p, is_yang))
            direction = "down"
            low = p
            last_price = p
    else:  # direction == 'down'
        if p < low:
            # Continue downtrend
            if kagi_segments:
                seg = kagi_segments[-1]
                kagi_segments[-1] = (seg[0], seg[1], seg[2], p, seg[4])
            low = p
            last_price = p
        elif (p - low) / low >= reversal_pct:
            # Reversal to up
            x_pos += 1
            # Add horizontal connector
            kagi_segments.append(
                (x_pos - 1, last_price, x_pos, last_price, kagi_segments[-1][4] if kagi_segments else False)
            )
            # Check if breaking above previous high (transition to yang)
            is_yang = p > high
            kagi_segments.append((x_pos, last_price, x_pos, p, is_yang))
            direction = "up"
            high = p
            last_price = p

# Separate segments by type
yang_xs, yang_ys = [], []
yin_xs, yin_ys = [], []

for seg in kagi_segments:
    x1, y1, x2, y2, is_yang = seg
    if is_yang:
        yang_xs.append([x1, x2])
        yang_ys.append([y1, y2])
    else:
        yin_xs.append([x1, x2])
        yin_ys.append([y1, y2])

# Create figure
p = figure(
    width=4800,
    height=2700,
    title="kagi-basic · bokeh · pyplots.ai",
    x_axis_label="Kagi Line Index",
    y_axis_label="Price ($)",
    tools="",
    toolbar_location=None,
)

# Plot yang (bullish) segments - thick green
for xs, ys in zip(yang_xs, yang_ys, strict=True):
    p.line(xs, ys, line_width=8, line_color="#2ca02c", line_cap="round")

# Plot yin (bearish) segments - thin red
for xs, ys in zip(yin_xs, yin_ys, strict=True):
    p.line(xs, ys, line_width=3, line_color="#d62728", line_cap="round")

# Style configuration
p.title.text_font_size = "28pt"
p.title.align = "center"
p.xaxis.axis_label_text_font_size = "22pt"
p.yaxis.axis_label_text_font_size = "22pt"
p.xaxis.major_label_text_font_size = "18pt"
p.yaxis.major_label_text_font_size = "18pt"

# Grid styling
p.grid.grid_line_alpha = 0.3
p.grid.grid_line_dash = "dashed"

# Background
p.background_fill_color = "#fafafa"

# Save PNG and HTML
export_png(p, filename="plot.png")
output_file("plot.html")
save(p)
