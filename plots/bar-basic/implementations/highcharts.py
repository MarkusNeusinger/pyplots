"""pyplots.ai
bar-basic: Basic Bar Chart
Library: highcharts 1.10.3 | Python 3.14
Quality: /100 | Updated: 2026-02-14
"""

import json
import tempfile
import time
import urllib.request
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Product sales by category (realistic retail scenario with clear ranking)
categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys"]
values = [4800, 3100, 2200, 1700, 950, 480]

# Chart options
chart_options = {
    "chart": {
        "type": "column",
        "width": 4800,
        "height": 2700,
        "backgroundColor": "#ffffff",
        "marginBottom": 250,
        "marginTop": 130,
        "style": {"fontFamily": "Arial, sans-serif"},
    },
    "title": {
        "text": "bar-basic \u00b7 highcharts \u00b7 pyplots.ai",
        "style": {"fontSize": "52px", "fontWeight": "bold", "color": "#333333"},
    },
    "xAxis": {
        "categories": categories,
        "title": {"text": "Product Category", "style": {"fontSize": "38px", "color": "#444444"}},
        "labels": {"style": {"fontSize": "30px", "color": "#444444"}},
        "lineColor": "#cccccc",
        "tickColor": "#cccccc",
    },
    "yAxis": {
        "title": {"text": "Sales (Units)", "style": {"fontSize": "38px", "color": "#444444"}},
        "labels": {"style": {"fontSize": "30px", "color": "#444444"}},
        "gridLineColor": "#eeeeee",
        "gridLineWidth": 0.5,
        "gridLineDashStyle": "Dot",
        "tickInterval": 1000,
    },
    "legend": {"enabled": False},
    "plotOptions": {"column": {"pointPadding": 0.15, "borderWidth": 0, "groupPadding": 0.1, "borderRadius": 4}},
    "series": [
        {
            "name": "Sales",
            "data": values,
            "color": "#306998",
            "dataLabels": {
                "enabled": True,
                "format": "{y:,.0f}",
                "style": {"fontSize": "28px", "fontWeight": "bold", "color": "#333333"},
            },
        }
    ],
    "credits": {"enabled": False},
}

# Download Highcharts JS for inline embedding (required for headless Chrome)
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# Generate HTML with inline scripts
chart_options_json = json.dumps(chart_options)
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            Highcharts.chart('container', {chart_options_json});
        }});
    </script>
</body>
</html>"""

# Write temp HTML file
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Save HTML for interactive viewing
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Take screenshot with headless Chrome
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

# Clean up temp file
Path(temp_path).unlink()
