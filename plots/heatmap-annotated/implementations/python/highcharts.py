""" anyplot.ai
heatmap-annotated: Annotated Heatmap
Library: highcharts unknown | Python 3.13.13
Quality: 23/100 | Updated: 2026-05-06
"""

import json
import os
import tempfile
import time
from pathlib import Path

import numpy as np
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


THEME = os.getenv("ANYPLOT_THEME", "light")
PAGE_BG = "#FAF8F1" if THEME == "light" else "#1A1A17"
ELEVATED_BG = "#FFFDF6" if THEME == "light" else "#242420"
INK = "#1A1A17" if THEME == "light" else "#F0EFE8"
INK_SOFT = "#4A4A44" if THEME == "light" else "#B8B7B0"
GRID = "rgba(26,26,23,0.10)" if THEME == "light" else "rgba(240,239,232,0.10)"

# Data: Correlation matrix for financial indicators
np.random.seed(42)
variables = ["Revenue", "Profit", "Growth", "ROI", "Debt", "Assets", "Employees"]
n = len(variables)

# Generate realistic correlation matrix (symmetric, diagonal = 1)
raw = np.random.randn(n, n) * 0.5
corr_matrix = (raw + raw.T) / 2
np.fill_diagonal(corr_matrix, 1.0)
corr_matrix = np.clip(corr_matrix, -1, 1)

# Prepare data for Highcharts heatmap format: [x_index, y_index, value]
data = []
for i in range(n):
    for j in range(n):
        data.append([j, i, round(corr_matrix[i, j], 2)])

# Build chart options as a dictionary
chart_options = {
    "chart": {
        "type": "heatmap",
        "width": 3600,
        "height": 3600,
        "backgroundColor": PAGE_BG,
        "marginTop": 150,
        "marginBottom": 200,
        "marginLeft": 250,
        "marginRight": 200,
    },
    "title": {
        "text": "heatmap-annotated · highcharts · anyplot.ai",
        "style": {"fontSize": "28px", "fontWeight": "bold", "color": INK},
    },
    "xAxis": {
        "categories": variables,
        "title": {"text": "Variables", "style": {"fontSize": "22px", "color": INK}},
        "labels": {"style": {"fontSize": "18px", "color": INK_SOFT}},
        "lineColor": INK_SOFT,
        "tickColor": INK_SOFT,
        "gridLineColor": GRID,
    },
    "yAxis": {
        "categories": variables,
        "title": {"text": "Variables", "style": {"fontSize": "22px", "color": INK}},
        "labels": {"style": {"fontSize": "18px", "color": INK_SOFT}},
        "lineColor": INK_SOFT,
        "tickColor": INK_SOFT,
        "gridLineColor": GRID,
        "reversed": True,
    },
    "colorAxis": {
        "min": -1,
        "max": 1,
        "stops": [[0, "#2166AC"], [0.5, PAGE_BG], [1, "#B35806"]],
        "labels": {"style": {"fontSize": "18px", "color": INK_SOFT}},
    },
    "legend": {
        "align": "right",
        "layout": "vertical",
        "verticalAlign": "middle",
        "symbolHeight": 600,
        "itemStyle": {"fontSize": "18px", "color": INK_SOFT},
        "backgroundColor": ELEVATED_BG,
        "borderColor": INK_SOFT,
        "borderWidth": 1,
    },
    "credits": {"enabled": False},
    "series": [
        {
            "type": "heatmap",
            "name": "Correlation",
            "data": data,
            "borderWidth": 2,
            "borderColor": PAGE_BG,
            "dataLabels": {
                "enabled": True,
                "format": "{point.value:.2f}",
                "style": {"fontSize": "20px", "fontWeight": "bold", "color": INK, "textOutline": "none"},
            },
        }
    ],
}

# Download Highcharts JS and heatmap module
highcharts_url = "https://code.highcharts.com/highcharts.js"
heatmap_url = "https://code.highcharts.com/modules/heatmap.js"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
highcharts_js = requests.get(highcharts_url, headers=headers, timeout=30).text
heatmap_js = requests.get(heatmap_url, headers=headers, timeout=30).text

# Convert options to JSON
options_json = json.dumps(chart_options)

# Generate HTML with inline scripts
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{heatmap_js}</script>
</head>
<body style="margin:0; background:{PAGE_BG};">
    <div id="container" style="width: 3600px; height: 3600px;"></div>
    <script>
        Highcharts.chart('container', {options_json});
    </script>
</body>
</html>"""

# Save HTML for interactive version
with open(f"plot-{THEME}.html", "w", encoding="utf-8") as f:
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
chrome_options.add_argument("--window-size=3600,3600")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)
driver.save_screenshot(f"plot-{THEME}.png")
driver.quit()

Path(temp_path).unlink()
