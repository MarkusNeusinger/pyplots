"""pyplots.ai
alluvial-opinion-flow: Opinion Flow Diagram
Library: pygal | Python 3.13
Quality: pending | Created: 2026-03-03
"""

import cairosvg
import numpy as np
import pygal
from pygal.style import Style


# Data
np.random.seed(42)

waves = ["Wave 1\n(Q1)", "Wave 2\n(Q2)", "Wave 3\n(Q3)", "Wave 4\n(Q4)"]
categories = ["Strongly Favor", "Favor", "Neutral", "Oppose", "Strongly Oppose"]

category_colors = {
    "Strongly Favor": "#306998",
    "Favor": "#5B9BD5",
    "Neutral": "#FFD43B",
    "Oppose": "#E07B54",
    "Strongly Oppose": "#D64541",
}

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

# Custom style
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#333333",
    foreground_subtle="#666666",
    title_font_size=72,
)

# Create minimal chart for title rendering
chart = pygal.XY(
    width=4800,
    height=2700,
    style=custom_style,
    title="alluvial-opinion-flow · pygal · pyplots.ai",
    show_legend=False,
    show_x_guides=False,
    show_y_guides=False,
    show_x_labels=False,
    show_y_labels=False,
    dots_size=0,
    stroke=False,
    range=(0, 100),
    xrange=(0, 100),
)
chart.add("", [(50, 50)])

# Render base SVG
base_svg = chart.render().decode("utf-8")

# SVG layout
margin_left = 700
margin_right = 700
margin_top = 350
margin_bottom = 400
chart_width = 4800 - margin_left - margin_right
chart_height = 2700 - margin_top - margin_bottom
node_gap = 20
bar_width = 160

n_waves = len(waves)
x_positions = [margin_left + i * chart_width / (n_waves - 1) for i in range(n_waves)]

# Calculate node positions with gaps
node_positions = {}
for wave_idx in range(n_waves):
    wave_total = respondent_counts[:, wave_idx].sum()
    available_height = chart_height - node_gap * (len(categories) - 1)
    y_top = margin_top

    for cat_idx, cat in enumerate(categories):
        height = (respondent_counts[cat_idx, wave_idx] / wave_total) * available_height
        node_positions[(wave_idx, cat)] = (y_top, y_top + height)
        y_top += height + node_gap

# Build SVG
alluvial_svg = '<g id="alluvial-opinion-flow">'

# Draw flows between consecutive waves
for flow_idx, flow_dict in enumerate(flows):
    x0 = x_positions[flow_idx]
    x1 = x_positions[flow_idx + 1]
    wave0_total = respondent_counts[:, flow_idx].sum()
    wave1_total = respondent_counts[:, flow_idx + 1].sum()
    available_h0 = chart_height - node_gap * (len(categories) - 1)
    available_h1 = chart_height - node_gap * (len(categories) - 1)

    source_offsets = {cat: node_positions[(flow_idx, cat)][0] for cat in categories}
    target_offsets = {cat: node_positions[(flow_idx + 1, cat)][0] for cat in categories}

    for (src, tgt), count in sorted(flow_dict.items(), key=lambda x: -x[1]):
        if count <= 0:
            continue

        src_height = (count / wave0_total) * available_h0
        tgt_height = (count / wave1_total) * available_h1

        y0_top = source_offsets[src]
        y0_bottom = y0_top + src_height
        y1_top = target_offsets[tgt]
        y1_bottom = y1_top + tgt_height

        band_x0 = x0 + bar_width / 2
        band_x1 = x1 - bar_width / 2
        cx0 = band_x0 + 0.4 * (band_x1 - band_x0)
        cx1 = band_x0 + 0.6 * (band_x1 - band_x0)

        # Stable flows (same category) get higher opacity
        is_stable = src == tgt
        opacity = 0.55 if is_stable else 0.2

        path_d = (
            f"M {band_x0:.0f},{y0_top:.0f} "
            f"C {cx0:.0f},{y0_top:.0f} {cx1:.0f},{y1_top:.0f} {band_x1:.0f},{y1_top:.0f} "
            f"L {band_x1:.0f},{y1_bottom:.0f} "
            f"C {cx1:.0f},{y1_bottom:.0f} {cx0:.0f},{y0_bottom:.0f} {band_x0:.0f},{y0_bottom:.0f} "
            f"Z"
        )

        alluvial_svg += f"""
    <path d="{path_d}" fill="{category_colors[src]}" fill-opacity="{opacity}" stroke="none"/>"""

        source_offsets[src] = y0_bottom
        target_offsets[tgt] = y1_bottom

# Draw node bars with respondent count labels
for wave_idx in range(n_waves):
    x = x_positions[wave_idx]

    for cat_idx, cat in enumerate(categories):
        y_top, y_bottom = node_positions[(wave_idx, cat)]
        height = y_bottom - y_top
        count = respondent_counts[cat_idx, wave_idx]

        alluvial_svg += f"""
    <rect x="{x - bar_width / 2:.0f}" y="{y_top:.0f}" width="{bar_width:.0f}" height="{height:.0f}"
          fill="{category_colors[cat]}" stroke="white" stroke-width="3" rx="4"/>"""

        # Respondent count label on node
        y_center = (y_top + y_bottom) / 2
        if height > 40:
            alluvial_svg += f"""
    <text x="{x:.0f}" y="{y_center + 6:.0f}" text-anchor="middle"
          font-size="32" font-weight="bold" font-family="DejaVu Sans, sans-serif"
          fill="white">{count}</text>"""

# Wave labels at bottom
for wave_idx, wave_label in enumerate(waves):
    x = x_positions[wave_idx]
    lines = wave_label.split("\n")
    alluvial_svg += f"""
    <text x="{x:.0f}" y="{margin_top + chart_height + 70:.0f}" text-anchor="middle"
          font-size="48" font-weight="bold" font-family="DejaVu Sans, sans-serif"
          fill="#333333">{lines[0]}</text>"""
    if len(lines) > 1:
        alluvial_svg += f"""
    <text x="{x:.0f}" y="{margin_top + chart_height + 120:.0f}" text-anchor="middle"
          font-size="36" font-family="DejaVu Sans, sans-serif"
          fill="#666666">{lines[1]}</text>"""

# Category labels on left side
for cat in categories:
    y_top, y_bottom = node_positions[(0, cat)]
    y_center = (y_top + y_bottom) / 2
    alluvial_svg += f"""
    <text x="{x_positions[0] - bar_width / 2 - 25:.0f}" y="{y_center + 6:.0f}" text-anchor="end"
          font-size="38" font-weight="bold" font-family="DejaVu Sans, sans-serif"
          fill="{category_colors[cat]}">{cat}</text>"""

# Category labels on right side
for cat in categories:
    y_top, y_bottom = node_positions[(n_waves - 1, cat)]
    y_center = (y_top + y_bottom) / 2
    alluvial_svg += f"""
    <text x="{x_positions[-1] + bar_width / 2 + 25:.0f}" y="{y_center + 6:.0f}" text-anchor="start"
          font-size="38" font-weight="bold" font-family="DejaVu Sans, sans-serif"
          fill="{category_colors[cat]}">{cat}</text>"""

# Legend for opacity distinction
legend_y = margin_top + chart_height + 200
alluvial_svg += f"""
    <rect x="1650" y="{legend_y:.0f}" width="40" height="20" fill="#306998" fill-opacity="0.55" rx="3"/>
    <text x="1700" y="{legend_y + 16:.0f}" font-size="32" font-family="DejaVu Sans, sans-serif"
          fill="#555555">Stable (same opinion)</text>
    <rect x="2350" y="{legend_y:.0f}" width="40" height="20" fill="#306998" fill-opacity="0.2" rx="3"/>
    <text x="2400" y="{legend_y + 16:.0f}" font-size="32" font-family="DejaVu Sans, sans-serif"
          fill="#555555">Changed opinion</text>"""

# Subtitle
alluvial_svg += f"""
    <text x="2400" y="{margin_top + chart_height + 280:.0f}" text-anchor="middle"
          font-size="34" font-style="italic" font-family="DejaVu Sans, sans-serif"
          fill="#888888">Renewable Energy Policy Survey · 1,000 Respondents Tracked Quarterly</text>"""

alluvial_svg += "\n</g>"

# Insert elements into SVG
svg_output = base_svg.replace("</svg>", f"{alluvial_svg}\n</svg>")

# Save
with open("plot.svg", "w") as f:
    f.write(svg_output)

cairosvg.svg2png(bytestring=svg_output.encode("utf-8"), write_to="plot.png")

with open("plot.html", "w") as f:
    f.write("""<!DOCTYPE html>
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
</html>""")
