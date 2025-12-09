"""
scatter-color-groups: Scatter Plot with Color Groups
Library: highcharts

Note: Highcharts requires a license for commercial use.
"""

import json
import tempfile
import time
import urllib.request
from pathlib import Path

from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.scatter import ScatterSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Color palette from style guide
COLORS = ["#306998", "#FFD43B", "#DC2626", "#059669", "#8B5CF6", "#F97316"]

# Data - Iris dataset (sepal_length, sepal_width) by species
# fmt: off
iris_data = {
    "setosa": [
        (5.1, 3.5), (4.9, 3.0), (4.7, 3.2), (4.6, 3.1), (5.0, 3.6), (5.4, 3.9), (4.6, 3.4), (5.0, 3.4),
        (4.4, 2.9), (4.9, 3.1), (5.4, 3.7), (4.8, 3.4), (4.8, 3.0), (4.3, 3.0), (5.8, 4.0), (5.7, 4.4),
        (5.4, 3.9), (5.1, 3.5), (5.7, 3.8), (5.1, 3.8), (5.4, 3.4), (5.1, 3.7), (4.6, 3.6), (5.1, 3.3),
        (4.8, 3.4), (5.0, 3.0), (5.0, 3.4), (5.2, 3.5), (5.2, 3.4), (4.7, 3.2), (4.8, 3.1), (5.4, 3.4),
        (5.2, 4.1), (5.5, 4.2), (4.9, 3.1), (5.0, 3.2), (5.5, 3.5), (4.9, 3.6), (4.4, 3.0), (5.1, 3.4),
        (5.0, 3.5), (4.5, 2.3), (4.4, 3.2), (5.0, 3.5), (5.1, 3.8), (4.8, 3.0), (5.1, 3.8), (4.6, 3.2),
        (5.3, 3.7), (5.0, 3.3),
    ],
    "versicolor": [
        (7.0, 3.2), (6.4, 3.2), (6.9, 3.1), (5.5, 2.3), (6.5, 2.8), (5.7, 2.8), (6.3, 3.3), (4.9, 2.4),
        (6.6, 2.9), (5.2, 2.7), (5.0, 2.0), (5.9, 3.0), (6.0, 2.2), (6.1, 2.9), (5.6, 2.9), (6.7, 3.1),
        (5.6, 3.0), (5.8, 2.7), (6.2, 2.2), (5.6, 2.5), (5.9, 3.2), (6.1, 2.8), (6.3, 2.5), (6.1, 2.8),
        (6.4, 2.9), (6.6, 3.0), (6.8, 2.8), (6.7, 3.0), (6.0, 2.9), (5.7, 2.6), (5.5, 2.4), (5.5, 2.4),
        (5.8, 2.7), (6.0, 2.7), (5.4, 3.0), (6.0, 3.4), (6.7, 3.1), (6.3, 2.3), (5.6, 3.0), (5.5, 2.5),
        (5.5, 2.6), (6.1, 3.0), (5.8, 2.6), (5.0, 2.3), (5.6, 2.7), (5.7, 3.0), (5.7, 2.9), (6.2, 2.9),
        (5.1, 2.5), (5.7, 2.8),
    ],
    "virginica": [
        (6.3, 3.3), (5.8, 2.7), (7.1, 3.0), (6.3, 2.9), (6.5, 3.0), (7.6, 3.0), (4.9, 2.5), (7.3, 2.9),
        (6.7, 2.5), (7.2, 3.6), (6.5, 3.2), (6.4, 2.7), (6.8, 3.0), (5.7, 2.5), (5.8, 2.8), (6.4, 3.2),
        (6.5, 3.0), (7.7, 3.8), (7.7, 2.6), (6.0, 2.2), (6.9, 3.2), (5.6, 2.8), (7.7, 2.8), (6.3, 2.7),
        (6.7, 3.3), (7.2, 3.2), (6.2, 2.8), (6.1, 3.0), (6.4, 2.8), (7.2, 3.0), (7.4, 2.8), (7.9, 3.8),
        (6.4, 2.8), (6.3, 2.8), (6.1, 2.6), (7.7, 3.0), (6.3, 3.4), (6.4, 3.1), (6.0, 3.0), (6.9, 3.1),
        (6.7, 3.1), (6.9, 3.1), (5.8, 2.7), (6.8, 3.2), (6.7, 3.3), (6.7, 3.0), (6.3, 2.5), (6.5, 3.0),
        (6.2, 3.4), (5.9, 3.0),
    ],
}
# fmt: on
groups = list(iris_data.keys())

# Create chart with container ID for rendering
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration - 4800 x 2700 px per style guide
chart.options.chart = {"type": "scatter", "width": 4800, "height": 2700, "backgroundColor": "#ffffff"}

# Title
chart.options.title = {
    "text": "Iris Dataset: Sepal Dimensions by Species",
    "style": {"fontSize": "48px", "fontWeight": "bold"},
}

# X-axis configuration
chart.options.x_axis = {
    "title": {"text": "Sepal Length (cm)", "style": {"fontSize": "36px"}},
    "labels": {"style": {"fontSize": "28px"}},
    "gridLineWidth": 1,
    "gridLineDashStyle": "Dot",
    "gridLineColor": "rgba(0, 0, 0, 0.15)",
}

# Y-axis configuration
chart.options.y_axis = {
    "title": {"text": "Sepal Width (cm)", "style": {"fontSize": "36px"}},
    "labels": {"style": {"fontSize": "28px"}},
    "gridLineWidth": 1,
    "gridLineDashStyle": "Dot",
    "gridLineColor": "rgba(0, 0, 0, 0.15)",
}

# Plot options for scatter
chart.options.plot_options = {
    "scatter": {
        "marker": {"radius": 12, "states": {"hover": {"enabled": True, "lineColor": "rgb(100,100,100)"}}},
        "states": {"hover": {"marker": {"enabled": False}}},
    }
}

# Add a series for each group with distinct colors
for i, group in enumerate(groups):
    series = ScatterSeries()
    series.name = group.capitalize()
    series.data = iris_data[group]
    series.color = COLORS[i % len(COLORS)]
    chart.add_series(series)

# Legend configuration
chart.options.legend = {
    "enabled": True,
    "align": "right",
    "verticalAlign": "middle",
    "layout": "vertical",
    "itemStyle": {"fontSize": "28px"},
}

# Tooltip configuration
chart.options.tooltip = {
    "headerFormat": "<b>{series.name}</b><br>",
    "pointFormat": "Sepal Length: {point.x} cm<br>Sepal Width: {point.y} cm",
    "style": {"fontSize": "24px"},
}

# Disable credits
chart.options.credits = {"enabled": False}

# Export to PNG via Selenium screenshot
# Download Highcharts JS (required for headless Chrome which can't load CDN)
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# Get chart options as JSON
opts_json = json.dumps(chart.options.to_dict())

html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
</head>
<body style="margin:0; padding:0; overflow:hidden;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>
        Highcharts.chart('container', {opts_json});
    </script>
</body>
</html>"""

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
time.sleep(5)  # Wait for chart to render
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()  # Clean up temp file
print("Plot saved to plot.png")
