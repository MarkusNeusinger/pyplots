""" pyplots.ai
campbell-basic: Campbell Diagram
Library: highcharts unknown | Python 3.14.3
Quality: 82/100 | Created: 2026-02-15
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.area import LineSeries
from highcharts_core.options.series.scatter import ScatterSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data — rotordynamic natural frequencies vs rotational speed
np.random.seed(42)
speed_rpm = np.linspace(0, 6000, 80)
speed_hz = speed_rpm / 60

# Natural frequency modes (Hz) — slight variation with speed due to gyroscopic effects
mode_1_bending = 18 + 0.0008 * speed_rpm + np.random.normal(0, 0.15, len(speed_rpm))
mode_2_bending = 45 - 0.0005 * speed_rpm + np.random.normal(0, 0.2, len(speed_rpm))
mode_1_torsional = 62 + 0.0003 * speed_rpm + np.random.normal(0, 0.15, len(speed_rpm))
mode_axial = 78 - 0.0002 * speed_rpm + np.random.normal(0, 0.18, len(speed_rpm))

modes = {
    "1st Bending": mode_1_bending,
    "2nd Bending": mode_2_bending,
    "1st Torsional": mode_1_torsional,
    "Axial": mode_axial,
}

# Engine order lines: frequency = order * speed_rpm / 60
orders = [1, 2, 3]

# Find critical speed intersections (engine order line crosses natural frequency curve)
critical_speeds = []
for order in orders:
    eo_freq = order * speed_hz
    for _, mode_freq in modes.items():
        diff = eo_freq - mode_freq
        sign_changes = np.where(np.diff(np.sign(diff)))[0]
        for idx in sign_changes:
            frac = abs(diff[idx]) / (abs(diff[idx]) + abs(diff[idx + 1]))
            rpm_val = speed_rpm[idx] + frac * (speed_rpm[idx + 1] - speed_rpm[idx])
            freq_val = order * rpm_val / 60
            critical_speeds.append((float(rpm_val), float(freq_val)))

# Chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

chart.options.chart = {
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "style": {"fontFamily": "'Segoe UI', Helvetica, Arial, sans-serif"},
    "marginTop": 160,
    "marginBottom": 200,
    "marginLeft": 220,
    "marginRight": 120,
}

chart.options.title = {
    "text": "campbell-basic \u00b7 highcharts \u00b7 pyplots.ai",
    "style": {"fontSize": "64px", "fontWeight": "600", "color": "#2c3e50", "letterSpacing": "1px"},
    "margin": 50,
}

chart.options.subtitle = {
    "text": "Natural Frequencies vs Rotational Speed \u2014 Turbine Rotor",
    "style": {"fontSize": "38px", "color": "#7f8c8d", "fontWeight": "400"},
}

chart.options.x_axis = {
    "title": {
        "text": "Rotational Speed (RPM)",
        "style": {"fontSize": "44px", "color": "#34495e", "fontWeight": "500"},
        "margin": 30,
    },
    "labels": {"style": {"fontSize": "34px", "color": "#7f8c8d"}},
    "min": 0,
    "max": 6000,
    "tickInterval": 1000,
    "gridLineWidth": 1,
    "gridLineColor": "rgba(0, 0, 0, 0.06)",
    "gridLineDashStyle": "Dot",
    "lineColor": "#bdc3c7",
    "lineWidth": 2,
}

chart.options.y_axis = {
    "title": {
        "text": "Frequency (Hz)",
        "style": {"fontSize": "44px", "color": "#34495e", "fontWeight": "500"},
        "margin": 30,
    },
    "labels": {"style": {"fontSize": "34px", "color": "#7f8c8d"}},
    "min": 0,
    "max": 110,
    "tickInterval": 10,
    "gridLineWidth": 1,
    "gridLineColor": "rgba(0, 0, 0, 0.06)",
    "gridLineDashStyle": "Dot",
    "lineColor": "#bdc3c7",
    "lineWidth": 2,
}

chart.options.legend = {
    "enabled": True,
    "align": "right",
    "verticalAlign": "top",
    "layout": "vertical",
    "x": -40,
    "y": 100,
    "floating": True,
    "backgroundColor": "rgba(255, 255, 255, 0.92)",
    "borderWidth": 1,
    "borderColor": "#e0e0e0",
    "borderRadius": 8,
    "itemStyle": {"fontSize": "32px", "fontWeight": "400", "color": "#34495e"},
    "padding": 18,
    "itemMarginTop": 6,
    "itemMarginBottom": 6,
}

chart.options.credits = {"enabled": False}

chart.options.tooltip = {
    "headerFormat": "",
    "pointFormat": (
        '<span style="font-size:24px;color:{series.color}">\u25cf</span> '
        '<span style="font-size:26px">'
        "{series.name}<br/>"
        "Speed: <b>{point.x:.0f} RPM</b><br/>"
        "Frequency: <b>{point.y:.1f} Hz</b></span>"
    ),
    "backgroundColor": "rgba(255, 255, 255, 0.95)",
    "borderRadius": 10,
    "borderWidth": 2,
    "style": {"fontSize": "26px"},
}

# Mode colors — cohesive palette starting with Python Blue
mode_colors = ["#306998", "#2ecc71", "#9b59b6", "#e67e22"]
mode_symbols = ["circle", "square", "triangle", "diamond"]

# Natural frequency mode series
for i, (mode_name, mode_freq) in enumerate(modes.items()):
    series = LineSeries()
    series.data = [[float(r), float(f)] for r, f in zip(speed_rpm, mode_freq, strict=True)]
    series.name = mode_name
    series.color = mode_colors[i]
    series.line_width = 5
    series.marker = {"enabled": False}
    series.z_index = 2
    chart.add_series(series)

# Engine order lines — dashed gray diagonal lines
eo_color = "#95a5a6"
for order in orders:
    eo_freq = order * speed_hz
    mask = eo_freq <= 110
    eo_data = [[float(r), float(f)] for r, f in zip(speed_rpm[mask], eo_freq[mask], strict=True)]
    series = LineSeries()
    series.data = eo_data
    series.name = f"{order}x Engine Order"
    series.color = eo_color
    series.line_width = 3
    series.dash_style = "LongDash"
    series.marker = {"enabled": False}
    series.enable_mouse_tracking = False
    series.z_index = 1
    chart.add_series(series)

# Critical speed intersection markers
if critical_speeds:
    crit_series = ScatterSeries()
    crit_series.data = [[rpm, freq] for rpm, freq in critical_speeds]
    crit_series.name = "Critical Speeds"
    crit_series.color = "#e74c3c"
    crit_series.marker = {
        "radius": 14,
        "symbol": "diamond",
        "lineWidth": 3,
        "lineColor": "#c0392b",
        "fillColor": "#e74c3c",
        "states": {"hover": {"radiusPlus": 4}},
    }
    crit_series.z_index = 5
    chart.add_series(crit_series)

# Download Highcharts JS
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# Generate HTML
html_str = chart.to_js_literal()
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
</head>
<body style="margin:0; background:#ffffff;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>{html_str}</script>
</body>
</html>"""

# Save interactive HTML
with open("plot.html", "w", encoding="utf-8") as f:
    interactive_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://code.highcharts.com/highcharts.js"></script>
</head>
<body style="margin:0; background:#ffffff;">
    <div id="container" style="width: 100%; height: 100vh;"></div>
    <script>{html_str}</script>
</body>
</html>"""
    f.write(interactive_html)

# PNG via headless Chrome
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4800,2700")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)

container = driver.find_element("id", "container")
container.screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()
