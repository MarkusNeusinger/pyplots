""" pyplots.ai
feynman-basic: Feynman Diagram for Particle Interactions
Library: highcharts unknown | Python 3.14.3
Quality: 84/100 | Created: 2026-03-07
"""

import json
import math
import tempfile
import time
import urllib.request
from pathlib import Path

from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data: Electron-positron annihilation into muon pair (e+e- -> gamma -> mu+mu-)
v1 = (3.0, 3.0)
v2 = (7.0, 3.0)

# Fermion propagators
# Convention: particles arrow forward in time, antiparticles arrow backward
fermion_lines = [
    {"start": (0.5, 5.0), "end": v1, "label": "e\u207b", "label_side": "above", "arrow_dir": "forward"},
    {"start": (0.5, 1.0), "end": v1, "label": "e\u207a", "label_side": "below", "arrow_dir": "backward"},
    {"start": v2, "end": (9.5, 5.0), "label": "\u03bc\u207b", "label_side": "above", "arrow_dir": "forward"},
    {"start": v2, "end": (9.5, 1.0), "label": "\u03bc\u207a", "label_side": "below", "arrow_dir": "backward"},
]

# Photon propagator (wavy line between vertices)
n_wave_points = 200
wave_amplitude = 0.35
wave_frequency = 7
photon_data = []
for i in range(n_wave_points + 1):
    t = i / n_wave_points
    px = v1[0] + (v2[0] - v1[0]) * t
    py = v1[1] + wave_amplitude * math.sin(2 * math.pi * wave_frequency * t)
    photon_data.append([round(px, 4), round(py, 4)])

series_list = []

# Colors
fermion_color = "#306998"
photon_color = "#D63384"
vertex_color = "#2c3e50"

# Arrowhead geometry
arrow_length = 0.35
arrow_spread = 0.18

for fl in fermion_lines:
    sx, sy = fl["start"]
    ex, ey = fl["end"]
    mx = (sx + ex) / 2
    my = (sy + ey) / 2

    # Direction and perpendicular unit vectors
    dx = ex - sx
    dy = ey - sy
    length = math.sqrt(dx * dx + dy * dy)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux

    # Arrow direction: forward = along line, backward = against line
    sign = 1.0 if fl["arrow_dir"] == "forward" else -1.0

    # Arrowhead: two lines from tip backward
    tip_x, tip_y = mx, my
    tail1_x = tip_x - sign * arrow_length * ux + arrow_spread * px
    tail1_y = tip_y - sign * arrow_length * uy + arrow_spread * py
    tail2_x = tip_x - sign * arrow_length * ux - arrow_spread * px
    tail2_y = tip_y - sign * arrow_length * uy - arrow_spread * py

    # Label offset
    label_y_offset = -55 if fl["label_side"] == "above" else 55

    # Main fermion line
    label_point = {
        "x": mx,
        "y": my,
        "marker": {"enabled": False},
        "dataLabels": {
            "enabled": True,
            "format": fl["label"],
            "y": label_y_offset,
            "style": {
                "fontSize": "72px",
                "fontWeight": "bold",
                "color": fermion_color,
                "textOutline": "4px #ffffff",
                "fontStyle": "italic",
            },
        },
    }

    series_list.append(
        {
            "type": "line",
            "data": [{"x": sx, "y": sy}, label_point, {"x": ex, "y": ey}],
            "color": fermion_color,
            "lineWidth": 8,
            "showInLegend": False,
            "enableMouseTracking": False,
            "marker": {"enabled": False},
        }
    )

    # Arrowhead (two line segments forming a V)
    series_list.append(
        {
            "type": "line",
            "data": [
                {"x": round(tail1_x, 4), "y": round(tail1_y, 4)},
                {"x": round(tip_x, 4), "y": round(tip_y, 4)},
                {"x": round(tail2_x, 4), "y": round(tail2_y, 4)},
            ],
            "color": fermion_color,
            "lineWidth": 7,
            "showInLegend": False,
            "enableMouseTracking": False,
            "marker": {"enabled": False},
        }
    )

# Photon wavy line with label at midpoint
photon_mid_idx = n_wave_points // 2
photon_series_data = []
for i, pt in enumerate(photon_data):
    point = {"x": pt[0], "y": pt[1], "marker": {"enabled": False}}
    if i == photon_mid_idx:
        point["dataLabels"] = {
            "enabled": True,
            "format": "\u03b3",
            "y": -70,
            "style": {
                "fontSize": "72px",
                "fontWeight": "bold",
                "color": photon_color,
                "textOutline": "4px #ffffff",
                "fontStyle": "italic",
            },
        }
    photon_series_data.append(point)

series_list.append(
    {
        "type": "spline",
        "data": photon_series_data,
        "color": photon_color,
        "lineWidth": 7,
        "showInLegend": False,
        "enableMouseTracking": False,
        "marker": {"enabled": False},
    }
)

# Vertex dots
vertex_data = [{"x": v1[0], "y": v1[1]}, {"x": v2[0], "y": v2[1]}]
series_list.append(
    {
        "type": "scatter",
        "data": vertex_data,
        "color": vertex_color,
        "marker": {"radius": 24, "symbol": "circle", "lineWidth": 4, "lineColor": "#ffffff"},
        "showInLegend": False,
        "enableMouseTracking": False,
        "zIndex": 10,
    }
)

# Legend entries
series_list.append(
    {
        "type": "line",
        "name": "Fermion (e\u207b, \u03bc\u207b, ...)",
        "data": [],
        "color": fermion_color,
        "lineWidth": 8,
        "showInLegend": True,
        "marker": {"enabled": False},
    }
)
series_list.append(
    {
        "type": "spline",
        "name": "Photon (\u03b3)",
        "data": [],
        "color": photon_color,
        "lineWidth": 7,
        "showInLegend": True,
        "marker": {"enabled": False},
    }
)
series_list.append(
    {
        "type": "scatter",
        "name": "Interaction Vertex",
        "data": [],
        "color": vertex_color,
        "marker": {"radius": 14, "symbol": "circle"},
        "showInLegend": True,
    }
)

# Chart options
chart_options = {
    "chart": {
        "width": 4800,
        "height": 2700,
        "backgroundColor": "#ffffff",
        "marginTop": 250,
        "marginBottom": 250,
        "marginLeft": 150,
        "marginRight": 150,
        "style": {"fontFamily": "'Segoe UI', Arial, Helvetica, sans-serif"},
    },
    "title": {
        "text": "Electron-Positron Annihilation \u00b7 feynman-basic \u00b7 highcharts \u00b7 pyplots.ai",
        "style": {"fontSize": "64px", "fontWeight": "700", "color": "#2c3e50", "letterSpacing": "1px"},
        "margin": 50,
    },
    "subtitle": {
        "text": "e\u207be\u207a \u2192 \u03b3 \u2192 \u03bc\u207b\u03bc\u207a  \u2014  Quantum Electrodynamics (QED) Process",
        "style": {"fontSize": "44px", "fontWeight": "400", "color": "#7f8c8d"},
    },
    "xAxis": {
        "visible": True,
        "min": -0.5,
        "max": 10.5,
        "lineWidth": 0,
        "gridLineWidth": 0,
        "tickWidth": 0,
        "labels": {"enabled": False},
        "title": {
            "text": "Time \u2192",
            "style": {"fontSize": "48px", "fontWeight": "600", "color": "#bdc3c7"},
            "align": "high",
            "offset": 0,
            "x": 40,
            "y": -20,
        },
    },
    "yAxis": {
        "visible": True,
        "min": -0.2,
        "max": 6.2,
        "lineWidth": 0,
        "gridLineWidth": 0,
        "tickWidth": 0,
        "labels": {"enabled": False},
        "title": {"text": None},
    },
    "legend": {
        "enabled": True,
        "layout": "horizontal",
        "align": "center",
        "verticalAlign": "bottom",
        "itemStyle": {"fontSize": "42px", "fontWeight": "500", "color": "#2c3e50"},
        "symbolWidth": 80,
        "symbolHeight": 10,
        "itemDistance": 100,
        "y": -10,
    },
    "tooltip": {"enabled": False},
    "plotOptions": {"series": {"animation": False, "states": {"hover": {"enabled": False}}}},
    "credits": {"enabled": False},
    "series": series_list,
}

options_json = json.dumps(chart_options)

# Download Highcharts JS
cdn_urls = ["https://cdn.jsdelivr.net/npm/highcharts@11/highcharts.js", "https://code.highcharts.com/highcharts.js"]
highcharts_js = None
for url in cdn_urls:
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            highcharts_js = response.read().decode("utf-8")
        break
    except urllib.error.HTTPError:
        time.sleep(2)
        continue
if highcharts_js is None:
    raise RuntimeError("Failed to download Highcharts JS from all CDNs")

chart_init_js = f"Highcharts.chart('container', {options_json});"

# Inline HTML for screenshot
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>{chart_init_js}</script>
</body>
</html>"""

# Standalone HTML for interactive viewing
standalone_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://cdn.jsdelivr.net/npm/highcharts@11/highcharts.js"></script>
</head>
<body style="margin:0; overflow:auto;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>{chart_init_js}</script>
</body>
</html>"""

with open("plot.html", "w", encoding="utf-8") as f:
    f.write(standalone_html)

# Screenshot via headless Chrome
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4800,2900")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)
driver.save_screenshot("plot_raw.png")
driver.quit()

# Crop to exact 4800x2700
img = Image.open("plot_raw.png")
img_cropped = img.crop((0, 0, 4800, 2700))
img_cropped.save("plot.png")
Path("plot_raw.png").unlink()

Path(temp_path).unlink()
