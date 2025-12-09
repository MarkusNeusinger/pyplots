"""
ridgeline-basic: Ridgeline Plot
Library: highcharts
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.area import AreaSplineSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Simple KDE implementation using Gaussian kernel
def gaussian_kde(data, x_points, bandwidth=None):
    """Compute kernel density estimate using Gaussian kernel."""
    n = len(data)
    if bandwidth is None:
        bandwidth = 1.06 * np.std(data) * n ** (-1 / 5)
    density = np.zeros_like(x_points, dtype=float)
    for xi in data:
        density += np.exp(-0.5 * ((x_points - xi) / bandwidth) ** 2)
    density /= n * bandwidth * np.sqrt(2 * np.pi)
    return density


# Data - Monthly temperature distributions
np.random.seed(42)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
base_temps = [5, 7, 12, 16, 20, 24, 26, 25, 21, 15, 10, 6]

# Generate distributions for each month
n_samples = 200
distributions = {}
for i, month in enumerate(months):
    distributions[month] = np.random.normal(base_temps[i], 3, n_samples)

# KDE parameters - temperature range
x_range = np.linspace(-5, 35, 150)

# Color palette (gradient from cool to warm colors)
colors = [
    "#306998",  # Python Blue (Jan - winter)
    "#3B7CA5",  # Feb
    "#4B8FB0",  # Mar
    "#5CA2B5",  # Apr
    "#6DB5B8",  # May
    "#7EC8B0",  # Jun
    "#059669",  # Jul - Teal Green (summer)
    "#5CA87A",  # Aug
    "#8FB85A",  # Sep
    "#C2C83A",  # Oct
    "#FFD43B",  # Nov - Python Yellow
    "#306998",  # Dec - back to winter
]

# Create chart with container
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration - standard (not inverted) for horizontal ridgelines
chart.options.chart = {
    "type": "areaspline",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "spacing": [80, 80, 80, 150],
}

# Title
chart.options.title = {
    "text": "Monthly Temperature Distribution",
    "style": {"fontSize": "56px", "fontWeight": "bold"},
    "y": 40,
}

# Subtitle
chart.options.subtitle = {
    "text": "Daily temperature variation by month (Ridgeline Plot)",
    "style": {"fontSize": "36px", "color": "#666666"},
    "y": 90,
}

# X-axis - Temperature values
chart.options.x_axis = {
    "title": {"text": "Temperature (°C)", "style": {"fontSize": "40px"}},
    "labels": {"style": {"fontSize": "32px"}},
    "min": -5,
    "max": 35,
    "tickInterval": 5,
    "gridLineWidth": 1,
    "gridLineColor": "rgba(0, 0, 0, 0.08)",
}

# Build y-axis labels for months
y_axis_labels = []
for i, month in enumerate(months):
    y_pos = (len(months) - 1 - i) * 0.7 + 0.3  # overlap_factor
    y_axis_labels.append(
        {
            "value": y_pos,
            "width": 0,
            "label": {
                "text": month,
                "align": "right",
                "x": -20,
                "style": {"fontSize": "32px", "fontWeight": "bold", "color": colors[i]},
            },
        }
    )

# Y-axis - Hidden, distributions use relative positioning
chart.options.y_axis = {
    "title": {"text": None},
    "labels": {"enabled": False},
    "gridLineWidth": 0,
    "min": 0,
    "max": 12,  # 12 months
    "plotLines": y_axis_labels,
}

# Plot options for ridgeline appearance
chart.options.plot_options = {
    "areaspline": {"fillOpacity": 0.7, "lineWidth": 2, "marker": {"enabled": False}, "trackByArea": True},
    "series": {"states": {"hover": {"enabled": True, "lineWidthPlus": 1}}, "animation": False},
}

# Create series for each month (Jan at top, Dec at bottom)
overlap_factor = 0.7  # Controls vertical overlap between distributions
scale_factor = 0.9  # Controls height of each distribution

for i, month in enumerate(months):
    # Calculate KDE for this month's distribution
    density = gaussian_kde(distributions[month], x_range)
    # Normalize density to [0, 1]
    density = density / density.max()

    # Calculate y-offset for this month (Jan at top = index 11, Dec at bottom = index 0)
    y_offset = (len(months) - 1 - i) * overlap_factor

    # Create data points: [x, y] where y = offset + scaled_density
    data_points = []
    for x_val, d_val in zip(x_range, density, strict=True):
        data_points.append([float(x_val), float(y_offset + d_val * scale_factor)])

    series = AreaSplineSeries()
    series.name = month
    series.data = data_points
    series.color = colors[i]
    series.fill_opacity = 0.75
    series.line_color = colors[i]
    series.line_width = 2
    series.threshold = float(y_offset)  # Fill from this baseline

    chart.add_series(series)

# Legend
chart.options.legend = {"enabled": False}

# Credits
chart.options.credits = {"enabled": False}

# Tooltip
chart.options.tooltip = {
    "enabled": True,
    "headerFormat": "<b>{series.name}</b><br/>",
    "pointFormat": "Temperature: {point.x:.1f}°C",
    "style": {"fontSize": "28px"},
}

# Download Highcharts JS
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

# Save HTML file for interactive version
with open("plot.html", "w", encoding="utf-8") as f:
    html_output = (
        """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://code.highcharts.com/highcharts.js"></script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 100%; height: 100vh;"></div>
    <script>"""
        + html_str
        + """</script>
</body>
</html>"""
    )
    f.write(html_output)

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
