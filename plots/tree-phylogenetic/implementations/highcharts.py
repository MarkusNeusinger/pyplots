""" pyplots.ai
tree-phylogenetic: Phylogenetic Tree Diagram
Library: highcharts unknown | Python 3.13.11
Quality: 72/100 | Created: 2025-12-31
"""

import json
import tempfile
import time
import urllib.request
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Primate phylogenetic tree based on mitochondrial DNA
# Node definitions with taxonomic rank information
tree_nodes = [
    # Root node - level 0
    {"id": "Primates", "name": "Primates", "title": "Order", "color": "#306998"},
    # Superfamilies - level 1
    {"id": "Hominoidea", "name": "Hominoidea", "title": "Superfamily", "color": "#306998"},
    {"id": "Cercopithecoidea", "name": "Cercopithecoidea", "title": "Superfamily", "color": "#306998"},
    # Families - level 2
    {"id": "Hominidae", "name": "Hominidae", "title": "Family", "color": "#4A90D9"},
    {"id": "Hylobatidae", "name": "Hylobatidae", "title": "Family", "color": "#4A90D9"},
    {"id": "Cercopithecidae", "name": "Cercopithecidae", "title": "Family", "color": "#4A90D9"},
    # Subfamilies/Tribes - level 3
    {"id": "Hominini", "name": "Hominini", "title": "Tribe", "color": "#6BA3E0"},
    {"id": "Ponginae", "name": "Ponginae", "title": "Subfamily", "color": "#6BA3E0"},
    {"id": "Cercopithecinae", "name": "Cercopithecinae", "title": "Subfamily", "color": "#6BA3E0"},
    {"id": "Colobinae", "name": "Colobinae", "title": "Subfamily", "color": "#6BA3E0"},
    # Species (leaf nodes) - level 4
    {"id": "Homo", "name": "Homo sapiens", "title": "Species", "color": "#FFD43B"},
    {"id": "Pan", "name": "Pan troglodytes", "title": "Species", "color": "#FFD43B"},
    {"id": "Pongo", "name": "Pongo pygmaeus", "title": "Species", "color": "#FFD43B"},
    {"id": "Hylobates", "name": "Hylobates lar", "title": "Species", "color": "#FFD43B"},
    {"id": "Symphalangus", "name": "Symphalangus", "title": "Species", "color": "#FFD43B"},
    {"id": "Macaca", "name": "Macaca mulatta", "title": "Species", "color": "#FFD43B"},
    {"id": "Papio", "name": "Papio anubis", "title": "Species", "color": "#FFD43B"},
    {"id": "Colobus", "name": "Colobus guereza", "title": "Species", "color": "#FFD43B"},
    {"id": "Nasalis", "name": "Nasalis larvatus", "title": "Species", "color": "#FFD43B"},
]

# Edge connections representing evolutionary relationships
tree_edges = [
    # From root to superfamilies
    ["Primates", "Hominoidea"],
    ["Primates", "Cercopithecoidea"],
    # From superfamilies to families
    ["Hominoidea", "Hominidae"],
    ["Hominoidea", "Hylobatidae"],
    ["Cercopithecoidea", "Cercopithecidae"],
    # From families to subfamilies/tribes
    ["Hominidae", "Hominini"],
    ["Hominidae", "Ponginae"],
    ["Cercopithecidae", "Cercopithecinae"],
    ["Cercopithecidae", "Colobinae"],
    # From subfamilies to species
    ["Hominini", "Homo"],
    ["Hominini", "Pan"],
    ["Ponginae", "Pongo"],
    ["Hylobatidae", "Hylobates"],
    ["Hylobatidae", "Symphalangus"],
    ["Cercopithecinae", "Macaca"],
    ["Cercopithecinae", "Papio"],
    ["Colobinae", "Colobus"],
    ["Colobinae", "Nasalis"],
]

# Highcharts configuration using organization chart
chart_config = {
    "chart": {
        "width": 4800,
        "height": 2700,
        "backgroundColor": "#ffffff",
        "inverted": True,
        "marginTop": 120,
        "marginBottom": 80,
        "marginLeft": 80,
        "marginRight": 80,
    },
    "title": {
        "text": "Primate Phylogeny · tree-phylogenetic · highcharts · pyplots.ai",
        "style": {"fontSize": "56px", "fontWeight": "bold"},
    },
    "subtitle": {
        "text": "Evolutionary relationships based on mitochondrial DNA analysis",
        "style": {"fontSize": "36px", "color": "#666666"},
    },
    "credits": {"enabled": False},
    "tooltip": {
        "outside": True,
        "style": {"fontSize": "28px"},
        "pointFormat": "<b>{point.name}</b><br/>Rank: {point.title}",
    },
    "series": [
        {
            "type": "organization",
            "name": "Primate Phylogeny",
            "keys": ["from", "to"],
            "data": tree_edges,
            "nodes": tree_nodes,
            "colorByPoint": False,
            "borderColor": "#ffffff",
            "borderWidth": 4,
            "borderRadius": 8,
            "dataLabels": {
                "enabled": True,
                "color": "#ffffff",
                "style": {"fontSize": "24px", "fontWeight": "bold", "textOutline": "none"},
                "nodeFormat": "{point.name}<br/><span style='font-size:18px;font-weight:normal;opacity:0.8'>{point.title}</span>",
            },
            "link": {"lineWidth": 4, "color": "#306998", "type": "curved"},
            "levels": [
                {"level": 0, "color": "#306998", "dataLabels": {"style": {"fontSize": "32px"}}, "height": 90},
                {"level": 1, "color": "#306998", "dataLabels": {"style": {"fontSize": "28px"}}, "height": 85},
                {"level": 2, "color": "#4A90D9", "dataLabels": {"style": {"fontSize": "26px"}}, "height": 80},
                {"level": 3, "color": "#6BA3E0", "dataLabels": {"style": {"fontSize": "24px"}}, "height": 75},
                {
                    "level": 4,
                    "color": "#FFD43B",
                    "dataLabels": {"style": {"fontSize": "22px", "color": "#333333"}},
                    "height": 70,
                },
            ],
            "nodeWidth": 220,
            "nodePadding": 15,
        }
    ],
}

# Convert config to JSON
config_json = json.dumps(chart_config)

# Download Highcharts JS and required modules
modules = [
    ("highcharts", "https://code.highcharts.com/highcharts.js"),
    ("sankey", "https://code.highcharts.com/modules/sankey.js"),
    ("organization", "https://code.highcharts.com/modules/organization.js"),
]

js_modules = {}
for name, url in modules:
    with urllib.request.urlopen(url, timeout=30) as response:
        js_modules[name] = response.read().decode("utf-8")

# Generate HTML with inline scripts
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{js_modules["highcharts"]}</script>
    <script>{js_modules["sankey"]}</script>
    <script>{js_modules["organization"]}</script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>
        Highcharts.chart('container', {config_json});
    </script>
</body>
</html>"""

# Save HTML file
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Write temp HTML and take screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4800,2800")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(6)

# Get container element and screenshot it
container = driver.find_element("id", "container")
container.screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()
