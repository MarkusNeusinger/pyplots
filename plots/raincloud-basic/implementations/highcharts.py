"""pyplots.ai
raincloud-basic: Basic Raincloud Plot
Library: highcharts | Python 3.13
Quality: pending | Created: 2025-12-24
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

# Create jittered scatter data (the "rain")
scatter_data = []
for i, data in enumerate(all_data):
    for val in data:
        jitter = np.random.uniform(-0.08, 0.08)
        scatter_data.append([i + 0.25 + jitter, float(val)])


# Create KDE data for half-violin (the "cloud")
def compute_kde_simple(data, num_points=50):
    """Compute kernel density estimate using Gaussian kernel."""
    data = np.array(data)
    n = len(data)
    std = np.std(data)
    iqr = np.percentile(data, 75) - np.percentile(data, 25)
    bandwidth = 0.9 * min(std, iqr / 1.34) * (n ** (-0.2))

    y_range = np.linspace(min(data) - 20, max(data) + 20, num_points)
    density = np.zeros(num_points)

    for point in data:
        density += np.exp(-0.5 * ((y_range - point) / bandwidth) ** 2)

    density = density / (n * bandwidth * np.sqrt(2 * np.pi))
    density = density / density.max() * 0.35
    return y_range, density


violin_series = []
for i, data in enumerate(all_data):
    y_vals, density = compute_kde_simple(data)
    violin_points = []
    for y, d in zip(y_vals, density, strict=True):
        violin_points.append([i - d - 0.05, float(y)])
    violin_series.append(violin_points)

# Box plot series data
box_series_data = []
for box in box_data:
    box_series_data.append([box["low"], box["q1"], box["median"], box["q3"], box["high"]])

# Build chart JavaScript
chart_js = f"""
Highcharts.chart('container', {{
    chart: {{
        type: 'boxplot',
        width: 4800,
        height: 2700,
        backgroundColor: '#ffffff',
        marginBottom: 280,
        marginLeft: 220,
        marginRight: 350,
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
        tickWidth: 2
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
        max: 650
    }},
    legend: {{
        enabled: true,
        itemStyle: {{ fontSize: '32px' }},
        align: 'right',
        verticalAlign: 'top',
        layout: 'vertical',
        x: -50,
        y: 100
    }},
    plotOptions: {{
        boxplot: {{
            fillColor: 'rgba(48, 105, 152, 0.7)',
            medianColor: '#FFD43B',
            medianWidth: 6,
            stemWidth: 4,
            whiskerWidth: 4,
            whiskerLength: '40%',
            lineWidth: 3,
            color: '#306998',
            pointWidth: 60
        }},
        scatter: {{
            marker: {{
                radius: 10,
                symbol: 'circle'
            }}
        }},
        spline: {{
            lineWidth: 4
        }}
    }},
    series: [
        {{
            name: 'Box Plot',
            type: 'boxplot',
            data: {json.dumps(box_series_data)},
            color: '#306998',
            tooltip: {{
                headerFormat: '<b>{{point.key}}</b><br/>',
                pointFormat: 'Max: {{point.high:.0f}} ms<br/>Q3: {{point.q3:.0f}} ms<br/>Median: {{point.median:.0f}} ms<br/>Q1: {{point.q1:.0f}} ms<br/>Min: {{point.low:.0f}} ms'
            }}
        }},
        {{
            name: 'Individual Points',
            type: 'scatter',
            data: {json.dumps(scatter_data)},
            color: 'rgba(48, 105, 152, 0.5)',
            marker: {{
                radius: 8,
                lineWidth: 1,
                lineColor: '#306998'
            }},
            tooltip: {{
                pointFormat: 'Value: {{point.y:.0f}} ms'
            }}
        }},
        {{
            name: 'Density (Control)',
            type: 'spline',
            data: {json.dumps(violin_series[0])},
            color: '#306998',
            lineWidth: 4,
            marker: {{ enabled: false }},
            enableMouseTracking: false
        }},
        {{
            name: 'Density (Treatment A)',
            type: 'spline',
            data: {json.dumps(violin_series[1])},
            color: '#FFD43B',
            lineWidth: 4,
            marker: {{ enabled: false }},
            enableMouseTracking: false
        }},
        {{
            name: 'Density (Treatment B)',
            type: 'spline',
            data: {json.dumps(violin_series[2])},
            color: '#9467BD',
            lineWidth: 4,
            marker: {{ enabled: false }},
            enableMouseTracking: false
        }},
        {{
            name: 'Density (Treatment C)',
            type: 'spline',
            data: {json.dumps(violin_series[3])},
            color: '#17BECF',
            lineWidth: 4,
            marker: {{ enabled: false }},
            enableMouseTracking: false
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
