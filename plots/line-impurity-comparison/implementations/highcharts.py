""" pyplots.ai
line-impurity-comparison: Gini Impurity vs Entropy Comparison
Library: highcharts unknown | Python 3.14.3
Quality: 89/100 | Created: 2026-02-17
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.area import LineSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data
p = np.linspace(0, 1, 200)

# Gini impurity: 2 * p * (1 - p)
gini = 2 * p * (1 - p)

# Entropy: -p * log2(p) - (1-p) * log2(1-p), normalized to [0, 1]
# Handle edge cases at p=0 and p=1
with np.errstate(divide="ignore", invalid="ignore"):
    entropy_raw = -p * np.log2(p) - (1 - p) * np.log2(1 - p)
entropy_raw = np.nan_to_num(entropy_raw, nan=0.0)
entropy = entropy_raw  # max of entropy is 1.0 at p=0.5, already in [0, 1]

# Prepare data for Highcharts (list of [x, y] pairs)
gini_data = [[round(float(p[i]), 4), round(float(gini[i]), 6)] for i in range(len(p))]
entropy_data = [[round(float(p[i]), 4), round(float(entropy[i]), 6)] for i in range(len(p))]

# Colors
color_gini = "#306998"  # Python Blue
color_entropy = "#E8793A"  # Warm orange complement

# Chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

chart.options.chart = {
    "type": "line",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginLeft": 200,
    "marginRight": 150,
    "marginBottom": 200,
    "marginTop": 180,
}

chart.options.title = {
    "text": "line-impurity-comparison \u00b7 highcharts \u00b7 pyplots.ai",
    "style": {"fontSize": "56px", "fontWeight": "bold"},
}

chart.options.subtitle = {
    "text": "Gini Impurity vs Entropy as Decision Tree Splitting Criteria",
    "style": {"fontSize": "36px", "color": "#666666"},
}

chart.options.x_axis = {
    "title": {"text": "Probability (p)", "style": {"fontSize": "40px"}, "margin": 25},
    "labels": {"style": {"fontSize": "32px"}, "y": 40},
    "min": 0,
    "max": 1,
    "tickInterval": 0.1,
    "gridLineWidth": 1,
    "gridLineColor": "rgba(0, 0, 0, 0.08)",
    "lineWidth": 2,
    "lineColor": "#333333",
}

chart.options.y_axis = {
    "title": {"text": "Impurity Measure", "style": {"fontSize": "40px"}},
    "labels": {"style": {"fontSize": "32px"}},
    "min": 0,
    "max": 1.05,
    "tickInterval": 0.2,
    "gridLineWidth": 1,
    "gridLineColor": "rgba(0, 0, 0, 0.10)",
    "lineWidth": 2,
    "lineColor": "#333333",
}

chart.options.legend = {
    "enabled": True,
    "align": "right",
    "verticalAlign": "top",
    "layout": "vertical",
    "x": -80,
    "y": 80,
    "itemStyle": {"fontSize": "34px", "fontWeight": "normal"},
    "itemMarginBottom": 15,
    "backgroundColor": "rgba(255, 255, 255, 0.9)",
    "borderRadius": 8,
    "padding": 20,
}

chart.options.credits = {"enabled": False}

chart.options.plot_options = {"series": {"animation": False}, "line": {"lineWidth": 6, "marker": {"enabled": False}}}

# Annotation at p=0.5 maximum
chart.options.annotations = [
    {
        "draggable": "",
        "labelOptions": {
            "backgroundColor": "rgba(255, 255, 255, 0.9)",
            "borderColor": "#333333",
            "borderRadius": 6,
            "borderWidth": 2,
            "style": {"fontSize": "28px", "color": "#333333"},
            "padding": 12,
        },
        "labels": [
            {"point": {"x": 0.5, "y": 1.0, "xAxis": 0, "yAxis": 0}, "text": "Maximum impurity at p = 0.5", "y": -30}
        ],
    }
]

# Gini series
gini_series = LineSeries()
gini_series.data = gini_data
gini_series.name = "Gini Impurity: 2p(1\u2212p)"
gini_series.color = color_gini
chart.add_series(gini_series)

# Entropy series
entropy_series = LineSeries()
entropy_series.data = entropy_data
entropy_series.name = "Entropy: \u2212p log\u2082p \u2212 (1\u2212p) log\u2082(1\u2212p)"
entropy_series.color = color_entropy
chart.add_series(entropy_series)

# Download Highcharts JS and annotations module
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

annotations_url = "https://code.highcharts.com/modules/annotations.js"
with urllib.request.urlopen(annotations_url, timeout=30) as response:
    annotations_js = response.read().decode("utf-8")

# Generate HTML with inline scripts
html_str = chart.to_js_literal()
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{annotations_js}</script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>{html_str}</script>
</body>
</html>"""

# Save interactive HTML
with open("plot.html", "w", encoding="utf-8") as f:
    portable_html = (
        """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/modules/annotations.js"></script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 100%; height: 100vh;"></div>
    <script>"""
        + html_str
        + """</script>
</body>
</html>"""
    )
    f.write(portable_html)

# Write temp HTML and take screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

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
