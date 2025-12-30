"""pyplots.ai
network-directed: Directed Network Graph
Library: highcharts | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import tempfile
import time
import urllib.request
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Software module dependencies showing import direction
nodes = [
    {"id": "main", "name": "main"},
    {"id": "api", "name": "api"},
    {"id": "auth", "name": "auth"},
    {"id": "database", "name": "database"},
    {"id": "models", "name": "models"},
    {"id": "utils", "name": "utils"},
    {"id": "config", "name": "config"},
    {"id": "cache", "name": "cache"},
    {"id": "logging", "name": "logging"},
    {"id": "validation", "name": "validation"},
    {"id": "routes", "name": "routes"},
    {"id": "middleware", "name": "middleware"},
]

# Directed edges (source -> target) showing import dependencies
edges = [
    ("main", "api"),
    ("main", "config"),
    ("main", "logging"),
    ("api", "routes"),
    ("api", "middleware"),
    ("routes", "auth"),
    ("routes", "database"),
    ("routes", "models"),
    ("routes", "validation"),
    ("middleware", "auth"),
    ("middleware", "logging"),
    ("auth", "database"),
    ("auth", "cache"),
    ("auth", "utils"),
    ("database", "models"),
    ("database", "config"),
    ("database", "logging"),
    ("models", "validation"),
    ("cache", "config"),
    ("cache", "logging"),
    ("utils", "config"),
    ("validation", "utils"),
]

# Format data for Highcharts networkgraph
nodes_data = [{"id": n["id"], "name": n["name"]} for n in nodes]
links_data = [{"from": src, "to": tgt} for src, tgt in edges]

# Download Highcharts JS files
highcharts_url = "https://code.highcharts.com/highcharts.js"
networkgraph_url = "https://code.highcharts.com/modules/networkgraph.js"

with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

with urllib.request.urlopen(networkgraph_url, timeout=30) as response:
    networkgraph_js = response.read().decode("utf-8")

# Build the chart configuration directly as JavaScript
# Using force-directed layout for network visualization
nodes_json = str(nodes_data).replace("'", '"')
links_json = str(links_data).replace("'", '"')

chart_js = f"""
Highcharts.chart('container', {{
    chart: {{
        type: 'networkgraph',
        width: 4800,
        height: 2700,
        backgroundColor: '#ffffff'
    }},
    title: {{
        text: 'network-directed · highcharts · pyplots.ai',
        style: {{
            fontSize: '48px',
            fontWeight: 'bold'
        }}
    }},
    subtitle: {{
        text: 'Software Module Dependencies',
        style: {{
            fontSize: '32px'
        }}
    }},
    plotOptions: {{
        networkgraph: {{
            layoutAlgorithm: {{
                enableSimulation: true,
                friction: -0.95,
                gravitationalConstant: 0.08,
                initialPositions: 'circle',
                linkLength: 350
            }},
            link: {{
                width: 3,
                color: '#306998'
            }},
            dataLabels: {{
                enabled: true,
                linkFormat: '',
                style: {{
                    fontSize: '28px',
                    fontWeight: 'normal',
                    textOutline: '3px white'
                }},
                y: 0
            }}
        }}
    }},
    series: [{{
        type: 'networkgraph',
        draggable: false,
        marker: {{
            radius: 45
        }},
        dataLabels: {{
            enabled: true,
            style: {{
                fontSize: '28px',
                fontWeight: 'normal',
                textOutline: '3px white'
            }}
        }},
        nodes: {nodes_json},
        data: {links_json},
        color: '#FFD43B'
    }}]
}});
"""

# Create HTML with inline scripts and SVG arrow marker
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{networkgraph_js}</script>
    <style>
        body {{ margin: 0; padding: 0; }}
        #container {{ width: 4800px; height: 2700px; }}
    </style>
</head>
<body>
    <!-- Define arrow marker in SVG for directed edges -->
    <svg style="position:absolute;width:0;height:0">
        <defs>
            <marker id="arrowhead" markerWidth="30" markerHeight="30"
                    refX="28" refY="15" orient="auto" markerUnits="userSpaceOnUse">
                <path d="M0,0 L0,30 L30,15 Z" fill="#306998"/>
            </marker>
        </defs>
    </svg>
    <div id="container"></div>
    <script>
        // After chart renders, add arrows to all network links
        function addArrowsToLinks() {{
            var svg = document.querySelector('#container svg');
            if (!svg) return;

            // Find all path elements that are links (not nodes)
            var paths = svg.querySelectorAll('path.highcharts-link');
            paths.forEach(function(path) {{
                path.setAttribute('marker-end', 'url(#arrowhead)');
            }});

            // Also try finding links by stroke color (fallback)
            var allPaths = svg.querySelectorAll('path');
            allPaths.forEach(function(path) {{
                var stroke = path.getAttribute('stroke');
                // Links have stroke but no fill (or transparent fill)
                var fill = path.getAttribute('fill');
                if (stroke && stroke === '#306998' && (!fill || fill === 'none' || fill === 'transparent')) {{
                    path.setAttribute('marker-end', 'url(#arrowhead)');
                }}
            }});
        }}

        // Run after chart initializes
        setTimeout(addArrowsToLinks, 1000);
        setTimeout(addArrowsToLinks, 2000);
        setTimeout(addArrowsToLinks, 3000);

        {chart_js}
    </script>
</body>
</html>"""

# Write temp HTML file
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Setup headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4800,2700")

# Take screenshot
driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)  # Wait for chart to render and simulation to settle
driver.save_screenshot("plot.png")
driver.quit()

# Also save the interactive HTML version
Path("plot.html").write_text(html_content, encoding="utf-8")

# Clean up temp file
Path(temp_path).unlink()
