"""
arc-basic: Basic Arc Diagram
Library: highcharts
"""

import json
import tempfile
import time
import urllib.request
from pathlib import Path

from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data: Character interactions in a story chapter
nodes = ["Alice", "Bob", "Carol", "David", "Eve", "Frank", "Grace", "Henry", "Iris", "Jack"]
n_nodes = len(nodes)

# Edges: pairs of connected nodes with weights (source, target, weight)
edges = [
    (0, 1, 3),  # Alice-Bob (strong connection)
    (0, 3, 2),  # Alice-David
    (1, 2, 2),  # Bob-Carol
    (2, 4, 1),  # Carol-Eve
    (3, 5, 2),  # David-Frank
    (4, 6, 1),  # Eve-Grace
    (0, 7, 1),  # Alice-Henry (long-range)
    (1, 5, 2),  # Bob-Frank
    (2, 3, 3),  # Carol-David (strong)
    (5, 8, 1),  # Frank-Iris
    (6, 9, 2),  # Grace-Jack
    (0, 9, 1),  # Alice-Jack (longest range)
    (3, 7, 2),  # David-Henry
    (7, 8, 1),  # Henry-Iris
    (8, 9, 2),  # Iris-Jack
]

# Colors
arc_color = "#306998"  # Python Blue
node_color = "#FFD43B"  # Python Yellow

# Chart dimensions
width = 4800
height = 2700

# Calculate positions
margin_left = 400
margin_right = 400
usable_width = width - margin_left - margin_right
node_spacing = usable_width / (n_nodes - 1)
baseline_y = height * 0.80  # Position nodes lower to make room for arcs above

# Create node positions
node_positions = []
for i in range(n_nodes):
    x = margin_left + i * node_spacing
    node_positions.append({"x": x, "y": baseline_y})

# Create arcs data for JS
arcs_data = []
for start, end, weight in edges:
    x_start = node_positions[start]["x"]
    x_end = node_positions[end]["x"]
    x_center = (x_start + x_end) / 2
    arc_width = abs(x_end - x_start)

    # Arc height proportional to distance
    distance = abs(end - start)
    arc_height = 100 * distance  # Scale for 4800x2700 canvas

    # Line width based on weight (scaled for 4800x2700)
    line_width = 4 + weight * 3

    arcs_data.append(
        {"xCenter": x_center, "yBase": baseline_y, "width": arc_width, "height": arc_height, "lineWidth": line_width}
    )

# Create nodes data for JS
nodes_data = []
for i, name in enumerate(nodes):
    nodes_data.append({"x": node_positions[i]["x"], "y": baseline_y, "name": name})

# Download Highcharts JS
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# Build the custom drawing script
draw_script = f"""
(function() {{
    var container = document.getElementById('container');
    var chart = Highcharts.chart('container', {{
        chart: {{
            width: {width},
            height: {height},
            backgroundColor: '#ffffff',
            events: {{
                load: function() {{
                    var renderer = this.renderer;
                    var arcs = {json.dumps(arcs_data)};
                    var nodes = {json.dumps(nodes_data)};
                    var arcColor = '{arc_color}';
                    var nodeColor = '{node_color}';

                    // Draw arcs above the baseline
                    arcs.forEach(function(arc) {{
                        var rx = arc.width / 2;
                        var ry = arc.height;
                        var startX = arc.xCenter - rx;
                        var endX = arc.xCenter + rx;
                        var y = arc.yBase;

                        // SVG arc path: sweep-flag=1 draws arc above (counterclockwise)
                        var path = [
                            'M', startX, y,
                            'A', rx, ry, 0, 0, 1, endX, y
                        ];

                        renderer.path(path)
                            .attr({{
                                'stroke': arcColor,
                                'stroke-width': arc.lineWidth,
                                'fill': 'none',
                                'stroke-opacity': 0.6
                            }})
                            .add();
                    }});

                    // Draw nodes
                    nodes.forEach(function(node) {{
                        renderer.circle(node.x, node.y, 35)
                            .attr({{
                                fill: nodeColor,
                                stroke: arcColor,
                                'stroke-width': 5
                            }})
                            .add();

                        renderer.text(node.name, node.x, node.y + 80)
                            .attr({{
                                align: 'center',
                                rotation: 0
                            }})
                            .css({{
                                fontSize: '36px',
                                fontWeight: 'bold',
                                color: arcColor
                            }})
                            .add();
                    }});
                }}
            }}
        }},
        title: {{
            text: 'Character Interactions · arc-basic · highcharts · pyplots.ai',
            style: {{
                fontSize: '48px',
                fontWeight: 'bold'
            }}
        }},
        credits: {{
            enabled: false
        }}
    }});
}})();
"""

# Generate HTML with inline scripts
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
</head>
<body style="margin:0;">
    <div id="container" style="width: {width}px; height: {height}px;"></div>
    <script>{draw_script}</script>
</body>
</html>"""

# Save HTML for interactive version
standalone_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://code.highcharts.com/highcharts.js"></script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 100%; height: 100vh;"></div>
    <script>{draw_script}</script>
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
