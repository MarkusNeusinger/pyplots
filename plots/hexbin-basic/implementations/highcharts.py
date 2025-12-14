"""
hexbin-basic: Basic Hexbin Plot
Library: highcharts
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - generate clustered bivariate data (10,000 points)
np.random.seed(42)
n_points = 10000

# Create clustered distribution with 3 centers
centers = [(0, 0), (3, 3), (-2, 4)]
points_per_cluster = n_points // 3

x_data = []
y_data = []

for cx, cy in centers:
    x_data.extend(np.random.randn(points_per_cluster) * 1.2 + cx)
    y_data.extend(np.random.randn(points_per_cluster) * 1.2 + cy)

x = np.array(x_data)
y = np.array(y_data)

# Hexbin computation
gridsize = 25
x_min, x_max = x.min() - 0.5, x.max() + 0.5
y_min, y_max = y.min() - 0.5, y.max() + 0.5

# Hexagon geometry: pointy-top orientation
hex_size = (x_max - x_min) / gridsize / 2
hex_width = hex_size * np.sqrt(3)
hex_height = hex_size * 2
hex_horiz_spacing = hex_width
hex_vert_spacing = hex_height * 0.75

# Compute hexagonal bin centers and counts
hex_bins = {}
for xi, yi in zip(x, y, strict=True):
    row = int((yi - y_min) / hex_vert_spacing)
    col_offset = (row % 2) * hex_width * 0.5
    col = int((xi - x_min - col_offset) / hex_horiz_spacing)
    hx = x_min + col * hex_horiz_spacing + col_offset + hex_width / 2
    hy = y_min + row * hex_vert_spacing + hex_height / 2
    key = (col, row)
    if key not in hex_bins:
        hex_bins[key] = {"x": hx, "y": hy, "count": 0}
    hex_bins[key]["count"] += 1

# Extract bin data
hex_centers_x = [v["x"] for v in hex_bins.values()]
hex_centers_y = [v["y"] for v in hex_bins.values()]
counts = np.array([v["count"] for v in hex_bins.values()])
max_count = counts.max()

# Viridis colorscale
viridis_colors = [(0.0, "#440154"), (0.25, "#3b528b"), (0.5, "#21918c"), (0.75, "#5ec962"), (1.0, "#fde725")]


def get_viridis_color(val):
    """Interpolate viridis color for value 0-1."""
    for i in range(len(viridis_colors) - 1):
        v1, c1 = viridis_colors[i]
        v2, c2 = viridis_colors[i + 1]
        if v1 <= val <= v2:
            t = (val - v1) / (v2 - v1)
            r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
            r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
            r = int(r1 + t * (r2 - r1))
            g = int(g1 + t * (g2 - g1))
            b = int(b1 + t * (b2 - b1))
            return f"#{r:02x}{g:02x}{b:02x}"
    return "#fde725"


def hexagon_vertices(cx, cy, size):
    """Pointy-top hexagon vertices."""
    angles = np.array([30, 90, 150, 210, 270, 330]) * np.pi / 180
    vx = cx + size * np.cos(angles)
    vy = cy + size * np.sin(angles)
    return list(zip(vx, vy, strict=True))


# Download Highcharts JS for inline embedding
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# Download highcharts-more for polygon support
highcharts_more_url = "https://code.highcharts.com/highcharts-more.js"
with urllib.request.urlopen(highcharts_more_url, timeout=30) as response:
    highcharts_more_js = response.read().decode("utf-8")

# Build series data - each hexagon as a separate polygon series
series_js_parts = []
for hx, hy, count in zip(hex_centers_x, hex_centers_y, counts, strict=True):
    norm_count = count / max_count
    color = get_viridis_color(norm_count)
    vertices = hexagon_vertices(hx, hy, hex_size * 1.02)
    coords_str = ", ".join([f"[{vx:.4f}, {vy:.4f}]" for vx, vy in vertices])
    series_js_parts.append(
        f'{{type: "polygon", data: [{coords_str}], color: "{color}", enableMouseTracking: false, animation: false}}'
    )

series_js = "[" + ", ".join(series_js_parts) + "]"

# Create custom HTML with Highcharts
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{highcharts_more_js}</script>
    <style>
        body {{ margin: 0; padding: 0; background: #ffffff; }}
        #container {{ width: 4800px; height: 2700px; }}
        .colorbar-wrapper {{
            position: absolute;
            right: 60px;
            top: 350px;
            display: flex;
            flex-direction: row;
            font-family: Arial, sans-serif;
        }}
        .colorbar {{
            width: 40px;
            height: 800px;
            background: linear-gradient(to bottom, #fde725, #5ec962, #21918c, #3b528b, #440154);
            border: 1px solid #333;
        }}
        .colorbar-labels {{
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            margin-left: 12px;
            font-size: 24px;
            height: 800px;
        }}
        .colorbar-title {{
            position: absolute;
            right: 45px;
            top: 290px;
            font-size: 32px;
            font-family: Arial, sans-serif;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div id="container"></div>
    <div class="colorbar-title">Count</div>
    <div class="colorbar-wrapper">
        <div class="colorbar"></div>
        <div class="colorbar-labels">
            <span>{int(max_count)}</span>
            <span>{int(max_count // 2)}</span>
            <span>0</span>
        </div>
    </div>
    <script>
        Highcharts.chart('container', {{
            chart: {{
                width: 4800,
                height: 2700,
                backgroundColor: '#ffffff',
                marginRight: 250,
                marginBottom: 250,
                marginLeft: 150,
                marginTop: 120,
                animation: false
            }},
            title: {{
                text: 'hexbin-basic \\u00b7 highcharts \\u00b7 pyplots.ai',
                style: {{ fontSize: '48px' }}
            }},
            xAxis: {{
                title: {{
                    text: 'X Value',
                    style: {{ fontSize: '32px' }},
                    margin: 20
                }},
                labels: {{
                    style: {{ fontSize: '24px' }},
                    y: 35
                }},
                gridLineWidth: 1,
                gridLineColor: 'rgba(128, 128, 128, 0.3)',
                lineWidth: 2,
                tickWidth: 2,
                tickLength: 10,
                min: {x_min:.2f},
                max: {x_max:.2f}
            }},
            yAxis: {{
                title: {{
                    text: 'Y Value',
                    style: {{ fontSize: '32px' }}
                }},
                labels: {{
                    style: {{ fontSize: '24px' }}
                }},
                gridLineWidth: 1,
                gridLineColor: 'rgba(128, 128, 128, 0.3)',
                lineWidth: 2,
                min: {y_min:.2f},
                max: {y_max:.2f}
            }},
            legend: {{
                enabled: false
            }},
            credits: {{
                enabled: false
            }},
            tooltip: {{
                enabled: false
            }},
            plotOptions: {{
                polygon: {{
                    animation: false,
                    lineWidth: 0,
                    states: {{
                        hover: {{ enabled: false }},
                        inactive: {{ enabled: false }}
                    }}
                }}
            }},
            series: {series_js}
        }});
    </script>
</body>
</html>"""

# Write temp HTML
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Save interactive HTML
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Take screenshot with headless Chrome
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

Path(temp_path).unlink()
