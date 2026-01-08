"""pyplots.ai
heatmap-interactive: Interactive Heatmap with Hover and Zoom
Library: highcharts | Python 3.13
Quality: pending | Created: 2026-01-08
"""

import json
import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Monthly website page views by category (20 categories x 12 months)
np.random.seed(42)

categories = [
    "Homepage",
    "Products",
    "Services",
    "About",
    "Contact",
    "Blog",
    "FAQ",
    "Support",
    "Pricing",
    "Careers",
    "News",
    "Events",
    "Resources",
    "Documentation",
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

# Render at 2400x1350 and scale up to 4800x2700 for better Chrome compatibility
RENDER_WIDTH = 2400
RENDER_HEIGHT = 1350
OUTPUT_WIDTH = 4800
OUTPUT_HEIGHT = 2700

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
<body style="margin:0;">
    <div id="container" style="width: {RENDER_WIDTH}px; height: {RENDER_HEIGHT}px;"></div>
    <script>
    document.addEventListener('DOMContentLoaded', function() {{
        Highcharts.chart('container', {{
            chart: {{
                type: 'heatmap',
                width: {RENDER_WIDTH},
                height: {RENDER_HEIGHT},
                backgroundColor: '#ffffff',
                marginBottom: 90,
                marginRight: 100,
                marginLeft: 140,
                zoomType: 'xy',
                panning: {{ enabled: true, type: 'xy' }},
                panKey: 'shift',
                resetZoomButton: {{
                    position: {{ align: 'right', verticalAlign: 'top', x: -10, y: 10 }},
                    theme: {{ style: {{ fontSize: '14px' }} }}
                }}
            }},
            title: {{
                text: 'heatmap-interactive · highcharts · pyplots.ai',
                style: {{ fontSize: '24px', fontWeight: 'bold' }}
            }},
            subtitle: {{
                text: 'Website Page Views by Category and Month (thousands) - Click and drag to zoom, Shift+drag to pan',
                style: {{ fontSize: '14px', color: '#666666' }}
            }},
            xAxis: {{
                categories: {json.dumps(months)},
                title: {{ text: 'Month', style: {{ fontSize: '16px' }} }},
                labels: {{ style: {{ fontSize: '12px' }} }},
                gridLineWidth: 1,
                gridLineColor: '#e0e0e0'
            }},
            yAxis: {{
                categories: {json.dumps(categories)},
                title: {{ text: 'Page Category', style: {{ fontSize: '16px' }} }},
                labels: {{ style: {{ fontSize: '11px' }} }},
                reversed: true,
                gridLineWidth: 1,
                gridLineColor: '#e0e0e0'
            }},
            colorAxis: {{
                min: 5,
                max: 150,
                stops: [
                    [0, '#ffffff'],
                    [0.25, '#FFD43B'],
                    [0.5, '#FFA500'],
                    [0.75, '#306998'],
                    [1, '#1a3a5c']
                ],
                labels: {{ style: {{ fontSize: '11px' }} }}
            }},
            legend: {{
                align: 'right',
                layout: 'vertical',
                verticalAlign: 'middle',
                symbolHeight: 250,
                symbolWidth: 20,
                itemStyle: {{ fontSize: '11px' }},
                title: {{
                    text: 'Page Views (K)',
                    style: {{ fontSize: '12px', fontWeight: 'bold' }}
                }}
            }},
            tooltip: {{
                enabled: true,
                useHTML: true,
                formatter: function() {{
                    return '<div style="font-size: 14px; padding: 8px;">' +
                        '<b>Category:</b> ' + this.series.yAxis.categories[this.point.y] + '<br/>' +
                        '<b>Month:</b> ' + this.series.xAxis.categories[this.point.x] + '<br/>' +
                        '<b>Views:</b> ' + this.point.value + 'K</div>';
                }},
                style: {{ fontSize: '12px' }}
            }},
            plotOptions: {{
                heatmap: {{
                    borderWidth: 2,
                    borderColor: '#ffffff',
                    dataLabels: {{ enabled: false }},
                    states: {{
                        hover: {{
                            brightness: 0.1,
                            borderWidth: 4,
                            borderColor: '#000000'
                        }}
                    }}
                }},
                series: {{
                    cursor: 'pointer',
                    stickyTracking: true
                }}
            }},
            series: [{{
                type: 'heatmap',
                name: 'Page Views',
                data: {json.dumps(heatmap_data)},
                borderWidth: 2,
                borderColor: '#ffffff',
                nullColor: '#e0e0e0'
            }}]
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
chrome_options.add_argument(f"--window-size={RENDER_WIDTH + 100},{RENDER_HEIGHT + 100}")
chrome_options.add_argument("--force-device-scale-factor=1")

driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(RENDER_WIDTH + 100, RENDER_HEIGHT + 100)
driver.get(f"file://{temp_path}")
time.sleep(5)

# Take screenshot at render size
driver.save_screenshot("plot_temp.png")
driver.quit()

# Resize to output dimensions using high-quality resampling
img = Image.open("plot_temp.png")
# Crop to exact chart dimensions, leaving out any browser chrome
crop_height = min(RENDER_HEIGHT, img.height)
img = img.crop((0, 0, RENDER_WIDTH, crop_height))
# Create white canvas at target size and paste the cropped image
canvas = Image.new("RGB", (RENDER_WIDTH, RENDER_HEIGHT), (255, 255, 255))
canvas.paste(img, (0, 0))
# Resize to output size with high-quality resampling
img_resized = canvas.resize((OUTPUT_WIDTH, OUTPUT_HEIGHT), Image.Resampling.LANCZOS)
img_resized.save("plot.png", "PNG")

# Clean up temp files
Path("plot_temp.png").unlink()
Path(temp_path).unlink()
