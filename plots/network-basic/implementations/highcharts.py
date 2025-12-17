"""
network-basic: Basic Network Graph
Library: highcharts
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


# Data - Small social network with 20 people and friendship connections
# Nodes represent people with group membership (e.g., work, hobby, family)
nodes = [
    # Work colleagues (Group 1 - Python Blue)
    {"id": "Alice", "group": 1},
    {"id": "Bob", "group": 1},
    {"id": "Carol", "group": 1},
    {"id": "David", "group": 1},
    {"id": "Eve", "group": 1},
    # Sports club (Group 2 - Python Yellow)
    {"id": "Frank", "group": 2},
    {"id": "Grace", "group": 2},
    {"id": "Henry", "group": 2},
    {"id": "Ivy", "group": 2},
    {"id": "Jack", "group": 2},
    # Book club (Group 3 - Purple)
    {"id": "Karen", "group": 3},
    {"id": "Leo", "group": 3},
    {"id": "Mia", "group": 3},
    {"id": "Nick", "group": 3},
    # Family (Group 4 - Cyan)
    {"id": "Olivia", "group": 4},
    {"id": "Paul", "group": 4},
    {"id": "Quinn", "group": 4},
    {"id": "Rachel", "group": 4},
    {"id": "Sam", "group": 4},
    {"id": "Tina", "group": 4},
]

# Edges - connections between people (friendships)
# Includes within-group and cross-group connections
edges = [
    # Work colleague connections
    ("Alice", "Bob"),
    ("Alice", "Carol"),
    ("Bob", "Carol"),
    ("Bob", "David"),
    ("Carol", "David"),
    ("David", "Eve"),
    ("Alice", "Eve"),
    # Sports club connections
    ("Frank", "Grace"),
    ("Frank", "Henry"),
    ("Grace", "Henry"),
    ("Grace", "Ivy"),
    ("Henry", "Jack"),
    ("Ivy", "Jack"),
    # Book club connections
    ("Karen", "Leo"),
    ("Karen", "Mia"),
    ("Leo", "Mia"),
    ("Leo", "Nick"),
    ("Mia", "Nick"),
    # Family connections
    ("Olivia", "Paul"),
    ("Olivia", "Quinn"),
    ("Paul", "Quinn"),
    ("Paul", "Rachel"),
    ("Quinn", "Sam"),
    ("Rachel", "Sam"),
    ("Rachel", "Tina"),
    ("Sam", "Tina"),
    ("Olivia", "Tina"),
    # Cross-group connections (bridges between communities)
    ("Alice", "Frank"),  # Work-Sports
    ("Bob", "Karen"),  # Work-Book club
    ("Carol", "Olivia"),  # Work-Family
    ("Grace", "Leo"),  # Sports-Book club
    ("Henry", "Paul"),  # Sports-Family
    ("Mia", "Rachel"),  # Book club-Family
    ("Eve", "Ivy"),  # Work-Sports
    ("Jack", "Nick"),  # Sports-Book club
]

# Colorblind-safe colors for groups
group_colors = {
    1: "#306998",  # Python Blue - Work
    2: "#FFD43B",  # Python Yellow - Sports
    3: "#9467BD",  # Purple - Book club
    4: "#17BECF",  # Cyan - Family
}

group_names = {1: "Work", 2: "Sports", 3: "Book Club", 4: "Family"}

# Create nodes data with marker colors based on group
nodes_data = []
for node in nodes:
    nodes_data.append({"id": node["id"], "color": group_colors[node["group"]], "marker": {"radius": 45}})

# Create links data
links_data = [{"from": source, "to": target} for source, target in edges]

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {"type": "networkgraph", "width": 4800, "height": 2700, "backgroundColor": "#ffffff"}

# Title
chart.options.title = {
    "text": "Social Network · network-basic · highcharts · pyplots.ai",
    "style": {"fontSize": "64px", "fontWeight": "bold"},
}

# Subtitle
chart.options.subtitle = {"text": "Friendship connections across four communities", "style": {"fontSize": "36px"}}

# Tooltip
chart.options.tooltip = {"style": {"fontSize": "28px"}}

# Plot options for network graph
chart.options.plot_options = {
    "networkgraph": {
        "keys": ["from", "to"],
        "layoutAlgorithm": {
            "enableSimulation": True,
            "friction": -0.9,
            "linkLength": 400,
            "gravitationalConstant": 0.1,
            "integration": "verlet",
            "approximation": "none",
            "initialPositions": "circle",
        },
        "link": {"color": "#AAAAAA", "width": 3},
        "dataLabels": {
            "enabled": True,
            "linkFormat": "",
            "format": "{point.id}",
            "style": {"fontSize": "32px", "fontWeight": "normal", "textOutline": "3px white"},
        },
    }
}

# Network series configuration
series_config = {
    "type": "networkgraph",
    "name": "Friendships",
    "nodes": nodes_data,
    "data": links_data,
    "marker": {"radius": 45},
}

chart.options.series = [series_config]

# Disable legend (networkgraph doesn't support legend for node colors)
chart.options.legend = {"enabled": False}

# Disable credits
chart.options.credits = {"enabled": False}

# Download Highcharts JS and networkgraph module
highcharts_url = "https://code.highcharts.com/highcharts.js"
networkgraph_url = "https://code.highcharts.com/modules/networkgraph.js"

with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

with urllib.request.urlopen(networkgraph_url, timeout=30) as response:
    networkgraph_js = response.read().decode("utf-8")

# Generate JS literal and manually ensure node colors are in the output
html_str = chart.to_js_literal()

# Build the HTML with inline scripts
# Add custom JS to apply node colors after chart renders
custom_js = """
Highcharts.chart('container', {
    chart: {
        type: 'networkgraph',
        width: 4800,
        height: 2700,
        backgroundColor: '#ffffff'
    },
    title: {
        text: 'Social Network · network-basic · highcharts · pyplots.ai',
        style: { fontSize: '64px', fontWeight: 'bold' }
    },
    subtitle: {
        text: 'Friendship connections across four communities',
        style: { fontSize: '36px' }
    },
    tooltip: {
        style: { fontSize: '28px' }
    },
    credits: { enabled: false },
    legend: { enabled: false },
    plotOptions: {
        networkgraph: {
            keys: ['from', 'to'],
            layoutAlgorithm: {
                enableSimulation: true,
                friction: -0.9,
                linkLength: 400,
                gravitationalConstant: 0.1,
                integration: 'verlet',
                approximation: 'none',
                initialPositions: 'circle'
            },
            link: {
                color: '#AAAAAA',
                width: 3
            },
            dataLabels: {
                enabled: true,
                linkFormat: '',
                format: '{point.id}',
                style: {
                    fontSize: '32px',
                    fontWeight: 'normal',
                    textOutline: '3px white'
                }
            }
        }
    },
    series: [{
        type: 'networkgraph',
        name: 'Friendships',
        marker: { radius: 45 },
        nodes: [
            { id: 'Alice', color: '#306998', marker: { radius: 45 } },
            { id: 'Bob', color: '#306998', marker: { radius: 45 } },
            { id: 'Carol', color: '#306998', marker: { radius: 45 } },
            { id: 'David', color: '#306998', marker: { radius: 45 } },
            { id: 'Eve', color: '#306998', marker: { radius: 45 } },
            { id: 'Frank', color: '#FFD43B', marker: { radius: 45 } },
            { id: 'Grace', color: '#FFD43B', marker: { radius: 45 } },
            { id: 'Henry', color: '#FFD43B', marker: { radius: 45 } },
            { id: 'Ivy', color: '#FFD43B', marker: { radius: 45 } },
            { id: 'Jack', color: '#FFD43B', marker: { radius: 45 } },
            { id: 'Karen', color: '#9467BD', marker: { radius: 45 } },
            { id: 'Leo', color: '#9467BD', marker: { radius: 45 } },
            { id: 'Mia', color: '#9467BD', marker: { radius: 45 } },
            { id: 'Nick', color: '#9467BD', marker: { radius: 45 } },
            { id: 'Olivia', color: '#17BECF', marker: { radius: 45 } },
            { id: 'Paul', color: '#17BECF', marker: { radius: 45 } },
            { id: 'Quinn', color: '#17BECF', marker: { radius: 45 } },
            { id: 'Rachel', color: '#17BECF', marker: { radius: 45 } },
            { id: 'Sam', color: '#17BECF', marker: { radius: 45 } },
            { id: 'Tina', color: '#17BECF', marker: { radius: 45 } }
        ],
        data: [
            ['Alice', 'Bob'], ['Alice', 'Carol'], ['Bob', 'Carol'],
            ['Bob', 'David'], ['Carol', 'David'], ['David', 'Eve'],
            ['Alice', 'Eve'], ['Frank', 'Grace'], ['Frank', 'Henry'],
            ['Grace', 'Henry'], ['Grace', 'Ivy'], ['Henry', 'Jack'],
            ['Ivy', 'Jack'], ['Karen', 'Leo'], ['Karen', 'Mia'],
            ['Leo', 'Mia'], ['Leo', 'Nick'], ['Mia', 'Nick'],
            ['Olivia', 'Paul'], ['Olivia', 'Quinn'], ['Paul', 'Quinn'],
            ['Paul', 'Rachel'], ['Quinn', 'Sam'], ['Rachel', 'Sam'],
            ['Rachel', 'Tina'], ['Sam', 'Tina'], ['Olivia', 'Tina'],
            ['Alice', 'Frank'], ['Bob', 'Karen'], ['Carol', 'Olivia'],
            ['Grace', 'Leo'], ['Henry', 'Paul'], ['Mia', 'Rachel'],
            ['Eve', 'Ivy'], ['Jack', 'Nick']
        ]
    }]
});
"""

html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{networkgraph_js}</script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>{custom_js}</script>
</body>
</html>"""

# Save HTML for interactive version (use CDN for standalone)
standalone_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/modules/networkgraph.js"></script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 100%; height: 100vh;"></div>
    <script>{custom_js}</script>
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
