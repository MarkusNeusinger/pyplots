"""pyplots.ai
facet-grid: Faceted Grid Plot
Library: highcharts | Python 3.13
Quality: pending | Created: 2025-12-30
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - synthetic dataset for faceted visualization
np.random.seed(42)

# Create data with two faceting variables (Region and Season)
regions = ["North", "South", "East"]
seasons = ["Spring", "Summer"]
n_per_group = 25

data_by_facet = {}
for region in regions:
    for season in seasons:
        # Generate correlated data with group-specific patterns
        base_x = np.random.uniform(10, 90, n_per_group)
        noise = np.random.normal(0, 8, n_per_group)

        # Different slopes and intercepts per group for variety
        slope = 0.5 + (regions.index(region) * 0.2) + (seasons.index(season) * 0.15)
        intercept = 10 + (regions.index(region) * 5) - (seasons.index(season) * 3)

        y = intercept + slope * base_x + noise
        data_by_facet[(region, season)] = (base_x.tolist(), y.tolist())

# Chart dimensions
width = 4800
height = 2700
n_cols = len(seasons)
n_rows = len(regions)

# Calculate subplot dimensions with margins
margin_top = 200
margin_bottom = 150
margin_left = 200
margin_right = 100
gap_x = 80
gap_y = 100

plot_area_width = width - margin_left - margin_right
plot_area_height = height - margin_top - margin_bottom
subplot_width = (plot_area_width - (n_cols - 1) * gap_x) // n_cols
subplot_height = (plot_area_height - (n_rows - 1) * gap_y) // n_rows

# Colors for scatter points
point_color = "#306998"

# Download Highcharts JS
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# Build chart configurations for each facet
charts_js = []
chart_divs = []

for i, region in enumerate(regions):
    for j, season in enumerate(seasons):
        x_data, y_data = data_by_facet[(region, season)]
        data_points = [[x, y] for x, y in zip(x_data, y_data, strict=True)]

        # Calculate position
        left = margin_left + j * (subplot_width + gap_x)
        top = margin_top + i * (subplot_height + gap_y)

        chart_id = f"chart_{i}_{j}"
        chart_divs.append(
            f'<div id="{chart_id}" style="position:absolute; left:{left}px; '
            f'top:{top}px; width:{subplot_width}px; height:{subplot_height}px;"></div>'
        )

        # Determine axis visibility
        show_y_title = j == 0
        show_x_title = i == n_rows - 1

        chart_config = f"""
Highcharts.chart('{chart_id}', {{
    chart: {{
        type: 'scatter',
        backgroundColor: '#ffffff',
        animation: false,
        style: {{ fontFamily: 'Arial, sans-serif' }}
    }},
    title: {{
        text: '{region} · {season}',
        style: {{ fontSize: '28px', fontWeight: 'bold', color: '#333333' }}
    }},
    xAxis: {{
        min: 0,
        max: 100,
        title: {{
            text: {'"Measurement X" ' if show_x_title else "null"},
            style: {{ fontSize: '22px', color: '#333333' }}
        }},
        labels: {{ style: {{ fontSize: '18px', color: '#555555' }} }},
        gridLineWidth: 1,
        gridLineColor: 'rgba(0,0,0,0.1)',
        lineWidth: 2,
        lineColor: '#333333'
    }},
    yAxis: {{
        min: 0,
        max: 100,
        title: {{
            text: {'"Response Y" ' if show_y_title else "null"},
            style: {{ fontSize: '22px', color: '#333333' }}
        }},
        labels: {{ style: {{ fontSize: '18px', color: '#555555' }} }},
        gridLineWidth: 1,
        gridLineColor: 'rgba(0,0,0,0.1)'
    }},
    legend: {{ enabled: false }},
    credits: {{ enabled: false }},
    plotOptions: {{
        scatter: {{
            marker: {{
                radius: 10,
                fillColor: '{point_color}',
                lineWidth: 1,
                lineColor: '#1a4d73',
                symbol: 'circle'
            }},
            states: {{ hover: {{ enabled: false }} }}
        }}
    }},
    series: [{{
        name: 'Data',
        data: {data_points},
        color: '{point_color}'
    }}]
}});
"""
        charts_js.append(chart_config)

# Main title
main_title = "facet-grid · highcharts · pyplots.ai"

# Build complete HTML
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
</head>
<body style="margin:0; background-color:#ffffff;">
    <div style="position:relative; width:{width}px; height:{height}px;">
        <!-- Main title -->
        <div style="position:absolute; left:0; top:0; width:{width}px; text-align:center;
                    font-size:42px; font-weight:bold; font-family:Arial,sans-serif;
                    color:#333333; padding-top:40px;">
            {main_title}
        </div>

        <!-- Row labels (left side) -->
        <div style="position:absolute; left:40px; top:{margin_top}px;
                    width:120px; height:{plot_area_height}px; display:flex;
                    flex-direction:column; justify-content:space-around;">
            {"".join(f'<div style="font-size:26px; font-weight:bold; color:#306998; text-align:center; height:{subplot_height}px; display:flex; align-items:center; justify-content:center; writing-mode:vertical-rl; transform:rotate(180deg);">{region}</div>' for region in regions)}
        </div>

        <!-- Column labels (top) -->
        <div style="position:absolute; left:{margin_left}px; top:{margin_top - 60}px;
                    width:{plot_area_width}px; display:flex; justify-content:space-around;">
            {"".join(f'<div style="font-size:26px; font-weight:bold; color:#306998; width:{subplot_width}px; text-align:center;">{season}</div>' for season in seasons)}
        </div>

        <!-- Chart containers -->
        {"".join(chart_divs)}
    </div>
    <script>
        {"".join(charts_js)}
    </script>
</body>
</html>"""

# Save HTML for interactive version
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Export to PNG using Selenium
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument(f"--window-size={width},{height}")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()
