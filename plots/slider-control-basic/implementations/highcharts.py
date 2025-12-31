"""pyplots.ai
slider-control-basic: Interactive Plot with Slider Control
Library: highcharts | Python 3.13
Quality: pending | Created: 2025-12-31
"""

import json
import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Monthly sales data across 5 years (2019-2023)
np.random.seed(42)
years = [2019, 2020, 2021, 2022, 2023]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Generate sales data with yearly trends
base_sales = np.array([120, 110, 135, 150, 165, 180, 175, 190, 160, 145, 170, 210])
yearly_data = {}
for i, year in enumerate(years):
    growth = 1 + 0.08 * i  # 8% yearly growth
    seasonal = base_sales * growth + np.random.randn(12) * 15
    yearly_data[year] = [round(max(50, v), 1) for v in seasonal]

# Download Highcharts JS
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# Build series data for all years - colorblind-safe palette
colors = ["#306998", "#FFD43B", "#9467BD", "#17BECF", "#8C564B"]
series_configs = []

for i, year in enumerate(years):
    series_configs.append(
        {
            "name": str(year),
            "data": yearly_data[year],
            "color": colors[i % len(colors)],
            "visible": year == 2023,  # Only show 2023 initially
            "lineWidth": 6,
            "marker": {"radius": 14, "symbol": "circle", "lineWidth": 2, "lineColor": "#ffffff"},
        }
    )

# Create Highcharts options with slider control
chart_options = {
    "chart": {
        "type": "line",
        "width": 4800,
        "height": 2200,
        "backgroundColor": "#ffffff",
        "marginBottom": 180,
        "marginTop": 200,
        "marginLeft": 280,
        "marginRight": 120,
        "style": {"fontFamily": "Arial, sans-serif"},
    },
    "title": {
        "text": "slider-control-basic · highcharts · pyplots.ai",
        "style": {"fontSize": "72px", "fontWeight": "bold", "color": "#333333"},
        "y": 80,
    },
    "subtitle": {
        "text": "Monthly Sales by Year - Use slider below to filter by year",
        "style": {"fontSize": "44px", "color": "#666666"},
        "y": 140,
    },
    "xAxis": {
        "categories": months,
        "title": {"text": "Month", "style": {"fontSize": "48px", "color": "#333333"}, "margin": 25},
        "labels": {"style": {"fontSize": "40px", "color": "#333333"}, "y": 35},
        "lineWidth": 3,
        "tickWidth": 3,
        "tickLength": 15,
    },
    "yAxis": {
        "title": {"text": "Sales (thousands USD)", "style": {"fontSize": "48px", "color": "#333333"}, "margin": 25},
        "labels": {"style": {"fontSize": "40px", "color": "#333333"}, "x": -15},
        "gridLineWidth": 2,
        "gridLineColor": "rgba(0,0,0,0.12)",
        "gridLineDashStyle": "Dash",
        "min": 0,
    },
    "legend": {
        "enabled": False  # Disabled - using slider instead
    },
    "tooltip": {
        "enabled": True,
        "style": {"fontSize": "32px"},
        "headerFormat": '<span style="font-size: 32px; font-weight: bold;">{point.key}</span><br/>',
        "pointFormat": '<span style="color:{series.color}">●</span> {series.name}: <b>${point.y:.1f}K</b><br/>',
    },
    "plotOptions": {
        "line": {"lineWidth": 6, "marker": {"radius": 14, "symbol": "circle"}, "states": {"hover": {"lineWidth": 8}}},
        "series": {"animation": False},
    },
    "credits": {"enabled": False},
    "series": series_configs,
}

# Convert to JavaScript - using JSON for clean serialization
chart_json = json.dumps(chart_options)

# Custom slider HTML with JavaScript for interactivity
slider_html = """
<div id="slider-container" style="
    position: absolute;
    bottom: 80px;
    left: 50%;
    transform: translateX(-50%);
    width: 70%;
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    padding: 50px 80px;
    border-radius: 30px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.15);
    text-align: center;
    z-index: 1000;
    border: 3px solid #dee2e6;
">
    <div style="margin-bottom: 30px; font-size: 42px; color: #495057; font-weight: 600;">
        Select Year to Display
    </div>
    <div style="display: flex; align-items: center; justify-content: center; gap: 60px;">
        <span style="font-size: 48px; font-weight: bold; color: #306998;">2019</span>
        <input type="range" id="year-slider" min="2019" max="2023" value="2023" step="1"
            style="
                width: 55%;
                height: 40px;
                cursor: pointer;
                -webkit-appearance: none;
                appearance: none;
                background: linear-gradient(to right, #306998, #FFD43B);
                border-radius: 20px;
                outline: none;
                box-shadow: inset 0 2px 8px rgba(0,0,0,0.2);
            "
        />
        <span style="font-size: 48px; font-weight: bold; color: #FFD43B; text-shadow: 1px 1px 2px #999;">2023</span>
    </div>
    <div id="current-year" style="
        margin-top: 40px;
        font-size: 72px;
        font-weight: bold;
        color: #306998;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    ">2023</div>
</div>
"""

slider_js = """
<script>
document.getElementById('year-slider').addEventListener('input', function() {
    var selectedYear = parseInt(this.value);
    document.getElementById('current-year').textContent = selectedYear;

    var chart = Highcharts.charts[0];
    if (chart) {
        chart.series.forEach(function(series) {
            var seriesYear = parseInt(series.name);
            if (seriesYear === selectedYear) {
                series.show();
            } else {
                series.hide();
            }
        });
    }
});

// Style the slider thumb
var style = document.createElement('style');
style.textContent = `
    #year-slider::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        width: 70px;
        height: 70px;
        background: #306998;
        border-radius: 50%;
        cursor: pointer;
        box-shadow: 0 6px 20px rgba(0,0,0,0.4);
        border: 4px solid #ffffff;
    }
    #year-slider::-moz-range-thumb {
        width: 70px;
        height: 70px;
        background: #306998;
        border-radius: 50%;
        cursor: pointer;
        box-shadow: 0 6px 20px rgba(0,0,0,0.4);
        border: 4px solid #ffffff;
    }
`;
document.head.appendChild(style);
</script>
"""

# Create HTML with embedded Highcharts
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: #ffffff;
        }}
    </style>
</head>
<body>
    <div id="container" style="width: 4800px; height: 2200px;"></div>
    {slider_html}
    <script>
        Highcharts.chart('container', {chart_json});
    </script>
    {slider_js}
</body>
</html>"""

# Save HTML for interactive version
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Screenshot with Selenium
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4800,2700")
chrome_options.add_argument("--force-device-scale-factor=1")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)  # Wait for chart to render
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()  # Clean up temp file
