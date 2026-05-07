""" anyplot.ai
windrose-basic: Wind Rose Chart
Library: highcharts unknown | Python 3.13.13
Quality: 76/100 | Updated: 2026-05-07
"""

import json
import os
import tempfile
import time
from pathlib import Path

import numpy as np
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Theme tokens
THEME = os.getenv("ANYPLOT_THEME", "light")
PAGE_BG = "#FAF8F1" if THEME == "light" else "#1A1A17"
ELEVATED_BG = "#FFFDF6" if THEME == "light" else "#242420"
INK = "#1A1A17" if THEME == "light" else "#F0EFE8"
INK_SOFT = "#4A4A44" if THEME == "light" else "#B8B7B0"
GRID = "rgba(26,26,23,0.10)" if THEME == "light" else "rgba(240,239,232,0.10)"

# Data - Simulated hourly wind measurements (8760 observations, one year)
np.random.seed(42)
n_obs = 8760

# Create wind directions with prevailing westerly pattern
direction_base = np.concatenate(
    [
        np.random.normal(270, 40, int(n_obs * 0.35)),
        np.random.normal(225, 30, int(n_obs * 0.20)),
        np.random.normal(180, 50, int(n_obs * 0.15)),
        np.random.normal(315, 35, int(n_obs * 0.15)),
        np.random.uniform(0, 360, int(n_obs * 0.15)),
    ]
)
directions = direction_base[:n_obs] % 360

# Create wind speeds with Weibull-like distribution
speeds = np.random.weibull(2, n_obs) * 6

# Define direction bins (8 sectors)
dir_bins = np.arange(0, 361, 45)
dir_labels = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

# Define speed bins (m/s)
speed_bins = [0, 3, 6, 9, 12, np.inf]
speed_labels = ["0-3", "3-6", "6-9", "9-12", ">12"]

# Adjust directions for binning (shift so N is centered at 0)
dir_shifted = (directions + 22.5) % 360
dir_indices = np.digitize(dir_shifted, dir_bins) - 1
dir_indices = np.clip(dir_indices, 0, 7)

# Calculate frequencies for each direction/speed combination
speed_indices = np.digitize(speeds, speed_bins[:-1]) - 1
speed_indices = np.clip(speed_indices, 0, len(speed_labels) - 1)

freq_matrix = np.zeros((8, len(speed_labels)))
for d_idx in range(8):
    for s_idx in range(len(speed_labels)):
        mask = (dir_indices == d_idx) & (speed_indices == s_idx)
        freq_matrix[d_idx, s_idx] = np.sum(mask)

# Convert to percentages
total_obs = len(directions)
freq_pct = (freq_matrix / total_obs) * 100

# Colors - viridis-inspired for continuous speed data (cool to warm)
colors = ["#440154", "#31688e", "#35b779", "#fde724", "#ff6e3a"]

# Build Highcharts series data for polar column chart
series_data = []
for s_idx, (speed_label, color) in enumerate(zip(speed_labels, colors, strict=True)):
    data_points = []
    for d_idx, dir_label in enumerate(dir_labels):
        data_points.append({"name": dir_label, "y": round(freq_pct[d_idx, s_idx], 2)})
    series_data.append({"name": f"{speed_label} m/s", "data": data_points, "color": color})

# Build the Highcharts configuration for polar chart
chart_config = {
    "chart": {
        "polar": True,
        "type": "column",
        "width": 4800,
        "height": 2700,
        "backgroundColor": PAGE_BG,
        "marginTop": 120,
        "marginBottom": 80,
        "marginRight": 200,
        "marginLeft": 100,
    },
    "title": {
        "text": "windrose-basic · highcharts · anyplot.ai",
        "style": {"fontSize": "28px", "color": INK, "fontWeight": "normal"},
        "y": 30,
    },
    "pane": {"size": "70%", "center": ["45%", "50%"]},
    "legend": {
        "align": "right",
        "verticalAlign": "middle",
        "layout": "vertical",
        "x": -40,
        "y": 0,
        "itemStyle": {"fontSize": "18px", "color": INK_SOFT},
        "backgroundColor": ELEVATED_BG,
        "borderColor": INK_SOFT,
        "borderWidth": 1,
        "symbolRadius": 3,
        "symbolHeight": 14,
        "symbolWidth": 14,
        "itemMarginBottom": 8,
    },
    "xAxis": {
        "tickmarkPlacement": "on",
        "categories": dir_labels,
        "labels": {"style": {"fontSize": "18px", "color": INK_SOFT}, "distance": 15},
        "lineColor": INK_SOFT,
        "tickColor": INK_SOFT,
    },
    "yAxis": {
        "min": 0,
        "endOnTick": False,
        "showLastLabel": True,
        "title": {"text": "Frequency (%)", "style": {"fontSize": "22px", "color": INK}},
        "labels": {"style": {"fontSize": "18px", "color": INK_SOFT}, "format": "{value}%"},
        "reversedStacks": False,
        "gridLineWidth": 1,
        "gridLineColor": GRID,
        "lineColor": INK_SOFT,
        "tickColor": INK_SOFT,
    },
    "tooltip": {"valueSuffix": "%", "style": {"fontSize": "16px", "color": INK}},
    "plotOptions": {
        "series": {
            "stacking": "normal",
            "shadow": False,
            "groupPadding": 0,
            "pointPlacement": "on",
            "borderWidth": 1,
            "borderColor": PAGE_BG,
        }
    },
    "series": series_data,
}

# Convert config to JavaScript
chart_js = json.dumps(chart_config)

# Download Highcharts JS and Highcharts More (for polar charts)
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

try:
    highcharts_url = "https://code.highcharts.com/highcharts.js"
    resp = requests.get(highcharts_url, headers=headers, timeout=30)
    resp.raise_for_status()
    highcharts_js = resp.text
except Exception:
    highcharts_url = "https://cdn.jsdelivr.net/npm/highcharts@11.0.1/highcharts.js"
    resp = requests.get(highcharts_url, headers=headers, timeout=30)
    resp.raise_for_status()
    highcharts_js = resp.text

try:
    highcharts_more_url = "https://code.highcharts.com/highcharts-more.js"
    resp_more = requests.get(highcharts_more_url, headers=headers, timeout=30)
    resp_more.raise_for_status()
    highcharts_more_js = resp_more.text
except Exception:
    highcharts_more_url = "https://cdn.jsdelivr.net/npm/highcharts@11.0.1/highcharts-more.js"
    resp_more = requests.get(highcharts_more_url, headers=headers, timeout=30)
    resp_more.raise_for_status()
    highcharts_more_js = resp_more.text

# Generate HTML with inline scripts
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{highcharts_more_js}</script>
</head>
<body style="margin:0; background-color:{PAGE_BG};">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>
        Highcharts.chart('container', {chart_js});
    </script>
</body>
</html>"""

# Save HTML artifact (both themes)
with open(f"plot-{THEME}.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Write temp HTML and take screenshot for PNG
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
driver.save_screenshot(f"plot-{THEME}.png")
driver.quit()

Path(temp_path).unlink()
