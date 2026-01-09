""" pyplots.ai
heatmap-interactive: Interactive Heatmap with Hover and Zoom
Library: highcharts unknown | Python 3.13.11
Quality: 92/100 | Created: 2026-01-09
"""

import json
import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Monthly website page views by category (20 categories x 12 months)
np.random.seed(42)

categories = [
    "Homepage",
    "Products",
    "Services",
    "About Us",
    "Contact",
    "Blog",
    "FAQ",
    "Support",
    "Pricing",
    "Careers",
    "News",
    "Events",
    "Resources",
    "Docs",
    "Tutorials",
    "API",
    "Downloads",
    "Partners",
    "Investors",
    "Legal",
]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Generate realistic page view data (thousands of views)
base_views = np.random.randint(10, 100, size=(len(categories), len(months)))
seasonal = np.sin(np.linspace(0, 2 * np.pi, 12)) * 20 + 50
values = base_views + seasonal.astype(int)
values = np.clip(values, 5, 150)

# Convert to Highcharts heatmap data format: [x, y, value]
heatmap_data = []
for y_idx in range(len(categories)):
    for x_idx in range(len(months)):
        heatmap_data.append([x_idx, y_idx, int(values[y_idx, x_idx])])

# Canvas dimensions
WIDTH = 4800
HEIGHT = 2700

# Download Highcharts JS and heatmap module
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

heatmap_url = "https://code.highcharts.com/modules/heatmap.js"
with urllib.request.urlopen(heatmap_url, timeout=30) as response:
    heatmap_js = response.read().decode("utf-8")

# Create HTML with Highcharts configuration
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{heatmap_js}</script>
</head>
<body style="margin:0; padding:0; background:#ffffff;">
    <div id="container" style="width: {WIDTH}px; height: {HEIGHT}px;"></div>
    <script>
    document.addEventListener('DOMContentLoaded', function() {{
        Highcharts.chart('container', {{
            chart: {{
                type: 'heatmap',
                width: {WIDTH},
                height: {HEIGHT},
                backgroundColor: '#ffffff',
                marginTop: 120,
                marginBottom: 180,
                marginRight: 200,
                marginLeft: 280,
                zoomType: 'xy',
                panning: {{ enabled: true, type: 'xy' }},
                panKey: 'shift',
                resetZoomButton: {{
                    position: {{ align: 'right', verticalAlign: 'top', x: -30, y: 20 }},
                    theme: {{
                        style: {{ fontSize: '24px' }},
                        padding: 12,
                        r: 6
                    }}
                }}
            }},
            title: {{
                text: 'heatmap-interactive · highcharts · pyplots.ai',
                style: {{ fontSize: '48px', fontWeight: 'bold', color: '#333333' }}
            }},
            subtitle: {{
                text: 'Website Page Views by Category and Month (thousands) — Click and drag to zoom, Shift+drag to pan',
                style: {{ fontSize: '28px', color: '#666666' }}
            }},
            xAxis: {{
                categories: {json.dumps(months)},
                title: {{
                    text: 'Month',
                    style: {{ fontSize: '36px', fontWeight: 'bold', color: '#333333' }}
                }},
                labels: {{ style: {{ fontSize: '28px', color: '#333333' }} }},
                gridLineWidth: 1,
                gridLineColor: '#e0e0e0',
                tickLength: 0
            }},
            yAxis: {{
                categories: {json.dumps(categories)},
                title: {{
                    text: 'Page Category',
                    style: {{ fontSize: '36px', fontWeight: 'bold', color: '#333333' }}
                }},
                labels: {{ style: {{ fontSize: '26px', color: '#333333' }} }},
                reversed: true,
                gridLineWidth: 1,
                gridLineColor: '#e0e0e0'
            }},
            colorAxis: {{
                min: 5,
                max: 150,
                stops: [
                    [0, '#f7fbff'],
                    [0.2, '#FFD43B'],
                    [0.5, '#fd8d3c'],
                    [0.75, '#306998'],
                    [1, '#1a3a5c']
                ],
                labels: {{ style: {{ fontSize: '24px', color: '#333333' }} }}
            }},
            legend: {{
                align: 'right',
                layout: 'vertical',
                verticalAlign: 'middle',
                symbolHeight: 500,
                symbolWidth: 40,
                itemStyle: {{ fontSize: '24px', color: '#333333' }},
                title: {{
                    text: 'Views (K)',
                    style: {{ fontSize: '28px', fontWeight: 'bold', color: '#333333' }}
                }}
            }},
            tooltip: {{
                enabled: true,
                useHTML: true,
                formatter: function() {{
                    return '<div style="font-size: 28px; padding: 16px; line-height: 1.6;">' +
                        '<b style="color: #306998;">Category:</b> ' + this.series.yAxis.categories[this.point.y] + '<br/>' +
                        '<b style="color: #306998;">Month:</b> ' + this.series.xAxis.categories[this.point.x] + '<br/>' +
                        '<b style="color: #306998;">Views:</b> ' + this.point.value + 'K</div>';
                }}
            }},
            plotOptions: {{
                heatmap: {{
                    borderWidth: 3,
                    borderColor: '#ffffff',
                    dataLabels: {{ enabled: false }},
                    states: {{
                        hover: {{
                            brightness: 0.15,
                            borderWidth: 6,
                            borderColor: '#000000'
                        }}
                    }}
                }},
                series: {{
                    cursor: 'crosshair',
                    stickyTracking: true
                }}
            }},
            series: [{{
                type: 'heatmap',
                name: 'Page Views',
                data: {json.dumps(heatmap_data)},
                borderWidth: 3,
                borderColor: '#ffffff',
                nullColor: '#e0e0e0'
            }}],
            credits: {{ enabled: false }}
        }});
    }});
    </script>
</body>
</html>"""

# Write temp HTML and take screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Save HTML for interactive viewing
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument(f"--window-size={WIDTH},{HEIGHT + 200}")
chrome_options.add_argument("--force-device-scale-factor=1")
chrome_options.add_argument("--hide-scrollbars")

driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(WIDTH, HEIGHT + 200)
driver.get(f"file://{temp_path}")
time.sleep(5)

# Find the container element and take a screenshot of just that element
container = driver.find_element("id", "container")
container.screenshot("plot.png")
driver.quit()

# Clean up temp file
Path(temp_path).unlink()
