""" pyplots.ai
chart-export-menu: Chart with Built-in Export Menu
Library: highcharts unknown | Python 3.13.11
Quality: 91/100 | Created: 2026-01-19
"""

import json
import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Monthly sales over a year
np.random.seed(42)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
sales = (np.cumsum(np.random.randint(50, 150, size=12)) + 500).tolist()

# Chart configuration with export menu - defined as dict for full control
chart_options = {
    "chart": {
        "type": "line",
        "width": 4800,
        "height": 2700,
        "backgroundColor": "#ffffff",
        "marginBottom": 200,
        "marginTop": 180,
        "spacingRight": 200,
    },
    "title": {
        "text": "chart-export-menu · highcharts · pyplots.ai",
        "style": {"fontSize": "48px", "fontWeight": "bold"},
    },
    "subtitle": {
        "text": "Click the menu icon (≡) in top right to export as PNG, SVG, PDF, or CSV",
        "style": {"fontSize": "28px", "color": "#666666"},
    },
    "xAxis": {
        "categories": months,
        "title": {"text": "Month", "style": {"fontSize": "32px"}},
        "labels": {"style": {"fontSize": "24px"}},
    },
    "yAxis": {
        "title": {"text": "Sales (units)", "style": {"fontSize": "32px"}},
        "labels": {"style": {"fontSize": "24px"}},
        "gridLineWidth": 1,
        "gridLineColor": "#e0e0e0",
    },
    # Exporting configuration - the key feature of this chart
    "exporting": {
        "enabled": True,
        "buttons": {
            "contextButton": {
                "menuItems": [
                    "downloadPNG",
                    "downloadSVG",
                    "downloadPDF",
                    "separator",
                    "downloadCSV",
                    "downloadXLS",
                    "separator",
                    "printChart",
                ],
                "symbolSize": 48,
                "symbolStrokeWidth": 6,
                "symbolX": 32,
                "symbolY": 30,
                "height": 64,
                "width": 68,
                "y": -10,
                "theme": {
                    "fill": "#306998",
                    "stroke": "#306998",
                    "r": 10,
                    "states": {
                        "hover": {"fill": "#FFD43B", "stroke": "#FFD43B"},
                        "select": {"fill": "#FFD43B", "stroke": "#FFD43B"},
                    },
                },
                "symbolFill": "#ffffff",
                "symbolStroke": "#ffffff",
            }
        },
        "sourceWidth": 1200,
        "sourceHeight": 675,
        "scale": 2,
        "fallbackToExportServer": True,
    },
    # Navigation menu styling for dropdown
    "navigation": {
        "menuStyle": {
            "background": "#ffffff",
            "border": "2px solid #306998",
            "padding": "15px",
            "boxShadow": "3px 3px 10px rgba(0,0,0,0.2)",
        },
        "menuItemStyle": {"fontSize": "24px", "padding": "12px 20px", "color": "#333333"},
        "menuItemHoverStyle": {"background": "#306998", "color": "#ffffff"},
    },
    "plotOptions": {
        "line": {
            "lineWidth": 6,
            "marker": {"radius": 14, "symbol": "circle", "lineWidth": 3, "lineColor": "#ffffff"},
            "dataLabels": {"enabled": True, "style": {"fontSize": "22px", "fontWeight": "bold"}},
        }
    },
    "legend": {"enabled": True, "itemStyle": {"fontSize": "28px"}, "itemMarginTop": 15, "y": 30},
    "credits": {"enabled": False},
    "series": [{"name": "Monthly Sales", "data": sales, "color": "#306998"}],
}

# Convert to JSON for JavaScript
chart_json = json.dumps(chart_options)

# Download required Highcharts JS files (including exporting module)
highcharts_url = "https://code.highcharts.com/highcharts.js"
exporting_url = "https://code.highcharts.com/modules/exporting.js"
export_data_url = "https://code.highcharts.com/modules/export-data.js"

with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

with urllib.request.urlopen(exporting_url, timeout=30) as response:
    exporting_js = response.read().decode("utf-8")

with urllib.request.urlopen(export_data_url, timeout=30) as response:
    export_data_js = response.read().decode("utf-8")

# Generate HTML with inline scripts including export modules
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{exporting_js}</script>
    <script>{export_data_js}</script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>
        Highcharts.chart('container', {chart_json});
    </script>
</body>
</html>"""

# Write temp HTML and take screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Save HTML for interactive use
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

Path(temp_path).unlink()
