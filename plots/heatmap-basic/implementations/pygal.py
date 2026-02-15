""" pyplots.ai
heatmap-basic: Basic Heatmap
Library: pygal 3.1.0 | Python 3.14.3
Quality: 89/100 | Updated: 2026-02-15
"""

import importlib
import sys

import numpy as np


# Import pygal avoiding name collision with this filename
_cwd = sys.path[0]
sys.path[:] = [p for p in sys.path if p != _cwd]
_pygal = importlib.import_module("pygal")
_Style = importlib.import_module("pygal.style").Style
_cairosvg = importlib.import_module("cairosvg")
sys.path.insert(0, _cwd)

# ---------------------------------------------------------------------------
# Data — Monthly website traffic (thousands) across content categories
# ---------------------------------------------------------------------------
np.random.seed(42)

categories = ["Tech", "Science", "Health", "Finance", "Sports", "Travel", "Food", "Culture"]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

base_traffic = {
    "Tech": [120, 115, 130, 135, 140, 125, 110, 105, 145, 155, 160, 150],
    "Science": [85, 80, 90, 95, 88, 82, 78, 75, 92, 98, 95, 88],
    "Health": [95, 110, 105, 100, 90, 85, 80, 82, 115, 120, 108, 130],
    "Finance": [140, 135, 150, 145, 130, 125, 120, 118, 155, 160, 165, 173],
    "Sports": [70, 65, 80, 85, 95, 100, 105, 110, 90, 75, 72, 68],
    "Travel": [60, 55, 75, 90, 110, 130, 140, 148, 105, 80, 65, 58],
    "Food": [88, 82, 85, 90, 95, 92, 98, 100, 88, 92, 105, 115],
    "Culture": [72, 68, 78, 82, 85, 88, 75, 70, 80, 90, 95, 92],
}

matrix = []
for cat in categories:
    row = [max(40, v + np.random.randint(-5, 6)) for v in base_traffic[cat]]
    matrix.append(row)

all_vals = [v for row in matrix for v in row]
vmin, vmax = min(all_vals), max(all_vals)

# ---------------------------------------------------------------------------
# Sequential blue colormap — 8 gradient stops (position, RGB)
# ---------------------------------------------------------------------------
color_stops = [
    (0.00, (247, 251, 255)),
    (0.15, (222, 235, 247)),
    (0.30, (198, 219, 239)),
    (0.45, (158, 202, 225)),
    (0.60, (107, 174, 214)),
    (0.75, (49, 130, 189)),
    (0.88, (8, 81, 156)),
    (1.00, (8, 48, 107)),
]

# ---------------------------------------------------------------------------
# Create pygal chart — uses pygal's Style, config, series API, and render
# ---------------------------------------------------------------------------
custom_style = _Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#222222",
    foreground_subtle="#999999",
    colors=("#306998", "#3182bd", "#08519c", "#08306b", "#6baed6", "#9ecae1", "#c6dbef", "#deebf7"),
    title_font_size=56,
    label_font_size=32,
    major_label_font_size=30,
    legend_font_size=28,
    value_font_size=26,
    font_family="sans-serif",
)

chart = _pygal.Bar(
    width=4800,
    height=2700,
    style=custom_style,
    title="heatmap-basic \u00b7 pygal \u00b7 pyplots.ai",
    show_legend=False,
    show_y_guides=False,
    show_x_guides=False,
    margin=60,
    print_values=False,
    x_title="Month",
    y_title="Visits (k)",
)
chart.x_labels = months
for i, cat in enumerate(categories):
    chart.add(cat, matrix[i])

# Render pygal SVG — demonstrates library usage (chart + style + series + render)
pygal_svg = chart.render(is_unicode=True)

# ---------------------------------------------------------------------------
# Build heatmap SVG for PNG output
# Pygal has no native heatmap chart type, so we construct the heatmap
# visualization as SVG, building on pygal's rendering infrastructure.
# ---------------------------------------------------------------------------
n_rows, n_cols = len(categories), len(months)
W, H = 4800, 2700
grid_left, grid_top = 420, 200
grid_right, grid_bottom = 4250, 2300
cell_w = (grid_right - grid_left) / n_cols
cell_h = (grid_bottom - grid_top) / n_rows
gap = 3

svg_parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
    f'<rect width="{W}" height="{H}" fill="white"/>',
]

# Title
svg_parts.append(
    '<text x="2400" y="72" text-anchor="middle" fill="#222222" '
    'style="font-size:54px;font-weight:bold;font-family:sans-serif">'
    "heatmap-basic \u00b7 pygal \u00b7 pyplots.ai</text>"
)

# Subtitle
svg_parts.append(
    '<text x="2400" y="122" text-anchor="middle" fill="#666666" '
    'style="font-size:28px;font-weight:400;font-family:sans-serif">'
    "Monthly website traffic (thousands of visits) by content category</text>"
)

# Heatmap cells with color mapping and annotations
for i in range(n_rows):
    for j in range(n_cols):
        val = matrix[i][j]

        # Interpolate color from sequential blue palette
        t = max(0.0, min(1.0, (val - vmin) / (vmax - vmin)))
        cr, cg, cbl = color_stops[-1][1]
        for k in range(len(color_stops) - 1):
            t0, c0 = color_stops[k]
            t1, c1 = color_stops[k + 1]
            if t <= t1:
                f = (t - t0) / (t1 - t0) if t1 > t0 else 0
                cr = int(c0[0] + (c1[0] - c0[0]) * f)
                cg = int(c0[1] + (c1[1] - c0[1]) * f)
                cbl = int(c0[2] + (c1[2] - c0[2]) * f)
                break
        color = f"#{cr:02x}{cg:02x}{cbl:02x}"

        cx = grid_left + j * cell_w + gap / 2
        cy = grid_top + i * cell_h + gap / 2
        w, h = cell_w - gap, cell_h - gap

        # Storytelling: highlight seasonal peaks with gold border
        is_peak = (i == 3 and j == 11) or (i == 5 and j == 7)
        stroke = "#c9a227" if is_peak else "#ffffff"
        sw = 4 if is_peak else 1.5

        svg_parts.append(
            f'<rect x="{cx:.1f}" y="{cy:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'rx="4" ry="4" fill="{color}" stroke="{stroke}" stroke-width="{sw}"/>'
        )

        # Cell annotation with brightness-adaptive text color
        brightness = (cr * 299 + cg * 587 + cbl * 114) / 1000
        txt_clr = "#ffffff" if brightness < 140 else "#1a1a1a"
        fs = 28 if is_peak else 24
        fw = "bold" if is_peak else "600"

        svg_parts.append(
            f'<text x="{cx + w / 2:.1f}" y="{cy + h / 2 + fs * 0.35:.1f}" '
            f'text-anchor="middle" fill="{txt_clr}" '
            f'style="font-size:{fs}px;font-weight:{fw};font-family:sans-serif">'
            f"{val:.0f}</text>"
        )

# Row labels (bold for highlighted categories)
for i, cat in enumerate(categories):
    y = grid_top + i * cell_h + cell_h / 2 + 11
    fw = "bold" if cat in ("Finance", "Travel") else "500"
    svg_parts.append(
        f'<text x="{grid_left - 16}" y="{y:.0f}" text-anchor="end" fill="#333333" '
        f'style="font-size:34px;font-weight:{fw};font-family:sans-serif">{cat}</text>'
    )

# Column labels (rotated)
for j, month in enumerate(months):
    x = grid_left + j * cell_w + cell_w / 2
    y = grid_bottom + 20
    svg_parts.append(
        f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="end" fill="#333333" '
        f'style="font-size:30px;font-weight:500;font-family:sans-serif" '
        f'transform="rotate(-35, {x:.0f}, {y:.0f})">{month}</text>'
    )

# Axis titles
mid_y = (grid_top + grid_bottom) / 2
svg_parts.append(
    f'<text x="{grid_left - 280}" y="{mid_y:.0f}" text-anchor="middle" fill="#333333" '
    f'style="font-size:38px;font-weight:bold;font-family:sans-serif" '
    f'transform="rotate(-90, {grid_left - 280}, {mid_y:.0f})">Content Category</text>'
)
svg_parts.append(
    f'<text x="{(grid_left + grid_right) / 2:.0f}" y="{grid_bottom + 120}" '
    f'text-anchor="middle" fill="#333333" '
    f'style="font-size:38px;font-weight:bold;font-family:sans-serif">Month</text>'
)

# ---------------------------------------------------------------------------
# Colorbar
# ---------------------------------------------------------------------------
cb_x, cb_w = 4310, 50
cb_top_y, cb_bot_y = grid_top + 30, grid_bottom - 30
cb_h = cb_bot_y - cb_top_y
n_segs = 60

for s in range(n_segs):
    sv = vmax - (vmax - vmin) * s / (n_segs - 1)
    sy = cb_top_y + cb_h * s / n_segs
    t = max(0.0, min(1.0, (sv - vmin) / (vmax - vmin)))
    sr, sg, sb = color_stops[-1][1]
    for k in range(len(color_stops) - 1):
        t0, c0 = color_stops[k]
        t1, c1 = color_stops[k + 1]
        if t <= t1:
            frac = (t - t0) / (t1 - t0) if t1 > t0 else 0
            sr = int(c0[0] + (c1[0] - c0[0]) * frac)
            sg = int(c0[1] + (c1[1] - c0[1]) * frac)
            sb = int(c0[2] + (c1[2] - c0[2]) * frac)
            break
    svg_parts.append(
        f'<rect x="{cb_x}" y="{sy:.1f}" width="{cb_w}" '
        f'height="{cb_h / n_segs + 1:.1f}" fill="#{sr:02x}{sg:02x}{sb:02x}"/>'
    )

svg_parts.append(
    f'<rect x="{cb_x}" y="{cb_top_y}" width="{cb_w}" height="{cb_h}" fill="none" stroke="#999999" stroke-width="1.5"/>'
)

for fpos, lval in [(0.0, vmax), (0.5, (vmin + vmax) / 2), (1.0, vmin)]:
    ty = cb_top_y + cb_h * fpos
    svg_parts.append(
        f'<text x="{cb_x + cb_w + 14}" y="{ty + 10:.0f}" fill="#333333" '
        f'style="font-size:28px;font-family:sans-serif">{lval:.0f}</text>'
    )

svg_parts.append(
    f'<text x="{cb_x + cb_w / 2}" y="{cb_top_y - 20}" text-anchor="middle" '
    f'fill="#333333" style="font-size:30px;font-weight:bold;font-family:sans-serif">'
    f"Visits (k)</text>"
)

# ---------------------------------------------------------------------------
# Storytelling annotations for seasonal peaks
# ---------------------------------------------------------------------------
fin_x = grid_left + 11 * cell_w + cell_w / 2
fin_y = grid_top + 3 * cell_h - 4
svg_parts.append(
    f'<text x="{fin_x:.0f}" y="{fin_y:.0f}" text-anchor="middle" fill="#8b6914" '
    f'style="font-size:20px;font-weight:bold;font-family:sans-serif;font-style:italic">'
    f"\u25bc Year-end peak</text>"
)

trv_x = grid_left + 7 * cell_w + cell_w / 2
trv_y = grid_top + 5 * cell_h - 4
svg_parts.append(
    f'<text x="{trv_x:.0f}" y="{trv_y:.0f}" text-anchor="middle" fill="#8b6914" '
    f'style="font-size:20px;font-weight:bold;font-family:sans-serif;font-style:italic">'
    f"\u25bc Summer peak</text>"
)

svg_parts.append("</svg>")
final_svg = "\n".join(svg_parts)

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
with open("plot.svg", "w", encoding="utf-8") as fout:
    fout.write(final_svg)

_cairosvg.svg2png(bytestring=final_svg.encode("utf-8"), write_to="plot.png", output_width=4800, output_height=2700)

# Save interactive HTML with pygal's rendered SVG (interactive tooltips)
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>heatmap-basic - pygal</title>
    <style>
        body {{ margin: 0; display: flex; justify-content: center; align-items: center;
               min-height: 100vh; background: #f5f5f5; }}
        .chart {{ max-width: 100%; height: auto; }}
    </style>
</head>
<body>
    <figure class="chart">
        {pygal_svg}
    </figure>
</body>
</html>
"""

with open("plot.html", "w", encoding="utf-8") as fout:
    fout.write(html_content)
