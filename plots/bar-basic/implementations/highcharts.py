"""
bar-basic: Basic Bar Chart
Library: highcharts
"""

import json
import tempfile
import time
import urllib.request
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Product sales by category
categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys"]
values = [4200, 3100, 2800, 2400, 1900, 1500]

# Chart options as dictionary (directly for Highcharts)
chart_options = {
    "chart": {
        "type": "column",
        "width": 4800,
        "height": 2700,
        "backgroundColor": "#ffffff",
        "marginBottom": 250,
        "style": {"fontFamily": "Arial, sans-serif"},
    },
    "title": {"text": "Product Sales by Category", "style": {"fontSize": "48px", "fontWeight": "bold"}},
    "xAxis": {
        "categories": categories,
        "title": {"text": "Category", "style": {"fontSize": "36px"}},
        "labels": {"style": {"fontSize": "28px"}},
    },
    "yAxis": {
        "title": {"text": "Sales ($)", "style": {"fontSize": "36px"}},
        "labels": {"style": {"fontSize": "28px"}},
        "gridLineColor": "#e0e0e0",
    },
    "legend": {"enabled": False},
    "plotOptions": {"column": {"pointPadding": 0.2, "borderWidth": 0, "groupPadding": 0.1}},
    "series": [
        {
            "name": "Sales",
            "data": values,
            "color": "#306998",
            "dataLabels": {"enabled": True, "format": "{y:,.0f}", "style": {"fontSize": "24px", "fontWeight": "bold"}},
        }
    ],
}

# Download Highcharts JS for inline embedding
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

# Also save the HTML for interactive viewing
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
