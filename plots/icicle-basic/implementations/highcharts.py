"""pyplots.ai
icicle-basic: Basic Icicle Chart
Library: highcharts | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import tempfile
import time
import urllib.request
from pathlib import Path

from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - File system hierarchy with folders and files
# Hierarchical structure showing directories and file sizes (KB)
data = [
    # Root
    {"id": "root", "name": "Project Files", "color": "#306998"},
    # Level 1 - Main directories
    {"id": "src", "name": "src", "parent": "root", "color": "#306998"},
    {"id": "docs", "name": "docs", "parent": "root", "color": "#FFD43B"},
    {"id": "tests", "name": "tests", "parent": "root", "color": "#9467BD"},
    {"id": "assets", "name": "assets", "parent": "root", "color": "#17BECF"},
    # Level 2 - src subdirectories
    {"id": "components", "name": "components", "parent": "src"},
    {"id": "utils", "name": "utils", "parent": "src"},
    {"id": "api", "name": "api", "parent": "src"},
    # Level 2 - docs files (leaf nodes with values)
    {"name": "README.md", "parent": "docs", "value": 45},
    {"name": "guide.md", "parent": "docs", "value": 120},
    {"name": "api.md", "parent": "docs", "value": 85},
    # Level 2 - tests files
    {"name": "test_main.py", "parent": "tests", "value": 65},
    {"name": "test_utils.py", "parent": "tests", "value": 48},
    {"name": "test_api.py", "parent": "tests", "value": 72},
    # Level 2 - assets subdirectories
    {"id": "images", "name": "images", "parent": "assets"},
    {"id": "styles", "name": "styles", "parent": "assets"},
    # Level 3 - components files
    {"name": "Header.tsx", "parent": "components", "value": 95},
    {"name": "Footer.tsx", "parent": "components", "value": 55},
    {"name": "Sidebar.tsx", "parent": "components", "value": 110},
    {"name": "Modal.tsx", "parent": "components", "value": 78},
    # Level 3 - utils files
    {"name": "helpers.ts", "parent": "utils", "value": 42},
    {"name": "constants.ts", "parent": "utils", "value": 28},
    {"name": "validators.ts", "parent": "utils", "value": 65},
    # Level 3 - api files
    {"name": "client.ts", "parent": "api", "value": 88},
    {"name": "endpoints.ts", "parent": "api", "value": 56},
    {"name": "types.ts", "parent": "api", "value": 34},
    # Level 3 - images files
    {"name": "logo.png", "parent": "images", "value": 125},
    {"name": "banner.jpg", "parent": "images", "value": 280},
    {"name": "icons.svg", "parent": "images", "value": 45},
    # Level 3 - styles files
    {"name": "main.css", "parent": "styles", "value": 92},
    {"name": "theme.css", "parent": "styles", "value": 68},
]

# Create chart using highcharts-core
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration - using treemap with stripes layout for icicle effect
chart.options.chart = {"type": "treemap", "width": 4800, "height": 2700, "backgroundColor": "#ffffff"}

# Title
chart.options.title = {
    "text": "File System Structure · icicle-basic · highcharts · pyplots.ai",
    "style": {"fontSize": "56px", "fontWeight": "bold"},
}

# Subtitle
chart.options.subtitle = {"text": "Directory hierarchy showing file sizes (KB)", "style": {"fontSize": "36px"}}

# Tooltip
chart.options.tooltip = {"style": {"fontSize": "32px"}, "pointFormat": "<b>{point.name}</b><br/>Size: {point.value} KB"}

# Treemap series with stripes layout algorithm for icicle-like visualization
# stripes layout creates horizontal bands at each level
series_config = {
    "type": "treemap",
    "name": "File Size",
    "layoutAlgorithm": "stripes",
    "layoutStartingDirection": "vertical",
    "alternateStartingDirection": False,
    "allowTraversingTree": True,
    "animationLimit": 1000,
    "borderWidth": 3,
    "borderColor": "#ffffff",
    "dataLabels": {"enabled": True, "style": {"fontSize": "26px", "fontWeight": "normal", "textOutline": "2px white"}},
    "levels": [
        {
            "level": 1,
            "dataLabels": {
                "enabled": True,
                "align": "center",
                "verticalAlign": "middle",
                "style": {"fontSize": "44px", "fontWeight": "bold", "textOutline": "3px white"},
            },
            "borderWidth": 5,
            "borderColor": "#ffffff",
            "layoutAlgorithm": "stripes",
        },
        {
            "level": 2,
            "dataLabels": {
                "enabled": True,
                "style": {"fontSize": "34px", "fontWeight": "bold", "textOutline": "2px white"},
            },
            "borderWidth": 4,
            "borderColor": "#ffffff",
            "colorVariation": {"key": "brightness", "to": -0.2},
        },
        {
            "level": 3,
            "dataLabels": {
                "enabled": True,
                "style": {"fontSize": "28px", "fontWeight": "normal", "textOutline": "2px white"},
            },
            "borderWidth": 3,
            "borderColor": "#ffffff",
            "colorVariation": {"key": "brightness", "to": 0.2},
        },
        {
            "level": 4,
            "dataLabels": {
                "enabled": True,
                "style": {"fontSize": "24px", "fontWeight": "normal", "textOutline": "2px white"},
            },
            "borderWidth": 2,
            "borderColor": "#ffffff",
            "colorVariation": {"key": "brightness", "to": 0.4},
        },
    ],
    "data": data,
}

chart.options.series = [series_config]

# Disable legend (colors visible in rectangles)
chart.options.legend = {"enabled": False}

# Download Highcharts JS and treemap module
highcharts_url = "https://code.highcharts.com/highcharts.js"
treemap_url = "https://code.highcharts.com/modules/treemap.js"

with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

with urllib.request.urlopen(treemap_url, timeout=30) as response:
    treemap_js = response.read().decode("utf-8")

# Generate HTML with inline scripts
html_str = chart.to_js_literal()
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{treemap_js}</script>
</head>
<body style="margin:0; padding:0; background:#ffffff;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>{html_str}</script>
</body>
</html>"""

# Save HTML for interactive version
with open("plot.html", "w", encoding="utf-8") as f:
    standalone_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>icicle-basic · highcharts · pyplots.ai</title>
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/modules/treemap.js"></script>
    <style>
        body {{ margin: 0; padding: 20px; font-family: sans-serif; background: #ffffff; }}
        #container {{ width: 100%; height: 90vh; min-height: 600px; }}
    </style>
</head>
<body>
    <div id="container"></div>
    <script>{html_str}</script>
</body>
</html>"""
    f.write(standalone_html)

# Write temp HTML and take screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

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
