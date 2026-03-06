""" pyplots.ai
heatmap-stripes-climate: Climate Warming Stripes
Library: pygal 3.1.0 | Python 3.14.3
Quality: 82/100 | Created: 2026-03-06
"""

import importlib
import re
import sys

import numpy as np


# Avoid importing this file instead of the pygal package
_script_dir = sys.path[0]
sys.path.remove(_script_dir)
pygal = importlib.import_module("pygal")
Style = importlib.import_module("pygal.style").Style
cairosvg = importlib.import_module("cairosvg")
sys.path.insert(0, _script_dir)

# Data - Simulated global temperature anomalies (relative to 1961-1990 baseline)
np.random.seed(42)
years = list(range(1850, 2025))
n_years = len(years)

# Build realistic warming trend: slight cooling mid-century, strong warming post-1980
base_trend = np.concatenate(
    [
        np.linspace(-0.35, -0.15, 50),
        np.linspace(-0.15, -0.25, 30),
        np.linspace(-0.25, -0.05, 30),
        np.linspace(-0.05, 0.30, 25),
        np.linspace(0.30, 1.20, 40),
    ]
)
noise = np.random.normal(0, 0.10, n_years)
anomalies = base_trend + noise
anomalies = np.round(anomalies, 2)

# Color scale symmetric around zero; use 90th percentile as saturation cap
# so moderate anomalies still show visible color
vmax = float(np.percentile(np.abs(anomalies), 90))
vmin = -vmax

# Diverging blue-to-red color stops with steep transitions for visual impact
color_stops = [
    (0.00, (8, 48, 107)),
    (0.12, (33, 102, 172)),
    (0.25, (67, 147, 195)),
    (0.42, (146, 197, 222)),
    (0.50, (245, 245, 245)),
    (0.58, (244, 165, 130)),
    (0.75, (214, 96, 77)),
    (0.88, (178, 24, 43)),
    (1.00, (103, 0, 13)),
]


def anomaly_to_hex(anomaly):
    """Map anomaly value to hex color using diverging colormap."""
    t = max(0.0, min(1.0, (anomaly - vmin) / (vmax - vmin)))
    r, g, b = color_stops[-1][1]
    for k in range(len(color_stops) - 1):
        t0, c0 = color_stops[k]
        t1, c1 = color_stops[k + 1]
        if t <= t1:
            f = (t - t0) / (t1 - t0) if t1 > t0 else 0
            r = int(c0[0] + (c1[0] - c0[0]) * f)
            g = int(c0[1] + (c1[1] - c0[1]) * f)
            b = int(c0[2] + (c1[2] - c0[2]) * f)
            break
    return f"#{r:02x}{g:02x}{b:02x}"


# Compute per-year colors
bar_colors = [anomaly_to_hex(a) for a in anomalies]

# Pygal style - minimal chrome for warming stripes
custom_style = Style(
    background="white",
    plot_background="white",
    foreground="#333333",
    foreground_strong="#222222",
    foreground_subtle="#cccccc",
    colors=("#306998",),
    title_font_size=36,
    label_font_size=22,
    major_label_font_size=26,
    value_font_size=14,
    font_family="sans-serif",
)


def make_chart(for_html=False):
    """Create pygal bar chart configured for warming stripes."""
    chart = pygal.Bar(
        width=4800,
        height=2700,
        style=custom_style,
        title="heatmap-stripes-climate \u00b7 pygal \u00b7 pyplots.ai",
        show_legend=False,
        show_y_guides=False,
        show_x_guides=False,
        show_y_labels=False,
        show_x_labels=True,
        margin=0,
        margin_top=150,
        margin_bottom=180,
        margin_left=10,
        margin_right=10,
        spacing=0,
        print_values=False,
        range=(0, 1),
        stroke=False,
        truncate_label=-1,
    )
    chart._series_margin = 0
    chart._serie_margin = 0

    if for_html:
        chart.x_labels = [str(y) for y in years]
        chart.x_labels_major = [str(y) for y in years if y % 25 == 0]
        chart.show_minor_x_labels = False
        data = [
            {"value": 1, "color": bar_colors[i], "label": f"{years[i]}: {anomalies[i]:+.2f}\u00b0C"}
            for i in range(n_years)
        ]
    else:
        chart.x_labels = [str(y) if y in (years[0], years[-1]) else "" for y in years]
        data = [{"value": 1, "color": bar_colors[i]} for i in range(n_years)]

    chart.add("Temperature Anomaly", data)
    return chart


# Render static chart
chart = make_chart(for_html=False)
svg_str = chart.render(is_unicode=True)

# Remove guide lines and axis lines for clean warming stripes PNG
svg_str = re.sub(r'<path[^>]*class="[^"]*guide line[^"]*"[^>]*/>', "", svg_str)
svg_str = re.sub(r'<path[^>]*class="line"[^>]*/>', "", svg_str)

# Save cleaned SVG and render PNG
with open("plot.svg", "w", encoding="utf-8") as fout:
    fout.write(svg_str)
cairosvg.svg2png(bytestring=svg_str.encode("utf-8"), write_to="plot.png")

# Interactive HTML version with tooltips
html_chart = make_chart(for_html=True)
interactive_svg = html_chart.render(is_unicode=True)
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>heatmap-stripes-climate - pygal</title>
    <style>
        body {{ margin: 0; display: flex; justify-content: center; align-items: center;
               min-height: 100vh; background: #f5f5f5; }}
        .chart {{ max-width: 100%; height: auto; }}
    </style>
</head>
<body>
    <figure class="chart">
        {interactive_svg}
    </figure>
</body>
</html>
"""

with open("plot.html", "w", encoding="utf-8") as fout:
    fout.write(html_content)
