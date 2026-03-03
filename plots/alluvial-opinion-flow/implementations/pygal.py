"""pyplots.ai
alluvial-opinion-flow: Opinion Flow Diagram
Library: pygal 3.1.0 | Python 3.14.3
Quality: repair-1 | Created: 2026-03-03
"""

import re

import cairosvg
import numpy as np
import pygal
from pygal.style import Style


np.random.seed(42)

# Data
waves = ["Wave 1 (Q1)", "Wave 2 (Q2)", "Wave 3 (Q3)", "Wave 4 (Q4)"]
categories = ["Strongly Favor", "Favor", "Neutral", "Oppose", "Strongly Oppose"]

# Improved color palette - better contrast between Oppose/Strongly Oppose
cat_colors = ["#1a5276", "#5499c7", "#f4d03f", "#af601a", "#7b241c"]
# Respondent counts per category at each wave (1000 total respondents)
respondent_counts = np.array(
    [
        [180, 210, 250, 270],  # Strongly Favor
        [250, 230, 220, 240],  # Favor
        [280, 240, 180, 150],  # Neutral
        [190, 200, 210, 200],  # Oppose
        [100, 120, 140, 140],  # Strongly Oppose
    ]
)

# Flow transitions between consecutive waves
flows = [
    # Wave 1 -> Wave 2
    {
        ("Strongly Favor", "Strongly Favor"): 150,
        ("Strongly Favor", "Favor"): 25,
        ("Strongly Favor", "Neutral"): 5,
        ("Favor", "Strongly Favor"): 40,
        ("Favor", "Favor"): 170,
        ("Favor", "Neutral"): 30,
        ("Favor", "Oppose"): 10,
        ("Neutral", "Strongly Favor"): 10,
        ("Neutral", "Favor"): 25,
        ("Neutral", "Neutral"): 190,
        ("Neutral", "Oppose"): 45,
        ("Neutral", "Strongly Oppose"): 10,
        ("Oppose", "Favor"): 10,
        ("Oppose", "Neutral"): 15,
        ("Oppose", "Oppose"): 135,
        ("Oppose", "Strongly Oppose"): 30,
        ("Strongly Oppose", "Neutral"): 5,
        ("Strongly Oppose", "Oppose"): 10,
        ("Strongly Oppose", "Strongly Oppose"): 85,
    },
    # Wave 2 -> Wave 3
    {
        ("Strongly Favor", "Strongly Favor"): 180,
        ("Strongly Favor", "Favor"): 20,
        ("Strongly Favor", "Neutral"): 10,
        ("Favor", "Strongly Favor"): 50,
        ("Favor", "Favor"): 150,
        ("Favor", "Neutral"): 20,
        ("Favor", "Oppose"): 10,
        ("Neutral", "Strongly Favor"): 10,
        ("Neutral", "Favor"): 40,
        ("Neutral", "Neutral"): 140,
        ("Neutral", "Oppose"): 40,
        ("Neutral", "Strongly Oppose"): 10,
        ("Oppose", "Favor"): 10,
        ("Oppose", "Neutral"): 10,
        ("Oppose", "Oppose"): 150,
        ("Oppose", "Strongly Oppose"): 30,
        ("Strongly Oppose", "Oppose"): 10,
        ("Strongly Oppose", "Strongly Oppose"): 110,
    },
    # Wave 3 -> Wave 4
    {
        ("Strongly Favor", "Strongly Favor"): 220,
        ("Strongly Favor", "Favor"): 20,
        ("Strongly Favor", "Neutral"): 10,
        ("Favor", "Strongly Favor"): 30,
        ("Favor", "Favor"): 170,
        ("Favor", "Neutral"): 15,
        ("Favor", "Oppose"): 5,
        ("Neutral", "Strongly Favor"): 10,
        ("Neutral", "Favor"): 40,
        ("Neutral", "Neutral"): 110,
        ("Neutral", "Oppose"): 15,
        ("Neutral", "Strongly Oppose"): 5,
        ("Oppose", "Favor"): 10,
        ("Oppose", "Neutral"): 15,
        ("Oppose", "Oppose"): 165,
        ("Oppose", "Strongly Oppose"): 20,
        ("Strongly Oppose", "Neutral"): 5,
        ("Strongly Oppose", "Oppose"): 15,
        ("Strongly Oppose", "Strongly Oppose"): 120,
    },
]

# Compute top cross-category flows for polarization highlighting
cross_flows = []
for flow_dict in flows:
    for (src, tgt), count in flow_dict.items():
        if src != tgt:
            cross_flows.append(count)
cross_flows.sort(reverse=True)
highlight_threshold = cross_flows[7] if len(cross_flows) > 7 else 0

# Custom style - extensive use of pygal's Style system
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#222222",
    foreground_subtle="#999999",
    colors=tuple(cat_colors),
    title_font_size=72,
    label_font_size=44,
    major_label_font_size=44,
    legend_font_size=34,
    value_font_size=32,
    value_label_font_size=32,
    font_family="DejaVu Sans, sans-serif",
    label_font_family="DejaVu Sans, sans-serif",
    title_font_family="DejaVu Sans, sans-serif",
    legend_font_family="DejaVu Sans, sans-serif",
    value_font_family="DejaVu Sans, sans-serif",
)

# Create StackedBar chart using pygal's chart system for the node columns
chart = pygal.StackedBar(
    width=4800,
    height=2700,
    style=custom_style,
    title="alluvial-opinion-flow · pygal · pyplots.ai",
    x_title="Renewable Energy Policy Survey · 1,000 Respondents Tracked Quarterly",
    show_legend=True,
    legend_at_bottom=True,
    legend_at_bottom_columns=5,
    legend_box_size=24,
    show_y_guides=False,
    show_x_guides=False,
    show_y_labels=False,
    print_values=True,
    print_values_position="center",
    value_formatter=lambda x: f"{int(x)}",
    x_label_rotation=0,
    rounded_bars=6,
    margin_bottom=10,
)
chart.x_labels = waves

# Add data series with descriptive tooltips using pygal's data API
for cat_idx, cat in enumerate(categories):
    chart.add(cat, [{"value": int(v), "label": f"{cat}: {int(v)} respondents"} for v in respondent_counts[cat_idx]])

# Render chart to SVG
svg_str = chart.render().decode("utf-8")

# Parse bar rect positions from the SVG using pygal's desc metadata
# Structure: <g class="bar"><rect .../><desc class="value">N</desc>
#            <desc class="x centered">X</desc><desc class="y centered">Y</desc></g>
bar_info = []  # (series_idx, bar_idx, x, y, w, h, center_x)
for series_match in re.finditer(r'<g class="series serie-(\d+) color-\d+">(.*?)</g>\s*</g>', svg_str, re.DOTALL):
    series_idx = int(series_match.group(1))
    content = series_match.group(2)
    bar_idx = 0
    for bar_match in re.finditer(r'<g class="bar[^"]*">(.*?)</g>', content, re.DOTALL):
        bar_content = bar_match.group(1)
        rect_m = re.search(
            r"<rect\s+x=\"([\d.e+-]+)\"\s+y=\"([\d.e+-]+)\"\s+"
            r"rx=\"\d+\"\s+ry=\"\d+\"\s+"
            r"width=\"([\d.e+-]+)\"\s+height=\"([\d.e+-]+)\"",
            bar_content,
        )
        cx_m = re.search(r'<desc class="x centered">([\d.e+-]+)</desc>', bar_content)
        if rect_m and cx_m:
            x = float(rect_m.group(1))
            y = float(rect_m.group(2))
            w = float(rect_m.group(3))
            h = float(rect_m.group(4))
            cx = float(cx_m.group(1))
            bar_info.append((series_idx, bar_idx, x, y, w, h, cx))
        bar_idx += 1

# Narrow bars from full-width stacked bars to alluvial node columns
# and add white stroke for visual separation
NODE_WIDTH = 160
for _series_idx, _bar_idx, x, y, w, h, cx in bar_info:
    new_x = cx - NODE_WIDTH / 2
    old_rect = f'x="{x}" y="{y}" rx="6" ry="6" width="{w}" height="{h}"'
    new_rect = (
        f'x="{new_x:.2f}" y="{y}" rx="6" ry="6" width="{NODE_WIDTH}" height="{h}" stroke="white" stroke-width="3"'
    )
    svg_str = svg_str.replace(old_rect, new_rect, 1)

# Build position lookup: (series_idx, wave_idx) -> (y_top, y_bottom, center_x)
bar_positions = {}
for series_idx, bar_idx, _x, y, _w, h, cx in bar_info:
    bar_positions[(series_idx, bar_idx)] = (y, y + h, cx)

# Category name to series index mapping
cat_to_series = {cat: idx for idx, cat in enumerate(categories)}

# Build flow SVG paths
flow_svg = '<g id="alluvial-flows">\n'

for flow_idx, flow_dict in enumerate(flows):
    # Track vertical offsets within each bar segment for flow stacking
    source_offsets = {}
    target_offsets = {}
    for cat_idx in range(len(categories)):
        src_pos = bar_positions.get((cat_idx, flow_idx))
        if src_pos:
            source_offsets[cat_idx] = src_pos[0]
        tgt_pos = bar_positions.get((cat_idx, flow_idx + 1))
        if tgt_pos:
            target_offsets[cat_idx] = tgt_pos[0]

    for (src_cat, tgt_cat), count in sorted(flow_dict.items(), key=lambda x: -x[1]):
        if count <= 0:
            continue

        src_idx = cat_to_series[src_cat]
        tgt_idx = cat_to_series[tgt_cat]

        src_bar = bar_positions.get((src_idx, flow_idx))
        tgt_bar = bar_positions.get((tgt_idx, flow_idx + 1))
        if not src_bar or not tgt_bar:
            continue

        src_total = respondent_counts[src_idx, flow_idx]
        tgt_total = respondent_counts[tgt_idx, flow_idx + 1]
        src_bar_h = src_bar[1] - src_bar[0]
        tgt_bar_h = tgt_bar[1] - tgt_bar[0]

        src_frac_h = (count / src_total) * src_bar_h
        tgt_frac_h = (count / tgt_total) * tgt_bar_h

        y0_top = source_offsets[src_idx]
        y0_bottom = y0_top + src_frac_h
        y1_top = target_offsets[tgt_idx]
        y1_bottom = y1_top + tgt_frac_h

        band_x0 = src_bar[2] + NODE_WIDTH / 2
        band_x1 = tgt_bar[2] - NODE_WIDTH / 2
        cx0 = band_x0 + 0.4 * (band_x1 - band_x0)
        cx1 = band_x0 + 0.6 * (band_x1 - band_x0)

        is_stable = src_cat == tgt_cat
        if is_stable:
            opacity = 0.55
        elif count >= highlight_threshold:
            opacity = 0.45
        else:
            opacity = 0.30

        path_d = (
            f"M {band_x0:.1f},{y0_top:.1f} "
            f"C {cx0:.1f},{y0_top:.1f} {cx1:.1f},{y1_top:.1f} {band_x1:.1f},{y1_top:.1f} "
            f"L {band_x1:.1f},{y1_bottom:.1f} "
            f"C {cx1:.1f},{y1_bottom:.1f} {cx0:.1f},{y0_bottom:.1f} {band_x0:.1f},{y0_bottom:.1f} "
            f"Z"
        )

        flow_svg += f'  <path d="{path_d}" fill="{cat_colors[src_idx]}" fill-opacity="{opacity}" stroke="none"/>\n'

        source_offsets[src_idx] = y0_bottom
        target_offsets[tgt_idx] = y1_bottom

flow_svg += "</g>\n"

# Insert flows BEFORE series groups so bars render on top
first_series = svg_str.find('<g class="series')
if first_series > 0:
    svg_str = svg_str[:first_series] + flow_svg + svg_str[first_series:]

# Add polarization annotation below title, right-aligned within chart area
annotation_svg = (
    '<text x="4720" y="90" text-anchor="end" font-size="32" font-style="italic" '
    'font-family="DejaVu Sans, sans-serif" fill="#888888">'
    "Solid = stable opinion · Faded = changed · "
    "Polarization: Neutral 280&#x2192;150"
    "</text>\n"
)
svg_str = svg_str.replace("</svg>", f"{annotation_svg}</svg>")

# Save outputs
with open("plot.svg", "w") as f:
    f.write(svg_str)

cairosvg.svg2png(bytestring=svg_str.encode("utf-8"), write_to="plot.png")

with open("plot.html", "w") as f:
    f.write(
        """<!DOCTYPE html>
<html>
<head>
    <title>alluvial-opinion-flow · pygal · pyplots.ai</title>
    <style>
        body { margin: 0; padding: 20px; background: #f5f5f5; font-family: sans-serif; }
        .container { max-width: 100%; margin: 0 auto; }
        object { width: 100%; height: auto; }
    </style>
</head>
<body>
    <div class="container">
        <object type="image/svg+xml" data="plot.svg">
            Opinion Flow Diagram not supported
        </object>
    </div>
</body>
</html>"""
    )
