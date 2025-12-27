""" pyplots.ai
forest-basic: Meta-Analysis Forest Plot
Library: highcharts unknown | Python 3.13.11
Quality: 78/100 | Created: 2025-12-27
"""

import tempfile
import time
import urllib.request
from pathlib import Path

from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.scatter import ScatterSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data: Meta-analysis of treatment effect studies (mean difference)
studies = [
    "Smith et al. 2018",
    "Johnson et al. 2019",
    "Williams et al. 2019",
    "Brown et al. 2020",
    "Davis et al. 2020",
    "Miller et al. 2021",
    "Wilson et al. 2021",
    "Moore et al. 2022",
    "Taylor et al. 2022",
    "Anderson et al. 2023",
]

# Effect sizes (mean differences) with confidence intervals
effect_sizes = [-0.35, 0.12, -0.52, -0.28, 0.05, -0.41, -0.18, -0.55, -0.22, -0.38]
ci_lower = [-0.68, -0.21, -0.88, -0.55, -0.32, -0.72, -0.48, -0.91, -0.52, -0.65]
ci_upper = [-0.02, 0.45, -0.16, -0.01, 0.42, -0.10, 0.12, -0.19, 0.08, -0.11]
weights = [8.5, 6.2, 9.1, 10.3, 5.8, 8.9, 7.4, 6.8, 9.5, 11.2]  # Study weights (%)

# Pooled estimate (diamond)
pooled_effect = -0.28
pooled_ci_lower = -0.42
pooled_ci_upper = -0.14

# Create chart with container
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {
    "type": "scatter",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginLeft": 350,
    "marginRight": 150,
    "marginBottom": 150,
    "marginTop": 120,
}

# Title
chart.options.title = {
    "text": "forest-basic · highcharts · pyplots.ai",
    "style": {"fontSize": "48px", "fontWeight": "bold"},
}

chart.options.subtitle = {"text": "Meta-Analysis of Treatment Effect on Primary Outcome", "style": {"fontSize": "32px"}}

# Y-axis labels: studies at top, pooled at bottom (reversed order for categories)
all_labels = ["Pooled Estimate", ""] + list(reversed(studies))
n_studies = len(studies)

# X-axis (effect size)
chart.options.x_axis = {
    "title": {"text": "Mean Difference (95% CI)", "style": {"fontSize": "32px"}},
    "labels": {"style": {"fontSize": "24px"}},
    "plotLines": [
        {
            "value": 0,
            "color": "#666666",
            "width": 3,
            "dashStyle": "Dash",
            "zIndex": 3,
            "label": {"text": "No Effect", "style": {"fontSize": "20px", "color": "#666666"}, "rotation": 0, "y": -10},
        }
    ],
    "min": -1.2,
    "max": 0.8,
    "gridLineWidth": 1,
    "gridLineColor": "#e0e0e0",
}

# Y-axis (studies)
chart.options.y_axis = {
    "title": {"text": None},
    "categories": all_labels,
    "reversed": False,
    "labels": {"style": {"fontSize": "26px"}},
    "gridLineWidth": 0,
    "min": 0,
    "max": len(all_labels) - 1,
    "tickPositions": list(range(len(all_labels))),
}

# Disable legend (we use labels)
chart.options.legend = {"enabled": False}

# Create series for study points (map indices: study 0 -> y = n_studies+1, study 1 -> y = n_studies, etc.)
study_points_data = []
for i, (es, w) in enumerate(zip(effect_sizes, weights)):
    # Marker radius proportional to weight (scaled for visibility)
    radius = 8 + (w / max(weights)) * 16
    y_pos = n_studies + 1 - i  # First study at top (y = n_studies+1), last at y = 2
    study_points_data.append({"x": es, "y": y_pos, "marker": {"radius": radius, "symbol": "square"}})

study_series = ScatterSeries()
study_series.data = study_points_data
study_series.name = "Study Effect"
study_series.color = "#306998"
study_series.marker = {"symbol": "square", "lineWidth": 2, "lineColor": "#306998"}

chart.add_series(study_series)

# Create series for confidence interval lines
for i, (lower, upper) in enumerate(zip(ci_lower, ci_upper)):
    y_pos = n_studies + 1 - i
    ci_series = ScatterSeries()
    ci_series.data = [{"x": lower, "y": y_pos}, {"x": upper, "y": y_pos}]
    ci_series.name = f"CI {i}"
    ci_series.color = "#306998"
    ci_series.marker = {"enabled": False}
    ci_series.enable_mouse_tracking = False
    ci_series.show_in_legend = False
    ci_series.line_width = 3
    ci_series.type = "line"
    chart.add_series(ci_series)

# Pooled estimate (diamond) - at y = 0
pooled_y = 0

# Create diamond shape for pooled estimate
diamond_series = ScatterSeries()
diamond_series.data = [{"x": pooled_effect, "y": pooled_y}]
diamond_series.name = "Pooled Estimate"
diamond_series.color = "#FFD43B"
diamond_series.marker = {
    "symbol": "diamond",
    "radius": 20,
    "lineWidth": 3,
    "lineColor": "#306998",
    "fillColor": "#FFD43B",
}

chart.add_series(diamond_series)

# CI line for pooled estimate
pooled_ci_series = ScatterSeries()
pooled_ci_series.data = [{"x": pooled_ci_lower, "y": pooled_y}, {"x": pooled_ci_upper, "y": pooled_y}]
pooled_ci_series.name = "Pooled CI"
pooled_ci_series.color = "#306998"
pooled_ci_series.marker = {"enabled": False}
pooled_ci_series.line_width = 4
pooled_ci_series.type = "line"
pooled_ci_series.enable_mouse_tracking = False
pooled_ci_series.show_in_legend = False

chart.add_series(pooled_ci_series)

# Tooltip
chart.options.tooltip = {
    "headerFormat": "",
    "pointFormat": "<b>{point.name}</b><br/>Effect: {point.x:.2f}",
    "style": {"fontSize": "20px"},
}

# Credits
chart.options.credits = {"enabled": False}

# Download Highcharts JS for inline embedding
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# Generate HTML with inline scripts
html_str = chart.to_js_literal()
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>{html_str}</script>
</body>
</html>"""

# Save HTML file
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

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
time.sleep(5)  # Wait for chart to render
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()  # Clean up temp file
