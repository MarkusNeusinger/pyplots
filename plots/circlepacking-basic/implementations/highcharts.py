"""pyplots.ai
circlepacking-basic: Circle Packing Chart
Library: highcharts | Python 3.13
Quality: pending | Created: 2025-12-30
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
data = [
    # Root
    {"id": "project", "name": "Software Project", "parent": None},
    # Level 1: Main modules
    {"id": "frontend", "name": "Frontend", "parent": "project"},
    {"id": "backend", "name": "Backend", "parent": "project"},
    {"id": "shared", "name": "Shared", "parent": "project"},
    # Level 2: Frontend components (leaf nodes with values - lines of code)
    {"id": "components", "name": "Components", "parent": "frontend", "value": 8500},
    {"id": "pages", "name": "Pages", "parent": "frontend", "value": 6200},
    {"id": "hooks", "name": "Hooks", "parent": "frontend", "value": 2100},
    {"id": "styles", "name": "Styles", "parent": "frontend", "value": 3800},
    {"id": "assets", "name": "Assets", "parent": "frontend", "value": 1200},
    # Level 2: Backend components
    {"id": "api", "name": "API Routes", "parent": "backend", "value": 5400},
    {"id": "services", "name": "Services", "parent": "backend", "value": 7200},
    {"id": "models", "name": "Models", "parent": "backend", "value": 3100},
    {"id": "middleware", "name": "Middleware", "parent": "backend", "value": 1800},
    {"id": "database", "name": "Database", "parent": "backend", "value": 4500},
    # Level 2: Shared components
    {"id": "utils", "name": "Utilities", "parent": "shared", "value": 2800},
    {"id": "types", "name": "Types", "parent": "shared", "value": 1500},
    {"id": "constants", "name": "Constants", "parent": "shared", "value": 800},
]

# Create chart with container
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration for 4800x2700 with proper margins
chart.options.chart = {
    "type": "packedbubble",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "spacingTop": 100,
    "spacingBottom": 120,
}

# Title
chart.options.title = {
    "text": "circlepacking-basic · highcharts · pyplots.ai",
    "style": {"fontSize": "60px", "fontWeight": "bold"},
    "margin": 30,
}

# Subtitle with context
chart.options.subtitle = {
    "text": "Software Project Structure by Lines of Code",
    "style": {"fontSize": "40px", "color": "#666666"},
}

# Tooltip configuration
chart.options.tooltip = {
    "useHTML": True,
    "headerFormat": "",
    "pointFormat": "<b>{point.name}</b><br/>Lines of Code: {point.value:,.0f}",
    "style": {"fontSize": "28px"},
}

# Legend configuration - place at top right to avoid cutoff
chart.options.legend = {
    "enabled": True,
    "itemStyle": {"fontSize": "36px", "fontWeight": "normal"},
    "symbolRadius": 14,
    "symbolHeight": 28,
    "symbolWidth": 28,
    "layout": "vertical",
    "align": "right",
    "verticalAlign": "top",
    "x": -50,
    "y": 150,
    "floating": True,
    "backgroundColor": "rgba(255, 255, 255, 0.9)",
    "borderWidth": 1,
    "borderColor": "#cccccc",
    "padding": 20,
}

# Colors for each module (colorblind-safe)
colors = {
    "Frontend": "#306998",  # Python Blue
    "Backend": "#FFD43B",  # Python Yellow
    "Shared": "#9467BD",  # Purple
}

# Plot options for packed bubble - make bubbles much larger
chart.options.plot_options = {
    "packedbubble": {
        "minSize": "40%",
        "maxSize": "250%",
        "zMin": 0,
        "zMax": 9000,
        "useSimulation": True,
        "layoutAlgorithm": {
            "gravitationalConstant": 0.015,
            "splitSeries": True,
            "seriesInteraction": False,
            "dragBetweenSeries": False,
            "parentNodeLimit": True,
            "parentNodeOptions": {"bubblePadding": 40},
            "initialPositions": "random",
            "enableSimulation": True,
            "maxIterations": 200,
        },
        "dataLabels": {
            "enabled": True,
            "format": "{point.name}",
            "style": {"fontSize": "30px", "textOutline": "3px white", "fontWeight": "bold", "color": "#333333"},
            "filter": {"property": "value", "operator": ">", "value": 1000},
        },
        "marker": {"fillOpacity": 0.85, "lineWidth": 3, "lineColor": "#ffffff"},
    }
}

# Build series data grouped by parent module
frontend_data = []
backend_data = []
shared_data = []

for item in data:
    if item.get("value"):  # Only leaf nodes
        entry = {"name": item["name"], "value": item["value"]}
        if item["parent"] == "frontend":
            frontend_data.append(entry)
        elif item["parent"] == "backend":
            backend_data.append(entry)
        elif item["parent"] == "shared":
            shared_data.append(entry)

# Add series using raw options (packedbubble series)
chart.options.series = [
    {"name": "Frontend", "data": frontend_data, "color": colors["Frontend"]},
    {"name": "Backend", "data": backend_data, "color": colors["Backend"]},
    {"name": "Shared", "data": shared_data, "color": colors["Shared"]},
]

# Download Highcharts JS for headless rendering
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# Download highcharts-more for packed bubble support
highcharts_more_url = "https://code.highcharts.com/highcharts-more.js"
with urllib.request.urlopen(highcharts_more_url, timeout=30) as response:
    highcharts_more_js = response.read().decode("utf-8")

# Generate HTML with inline scripts
html_str = chart.to_js_literal()
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{highcharts_more_js}</script>
</head>
<body style="margin:0; padding:0; background:#ffffff;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
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
    <script src="https://code.highcharts.com/highcharts-more.js"></script>
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
chrome_options.add_argument("--window-size=4800,2700")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)  # Wait for chart to render
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()  # Clean up temp file
