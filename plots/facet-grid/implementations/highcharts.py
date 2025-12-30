""" pyplots.ai
facet-grid: Faceted Grid Plot
Library: highcharts unknown | Python 3.13.11
Quality: 88/100 | Created: 2025-12-30
"""

import json
import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data
np.random.seed(42)

# Create faceted data: Plant growth by soil type (rows) and light condition (columns)
soil_types = ["Sandy", "Loamy", "Clay"]
light_conditions = ["Low", "Medium", "High"]
n_per_group = 25

data = []
for soil in soil_types:
    for light in light_conditions:
        # Base growth varies by light condition
        base_growth = {"Low": 5, "Medium": 12, "High": 18}[light]
        # Soil type affects growth rate
        soil_factor = {"Sandy": 0.8, "Loamy": 1.2, "Clay": 1.0}[soil]

        for _ in range(n_per_group):
            water = np.random.uniform(20, 100)
            # Growth depends on water, with some noise
            growth = base_growth * soil_factor + water * 0.15 * soil_factor + np.random.normal(0, 2)
            data.append({"soil": soil, "light": light, "water": water, "growth": max(0, growth)})

# Build subplot configurations
subplots = []
n_rows = len(soil_types)
n_cols = len(light_conditions)

# Calculate subplot dimensions with margins
chart_width = 4800
chart_height = 2700
margin_top = 180
margin_bottom = 120
margin_left = 180
margin_right = 80
spacing = 60

plot_area_width = chart_width - margin_left - margin_right
plot_area_height = chart_height - margin_top - margin_bottom
subplot_width = (plot_area_width - spacing * (n_cols - 1)) / n_cols
subplot_height = (plot_area_height - spacing * (n_rows - 1)) / n_rows

# Colors for facets
colors = ["#306998", "#FFD43B", "#9467BD", "#17BECF", "#8C564B"]

# Build series data for each facet
series_list = []
x_axes = []
y_axes = []

for row_idx, soil in enumerate(soil_types):
    for col_idx, light in enumerate(light_conditions):
        # Filter data for this facet
        facet_data = [d for d in data if d["soil"] == soil and d["light"] == light]
        points = [[d["water"], d["growth"]] for d in facet_data]

        # Calculate position
        left = margin_left + col_idx * (subplot_width + spacing)
        top = margin_top + row_idx * (subplot_height + spacing)

        # Create x-axis for this subplot
        x_axis_id = f"x{row_idx * n_cols + col_idx}"
        x_axes.append(
            {
                "id": x_axis_id,
                "left": left,
                "top": top + subplot_height,
                "width": subplot_width,
                "height": 0,
                "min": 15,
                "max": 105,
                "lineWidth": 2,
                "lineColor": "#333333",
                "tickWidth": 2,
                "tickLength": 8,
                "labels": {"style": {"fontSize": "16px", "color": "#333333"}, "y": 25},
                "title": {
                    "text": "Water (mm)" if row_idx == n_rows - 1 else None,
                    "style": {"fontSize": "18px", "color": "#333333"},
                    "y": 45,
                },
                "gridLineWidth": 1,
                "gridLineColor": "rgba(0,0,0,0.1)",
                "gridLineDashStyle": "Dash",
                "offset": 0,
            }
        )

        # Create y-axis for this subplot
        y_axis_id = f"y{row_idx * n_cols + col_idx}"
        y_axes.append(
            {
                "id": y_axis_id,
                "left": left,
                "top": top,
                "width": 0,
                "height": subplot_height,
                "min": 0,
                "max": 40,
                "lineWidth": 2,
                "lineColor": "#333333",
                "tickWidth": 2,
                "tickLength": 8,
                "labels": {"style": {"fontSize": "16px", "color": "#333333"}, "x": -10},
                "title": {
                    "text": "Growth (cm)" if col_idx == 0 else None,
                    "style": {"fontSize": "18px", "color": "#333333"},
                    "rotation": -90,
                    "x": -40,
                },
                "gridLineWidth": 1,
                "gridLineColor": "rgba(0,0,0,0.1)",
                "gridLineDashStyle": "Dash",
                "offset": 0,
            }
        )

        # Create series for this facet
        series_list.append(
            {
                "type": "scatter",
                "name": f"{soil} / {light}",
                "data": points,
                "xAxis": row_idx * n_cols + col_idx,
                "yAxis": row_idx * n_cols + col_idx,
                "marker": {
                    "radius": 8,
                    "symbol": "circle",
                    "fillColor": colors[row_idx % len(colors)],
                    "lineWidth": 1,
                    "lineColor": "#333333",
                },
                "showInLegend": False,
            }
        )

# Build annotations for facet labels
annotations = []

# Column headers (light conditions)
for col_idx, light in enumerate(light_conditions):
    left = margin_left + col_idx * (subplot_width + spacing) + subplot_width / 2
    annotations.append(
        {
            "labels": [
                {
                    "point": {"x": left, "y": margin_top - 50, "xAxis": None, "yAxis": None},
                    "text": f"Light: {light}",
                    "backgroundColor": "transparent",
                    "borderWidth": 0,
                    "style": {"fontSize": "22px", "fontWeight": "bold", "color": "#333333"},
                }
            ],
            "labelOptions": {"useHTML": True},
        }
    )

# Row labels (soil types)
for row_idx, soil in enumerate(soil_types):
    top = margin_top + row_idx * (subplot_height + spacing) + subplot_height / 2
    annotations.append(
        {
            "labels": [
                {
                    "point": {"x": chart_width - margin_right + 40, "y": top, "xAxis": None, "yAxis": None},
                    "text": f"Soil: {soil}",
                    "backgroundColor": "transparent",
                    "borderWidth": 0,
                    "style": {"fontSize": "20px", "fontWeight": "bold", "color": "#333333"},
                    "rotation": 90,
                }
            ],
            "labelOptions": {"useHTML": True},
        }
    )

# Build complete chart options as JavaScript
chart_options = {
    "chart": {
        "type": "scatter",
        "width": chart_width,
        "height": chart_height,
        "backgroundColor": "#ffffff",
        "style": {"fontFamily": "Arial, sans-serif"},
        "marginTop": margin_top,
        "marginBottom": margin_bottom,
        "marginLeft": margin_left,
        "marginRight": margin_right,
    },
    "title": {
        "text": "Plant Growth Study · facet-grid · highcharts · pyplots.ai",
        "style": {"fontSize": "32px", "fontWeight": "bold", "color": "#333333"},
        "y": 50,
    },
    "subtitle": {
        "text": "Growth by Soil Type (rows) and Light Condition (columns)",
        "style": {"fontSize": "22px", "color": "#666666"},
        "y": 100,
    },
    "credits": {"enabled": False},
    "legend": {"enabled": False},
    "xAxis": x_axes,
    "yAxis": y_axes,
    "series": series_list,
    "annotations": annotations,
    "plotOptions": {
        "scatter": {
            "marker": {"radius": 8, "states": {"hover": {"enabled": True, "lineColor": "#333333"}}},
            "states": {"inactive": {"opacity": 1}},
        }
    },
    "tooltip": {
        "headerFormat": "<b>{series.name}</b><br>",
        "pointFormat": "Water: {point.x:.1f} mm<br>Growth: {point.y:.1f} cm",
        "style": {"fontSize": "16px"},
    },
}

# Convert to JavaScript
options_json = json.dumps(chart_options, indent=2)

# Download Highcharts JS
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# Download annotations module
annotations_url = "https://code.highcharts.com/modules/annotations.js"
with urllib.request.urlopen(annotations_url, timeout=30) as response:
    annotations_js = response.read().decode("utf-8")

# Generate HTML with inline scripts
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{annotations_js}</script>
</head>
<body style="margin:0; padding:0;">
    <div id="container" style="width: {chart_width}px; height: {chart_height}px;"></div>
    <script>
        Highcharts.chart('container', {options_json});
    </script>
</body>
</html>"""

# Save HTML
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Create screenshot with Selenium
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4900,2800")

driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(4900, 2800)
driver.get(f"file://{temp_path}")
time.sleep(5)
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()
