"""pyplots.ai
kagi-basic: Basic Kagi Chart
Library: pygal 3.1.0 | Python 3.13.11
Quality: 72/100 | Created: 2026-01-08
"""

import re

import cairosvg
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

# Custom style
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#999999",
    colors=("#16A34A", "#DC2626"),
    title_font_size=72,
    label_font_size=48,
    major_label_font_size=40,
    legend_font_size=44,
    value_font_size=36,
    opacity=1.0,
    font_family="sans-serif",
)

# Create chart - legend disabled, we'll add custom legend text
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
    show_legend=False,
    margin=50,
    margin_bottom=120,
    spacing=20,
    xrange=(0, len(segments) + 1),
)

# Stroke widths - very dramatic difference for clear visibility
YANG_WIDTH = 18  # Thick line for bullish/yang
YIN_WIDTH = 4  # Thin line for bearish/yin

# Build paths for yang and yin segments
yang_paths = []
yin_paths = []

for i, (x, y_start, y_end, seg_is_yang) in enumerate(segments):
    path = [(x, y_start), (x, y_end)]
    if i < len(segments) - 1:
        path.append((x + 1, y_end))

    if seg_is_yang:
        yang_paths.append(path)
    else:
        yin_paths.append(path)

# Add yang series (thick green lines)
for path in yang_paths:
    chart.add("", path, stroke_style={"width": YANG_WIDTH}, show_dots=False)

# Add yin series (thin red lines)
for path in yin_paths:
    chart.add("", path, stroke_style={"width": YIN_WIDTH}, show_dots=False)

# Get the SVG output
svg_data = chart.render()
svg_str = svg_data.decode("utf-8")

# Extract stroke widths and colors from CSS
stroke_widths = {}
for match in re.finditer(r"\.series\.serie-(\d+)\{stroke-width:(\d+)\}", svg_str):
    serie_num = int(match.group(1))
    width = match.group(2)
    stroke_widths[serie_num] = width

colors = {}
for match in re.finditer(r"\.color-(\d+)[^{]*\{stroke:([^;]+);", svg_str):
    color_num = int(match.group(1))
    color = match.group(2)
    colors[color_num] = color


# Function to add inline style to path elements inside series groups
def process_series_group(match):
    full_group = match.group(0)
    class_attr = match.group(1)

    serie_match = re.search(r"serie-(\d+)", class_attr)
    color_match = re.search(r"color-(\d+)", class_attr)

    if serie_match and color_match:
        serie_num = int(serie_match.group(1))
        color_num = int(color_match.group(1))

        width = stroke_widths.get(serie_num, "1")
        color = colors.get(color_num, "#000")

        def add_style_to_path(path_match):
            path_tag = path_match.group(0)
            return path_tag.replace('class="line', f'style="stroke-width:{width};stroke:{color}" class="line')

        full_group = re.sub(r"<path[^>]*class=\"line[^>]*>", add_style_to_path, full_group)

    return full_group


# Process all series groups
svg_str = re.sub(
    r'<g class="(series serie-\d+ color-\d+)"[^>]*>.*?</g>', process_series_group, svg_str, flags=re.DOTALL
)

# Add custom legend at bottom
legend_svg = """
<g class="custom-legend" transform="translate(600, 2620)">
  <line x1="0" y1="0" x2="120" y2="0" stroke="#16A34A" stroke-width="18"/>
  <text x="140" y="12" font-size="44" fill="#333333" font-family="sans-serif">Yang (bullish) — thick line</text>
  <line x1="900" y1="0" x2="1020" y2="0" stroke="#DC2626" stroke-width="4"/>
  <text x="1040" y="12" font-size="44" fill="#333333" font-family="sans-serif">Yin (bearish) — thin line</text>
</g>
"""

# Insert legend before closing </svg> tag
svg_str = svg_str.replace("</svg>", legend_svg + "</svg>")

# Convert to PNG using cairosvg
cairosvg.svg2png(bytestring=svg_str.encode("utf-8"), write_to="plot.png")

# Save HTML version (without custom legend modifications for interactivity)
chart.render_to_file("plot.html")
