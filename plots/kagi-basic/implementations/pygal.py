"""pyplots.ai
kagi-basic: Basic Kagi Chart
Library: pygal 3.1.0 | Python 3.13.11
Quality: 72/100 | Created: 2026-01-08
"""

import os

import cairosvg
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

# Build XY points for each segment with connection points for continuity
yang_series_list = []
yin_series_list = []
prev_end_point = None

for seg in segments:
    points = []
    cols = seg["columns"]

    # Start from the connection point (previous segment's end)
    if prev_end_point is not None:
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

# Colors - vibrant green for yang, strong red for yin
YANG_COLOR = "#16A34A"  # Green - bullish/uptrend
YIN_COLOR = "#DC2626"  # Red - bearish/downtrend

# Stroke widths - extreme difference for visibility
YANG_WIDTH = 12  # Thick line for bullish yang
YIN_WIDTH = 3  # Thin line for bearish yin

# Custom style for large canvas
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#000000",
    foreground_subtle="#CCCCCC",
    colors=(YANG_COLOR, YIN_COLOR),
    title_font_size=64,
    label_font_size=42,
    major_label_font_size=38,
    legend_font_size=42,
    value_font_size=30,
    opacity=1.0,
    opacity_hover=1.0,
    guide_stroke_dasharray="4,4",
    stroke_width=YANG_WIDTH,  # Default to yang width
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
    legend_box_size=30,
)

# Combine all yang points into one series
yang_all_points = []
for points in yang_series_list:
    if yang_all_points:
        yang_all_points.append((None, None))  # Break between segments
    yang_all_points.extend(points)

# Combine all yin points into one series
yin_all_points = []
for points in yin_series_list:
    if yin_all_points:
        yin_all_points.append((None, None))  # Break between segments
    yin_all_points.extend(points)

# Add series - yang with thick stroke, yin with thin stroke
chart.add("Yang (Bullish) ━━━", yang_all_points, stroke_style={"width": YANG_WIDTH})
chart.add("Yin (Bearish) ─", yin_all_points, stroke_style={"width": YIN_WIDTH})

# Render SVG and manually fix stroke widths since pygal ignores stroke_style
svg_content = chart.render().decode("utf-8")

# Fix yang series stroke width (serie-0) - thick green line
svg_content = svg_content.replace(".serie-0 {", f".serie-0 {{stroke-width: {YANG_WIDTH}; stroke: {YANG_COLOR}; ")

# Fix yin series stroke width (serie-1) - thin red line
svg_content = svg_content.replace(".serie-1 {", f".serie-1 {{stroke-width: {YIN_WIDTH}; stroke: {YIN_COLOR}; ")

# Also ensure path elements get the right stroke width with !important
svg_content = svg_content.replace("stroke-width: 12", f"stroke-width: {YANG_WIDTH}")

# Add CSS overrides to ensure stroke widths are applied correctly
css_override = f"""
<style type="text/css">
  .serie-0 path {{ stroke-width: {YANG_WIDTH} !important; stroke: {YANG_COLOR} !important; }}
  .serie-1 path {{ stroke-width: {YIN_WIDTH} !important; stroke: {YIN_COLOR} !important; }}
  .legends .legend text {{ font-size: 42px !important; }}
</style>
"""

# Insert CSS override after opening svg tag
svg_content = svg_content.replace("<defs>", css_override + "<defs>")

# Save modified SVG and convert to PNG
with open("plot_temp.svg", "w", encoding="utf-8") as f:
    f.write(svg_content)

# Convert to PNG using cairosvg
cairosvg.svg2png(url="plot_temp.svg", write_to="plot.png")

# Clean up temp file
os.remove("plot_temp.svg")

# Save HTML version (original chart without modifications)
chart.render_to_file("plot.html")
