""" pyplots.ai
kagi-basic: Basic Kagi Chart
Library: pygal 3.1.0 | Python 3.13.11
Quality: 72/100 | Created: 2026-01-08
"""

import re

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

# Stroke widths - extreme difference for clear visibility
YANG_WIDTH = 36  # Very thick line for bullish/yang (4x difference from yin)
YIN_WIDTH = 9  # Thin line for bearish/yin
YANG_COLOR = "#16A34A"  # Green - spec requires green for yang/bullish
YIN_COLOR = "#DC2626"  # Red - spec requires red for yin/bearish

# Custom style for large canvas with subtle grid
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#000000",
    foreground_subtle="#CCCCCC",  # Lighter for subtle grid
    colors=(
        YANG_COLOR,
        YIN_COLOR,
        YANG_COLOR,
        YIN_COLOR,
        YANG_COLOR,
        YIN_COLOR,
        YANG_COLOR,
        YIN_COLOR,
        YANG_COLOR,
        YIN_COLOR,
        YANG_COLOR,
        YIN_COLOR,
    ),
    title_font_size=64,
    label_font_size=42,
    major_label_font_size=38,
    legend_font_size=38,
    value_font_size=30,
    opacity=1.0,
    opacity_hover=1.0,
    guide_stroke_dasharray="4,4",  # Dashed grid lines for subtlety
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

# Track series indices for yang vs yin for SVG post-processing
yang_series_indices = []
yin_series_indices = []
series_idx = 0

# Add yang segments (thick green lines) - bullish/uptrend
for i, points in enumerate(yang_series_list):
    label = "Yang (Bullish)" if i == 0 else None
    chart.add(label, points, stroke_style={"width": YANG_WIDTH})
    yang_series_indices.append(series_idx)
    series_idx += 1

# Add yin segments (thin red lines) - bearish/downtrend
for i, points in enumerate(yin_series_list):
    label = "Yin (Bearish)" if i == 0 else None
    chart.add(label, points, stroke_style={"width": YIN_WIDTH})
    yin_series_indices.append(series_idx)
    series_idx += 1

# Get the SVG output for post-processing
svg_data = chart.render()
svg_str = svg_data.decode("utf-8")


# Apply inline styles directly to path elements with explicit stroke-width
def apply_stroke_widths(svg_content):
    def replace_series(match):
        full_match = match.group(0)
        class_attr = match.group(1)

        # Extract serie number
        serie_match = re.search(r"serie-(\d+)", class_attr)
        if not serie_match:
            return full_match

        serie_num = int(serie_match.group(1))

        # Determine width and color based on yang/yin
        if serie_num in yang_series_indices:
            width = YANG_WIDTH
            color = YANG_COLOR
        else:
            width = YIN_WIDTH
            color = YIN_COLOR

        # Apply inline style to ALL path elements in this group
        def style_path(path_match):
            path_tag = path_match.group(0)
            if 'style="' in path_tag:
                return re.sub(r'style="[^"]*"', f'style="stroke:{color};stroke-width:{width};fill:none"', path_tag)
            else:
                return path_tag.replace("<path ", f'<path style="stroke:{color};stroke-width:{width};fill:none" ')

        full_match = re.sub(r"<path[^>]*>", style_path, full_match)
        return full_match

    return re.sub(r'<g class="(series serie-\d+ color-\d+)"[^>]*>.*?</g>', replace_series, svg_content, flags=re.DOTALL)


svg_str = apply_stroke_widths(svg_str)

# Override CSS stroke-width rules to ensure inline styles take precedence
svg_str = re.sub(r"(\.series\.serie-\d+\{)stroke-width:\d+", r"\1stroke-width:0", svg_str)


# Fix legend markers to be larger and correctly colored
def fix_legend_markers(svg_content):
    """Make legend markers larger and ensure correct colors."""

    # Find legend groups and enlarge circles/markers
    # Yang (series 0) should be green, Yin (first series after yang) should be red
    def enlarge_legend_marker(match):
        circle_tag = match.group(0)
        # Enlarge the circle radius from default ~6 to 16
        circle_tag = re.sub(r'r="(\d+(?:\.\d+)?)"', 'r="16"', circle_tag)
        return circle_tag

    # Enlarge legend circles
    svg_content = re.sub(r'<circle[^>]*class="[^"]*legend[^"]*"[^>]*>', enlarge_legend_marker, svg_content)

    # Also fix rect markers if used (pygal sometimes uses rects)
    def enlarge_legend_rect(match):
        rect_tag = match.group(0)
        rect_tag = re.sub(r'width="(\d+(?:\.\d+)?)"', 'width="32"', rect_tag)
        rect_tag = re.sub(r'height="(\d+(?:\.\d+)?)"', 'height="32"', rect_tag)
        return rect_tag

    svg_content = re.sub(r'<rect[^>]*class="[^"]*legend[^"]*"[^>]*>', enlarge_legend_rect, svg_content)

    # Ensure yang legend entry has green fill and yin has red fill
    # Pattern: Look for legend entries and fix their colors
    def fix_legend_color(match):
        entry = match.group(0)
        if "Yang" in entry:
            entry = re.sub(r'fill="[^"]*"', f'fill="{YANG_COLOR}"', entry, count=1)
        elif "Yin" in entry:
            entry = re.sub(r'fill="[^"]*"', f'fill="{YIN_COLOR}"', entry, count=1)
        return entry

    # Fix colors in legend circles/rects
    svg_content = re.sub(r'(<g class="legend[^"]*"[^>]*>.*?</g>)', fix_legend_color, svg_content, flags=re.DOTALL)

    return svg_content


svg_str = fix_legend_markers(svg_str)

# Convert to PNG using cairosvg for reliable stroke rendering
cairosvg.svg2png(bytestring=svg_str.encode("utf-8"), write_to="plot.png")

# Save HTML version
chart.render_to_file("plot.html")
