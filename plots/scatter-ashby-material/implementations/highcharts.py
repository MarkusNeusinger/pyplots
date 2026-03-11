""" pyplots.ai
scatter-ashby-material: Ashby Material Selection Chart
Library: highcharts unknown | Python 3.14.3
Quality: 80/100 | Created: 2026-03-11
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.scatter import ScatterSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Density (kg/m³) vs Young's Modulus (GPa) for material families
np.random.seed(42)

families = {
    "Metals & Alloys": {
        "color": "rgba(48, 105, 152, 0.55)",
        "border": "#1e4f7a",
        "density_range": (2700, 11000),
        "modulus_range": (40, 400),
        "n": 25,
        "label_pos": {"x": 7000, "y": 180},
    },
    "Ceramics & Glasses": {
        "color": "rgba(180, 70, 50, 0.55)",
        "border": "#8c3a1a",
        "density_range": (2200, 6000),
        "modulus_range": (60, 450),
        "n": 20,
        "label_pos": {"x": 3200, "y": 300},
    },
    "Polymers": {
        "color": "rgba(60, 145, 80, 0.55)",
        "border": "#2a6e3a",
        "density_range": (900, 1500),
        "modulus_range": (0.2, 4),
        "n": 20,
        "label_pos": {"x": 1100, "y": 1.5},
    },
    "Elastomers": {
        "color": "rgba(180, 140, 50, 0.55)",
        "border": "#9a7a1a",
        "density_range": (900, 1300),
        "modulus_range": (0.001, 0.1),
        "n": 15,
        "label_pos": {"x": 1050, "y": 0.01},
    },
    "Composites": {
        "color": "rgba(140, 80, 160, 0.55)",
        "border": "#6b3480",
        "density_range": (1400, 2200),
        "modulus_range": (15, 200),
        "n": 18,
        "label_pos": {"x": 1700, "y": 70},
    },
    "Foams": {
        "color": "rgba(100, 170, 200, 0.55)",
        "border": "#4a8aaa",
        "density_range": (25, 300),
        "modulus_range": (0.001, 1),
        "n": 15,
        "label_pos": {"x": 80, "y": 0.03},
    },
    "Natural Materials": {
        "color": "rgba(160, 120, 80, 0.55)",
        "border": "#7a5a30",
        "density_range": (150, 1300),
        "modulus_range": (0.5, 20),
        "n": 15,
        "label_pos": {"x": 500, "y": 5},
    },
}

# Generate realistic log-distributed data for each family
all_series = []
label_series_data = []

for family_name, props in families.items():
    n = props["n"]
    log_d_min, log_d_max = np.log10(props["density_range"][0]), np.log10(props["density_range"][1])
    log_m_min, log_m_max = np.log10(props["modulus_range"][0]), np.log10(props["modulus_range"][1])

    log_density = np.random.uniform(log_d_min, log_d_max, n)
    log_modulus = np.random.uniform(log_m_min, log_m_max, n)

    # Add some correlation within families
    correlation_noise = np.random.normal(0, 0.15, n)
    log_modulus += 0.3 * (log_density - np.mean(log_density)) + correlation_noise

    # Clamp back to valid range
    log_modulus = np.clip(log_modulus, log_m_min, log_m_max)

    density = 10**log_density
    modulus = 10**log_modulus

    data = [[round(float(d), 2), round(float(m), 4)] for d, m in zip(density, modulus, strict=True)]

    s = ScatterSeries()
    s.name = family_name
    s.data = data
    s.color = props["color"]
    s.marker = {"radius": 10, "symbol": "circle", "lineWidth": 2, "lineColor": props["border"]}
    all_series.append(s)

    # Collect label position
    label_series_data.append(
        {"name": family_name, "x": props["label_pos"]["x"], "y": props["label_pos"]["y"], "color": props["border"]}
    )

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

chart.options.chart = {
    "type": "scatter",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#fafbfc",
    "style": {"fontFamily": "'Segoe UI', Helvetica, Arial, sans-serif"},
    "marginTop": 160,
    "marginBottom": 220,
    "marginLeft": 260,
    "marginRight": 340,
}

chart.options.title = {
    "text": "Density vs. Young\u2019s Modulus \u00b7 scatter-ashby-material \u00b7 highcharts \u00b7 pyplots.ai",
    "style": {"fontSize": "54px", "fontWeight": "600", "color": "#2c3e50"},
    "margin": 50,
}

chart.options.subtitle = {
    "text": "Ashby material selection chart \u2014 7 material families across engineering property space",
    "style": {"fontSize": "36px", "color": "#7f8c8d", "fontWeight": "400"},
}

chart.options.x_axis = {
    "type": "logarithmic",
    "title": {
        "text": "Density (kg/m\u00b3)",
        "style": {"fontSize": "42px", "color": "#34495e", "fontWeight": "500"},
        "margin": 24,
    },
    "labels": {"style": {"fontSize": "32px", "color": "#7f8c8d"}},
    "min": 10,
    "max": 20000,
    "tickInterval": 1,
    "minorTickInterval": None,
    "gridLineWidth": 1,
    "gridLineColor": "rgba(0, 0, 0, 0.06)",
    "gridLineDashStyle": "Dot",
    "lineColor": "#bdc3c7",
    "lineWidth": 2,
    "tickColor": "#bdc3c7",
}

chart.options.y_axis = {
    "type": "logarithmic",
    "title": {
        "text": "Young\u2019s Modulus (GPa)",
        "style": {"fontSize": "42px", "color": "#34495e", "fontWeight": "500"},
        "margin": 24,
    },
    "labels": {"style": {"fontSize": "32px", "color": "#7f8c8d"}},
    "min": 0.0005,
    "max": 1000,
    "tickInterval": 1,
    "minorTickInterval": None,
    "gridLineWidth": 1,
    "gridLineColor": "rgba(0, 0, 0, 0.06)",
    "gridLineDashStyle": "Dot",
    "lineColor": "#bdc3c7",
    "lineWidth": 2,
    "tickColor": "#bdc3c7",
}

chart.options.legend = {
    "enabled": True,
    "align": "right",
    "verticalAlign": "top",
    "layout": "vertical",
    "x": -20,
    "y": 80,
    "floating": True,
    "backgroundColor": "rgba(255, 255, 255, 0.90)",
    "borderWidth": 1,
    "borderColor": "#e0e0e0",
    "borderRadius": 8,
    "itemStyle": {"fontSize": "30px", "fontWeight": "normal", "color": "#34495e"},
    "padding": 18,
    "itemMarginBottom": 8,
    "symbolRadius": 6,
}

chart.options.credits = {"enabled": False}

chart.options.tooltip = {
    "headerFormat": '<span style="font-size:28px;font-weight:bold;color:{series.color}">{series.name}</span><br/>',
    "pointFormat": '<span style="font-size:24px">'
    "Density: <b>{point.x:.1f} kg/m\u00b3</b><br/>"
    "Modulus: <b>{point.y:.4f} GPa</b></span>",
    "backgroundColor": "rgba(255, 255, 255, 0.95)",
    "borderColor": "#cccccc",
    "borderRadius": 8,
    "shadow": {"color": "rgba(0, 0, 0, 0.1)", "offsetX": 2, "offsetY": 2, "width": 4},
}

chart.options.plot_options = {"scatter": {"marker": {"radius": 10}, "states": {"hover": {"marker": {"radiusPlus": 4}}}}}

# Add label series (invisible scatter with data labels for family names)
label_s = ScatterSeries()
label_s.name = "Labels"
label_s.data = [
    {"x": item["x"], "y": item["y"], "name": item["name"], "dataLabels": {"format": item["name"]}}
    for item in label_series_data
]
label_s.color = "rgba(0, 0, 0, 0)"
label_s.marker = {"enabled": False}
label_s.show_in_legend = False
label_s.enable_mouse_tracking = False
label_s.data_labels = {
    "enabled": True,
    "style": {"fontSize": "28px", "fontWeight": "bold", "color": "#2c3e50", "textOutline": "3px white"},
    "padding": 0,
}

for s in all_series:
    chart.add_series(s)
chart.add_series(label_s)

# Download Highcharts JS
highcharts_url = "https://cdn.jsdelivr.net/npm/highcharts@11/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# Generate HTML with inline scripts
html_str = chart.to_js_literal()
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
</head>
<body style="margin:0; background:#fafbfc;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>{html_str}</script>
</body>
</html>"""

# Write temp HTML and take screenshot
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

# Save HTML for interactive version
with open("plot.html", "w", encoding="utf-8") as f:
    interactive_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://cdn.jsdelivr.net/npm/highcharts@11/highcharts.js"></script>
</head>
<body style="margin:0; background:#fafbfc;">
    <div id="container" style="width: 100%; height: 100vh;"></div>
    <script>{html_str}</script>
</body>
</html>"""
    f.write(interactive_html)
