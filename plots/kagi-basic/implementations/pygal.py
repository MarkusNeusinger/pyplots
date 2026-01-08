""" pyplots.ai
kagi-basic: Basic Kagi Chart
Library: pygal 3.1.0 | Python 3.13.11
Quality: 85/100 | Created: 2026-01-08
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

# Build individual line segments for proper Kagi rendering
# Each segment is a separate 2-point series to avoid polygon connections
yang_segments = []  # List of [(x1,y1), (x2,y2)] for yang
yin_segments = []  # List of [(x1,y1), (x2,y2)] for yin

prev_x = None
prev_y = None

for col in columns:
    x = col["x"]
    y_start = col["start"]
    y_end = col["end"]
    seg_type = col["type"]

    # Horizontal connector (shoulder/waist) from previous column
    if prev_x is not None and prev_x != x:
        h_segment = [(prev_x, prev_y), (x, prev_y)]
        if seg_type == "yang":
            yang_segments.append(h_segment)
        else:
            yin_segments.append(h_segment)

    # Vertical line segment
    v_segment = [(x, y_start), (x, y_end)]
    if seg_type == "yang":
        yang_segments.append(v_segment)
    else:
        yin_segments.append(v_segment)

    prev_x = x
    prev_y = y_end

# Colors and stroke widths - large difference for visibility
YANG_COLOR = "#16A34A"  # Green for bullish
YIN_COLOR = "#DC2626"  # Red for bearish
YANG_WIDTH = 16  # Thick for yang (5x thicker for clear distinction)
YIN_WIDTH = 3  # Thin for yin

# Custom style
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#000000",
    foreground_subtle="#999999",
    colors=tuple([YANG_COLOR] * len(yang_segments) + [YIN_COLOR] * len(yin_segments)),
    title_font_size=64,
    label_font_size=42,
    major_label_font_size=38,
    legend_font_size=38,
    value_font_size=30,
    guide_stroke_dasharray="4,4",
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
    truncate_legend=-1,
)

# Add each segment as a separate series
# First yang segment gets label, rest are unlabeled
for i, seg in enumerate(yang_segments):
    label = "Yang (Bullish)" if i == 0 else None
    chart.add(label, seg, stroke_style={"width": YANG_WIDTH, "linecap": "round", "linejoin": "round"})

# First yin segment gets label, rest are unlabeled
for i, seg in enumerate(yin_segments):
    label = "Yin (Bearish)" if i == 0 else None
    chart.add(label, seg, stroke_style={"width": YIN_WIDTH, "linecap": "round", "linejoin": "round"})

# Render to SVG
svg_data = chart.render()
svg_str = svg_data.decode("utf-8")

# Track which series indices are yang vs yin
num_yang = len(yang_segments)
num_yin = len(yin_segments)


# Post-process SVG to enforce stroke widths using CSS override
def fix_stroke_styles(svg_content):
    """Add CSS rules to enforce correct stroke widths."""

    # Build CSS rules for yang series
    yang_css = ""
    for i in range(num_yang):
        yang_css += f".serie-{i} path {{ stroke: {YANG_COLOR} !important; stroke-width: {YANG_WIDTH} !important; fill: none !important; stroke-linecap: round; }}\n"

    # Build CSS rules for yin series
    yin_css = ""
    for i in range(num_yin):
        serie_idx = num_yang + i
        yin_css += f".serie-{serie_idx} path {{ stroke: {YIN_COLOR} !important; stroke-width: {YIN_WIDTH} !important; fill: none !important; stroke-linecap: round; }}\n"

    # Insert CSS after opening style tag
    style_css = yang_css + yin_css
    svg_content = re.sub(r"(<style[^>]*>)", rf"\1\n{style_css}", svg_content, count=1)

    return svg_content


svg_str = fix_stroke_styles(svg_str)


# Fix legend markers to show line segments with correct thickness
def fix_legend_markers(svg_content):
    """Replace legend dots with line segments showing thickness difference."""

    # Find the legends container
    legends_match = re.search(r'(<g class="legends"[^>]*>)(.*?)(</g>\s*</g>)', svg_content, re.DOTALL)
    if not legends_match:
        return svg_content

    legends_content = legends_match.group(2)

    # Find Yang legend (serie-0) and Yin legend (serie-{num_yang})
    # Replace circles with thick/thin lines

    def replace_legend_circle(match):
        full_match = match.group(0)
        serie_num_match = re.search(r"activate-serie-(\d+)", full_match)
        if not serie_num_match:
            return full_match

        serie_num = int(serie_num_match.group(1))

        # Only modify the labeled series (serie-0 for Yang, serie-{num_yang} for Yin)
        if serie_num != 0 and serie_num != num_yang:
            return full_match

        # Find circle and replace with line
        circle_match = re.search(r'<circle[^>]*cx="([^"]+)"[^>]*cy="([^"]+)"[^>]*/>', full_match)
        if not circle_match:
            return full_match

        cx = float(circle_match.group(1))
        cy = float(circle_match.group(2))

        if serie_num == 0:  # Yang - thick green
            new_marker = (
                f'<line x1="{cx - 40}" y1="{cy}" x2="{cx + 40}" y2="{cy}" '
                f'stroke="{YANG_COLOR}" stroke-width="{YANG_WIDTH}" stroke-linecap="round"/>'
            )
        else:  # Yin - thin red
            new_marker = (
                f'<line x1="{cx - 40}" y1="{cy}" x2="{cx + 40}" y2="{cy}" '
                f'stroke="{YIN_COLOR}" stroke-width="{YIN_WIDTH}" stroke-linecap="round"/>'
            )

        return re.sub(r"<circle[^>]*/>", new_marker, full_match, count=1)

    # Process legend groups
    new_legends = re.sub(
        r'<g class="legend[^"]*activate-serie-\d+"[^>]*>.*?</g>',
        replace_legend_circle,
        legends_content,
        flags=re.DOTALL,
    )

    svg_content = svg_content.replace(legends_content, new_legends)
    return svg_content


svg_str = fix_legend_markers(svg_str)

# Convert to PNG
cairosvg.svg2png(bytestring=svg_str.encode("utf-8"), write_to="plot.png")

# Save HTML version
chart.render_to_file("plot.html")
