""" pyplots.ai
sunburst-basic: Basic Sunburst Chart
Library: highcharts 1.10.3 | Python 3.13.11
Quality: 95/100 | Created: 2025-12-14
"""

import tempfile
import time
import urllib.request
from pathlib import Path

from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Budget breakdown by department, team, and project
# Using a hierarchical structure with ids for parent references
data = [
    # Level 1: Departments (innermost ring)
    {"id": "engineering", "name": "Engineering", "color": "#306998"},
    {"id": "marketing", "name": "Marketing", "color": "#FFD43B"},
    {"id": "operations", "name": "Operations", "color": "#9467BD"},
    # Level 2: Teams
    {"id": "frontend", "name": "Frontend", "parent": "engineering", "value": 180},
    {"id": "backend", "name": "Backend", "parent": "engineering", "value": 220},
    {"id": "devops", "name": "DevOps", "parent": "engineering", "value": 120},
    {"id": "digital", "name": "Digital", "parent": "marketing", "value": 150},
    {"id": "content", "name": "Content", "parent": "marketing", "value": 90},
    {"id": "brand", "name": "Brand", "parent": "marketing", "value": 60},
    {"id": "hr", "name": "HR", "parent": "operations", "value": 80},
    {"id": "finance", "name": "Finance", "parent": "operations", "value": 70},
    {"id": "facilities", "name": "Facilities", "parent": "operations", "value": 50},
    # Level 3: Projects (outermost ring)
    {"name": "React App", "parent": "frontend", "value": 80},
    {"name": "Mobile UI", "parent": "frontend", "value": 60},
    {"name": "Design System", "parent": "frontend", "value": 40},
    {"name": "API v2", "parent": "backend", "value": 100},
    {"name": "Database", "parent": "backend", "value": 70},
    {"name": "Microservices", "parent": "backend", "value": 50},
    {"name": "CI/CD", "parent": "devops", "value": 60},
    {"name": "Cloud Infra", "parent": "devops", "value": 60},
    {"name": "SEO", "parent": "digital", "value": 50},
    {"name": "Social Media", "parent": "digital", "value": 60},
    {"name": "PPC", "parent": "digital", "value": 40},
    {"name": "Blog", "parent": "content", "value": 50},
    {"name": "Videos", "parent": "content", "value": 40},
    {"name": "Logo Refresh", "parent": "brand", "value": 30},
    {"name": "Guidelines", "parent": "brand", "value": 30},
    {"name": "Recruiting", "parent": "hr", "value": 40},
    {"name": "Training", "parent": "hr", "value": 40},
    {"name": "Payroll", "parent": "finance", "value": 35},
    {"name": "Audit", "parent": "finance", "value": 35},
    {"name": "Office", "parent": "facilities", "value": 30},
    {"name": "Equipment", "parent": "facilities", "value": 20},
]

# Create chart with sunburst type
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {"type": "sunburst", "width": 4800, "height": 2700, "backgroundColor": "#ffffff"}

# Title
chart.options.title = {
    "text": "sunburst-basic \u00b7 highcharts \u00b7 pyplots.ai",
    "style": {"fontSize": "48px", "fontWeight": "bold"},
}

# Subtitle
chart.options.subtitle = {"text": "Budget Allocation by Department, Team, and Project", "style": {"fontSize": "32px"}}

# Credits
chart.options.credits = {"enabled": False}

# Series data
chart.options.series = [
    {
        "type": "sunburst",
        "data": data,
        "name": "Budget",
        "allowDrillToNode": True,
        "cursor": "pointer",
        "dataLabels": {
            "format": "{point.name}",
            "style": {"fontSize": "24px", "textOutline": "2px white"},
            "rotationMode": "circular",
        },
        "levels": [
            {"level": 1, "colorByPoint": True, "dataLabels": {"style": {"fontSize": "32px", "fontWeight": "bold"}}},
            {
                "level": 2,
                "colorVariation": {"key": "brightness", "to": 0.2},
                "dataLabels": {"style": {"fontSize": "26px"}},
            },
            {
                "level": 3,
                "colorVariation": {"key": "brightness", "to": 0.4},
                "dataLabels": {"style": {"fontSize": "20px"}},
            },
        ],
    }
]

# Tooltip
chart.options.tooltip = {
    "headerFormat": "",
    "pointFormat": "<b>{point.name}</b>: ${point.value}K",
    "style": {"fontSize": "24px"},
}

# Download Highcharts JS and sunburst module
highcharts_url = "https://code.highcharts.com/highcharts.js"
sunburst_url = "https://code.highcharts.com/modules/sunburst.js"

with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

with urllib.request.urlopen(sunburst_url, timeout=30) as response:
    sunburst_js = response.read().decode("utf-8")

# Generate HTML with inline scripts
html_str = chart.to_js_literal()
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{sunburst_js}</script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>{html_str}</script>
</body>
</html>"""

# Write temp HTML file
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Also save as plot.html for interactive viewing
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Take screenshot with Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4800,2700")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)  # Wait for chart to render
driver.save_screenshot("plot.png")
driver.quit()

# Clean up temp file
Path(temp_path).unlink()
