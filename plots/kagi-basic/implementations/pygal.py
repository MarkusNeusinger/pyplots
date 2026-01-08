"""pyplots.ai
kagi-basic: Basic Kagi Chart
Library: pygal | Python 3.13
Quality: pending | Created: 2026-01-08
"""

import numpy as np
import pygal
from pygal.style import Style


# Data - Generate synthetic stock price data
np.random.seed(42)
n_days = 250
returns = np.random.normal(0.0005, 0.018, n_days)
prices = 100 * np.cumprod(1 + returns)

# Kagi chart calculation with 4% reversal threshold
reversal_pct = 0.04

# Build Kagi chart columns
columns = []
current_direction = "up"
last_high = prices[0]
last_low = prices[0]
prev_swing_high = prices[0]
prev_swing_low = prices[0]
col_idx = 0

current_col = {"x": col_idx, "start": prices[0], "end": prices[0], "type": "yang"}

for price in prices[1:]:
    if current_direction == "up":
        if price > last_high:
            last_high = price
            current_col["end"] = price
            if price > prev_swing_high:
                current_col["type"] = "yang"
        elif price < last_high * (1 - reversal_pct):
            columns.append(current_col)
            prev_swing_high = last_high
            col_idx += 1
            is_yin = price < prev_swing_low
            current_col = {
                "x": col_idx,
                "start": columns[-1]["end"],
                "end": price,
                "type": "yin" if is_yin else columns[-1]["type"],
            }
            current_direction = "down"
            last_low = price
    else:
        if price < last_low:
            last_low = price
            current_col["end"] = price
            if price < prev_swing_low:
                current_col["type"] = "yin"
        elif price > last_low * (1 + reversal_pct):
            columns.append(current_col)
            prev_swing_low = last_low
            col_idx += 1
            is_yang = price > prev_swing_high
            current_col = {
                "x": col_idx,
                "start": columns[-1]["end"],
                "end": price,
                "type": "yang" if is_yang else columns[-1]["type"],
            }
            current_direction = "up"
            last_high = price

columns.append(current_col)

# Group consecutive columns by type into segments
segments = []
current_segment = {"type": columns[0]["type"], "columns": [columns[0]]}

for col in columns[1:]:
    if col["type"] == current_segment["type"]:
        current_segment["columns"].append(col)
    else:
        segments.append(current_segment)
        current_segment = {"type": col["type"], "columns": [col]}
segments.append(current_segment)

# Build XY points for each segment
# Include connection point from previous segment to ensure continuity
yang_series_list = []
yin_series_list = []

prev_end_point = None

for seg in segments:
    points = []
    cols = seg["columns"]

    # Start from the connection point (previous segment's end)
    if prev_end_point is not None:
        # Add horizontal line from previous end to current start x
        first_col = cols[0]
        points.append((prev_end_point[0], prev_end_point[1]))
        points.append((first_col["x"], prev_end_point[1]))

    for i, col in enumerate(cols):
        x = col["x"]
        y_start = col["start"]
        y_end = col["end"]

        # Vertical line
        points.append((x, y_start))
        points.append((x, y_end))

        # Horizontal connector to next column (within same segment)
        if i < len(cols) - 1:
            next_x = cols[i + 1]["x"]
            points.append((next_x, y_end))

    # Track last point for next segment connection
    last_col = cols[-1]
    prev_end_point = (last_col["x"], last_col["end"])

    if seg["type"] == "yang":
        yang_series_list.append(points)
    else:
        yin_series_list.append(points)

# Custom style for large canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#000000",
    foreground_subtle="#555555",
    colors=(
        "#228B22",
        "#DC143C",
        "#228B22",
        "#DC143C",
        "#228B22",
        "#DC143C",
        "#228B22",
        "#DC143C",
        "#228B22",
        "#DC143C",
        "#228B22",
        "#DC143C",
    ),
    title_font_size=64,
    label_font_size=42,
    major_label_font_size=38,
    legend_font_size=38,
    value_font_size=30,
    opacity=1.0,
    opacity_hover=1.0,
)

# Create XY chart
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="kagi-basic · pygal · pyplots.ai",
    x_title="Kagi Line Index",
    y_title="Price ($)",
    show_dots=False,
    show_x_guides=False,
    show_y_guides=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=2,
    stroke=True,
    fill=False,
    margin=100,
    show_x_labels=True,
    show_y_labels=True,
    truncate_legend=-1,
)

# Add yang segments (thick green lines) - bullish/uptrend
for i, points in enumerate(yang_series_list):
    label = "Yang (Bullish)" if i == 0 else None
    chart.add(label, points, stroke_style={"width": 10})

# Add yin segments (thin red lines) - bearish/downtrend
for i, points in enumerate(yin_series_list):
    label = "Yin (Bearish)" if i == 0 else None
    chart.add(label, points, stroke_style={"width": 4})

# Save outputs
chart.render_to_file("plot.html")
chart.render_to_png("plot.png")
