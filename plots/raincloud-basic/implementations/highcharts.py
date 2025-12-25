""" pyplots.ai
raincloud-basic: Basic Raincloud Plot
Library: highcharts unknown | Python 3.13.11
Quality: 68/100 | Created: 2025-12-25
"""

import json
import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Reaction times (ms) for different experimental conditions
np.random.seed(42)
categories = ["Control", "Treatment A", "Treatment B", "Treatment C"]
colors = ["#306998", "#FFD43B", "#9467BD", "#17BECF"]
# Simplified fill colors (no rgba calculation)
fill_colors = ["#306998", "#FFD43B", "#9467BD", "#17BECF"]

# Generate realistic reaction time data with different distributions
control = np.random.normal(450, 60, 80)  # Normal distribution
treatment_a = np.random.normal(380, 50, 80)  # Faster responses
treatment_b = np.concatenate(
    [  # Bimodal distribution
        np.random.normal(350, 30, 40),
        np.random.normal(480, 35, 40),
    ]
)
treatment_c = np.random.normal(420, 80, 80)  # More variable

all_data = [control, treatment_a, treatment_b, treatment_c]

# Calculate statistics for box plots
box_data = []
for data in all_data:
    q1 = np.percentile(data, 25)
    median = np.percentile(data, 50)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    lower_whisker = max(np.min(data), q1 - 1.5 * iqr)
    upper_whisker = min(np.max(data), q3 + 1.5 * iqr)
    box_data.append(
        {
            "low": float(lower_whisker),
            "q1": float(q1),
            "median": float(median),
            "q3": float(q3),
            "high": float(upper_whisker),
        }
    )

# Create jittered scatter data (the "rain" - falls LEFT of the cloud for vertical orientation)
scatter_data = []
for i, data in enumerate(all_data):
    for val in data:
        jitter = np.random.uniform(-0.08, 0.08)
        # Rain on LEFT side (negative offset from category center)
        scatter_data.append({"x": i - 0.25 + jitter, "y": float(val), "color": colors[i]})

# Box plot series data with simplified fill colors
box_series_data = []
for i, box in enumerate(box_data):
    box_series_data.append(
        {
            "low": box["low"],
            "q1": box["q1"],
            "median": box["median"],
            "q3": box["q3"],
            "high": box["high"],
            "color": colors[i],
            "fillColor": fill_colors[i],
        }
    )

# Create polygon data for half-violin (the "cloud") - inline KDE
# Cloud on RIGHT side for vertical orientation (rain falls from cloud, so cloud is RIGHT/TOP)
violin_polygons = []
for i, data in enumerate(all_data):
    # Inline KDE computation (Gaussian kernel)
    data_arr = np.array(data)
    n = len(data_arr)
    std = np.std(data_arr)
    iqr_val = np.percentile(data_arr, 75) - np.percentile(data_arr, 25)
    bandwidth = 0.9 * min(std, iqr_val / 1.34) * (n ** (-0.2))
    y_range = np.linspace(min(data_arr) - 20, max(data_arr) + 20, 50)
    density = np.zeros(50)
    for point in data_arr:
        density += np.exp(-0.5 * ((y_range - point) / bandwidth) ** 2)
    density = density / (n * bandwidth * np.sqrt(2 * np.pi))
    density = density / density.max() * 0.35

    # Create polygon points for filled half-violin on RIGHT side (close the polygon)
    polygon_points = []
    # Right side: baseline at category, extend RIGHT (positive direction)
    for y, d in zip(y_range, density, strict=True):
        polygon_points.append([float(i + d + 0.05), float(y)])
    # Close polygon by going back along the baseline
    for y in reversed(y_range):
        polygon_points.append([float(i + 0.05), float(y)])
    # Close the polygon
    polygon_points.append(polygon_points[0])
    violin_polygons.append({"points": polygon_points, "color": colors[i]})

# Build chart JavaScript with polygon series for clouds
polygon_series_js = []
for idx, poly in enumerate(violin_polygons):
    show_legend = "true" if idx == 0 else "false"
    linked = "" if idx == 0 else "linkedTo: ':previous',"
    polygon_series_js.append(f"""{{
            name: 'Density Cloud',
            type: 'polygon',
            data: {json.dumps(poly["points"])},
            color: '{poly["color"]}',
            fillOpacity: 0.6,
            lineWidth: 2,
            lineColor: '{poly["color"]}',
            enableMouseTracking: false,
            showInLegend: {show_legend},
            {linked}
            marker: {{ enabled: false }}
        }}""")

chart_js = f"""
Highcharts.chart('container', {{
    chart: {{
        width: 4800,
        height: 2700,
        backgroundColor: '#ffffff',
        marginBottom: 280,
        marginLeft: 220,
        marginRight: 200,
        spacingBottom: 80
    }},
    title: {{
        text: 'raincloud-basic · highcharts · pyplots.ai',
        style: {{ fontSize: '56px', fontWeight: 'bold' }}
    }},
    xAxis: {{
        categories: {json.dumps(categories)},
        title: {{
            text: 'Experimental Condition',
            style: {{ fontSize: '44px' }}
        }},
        labels: {{
            style: {{ fontSize: '36px' }}
        }},
        lineWidth: 2,
        tickWidth: 2,
        min: -0.5,
        max: 3.5,
        tickPositions: [0, 1, 2, 3]
    }},
    yAxis: {{
        title: {{
            text: 'Reaction Time (ms)',
            style: {{ fontSize: '44px' }}
        }},
        labels: {{
            style: {{ fontSize: '36px' }}
        }},
        gridLineWidth: 1,
        gridLineDashStyle: 'Dash',
        min: 200,
        max: 660
    }},
    legend: {{
        enabled: true,
        itemStyle: {{ fontSize: '36px' }},
        align: 'right',
        verticalAlign: 'top',
        layout: 'vertical',
        x: -50,
        y: 100,
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        borderWidth: 1,
        borderColor: '#cccccc',
        padding: 20
    }},
    plotOptions: {{
        boxplot: {{
            medianColor: '#1a1a1a',
            medianWidth: 6,
            stemWidth: 4,
            whiskerWidth: 4,
            whiskerLength: '40%',
            lineWidth: 3,
            pointWidth: 60,
            fillOpacity: 0.7
        }},
        scatter: {{
            marker: {{
                radius: 18,
                symbol: 'circle'
            }}
        }},
        polygon: {{
            fillOpacity: 0.6,
            lineWidth: 2
        }}
    }},
    series: [
        {",".join(polygon_series_js)},
        {{
            name: 'Box Plot',
            type: 'boxplot',
            data: {json.dumps(box_series_data)},
            colorByPoint: true,
            tooltip: {{
                headerFormat: '<b>{{point.key}}</b><br/>',
                pointFormat: 'Max: {{point.high:.0f}} ms<br/>Q3: {{point.q3:.0f}} ms<br/>Median: {{point.median:.0f}} ms<br/>Q1: {{point.q1:.0f}} ms<br/>Min: {{point.low:.0f}} ms'
            }}
        }},
        {{
            name: 'Individual Points',
            type: 'scatter',
            data: {json.dumps(scatter_data)},
            marker: {{
                radius: 16,
                lineWidth: 2,
                lineColor: 'rgba(0,0,0,0.4)'
            }},
            opacity: 0.65,
            tooltip: {{
                pointFormat: 'Value: {{point.y:.0f}} ms'
            }}
        }}
    ]
}});
"""

# Download Highcharts JS and required modules
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

highcharts_more_url = "https://code.highcharts.com/highcharts-more.js"
with urllib.request.urlopen(highcharts_more_url, timeout=30) as response:
    highcharts_more_js = response.read().decode("utf-8")

# Generate HTML with inline scripts
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{highcharts_more_js}</script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>
    document.addEventListener('DOMContentLoaded', function() {{
        {chart_js}
    }});
    </script>
</body>
</html>"""

# Write temp HTML and take screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Also save the HTML file
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Setup Chrome for screenshot
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

Path(temp_path).unlink()  # Clean up temp file
