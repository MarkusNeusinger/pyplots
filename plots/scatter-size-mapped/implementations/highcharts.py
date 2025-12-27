""" pyplots.ai
scatter-size-mapped: Bubble Chart
Library: highcharts unknown | Python 3.13.11
Quality: 91/100 | Created: 2025-12-27
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.bubble import BubbleSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data: Country economic indicators
np.random.seed(42)

# Region colors (colorblind-safe)
regions = ["Americas", "Europe", "Asia", "Africa", "Oceania"]
region_colors = {
    "Americas": "#306998",  # Python Blue
    "Europe": "#FFD43B",  # Python Yellow
    "Asia": "#9467BD",  # Purple
    "Africa": "#17BECF",  # Cyan
    "Oceania": "#8C564B",  # Brown
}

# Generate 40 countries with realistic distributions per region
gdp_per_capita = []
life_expectancy = []
population = []
region_list = []
country_names = []

# Americas (higher GDP, moderate life expectancy)
for i in range(10):
    gdp_per_capita.append(np.random.uniform(15000, 70000))
    life_expectancy.append(np.random.uniform(72, 82))
    population.append(np.random.uniform(5e6, 350e6))
    region_list.append("Americas")
    country_names.append(f"Country A{i + 1}")

# Europe (high GDP, high life expectancy)
for i in range(10):
    gdp_per_capita.append(np.random.uniform(25000, 65000))
    life_expectancy.append(np.random.uniform(78, 85))
    population.append(np.random.uniform(5e6, 85e6))
    region_list.append("Europe")
    country_names.append(f"Country E{i + 1}")

# Asia (wide range of GDP, high life expectancy in developed nations)
for i in range(10):
    gdp_per_capita.append(np.random.uniform(3000, 55000))
    life_expectancy.append(np.random.uniform(65, 85))
    population.append(np.random.uniform(10e6, 1400e6))
    region_list.append("Asia")
    country_names.append(f"Country S{i + 1}")

# Africa (lower GDP, lower life expectancy)
for i in range(7):
    gdp_per_capita.append(np.random.uniform(1000, 15000))
    life_expectancy.append(np.random.uniform(55, 72))
    population.append(np.random.uniform(10e6, 220e6))
    region_list.append("Africa")
    country_names.append(f"Country F{i + 1}")

# Oceania (high GDP, high life expectancy)
for i in range(3):
    gdp_per_capita.append(np.random.uniform(35000, 60000))
    life_expectancy.append(np.random.uniform(80, 84))
    population.append(np.random.uniform(5e6, 30e6))
    region_list.append("Oceania")
    country_names.append(f"Country O{i + 1}")

# Convert to numpy arrays
gdp_per_capita = np.array(gdp_per_capita)
life_expectancy = np.array(life_expectancy)
population = np.array(population)
region_list = np.array(region_list)

# Create chart
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Chart configuration
chart.options.chart = {
    "type": "bubble",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#ffffff",
    "plotBorderWidth": 1,
    "plotBorderColor": "#cccccc",
    "spacingBottom": 100,
    "spacingLeft": 80,
    "marginRight": 320,
}

# Title
chart.options.title = {
    "text": "scatter-size-mapped · highcharts · pyplots.ai",
    "style": {"fontSize": "48px", "fontWeight": "bold"},
}

chart.options.subtitle = {
    "text": "GDP per Capita vs Life Expectancy (bubble size = population)",
    "style": {"fontSize": "32px"},
}

# X-axis (use simple format without special characters that get misinterpreted)
chart.options.x_axis = {
    "title": {"text": "GDP per Capita (USD)", "style": {"fontSize": "36px"}, "margin": 20},
    "labels": {"style": {"fontSize": "28px"}},
    "gridLineWidth": 1,
    "gridLineColor": "#e0e0e0",
    "min": 0,
    "max": 80000,
    "tickInterval": 10000,
}

# Y-axis
chart.options.y_axis = {
    "title": {"text": "Life Expectancy (years)", "style": {"fontSize": "36px"}, "margin": 20},
    "labels": {"style": {"fontSize": "28px"}},
    "gridLineWidth": 1,
    "gridLineColor": "#e0e0e0",
    "min": 50,
    "max": 90,
    "tickInterval": 5,
}

# Legend
chart.options.legend = {
    "enabled": True,
    "align": "right",
    "verticalAlign": "middle",
    "layout": "vertical",
    "itemStyle": {"fontSize": "28px"},
    "symbolHeight": 24,
    "symbolWidth": 24,
    "symbolRadius": 12,
}

# Plot options for bubble series
chart.options.plot_options = {
    "bubble": {
        "minSize": 40,
        "maxSize": 150,
        "opacity": 0.7,
        "dataLabels": {"enabled": False},
        "marker": {"lineWidth": 3, "lineColor": "#ffffff"},
    }
}

# Tooltip (single line format to avoid JS syntax errors from newlines)
chart.options.tooltip = {
    "useHTML": True,
    "headerFormat": '<span style="font-size: 24px; font-weight: bold;">{series.name}</span><br/>',
    "pointFormat": '<span style="font-size: 20px;">GDP: <b>${point.x:,.0f}</b><br/>Life Exp: <b>{point.y:.1f} yrs</b><br/>Pop: <b>{point.z:,.0f}</b></span>',
    "style": {"fontSize": "20px"},
}

# Add series by region (for legend colors)
for region in regions:
    mask = region_list == region
    if not np.any(mask):
        continue

    # Use array format [x, y, z] for bubble data (dict format loses x values)
    series_data = []
    for i in np.where(mask)[0]:
        series_data.append([float(gdp_per_capita[i]), float(life_expectancy[i]), float(population[i])])

    series = BubbleSeries()
    series.data = series_data
    series.name = region
    series.color = region_colors[region]
    chart.add_series(series)

# Download Highcharts JS and highcharts-more for bubble charts
highcharts_url = "https://code.highcharts.com/highcharts.js"
highcharts_more_url = "https://code.highcharts.com/highcharts-more.js"

with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

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
<body style="margin:0; padding:0; background-color:#ffffff;">
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
