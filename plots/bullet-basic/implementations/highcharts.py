"""pyplots.ai
bullet-basic: Basic Bullet Chart
Library: highcharts | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import json
import tempfile
import time
import urllib.request
from pathlib import Path

from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Multiple KPIs with actual values, targets, and qualitative ranges
# Normalized to percentage scale (0-100) for consistent display
metrics = [
    {
        "name": "Revenue",
        "actual": 275,
        "target": 250,
        "max_value": 300,
        "ranges": [50, 75, 100],  # Poor/Satisfactory/Good as percentages
        "unit": "$K",
    },
    {
        "name": "Profit",
        "actual": 22,
        "target": 27,
        "max_value": 35,
        "ranges": [43, 71, 100],  # 15/35, 25/35, 35/35 as percentages
        "unit": "%",
    },
    {
        "name": "New Customers",
        "actual": 1650,
        "target": 1500,
        "max_value": 2000,
        "ranges": [50, 70, 100],  # 1000/2000, 1400/2000, 2000/2000
        "unit": "",
    },
    {
        "name": "Satisfaction",
        "actual": 4.5,
        "target": 4.7,
        "max_value": 5.0,
        "ranges": [70, 84, 100],  # 3.5/5, 4.2/5, 5/5 as percentages
        "unit": "/5",
    },
]

# Grayscale colors for qualitative ranges (light to dark = poor to good)
range_colors = ["#e0e0e0", "#b0b0b0", "#808080"]

# Build series data - normalize all values to 0-100 scale for consistent display
series_data = []
for metric in metrics:
    max_val = metric["max_value"]
    series_data.append(
        {
            "y": round((metric["actual"] / max_val) * 100, 1),
            "target": round((metric["target"] / max_val) * 100, 1),
            # Store original values for display
            "actual_value": metric["actual"],
            "target_value": metric["target"],
            "unit": metric["unit"],
        }
    )

# Build categories with metric names
categories = []
for metric in metrics:
    if metric["unit"]:
        categories.append(f"{metric['name']} ({metric['unit']})")
    else:
        categories.append(metric["name"])

# Chart options for bullet chart
chart_options = {
    "chart": {
        "type": "bullet",
        "width": 4800,
        "height": 2700,
        "backgroundColor": "#ffffff",
        "inverted": True,  # Horizontal bullet charts
        "marginLeft": 450,  # Space for category labels
        "spacing": [100, 100, 100, 100],
    },
    "title": {"text": "bullet-basic · highcharts · pyplots.ai", "style": {"fontSize": "48px", "fontWeight": "bold"}},
    "subtitle": {
        "text": "Q4 Performance Dashboard - Actual vs Target",
        "style": {"fontSize": "32px", "color": "#666666"},
    },
    "xAxis": {"categories": categories, "labels": {"style": {"fontSize": "32px", "fontWeight": "bold"}}},
    "yAxis": {
        "gridLineWidth": 0,
        "min": 0,
        "max": 100,
        "title": {"text": "% of Target Range", "style": {"fontSize": "28px"}},
        "labels": {"format": "{value}%", "style": {"fontSize": "24px"}},
        "plotBands": [
            # Poor range (0-50%)
            {"from": 0, "to": 50, "color": range_colors[0]},
            # Satisfactory range (50-75%)
            {"from": 50, "to": 75, "color": range_colors[1]},
            # Good range (75-100%)
            {"from": 75, "to": 100, "color": range_colors[2]},
        ],
    },
    "legend": {"enabled": False},
    "plotOptions": {
        "bullet": {
            "pointPadding": 0.3,
            "borderWidth": 0,
            "groupPadding": 0.2,
            "color": "#306998",  # Python Blue for actual value bar
            "targetOptions": {
                "width": "180%",
                "height": 6,
                "borderWidth": 0,
                "color": "#1a1a1a",  # Dark target line
            },
            "dataLabels": {
                "enabled": True,
                "format": "{point.actual_value}{point.unit}",
                "style": {"fontSize": "28px", "fontWeight": "bold", "color": "#ffffff"},
                "inside": True,
                "align": "right",
            },
        }
    },
    "series": [{"name": "Performance", "data": series_data}],
    "tooltip": {
        "headerFormat": '<span style="font-size: 24px; font-weight: bold;">{point.key}</span><br/>',
        "pointFormat": '<span style="font-size: 20px;">Actual: <b>{point.actual_value}{point.unit}</b><br/>Target: <b>{point.target_value}{point.unit}</b><br/>Performance: <b>{point.y}%</b></span>',
        "style": {"fontSize": "20px"},
    },
    "credits": {"enabled": False},
}

# Download Highcharts JS files for inline embedding
highcharts_url = "https://code.highcharts.com/highcharts.js"
highcharts_more_url = "https://code.highcharts.com/highcharts-more.js"
bullet_url = "https://code.highcharts.com/modules/bullet.js"

with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

with urllib.request.urlopen(highcharts_more_url, timeout=30) as response:
    highcharts_more_js = response.read().decode("utf-8")

with urllib.request.urlopen(bullet_url, timeout=30) as response:
    bullet_js = response.read().decode("utf-8")

# Generate HTML with inline scripts
chart_options_json = json.dumps(chart_options)
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{highcharts_more_js}</script>
    <script>{bullet_js}</script>
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
chrome_options.add_argument("--window-size=4800,2900")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)  # Wait for chart to render
driver.save_screenshot("plot_raw.png")
driver.quit()

# Crop to exact 4800x2700 dimensions
img = Image.open("plot_raw.png")
img_cropped = img.crop((0, 0, 4800, 2700))
img_cropped.save("plot.png")
Path("plot_raw.png").unlink()

Path(temp_path).unlink()  # Clean up temp file
