"""pyplots.ai
circlepacking-basic: Circle Packing Chart
Library: highcharts unknown | Python 3.13.11
Quality: 45/100 | Created: 2025-12-30
"""

import tempfile
import time
import urllib.request
from pathlib import Path

from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data: Software project structure with lines of code
# Hierarchical structure: Project -> Modules -> Components
# Using square layout (3600x3600) for better circle packing visualization
data = [
    # Level 1: Main modules (innermost ring)
    {"id": "frontend", "name": "Frontend", "color": "#306998"},
    {"id": "backend", "name": "Backend", "color": "#FFD43B"},
    {"id": "shared", "name": "Shared", "color": "#9467BD"},
    # Level 2: Frontend components (leaf nodes with values - lines of code)
    {"name": "Components", "parent": "frontend", "value": 8500},
    {"name": "Pages", "parent": "frontend", "value": 6200},
    {"name": "Hooks", "parent": "frontend", "value": 2100},
    {"name": "Styles", "parent": "frontend", "value": 3800},
    {"name": "Assets", "parent": "frontend", "value": 1200},
    # Level 2: Backend components
    {"name": "API Routes", "parent": "backend", "value": 5400},
    {"name": "Services", "parent": "backend", "value": 7200},
    {"name": "Models", "parent": "backend", "value": 3100},
    {"name": "Middleware", "parent": "backend", "value": 1800},
    {"name": "Database", "parent": "backend", "value": 4500},
    # Level 2: Shared components (all nodes shown, including small ones)
    {"name": "Utilities", "parent": "shared", "value": 2800},
    {"name": "Types", "parent": "shared", "value": 1500},
    {"name": "Constants", "parent": "shared", "value": 800},
]

# Create chart with sunburst type for hierarchical nesting visualization
# Sunburst shows children nested within parent arcs, demonstrating hierarchy
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration - use square format for better radial visualization
chart.options.chart = {"type": "sunburst", "width": 3600, "height": 3600, "backgroundColor": "#ffffff"}

# Title
chart.options.title = {
    "text": "circlepacking-basic · highcharts · pyplots.ai",
    "style": {"fontSize": "56px", "fontWeight": "bold"},
}

# Subtitle with context
chart.options.subtitle = {
    "text": "Software Project Structure by Lines of Code",
    "style": {"fontSize": "36px", "color": "#666666"},
}

# Disable credits
chart.options.credits = {"enabled": False}

# Tooltip configuration
chart.options.tooltip = {
    "headerFormat": "",
    "pointFormat": "<b>{point.name}</b><br/>Lines of Code: {point.value:,.0f}",
    "style": {"fontSize": "28px"},
}

# Sunburst series configuration with hierarchy levels
chart.options.series = [
    {
        "type": "sunburst",
        "data": data,
        "name": "Lines of Code",
        "allowDrillToNode": True,
        "cursor": "pointer",
        "borderRadius": 3,
        "borderWidth": 2,
        "borderColor": "#ffffff",
        "dataLabels": {
            "format": "{point.name}",
            "style": {"fontSize": "28px", "textOutline": "3px white", "fontWeight": "500"},
        },
        "levels": [
            {
                "level": 1,
                "colorByPoint": True,
                "dataLabels": {
                    "enabled": True,
                    "style": {"fontSize": "48px", "fontWeight": "bold"},
                    "rotationMode": "circular",
                },
            },
            {
                "level": 2,
                "colorVariation": {"key": "brightness", "to": 0.25},
                "dataLabels": {
                    "enabled": True,
                    "style": {"fontSize": "32px", "fontWeight": "600"},
                    "rotationMode": "circular",
                    "allowOverlap": False,
                },
            },
        ],
    }
]

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
<body style="margin:0; padding:0; background:#ffffff;">
    <div id="container" style="width: 3600px; height: 3600px;"></div>
    <script>{html_str}</script>
</body>
</html>"""

# Write temp HTML and take screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Also save interactive HTML
with open("plot.html", "w", encoding="utf-8") as f:
    # Use CDN for standalone HTML
    html_standalone = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>circlepacking-basic · highcharts · pyplots.ai</title>
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/modules/sunburst.js"></script>
</head>
<body style="margin:0; padding:20px; background:#ffffff;">
    <div id="container" style="width: 100%; height: 90vh; min-height: 600px;"></div>
    <script>{html_str}</script>
</body>
</html>"""
    f.write(html_standalone)

# Chrome options for headless rendering
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=3600,3600")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)  # Wait for chart to render
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()  # Clean up temp file
