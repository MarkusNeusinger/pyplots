"""pyplots.ai
heatmap-basic: Basic Heatmap
Library: highcharts 1.10.3 | Python 3.14.3
Quality: /100 | Updated: 2026-02-15
"""

import json
import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Website traffic by day and time period (8x7 matrix)
np.random.seed(42)
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
time_periods = ["6–9 AM", "9 AM–Noon", "Noon–3 PM", "3–6 PM", "6–9 PM", "9 PM–Mid", "Mid–3 AM", "3–6 AM"]

# Generate realistic traffic patterns (visits per hour)
base = np.random.randint(20, 70, size=(len(time_periods), len(days)))

# Weekday business hours peak
base[1:4, 0:5] = np.clip(base[1:4, 0:5] * 1.6, 0, 100).astype(int)

# Weekend mornings and evenings higher (leisure browsing)
base[4:6, 5:7] = np.clip(base[4:6, 5:7] * 1.4, 0, 100).astype(int)

# Late night universally low
base[6:8, :] = np.clip(base[6:8, :] * 0.4, 0, 100).astype(int)

traffic = np.clip(base, 0, 100).astype(int)

# Build heatmap data in Highcharts format: [x_index, y_index, value]
heatmap_data = []
for y_idx in range(len(time_periods)):
    for x_idx in range(len(days)):
        heatmap_data.append([x_idx, y_idx, int(traffic[y_idx, x_idx])])

# Chart configuration
chart_options = {
    "chart": {
        "type": "heatmap",
        "width": 4800,
        "height": 2700,
        "backgroundColor": "#ffffff",
        "marginTop": 120,
        "marginBottom": 200,
        "marginRight": 420,
    },
    "title": {
        "text": "Website Traffic · heatmap-basic · highcharts · pyplots.ai",
        "style": {"fontSize": "56px", "fontWeight": "bold"},
    },
    "xAxis": {"categories": days, "title": {"text": None}, "labels": {"style": {"fontSize": "36px"}}},
    "yAxis": {
        "categories": time_periods,
        "title": {"text": None},
        "labels": {"style": {"fontSize": "32px"}},
        "reversed": True,
    },
    "colorAxis": {
        "min": 0,
        "max": 100,
        "stops": [[0, "#f0f6fc"], [0.3, "#b3d4ea"], [0.6, "#5a9fcf"], [1, "#1a6fad"]],
        "labels": {"style": {"fontSize": "28px"}},
    },
    "legend": {
        "title": {"text": "Visits/hr", "style": {"fontSize": "28px", "fontWeight": "normal"}},
        "align": "right",
        "layout": "vertical",
        "verticalAlign": "middle",
        "symbolHeight": 700,
        "symbolWidth": 40,
        "itemStyle": {"fontSize": "26px"},
        "x": -40,
    },
    "tooltip": {
        "style": {"fontSize": "32px"},
        "headerFormat": "",
        "pointFormat": "<b>{series.yAxis.categories.(point.y)}</b><br>"
        "<b>{series.xAxis.categories.(point.x)}</b><br>"
        "Visits/hr: <b>{point.value}</b>",
    },
    "credits": {"enabled": False},
    "series": [
        {
            "type": "heatmap",
            "name": "Traffic",
            "data": heatmap_data,
            "borderWidth": 3,
            "borderColor": "#ffffff",
            "dataLabels": {"enabled": True, "style": {"fontSize": "28px", "fontWeight": "bold", "textOutline": "none"}},
        }
    ],
}

# Download Highcharts JS and heatmap module
highcharts_url = "https://code.highcharts.com/highcharts.js"
heatmap_url = "https://code.highcharts.com/modules/heatmap.js"

with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

with urllib.request.urlopen(heatmap_url, timeout=30) as response:
    heatmap_js = response.read().decode("utf-8")

# Convert options to JSON
options_json = json.dumps(chart_options)

# Generate HTML with inline scripts and adaptive label colors
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{heatmap_js}</script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>
        var opts = {options_json};
        opts.series[0].dataLabels.formatter = function() {{
            var color = this.point.value > 60 ? '#ffffff' : '#333333';
            return '<span style="color:' + color + '">' + this.point.value + '</span>';
        }};
        opts.series[0].dataLabels.useHTML = true;
        Highcharts.chart('container', opts);
    </script>
</body>
</html>"""

# Save HTML for interactive version
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Take screenshot using headless Chrome
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
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()
