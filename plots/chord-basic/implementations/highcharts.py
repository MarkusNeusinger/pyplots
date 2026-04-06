""" pyplots.ai
chord-basic: Basic Chord Diagram
Library: highcharts 1.10.3 | Python 3.14
Quality: 87/100 | Updated: 2026-04-06
"""

import json
import tempfile
import time
import urllib.request
from pathlib import Path

from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Trade flows between continents (billions USD, approximate)
flows = [
    ["Europe", "N. America", 28],
    ["Europe", "Asia", 22],
    ["Europe", "Africa", 8],
    ["Europe", "S. America", 6],
    ["Europe", "Oceania", 4],
    ["Asia", "N. America", 35],
    ["Asia", "Europe", 25],
    ["Asia", "Oceania", 12],
    ["Asia", "Africa", 10],
    ["Asia", "S. America", 7],
    ["Africa", "Europe", 15],
    ["Africa", "Asia", 12],
    ["Africa", "N. America", 8],
    ["Africa", "S. America", 3],
    ["Africa", "Oceania", 2],
    ["N. America", "Europe", 26],
    ["N. America", "Asia", 30],
    ["N. America", "S. America", 18],
    ["N. America", "Oceania", 5],
    ["N. America", "Africa", 4],
    ["S. America", "N. America", 22],
    ["S. America", "Europe", 14],
    ["S. America", "Asia", 10],
    ["S. America", "Africa", 3],
    ["S. America", "Oceania", 2],
    ["Oceania", "Asia", 18],
    ["Oceania", "Europe", 6],
    ["Oceania", "N. America", 5],
    ["Oceania", "Africa", 1],
    ["Oceania", "S. America", 1],
]

# Refined palette — harmonious, colorblind-safe, muted-professional tones
nodes = [
    {"id": "Europe", "color": "#306998"},
    {"id": "Asia", "color": "#E8A838"},
    {"id": "Africa", "color": "#8B6CAF"},
    {"id": "N. America", "color": "#2BA5B5"},
    {"id": "S. America", "color": "#3DAA6D"},
    {"id": "Oceania", "color": "#D4654A"},
]

# Chart configuration
chart_config = {
    "chart": {
        "type": "dependencywheel",
        "width": 3600,
        "height": 3600,
        "backgroundColor": {
            "linearGradient": {"x1": 0, "y1": 0, "x2": 0, "y2": 1},
            "stops": [[0, "#FAFBFC"], [1, "#F0F2F5"]],
        },
        "marginTop": 160,
        "marginBottom": 40,
        "style": {"fontFamily": "'Segoe UI', Helvetica, Arial, sans-serif"},
    },
    "title": {
        "text": "chord-basic \u00b7 highcharts \u00b7 pyplots.ai",
        "style": {"fontSize": "60px", "fontWeight": "700", "color": "#1A2332", "letterSpacing": "0.5px"},
        "y": 50,
    },
    "subtitle": {
        "text": "Trade Flows Between Continents (Billions USD)",
        "style": {"fontSize": "40px", "fontWeight": "400", "color": "#5A6878", "letterSpacing": "0.3px"},
        "y": 110,
    },
    "tooltip": {
        "style": {"fontSize": "32px"},
        "backgroundColor": "rgba(255,255,255,0.96)",
        "borderWidth": 1,
        "borderColor": "#DDE1E6",
        "shadow": True,
        "nodeFormat": "<b>{point.name}</b><br/>Total: ${point.sum}B",
        "pointFormat": "{point.fromNode.name} \u2192 {point.toNode.name}<br/><b>${point.weight}B</b>",
    },
    "series": [
        {
            "type": "dependencywheel",
            "name": "Trade Flow",
            "keys": ["from", "to", "weight"],
            "data": flows,
            "nodes": nodes,
            "dataLabels": {
                "enabled": True,
                "style": {
                    "fontSize": "42px",
                    "fontWeight": "600",
                    "textOutline": "5px rgba(255,255,255,0.9)",
                    "color": "#1A2332",
                },
                "distance": 45,
                "padding": 10,
                "crop": False,
                "overflow": "allow",
            },
            "size": "78%",
            "center": ["50%", "54%"],
            "linkOpacity": 0.5,
            "curveFactor": 0.6,
            "nodePadding": 18,
            "nodeWidth": 40,
            "borderWidth": 2,
            "borderColor": "rgba(255,255,255,0.7)",
            "colorByPoint": True,
            "minLinkWidth": 4,
        }
    ],
    "legend": {"enabled": False},
    "credits": {"enabled": False},
    "accessibility": {"enabled": False},
}

# Download Highcharts JS and modules
headers = {"User-Agent": "Mozilla/5.0"}
highcharts_url = "https://cdn.jsdelivr.net/npm/highcharts@11/highcharts.js"
sankey_url = "https://cdn.jsdelivr.net/npm/highcharts@11/modules/sankey.js"
wheel_url = "https://cdn.jsdelivr.net/npm/highcharts@11/modules/dependency-wheel.js"

with urllib.request.urlopen(urllib.request.Request(highcharts_url, headers=headers), timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

with urllib.request.urlopen(urllib.request.Request(sankey_url, headers=headers), timeout=30) as response:
    sankey_js = response.read().decode("utf-8")

with urllib.request.urlopen(urllib.request.Request(wheel_url, headers=headers), timeout=30) as response:
    wheel_js = response.read().decode("utf-8")

# Generate HTML with custom CSS for extra polish
chart_json = json.dumps(chart_config)
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        body {{ margin: 0; font-family: 'Inter', 'Segoe UI', sans-serif; }}
        #container {{ width: 3600px; height: 3600px; }}
    </style>
    <script>{highcharts_js}</script>
    <script>{sankey_js}</script>
    <script>{wheel_js}</script>
</head>
<body>
    <div id="container"></div>
    <script>
        Highcharts.setOptions({{
            chart: {{ style: {{ fontFamily: "'Inter', 'Segoe UI', Helvetica, sans-serif" }} }}
        }});
        Highcharts.chart('container', {chart_json});
    </script>
</body>
</html>"""

# Save interactive HTML version
standalone_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        body {{ margin: 0; font-family: 'Inter', 'Segoe UI', sans-serif; }}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/highcharts@11/highcharts.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/highcharts@11/modules/sankey.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/highcharts@11/modules/dependency-wheel.js"></script>
</head>
<body>
    <div id="container" style="width: 100%; height: 100vh;"></div>
    <script>
        Highcharts.setOptions({{
            chart: {{ style: {{ fontFamily: "'Inter', 'Segoe UI', Helvetica, sans-serif" }} }}
        }});
        Highcharts.chart('container', {chart_json});
    </script>
</body>
</html>"""

with open("plot.html", "w", encoding="utf-8") as f:
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
chrome_options.add_argument("--window-size=3600,3700")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)
driver.save_screenshot("plot_raw.png")
driver.quit()

# Crop to exact dimensions
img = Image.open("plot_raw.png")
img_cropped = img.crop((0, 0, 3600, 3600))
img_cropped.save("plot.png")
Path("plot_raw.png").unlink()

Path(temp_path).unlink()
