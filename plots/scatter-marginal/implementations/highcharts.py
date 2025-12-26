""" pyplots.ai
scatter-marginal: Scatter Plot with Marginal Distributions
Library: highcharts unknown | Python 3.13.11
Quality: 85/100 | Created: 2025-12-26
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.bar import ColumnSeries
from highcharts_core.options.series.scatter import ScatterSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - bivariate normal with correlation
np.random.seed(42)
n_points = 150
x = np.random.randn(n_points) * 2 + 10
y = 0.7 * x + np.random.randn(n_points) * 1.5 + 5

# Calculate histogram bins for marginal distributions
n_bins = 15
x_hist, x_edges = np.histogram(x, bins=n_bins)
y_hist, y_edges = np.histogram(y, bins=n_bins)

# Bin centers
x_centers = (x_edges[:-1] + x_edges[1:]) / 2
y_centers = (y_edges[:-1] + y_edges[1:]) / 2

# Download Highcharts JS (required for headless Chrome)
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# Create the main scatter chart
main_chart = Chart(container="main-chart")
main_chart.options = HighchartsOptions()

main_chart.options.chart = {
    "type": "scatter",
    "width": 3400,
    "height": 2200,
    "backgroundColor": "#ffffff",
    "marginTop": 50,
    "marginRight": 50,
    "marginBottom": 120,
    "marginLeft": 120,
}

main_chart.options.title = {"text": ""}
main_chart.options.subtitle = {"text": ""}
main_chart.options.caption = {"text": ""}

main_chart.options.x_axis = {
    "title": {"text": "X Value", "style": {"fontSize": "28px", "color": "#333333"}},
    "labels": {"style": {"fontSize": "22px", "color": "#333333"}},
    "min": float(x.min() - 0.5),
    "max": float(x.max() + 0.5),
    "gridLineWidth": 1,
    "gridLineColor": "#e0e0e0",
    "gridLineDashStyle": "Dash",
    "lineWidth": 2,
    "lineColor": "#333333",
}

main_chart.options.y_axis = {
    "title": {"text": "Y Value", "style": {"fontSize": "28px", "color": "#333333"}},
    "labels": {"style": {"fontSize": "22px", "color": "#333333"}},
    "min": float(y.min() - 0.5),
    "max": float(y.max() + 0.5),
    "gridLineWidth": 1,
    "gridLineColor": "#e0e0e0",
    "gridLineDashStyle": "Dash",
    "lineWidth": 2,
    "lineColor": "#333333",
}

main_chart.options.legend = {"enabled": False}
main_chart.options.credits = {"enabled": False}
main_chart.options.exporting = {"enabled": False}

main_chart.options.plot_options = {
    "scatter": {
        "marker": {"radius": 10, "fillColor": "rgba(48, 105, 152, 0.65)", "lineWidth": 1, "lineColor": "#306998"}
    }
}

# Add scatter series
scatter_series = ScatterSeries()
scatter_series.data = [[float(xi), float(yi)] for xi, yi in zip(x, y, strict=True)]
scatter_series.name = "Data Points"
scatter_series.color = "#306998"
main_chart.add_series(scatter_series)

# Create top histogram (X marginal)
top_chart = Chart(container="top-chart")
top_chart.options = HighchartsOptions()

top_chart.options.chart = {
    "type": "column",
    "width": 3400,
    "height": 450,
    "backgroundColor": "#ffffff",
    "marginTop": 80,
    "marginRight": 50,
    "marginBottom": 10,
    "marginLeft": 120,
}

top_chart.options.title = {
    "text": "scatter-marginal · highcharts · pyplots.ai",
    "style": {"fontSize": "36px", "fontWeight": "bold", "color": "#333333"},
    "align": "center",
}
top_chart.options.subtitle = {"text": ""}
top_chart.options.caption = {"text": ""}

top_chart.options.x_axis = {
    "categories": [f"{c:.1f}" for c in x_centers],
    "labels": {"enabled": False},
    "title": {"text": "", "enabled": False},
    "lineWidth": 0,
    "tickWidth": 0,
    "min": 0,
    "max": n_bins - 1,
}

top_chart.options.y_axis = {
    "title": {"text": "Count", "style": {"fontSize": "20px", "color": "#333333"}},
    "labels": {"style": {"fontSize": "18px", "color": "#333333"}},
    "gridLineWidth": 1,
    "gridLineColor": "#e0e0e0",
    "gridLineDashStyle": "Dash",
}

top_chart.options.legend = {"enabled": False}
top_chart.options.credits = {"enabled": False}
top_chart.options.exporting = {"enabled": False}
top_chart.options.lang = {"chartTitle": ""}

top_chart.options.plot_options = {
    "column": {"borderWidth": 1, "borderColor": "#306998", "pointPadding": 0.05, "groupPadding": 0}
}

# Add histogram series for top
top_series = ColumnSeries()
top_series.data = [int(h) for h in x_hist]
top_series.name = "X Distribution"
top_series.color = "rgba(48, 105, 152, 0.5)"
top_chart.add_series(top_series)

# Create right histogram (Y marginal) - rotated view using bar chart
right_chart = Chart(container="right-chart")
right_chart.options = HighchartsOptions()

right_chart.options.chart = {
    "type": "bar",
    "width": 500,
    "height": 2200,
    "backgroundColor": "#ffffff",
    "marginTop": 50,
    "marginRight": 80,
    "marginBottom": 120,
    "marginLeft": 10,
}

right_chart.options.title = {"text": ""}
right_chart.options.subtitle = {"text": ""}
right_chart.options.caption = {"text": ""}

right_chart.options.x_axis = {
    "categories": [f"{c:.1f}" for c in y_centers],
    "labels": {"enabled": False},
    "title": {"text": "", "enabled": False},
    "lineWidth": 0,
    "tickWidth": 0,
    "reversed": True,  # Match y-axis orientation
}

right_chart.options.y_axis = {
    "title": {"text": "Count", "style": {"fontSize": "20px", "color": "#333333"}, "rotation": 0},
    "labels": {"style": {"fontSize": "18px", "color": "#333333"}},
    "gridLineWidth": 1,
    "gridLineColor": "#e0e0e0",
    "gridLineDashStyle": "Dash",
    "opposite": False,
}

right_chart.options.legend = {"enabled": False}
right_chart.options.credits = {"enabled": False}
right_chart.options.exporting = {"enabled": False}
right_chart.options.lang = {"chartTitle": ""}

right_chart.options.plot_options = {
    "bar": {"borderWidth": 1, "borderColor": "#306998", "pointPadding": 0.05, "groupPadding": 0}
}

# Add histogram series for right
right_series = ColumnSeries()
right_series.data = [int(h) for h in y_hist]
right_series.name = "Y Distribution"
right_series.color = "rgba(48, 105, 152, 0.5)"
right_chart.add_series(right_series)

# Generate JS literals
main_js = main_chart.to_js_literal()
top_js = top_chart.to_js_literal()
right_js = right_chart.to_js_literal()

# Create combined HTML with all three charts
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <style>
        body {{
            margin: 0;
            padding: 40px;
            background: #ffffff;
            display: grid;
            grid-template-columns: 3400px 500px;
            grid-template-rows: 450px 2200px;
            gap: 10px;
        }}
        #top-chart {{
            grid-column: 1;
            grid-row: 1;
        }}
        #corner {{
            grid-column: 2;
            grid-row: 1;
            background: #ffffff;
        }}
        #main-chart {{
            grid-column: 1;
            grid-row: 2;
        }}
        #right-chart {{
            grid-column: 2;
            grid-row: 2;
        }}
    </style>
</head>
<body>
    <div id="top-chart"></div>
    <div id="corner"></div>
    <div id="main-chart"></div>
    <div id="right-chart"></div>
    <script>
        // Override Highcharts defaults to remove "Chart title"
        Highcharts.setOptions({{
            lang: {{
                chartTitle: ''
            }},
            title: {{
                text: ''
            }}
        }});
        {top_js}
        {main_js}
        {right_js}
    </script>
</body>
</html>"""

# Write temp HTML and take screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Also save HTML for interactive viewing
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4100,2800")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)  # Wait for charts to render
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()  # Clean up temp file
