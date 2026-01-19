""" pyplots.ai
bar-realtime: Real-Time Updating Bar Chart
Library: highcharts unknown | Python 3.13.11
Quality: 91/100 | Created: 2026-01-19
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.bar import ColumnSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Live service metrics simulation with current and previous values for motion effect
np.random.seed(42)
categories = ["API Gateway", "Auth Service", "Database", "Cache", "Queue", "CDN"]
current_values = np.random.randint(150, 450, size=len(categories))
# Generate realistic changes: +/- 5-15% of current value, with controlled mix of increases/decreases
change_percentages = np.array([0.08, -0.10, 0.12, 0.05, -0.07, 0.15])  # Fixed mix of positive/negative
changes = (current_values * change_percentages).astype(int)
previous_values = current_values - changes

# Colors - using colorblind-safe palette (blue for increases, orange for decreases - NOT red/green)
increase_color = "#306998"  # Blue
decrease_color = "#E07B39"  # Orange (colorblind-safe alternative to red/green)
colors = [increase_color if changes[i] >= 0 else decrease_color for i in range(len(categories))]

# Create chart with container
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration for 4800x2700
chart.options.chart = {
    "type": "column",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "marginBottom": 300,
    "marginLeft": 200,
    "animation": {"duration": 1000},
}

# Title with real-time indicator
chart.options.title = {
    "text": "bar-realtime · highcharts · pyplots.ai",
    "style": {"fontSize": "72px", "fontWeight": "bold"},
}

chart.options.subtitle = {
    "text": "● LIVE — Service Throughput (requests/sec)",
    "style": {"fontSize": "48px", "color": "#059669"},
}

# X-axis with categories
chart.options.x_axis = {
    "categories": categories.tolist() if hasattr(categories, "tolist") else list(categories),
    "title": {"text": "Service", "style": {"fontSize": "48px"}},
    "labels": {"style": {"fontSize": "36px"}},
}

# Y-axis
chart.options.y_axis = {
    "title": {"text": "Requests per Second", "style": {"fontSize": "48px"}},
    "labels": {"style": {"fontSize": "36px"}},
    "min": 0,
    "gridLineWidth": 2,
    "gridLineColor": "#e5e7eb",
}

# Legend - clear distinction between Previous (ghost) and Current values
chart.options.legend = {
    "enabled": True,
    "itemStyle": {"fontSize": "40px", "fontWeight": "bold"},
    "align": "right",
    "verticalAlign": "top",
    "layout": "vertical",
    "x": -50,
    "y": 100,
}

# Plot options with animation settings
chart.options.plot_options = {
    "column": {
        "animation": {"duration": 1000, "easing": "easeOutBounce"},
        "borderRadius": 8,
        "dataLabels": {
            "enabled": True,
            "format": "{y}",
            "style": {"fontSize": "32px", "fontWeight": "bold", "textOutline": "none"},
        },
    }
}

# Add previous values as ghost bars (showing motion effect)
ghost_series = ColumnSeries()
ghost_series.data = [{"y": int(v), "color": "#d1d5db"} for v in previous_values]
ghost_series.name = "Previous"
ghost_series.opacity = 0.4
ghost_series.enable_mouse_tracking = False
chart.add_series(ghost_series)

# Add current values as main bars
current_series = ColumnSeries()
current_series.data = [{"y": int(current_values[i]), "color": colors[i]} for i in range(len(categories))]
current_series.name = "Current"
chart.add_series(current_series)

# Add annotations for change indicators - using colorblind-safe colors (blue/orange, NOT red/green)
annotations_data = []
increase_indicator_color = "#306998"  # Blue for positive change
decrease_indicator_color = "#E07B39"  # Orange for negative change (colorblind-safe)
for i, (curr, change) in enumerate(zip(current_values, changes, strict=True)):
    symbol = "▲" if change >= 0 else "▼"
    color = increase_indicator_color if change >= 0 else decrease_indicator_color
    annotations_data.append(
        {
            "point": {"x": i, "y": int(curr), "xAxis": 0, "yAxis": 0},
            "text": f"{symbol} {abs(change)}",
            "style": {"fontSize": "28px", "color": color, "fontWeight": "bold"},
            "y": -60,
        }
    )

chart.options.annotations = [
    {"labels": annotations_data, "labelOptions": {"backgroundColor": "transparent", "borderWidth": 0, "shape": "rect"}}
]

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

# Save HTML for interactive version
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Take screenshot with Selenium
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
