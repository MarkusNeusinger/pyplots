""" pyplots.ai
violin-split: Split Violin Plot
Library: highcharts unknown | Python 3.13.11
Quality: 91/100 | Created: 2025-12-25
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Employee satisfaction scores by department, comparing Remote vs Office workers
np.random.seed(42)

categories = ["Engineering", "Marketing", "Sales", "HR"]
split_groups = ["Remote", "Office"]

# Generate realistic satisfaction data (1-10 scale)
data = {}
for cat in categories:
    data[cat] = {}
    if cat == "Engineering":
        data[cat]["Remote"] = np.random.normal(7.8, 0.9, 120)
        data[cat]["Office"] = np.random.normal(6.5, 1.3, 100)
    elif cat == "Marketing":
        data[cat]["Remote"] = np.random.normal(7.0, 1.1, 80)
        data[cat]["Office"] = np.random.normal(7.2, 1.0, 90)
    elif cat == "Sales":
        data[cat]["Remote"] = np.random.normal(6.2, 1.4, 90)
        data[cat]["Office"] = np.random.normal(7.5, 0.8, 110)
    else:  # HR
        data[cat]["Remote"] = np.random.normal(7.5, 1.0, 70)
        data[cat]["Office"] = np.random.normal(7.3, 1.2, 85)

# Clip to valid range
for cat in categories:
    for group in split_groups:
        data[cat][group] = np.clip(data[cat][group], 1, 10)


# Compute KDE using numpy only (Gaussian kernel)
def compute_kde(values, n_points=100):
    """Compute kernel density estimate using Gaussian kernel."""
    values = np.asarray(values)
    n = len(values)
    std = np.std(values, ddof=1)
    bandwidth = 1.06 * std * n ** (-1 / 5)

    x_range = np.linspace(min(values) - 0.5, max(values) + 0.5, n_points)
    density = np.zeros(n_points)

    for v in values:
        density += np.exp(-0.5 * ((x_range - v) / bandwidth) ** 2)

    density = density / (n * bandwidth * np.sqrt(2 * np.pi))
    density = density / density.max() * 0.35
    return x_range, density


# Build series data for split violins
series_data = []
colors = {"Remote": "#306998", "Office": "#FFD43B"}

# Track which groups have been added to legend
legend_added = {"Remote": False, "Office": False}

for i, cat in enumerate(categories):
    cat_x = i

    for group in split_groups:
        values = data[cat][group]
        y_vals, density = compute_kde(values)

        area_data = []
        if group == "Remote":
            for y, d in zip(y_vals, density, strict=True):
                area_data.append({"x": float(y), "low": float(cat_x - d), "high": float(cat_x)})
        else:
            for y, d in zip(y_vals, density, strict=True):
                area_data.append({"x": float(y), "low": float(cat_x), "high": float(cat_x + d)})

        show_in_legend = not legend_added[group]
        legend_added[group] = True

        series_data.append(
            {
                "type": "areasplinerange",
                "name": group,
                "showInLegend": show_in_legend,
                "data": area_data,
                "color": colors[group],
                "fillOpacity": 0.75,
                "lineWidth": 2,
                "lineColor": colors[group],
                "marker": {"enabled": False},
            }
        )

# Add median markers
median_markers = []
for i, cat in enumerate(categories):
    for group in split_groups:
        values = data[cat][group]
        median_val = np.median(values)
        offset = -0.12 if group == "Remote" else 0.12
        x_pos = i + offset

        median_markers.append({"x": float(median_val), "y": float(x_pos)})

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {
    "type": "areasplinerange",
    "inverted": True,
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#FFFFFF",
    "marginBottom": 320,
    "marginLeft": 350,
    "marginRight": 200,
    "marginTop": 150,
}

# Title
chart.options.title = {
    "text": "violin-split · highcharts · pyplots.ai",
    "style": {"fontSize": "56px", "fontWeight": "bold"},
    "y": 60,
}

chart.options.subtitle = {
    "text": "Employee Satisfaction Scores: Remote vs Office Workers",
    "style": {"fontSize": "36px", "color": "#666666"},
    "y": 110,
}

# X-axis (vertical after inversion - shows satisfaction scores)
chart.options.x_axis = {
    "title": {"text": "Satisfaction Score", "style": {"fontSize": "40px", "fontWeight": "bold"}, "margin": 20},
    "labels": {"style": {"fontSize": "32px"}},
    "min": 1,
    "max": 10,
    "reversed": True,
    "gridLineWidth": 1,
    "gridLineColor": "#E0E0E0",
    "tickInterval": 1,
}

# Y-axis (horizontal after inversion - shows categories)
chart.options.y_axis = {
    "title": {"text": "Department", "style": {"fontSize": "40px", "fontWeight": "bold"}, "margin": 50},
    "labels": {"style": {"fontSize": "36px"}},
    "categories": categories,
    "min": -0.5,
    "max": 3.5,
    "gridLineWidth": 0,
    "tickPositions": [0, 1, 2, 3],
    "showLastLabel": True,
    "showFirstLabel": True,
}

# Legend
chart.options.legend = {
    "enabled": True,
    "align": "right",
    "verticalAlign": "top",
    "layout": "vertical",
    "x": -80,
    "y": 150,
    "itemStyle": {"fontSize": "32px", "fontWeight": "normal"},
    "symbolHeight": 28,
    "symbolWidth": 28,
    "symbolRadius": 6,
    "itemMarginBottom": 10,
}

# Tooltip
chart.options.tooltip = {
    "enabled": True,
    "style": {"fontSize": "28px"},
    "headerFormat": "<b>{series.name}</b><br/>",
    "pointFormat": "Score: {point.x:.1f}",
}

# Plot options
chart.options.plot_options = {
    "areasplinerange": {"fillOpacity": 0.75, "lineWidth": 2, "states": {"hover": {"lineWidth": 3}}},
    "series": {"animation": False},
}

# Add all series
for s in series_data:
    chart.options.add_series(s)

# Add scatter series for median markers
median_series = {
    "type": "scatter",
    "name": "Median",
    "showInLegend": False,
    "data": median_markers,
    "marker": {"symbol": "diamond", "radius": 12, "fillColor": "#FFFFFF", "lineColor": "#333333", "lineWidth": 3},
    "enableMouseTracking": False,
}
chart.options.add_series(median_series)

# Download Highcharts JS
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

highcharts_more_url = "https://code.highcharts.com/highcharts-more.js"
with urllib.request.urlopen(highcharts_more_url, timeout=30) as response:
    highcharts_more_js = response.read().decode("utf-8")

# Generate HTML with inline scripts
html_str = chart.to_js_literal()

html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{highcharts_more_js}</script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>{html_str}</script>
</body>
</html>"""

# Write temp HTML and take screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Also save the HTML file for interactive viewing
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4800,2700")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()
