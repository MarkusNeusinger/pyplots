""" pyplots.ai
heatmap-correlation: Correlation Matrix Heatmap
Library: highcharts unknown | Python 3.13.11
Quality: 88/100 | Created: 2025-12-25
"""

import json
import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Financial metrics correlation matrix
np.random.seed(42)
variables = ["Revenue", "Profit", "Expenses", "Growth", "ROI", "Debt", "Assets"]
n_vars = len(variables)

# Create realistic correlation matrix
base_corr = np.array(
    [
        [1.00, 0.85, 0.72, 0.45, 0.68, -0.32, 0.78],  # Revenue
        [0.85, 1.00, 0.35, 0.52, 0.89, -0.45, 0.62],  # Profit
        [0.72, 0.35, 1.00, 0.15, -0.28, 0.55, 0.48],  # Expenses
        [0.45, 0.52, 0.15, 1.00, 0.72, -0.18, 0.25],  # Growth
        [0.68, 0.89, -0.28, 0.72, 1.00, -0.58, 0.42],  # ROI
        [-0.32, -0.45, 0.55, -0.18, -0.58, 1.00, -0.22],  # Debt
        [0.78, 0.62, 0.48, 0.25, 0.42, -0.22, 1.00],  # Assets
    ]
)

# Prepare data for heatmap (lower triangle only to reduce redundancy)
heatmap_data = []
for i in range(n_vars):
    for j in range(i + 1):  # Lower triangle including diagonal
        heatmap_data.append([j, n_vars - 1 - i, round(base_corr[i, j], 2)])

# Variable labels for axes (reversed for y-axis)
reversed_vars = list(reversed(variables))

# Download Highcharts JS and Heatmap module
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

heatmap_url = "https://code.highcharts.com/modules/heatmap.js"
with urllib.request.urlopen(heatmap_url, timeout=30) as response:
    heatmap_js = response.read().decode("utf-8")

# Create complete HTML with inline Highcharts configuration
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{heatmap_js}</script>
</head>
<body style="margin:0; background-color: #ffffff;">
    <div id="container" style="width: 3600px; height: 3600px;"></div>
    <script>
        Highcharts.chart('container', {{
            chart: {{
                type: 'heatmap',
                width: 3600,
                height: 3600,
                backgroundColor: '#ffffff',
                marginTop: 180,
                marginBottom: 300,
                marginLeft: 280,
                marginRight: 220
            }},
            title: {{
                text: 'heatmap-correlation \\u00b7 highcharts \\u00b7 pyplots.ai',
                style: {{fontSize: '48px', fontWeight: 'bold'}}
            }},
            subtitle: {{
                text: 'Financial Metrics Correlation Matrix',
                style: {{fontSize: '32px', color: '#666666'}}
            }},
            xAxis: {{
                categories: {json.dumps(variables)},
                title: null,
                labels: {{
                    style: {{fontSize: '28px'}},
                    rotation: 315
                }}
            }},
            yAxis: {{
                categories: {json.dumps(reversed_vars)},
                title: null,
                labels: {{style: {{fontSize: '28px'}}}},
                reversed: false
            }},
            colorAxis: {{
                min: -1,
                max: 1,
                stops: [
                    [0, '#306998'],
                    [0.5, '#ffffff'],
                    [1, '#FFD43B']
                ],
                labels: {{style: {{fontSize: '24px'}}}},
                tickInterval: 0.5
            }},
            legend: {{
                align: 'right',
                layout: 'vertical',
                verticalAlign: 'middle',
                symbolHeight: 600,
                itemStyle: {{fontSize: '24px'}}
            }},
            tooltip: {{
                formatter: function() {{
                    var xCat = this.series.xAxis.categories[this.point.x];
                    var yCat = this.series.yAxis.categories[this.point.y];
                    return '<b>' + yCat + ' vs ' + xCat + '</b><br>Correlation: <b>' +
                           Highcharts.numberFormat(this.point.value, 2) + '</b>';
                }},
                style: {{fontSize: '20px'}}
            }},
            series: [{{
                type: 'heatmap',
                name: 'Correlation',
                data: {json.dumps(heatmap_data)},
                borderWidth: 3,
                borderColor: '#ffffff',
                dataLabels: {{
                    enabled: true,
                    formatter: function() {{
                        return Highcharts.numberFormat(this.point.value, 2);
                    }},
                    style: {{
                        fontSize: '26px',
                        fontWeight: 'bold',
                        textOutline: '2px white'
                    }}
                }}
            }}]
        }});
    </script>
</body>
</html>"""

# Write temp HTML file
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Also save the HTML file for interactive viewing
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Configure headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=3600,3600")

# Take screenshot
driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)  # Wait for chart to render
driver.save_screenshot("plot.png")
driver.quit()

# Clean up temp file
Path(temp_path).unlink()
