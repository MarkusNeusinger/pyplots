"""pyplots.ai
bump-basic: Basic Bump Chart
Library: highcharts | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import tempfile
import time
import urllib.request
from pathlib import Path

from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.area import LineSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data: Sports team rankings over a season (6 teams, 6 match weeks)
teams = ["Eagles", "Wolves", "Tigers", "Bears", "Sharks", "Lions"]
weeks = ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Week 6"]

# Rankings for each team across weeks (1 = best, 6 = worst)
# Designed to show various patterns: overtakes, stability, rise, fall
rankings = {
    "Eagles": [3, 2, 1, 1, 2, 1],  # Rise to top, brief dip, reclaim
    "Wolves": [1, 1, 2, 3, 3, 2],  # Start strong, fade then recover
    "Tigers": [4, 3, 3, 2, 1, 3],  # Steady rise to peak, then drop
    "Bears": [2, 4, 4, 4, 4, 4],  # Early drop, stabilize mid-table
    "Sharks": [5, 5, 5, 5, 5, 5],  # Consistently 5th
    "Lions": [6, 6, 6, 6, 6, 6],  # Consistently last
}

# Colorblind-safe palette for 6 teams
colors = ["#306998", "#FFD43B", "#9467BD", "#17BECF", "#E377C2", "#8C564B"]

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {
    "type": "line",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginLeft": 250,
    "marginRight": 250,
    "marginBottom": 250,
    "spacingTop": 100,
}

# Title
chart.options.title = {
    "text": "bump-basic · highcharts · pyplots.ai",
    "style": {"fontSize": "72px", "fontWeight": "bold"},
}

# Subtitle
chart.options.subtitle = {"text": "League Standings Over Season", "style": {"fontSize": "48px"}}

# X-axis (weeks)
chart.options.x_axis = {
    "categories": weeks,
    "title": {"text": "Match Week", "style": {"fontSize": "48px"}, "margin": 30},
    "labels": {"style": {"fontSize": "36px"}, "y": 50},
    "lineWidth": 2,
    "tickWidth": 2,
    "gridLineWidth": 1,
    "gridLineColor": "#e0e0e0",
}

# Y-axis (rankings - inverted so rank 1 is at top)
chart.options.y_axis = {
    "title": {"text": "Rank Position", "style": {"fontSize": "48px"}, "margin": 30},
    "labels": {"style": {"fontSize": "36px"}, "x": -15},
    "reversed": True,  # Rank 1 at top
    "min": 1,
    "max": 6,
    "tickInterval": 1,
    "gridLineWidth": 1,
    "gridLineDashStyle": "Dash",
    "gridLineColor": "#e0e0e0",
}

# Legend
chart.options.legend = {
    "enabled": True,
    "layout": "vertical",
    "align": "right",
    "verticalAlign": "middle",
    "itemStyle": {"fontSize": "36px"},
    "itemMarginBottom": 15,
}

# Plot options for line styling - bump charts need clear markers
chart.options.plot_options = {"line": {"lineWidth": 6, "marker": {"enabled": True, "radius": 14, "symbol": "circle"}}}

# Add series for each team
series_list = []
for i, team in enumerate(teams):
    series = LineSeries()
    series.name = team
    series.data = rankings[team]
    series.color = colors[i]
    series_list.append(series)

chart.options.series = series_list

# Download Highcharts JS (required for headless Chrome)
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

# Write temp HTML and take screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Also save as plot.html for interactive version
Path("plot.html").write_text(html_content, encoding="utf-8")

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
