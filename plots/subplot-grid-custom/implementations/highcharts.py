"""pyplots.ai
subplot-grid-custom: Custom Subplot Grid Layout
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


# Data - Generate sample dashboard data
np.random.seed(42)

# Main time series (stock price - spans 2 columns)
days = 90
dates = [f"Day {i + 1}" for i in range(days)]
base_price = 150
returns = np.random.randn(days) * 2
price = base_price + np.cumsum(returns)
price_data = [[i, float(price[i])] for i in range(days)]

# Volume data (bar chart - 1 cell)
volume = np.random.uniform(1, 5, days) * 1e6
volume_data = [[i, float(volume[i] / 1e6)] for i in range(days)]

# Returns distribution (histogram - 1 cell)
daily_returns = np.diff(price) / price[:-1] * 100
hist_counts, hist_edges = np.histogram(daily_returns, bins=15)
histogram_data = [[float(hist_edges[i]), int(hist_counts[i])] for i in range(len(hist_counts))]

# Performance metrics (scatter - 1 cell)
sectors = ["Tech", "Health", "Finance", "Energy", "Consumer"]
sector_returns = np.random.uniform(-5, 15, len(sectors))
sector_volatility = np.random.uniform(5, 20, len(sectors))
scatter_data = [
    {"x": float(sector_volatility[i]), "y": float(sector_returns[i]), "name": sectors[i]} for i in range(len(sectors))
]

# Build custom HTML with multiple Highcharts in a grid layout
# Use CSS grid to create the custom subplot layout
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# Colors
python_blue = "#306998"
python_yellow = "#FFD43B"
purple = "#9467BD"
cyan = "#17BECF"

# Chart configurations as JS objects
main_chart_config = f"""
{{
    chart: {{
        type: 'line',
        backgroundColor: '#ffffff'
    }},
    title: {{
        text: 'Stock Price (90 Days)',
        style: {{ fontSize: '32px', fontWeight: 'bold' }}
    }},
    xAxis: {{
        title: {{ text: 'Trading Day', style: {{ fontSize: '24px' }} }},
        labels: {{ style: {{ fontSize: '18px' }}, step: 15 }}
    }},
    yAxis: {{
        title: {{ text: 'Price ($)', style: {{ fontSize: '24px' }} }},
        labels: {{ style: {{ fontSize: '18px' }} }},
        gridLineColor: 'rgba(0,0,0,0.1)'
    }},
    legend: {{ enabled: false }},
    credits: {{ enabled: false }},
    plotOptions: {{
        line: {{ lineWidth: 4, marker: {{ radius: 6 }} }}
    }},
    series: [{{
        name: 'Price',
        data: {price_data},
        color: '{python_blue}'
    }}]
}}
"""

volume_chart_config = f"""
{{
    chart: {{
        type: 'column',
        backgroundColor: '#ffffff'
    }},
    title: {{
        text: 'Trading Volume',
        style: {{ fontSize: '28px', fontWeight: 'bold' }}
    }},
    xAxis: {{
        title: {{ text: 'Day', style: {{ fontSize: '20px' }} }},
        labels: {{ style: {{ fontSize: '14px' }}, step: 20 }}
    }},
    yAxis: {{
        title: {{ text: 'Volume (M)', style: {{ fontSize: '20px' }} }},
        labels: {{ style: {{ fontSize: '14px' }} }},
        gridLineColor: 'rgba(0,0,0,0.1)'
    }},
    legend: {{ enabled: false }},
    credits: {{ enabled: false }},
    plotOptions: {{
        column: {{ borderWidth: 0 }}
    }},
    series: [{{
        name: 'Volume',
        data: {volume_data},
        color: '{python_yellow}'
    }}]
}}
"""

histogram_chart_config = f"""
{{
    chart: {{
        type: 'column',
        backgroundColor: '#ffffff'
    }},
    title: {{
        text: 'Returns Distribution',
        style: {{ fontSize: '28px', fontWeight: 'bold' }}
    }},
    xAxis: {{
        title: {{ text: 'Daily Return (%)', style: {{ fontSize: '20px' }} }},
        labels: {{ style: {{ fontSize: '14px' }}, format: '{{value:.1f}}' }}
    }},
    yAxis: {{
        title: {{ text: 'Frequency', style: {{ fontSize: '20px' }} }},
        labels: {{ style: {{ fontSize: '14px' }} }},
        gridLineColor: 'rgba(0,0,0,0.1)'
    }},
    legend: {{ enabled: false }},
    credits: {{ enabled: false }},
    plotOptions: {{
        column: {{ borderWidth: 0, pointPadding: 0, groupPadding: 0 }}
    }},
    series: [{{
        name: 'Frequency',
        data: {histogram_data},
        color: '{purple}'
    }}]
}}
"""

scatter_chart_config = f"""
{{
    chart: {{
        type: 'scatter',
        backgroundColor: '#ffffff'
    }},
    title: {{
        text: 'Risk vs Return by Sector',
        style: {{ fontSize: '28px', fontWeight: 'bold' }}
    }},
    xAxis: {{
        title: {{ text: 'Volatility (%)', style: {{ fontSize: '20px' }} }},
        labels: {{ style: {{ fontSize: '14px' }} }},
        gridLineWidth: 1,
        gridLineColor: 'rgba(0,0,0,0.1)'
    }},
    yAxis: {{
        title: {{ text: 'Return (%)', style: {{ fontSize: '20px' }} }},
        labels: {{ style: {{ fontSize: '14px' }} }},
        gridLineColor: 'rgba(0,0,0,0.1)'
    }},
    legend: {{ enabled: false }},
    credits: {{ enabled: false }},
    tooltip: {{
        formatter: function() {{
            return '<b>' + this.point.name + '</b><br/>Volatility: ' + this.x.toFixed(1) + '%<br/>Return: ' + this.y.toFixed(1) + '%';
        }}
    }},
    plotOptions: {{
        scatter: {{
            marker: {{
                radius: 16,
                symbol: 'circle'
            }},
            dataLabels: {{
                enabled: true,
                format: '{{point.name}}',
                style: {{ fontSize: '16px', fontWeight: 'normal' }},
                y: -20
            }}
        }}
    }},
    series: [{{
        name: 'Sectors',
        data: {scatter_data},
        color: '{cyan}'
    }}]
}}
"""

# Main title for the dashboard
main_title = "subplot-grid-custom · highcharts · pyplots.ai"

html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <style>
        body {{
            margin: 0;
            padding: 40px;
            background: #ffffff;
            font-family: Arial, sans-serif;
        }}
        .dashboard-title {{
            text-align: center;
            font-size: 48px;
            font-weight: bold;
            color: #333;
            margin-bottom: 30px;
            padding: 20px 0;
        }}
        .grid-container {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            grid-template-rows: 1fr 1fr;
            gap: 30px;
            width: 4700px;
            height: 2450px;
        }}
        .chart-cell {{
            background: #ffffff;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
        }}
        .main-chart {{
            grid-column: 1;
            grid-row: 1 / 3;
        }}
        .top-right {{
            grid-column: 2;
            grid-row: 1;
        }}
        .bottom-right-left {{
            grid-column: 2;
            grid-row: 2;
        }}
    </style>
</head>
<body>
    <div class="dashboard-title">{main_title}</div>
    <div class="grid-container">
        <div id="main-chart" class="chart-cell main-chart"></div>
        <div id="volume-chart" class="chart-cell top-right"></div>
        <div id="scatter-chart" class="chart-cell bottom-right-left"></div>
    </div>
    <script>
        // Main chart - spans 2 rows
        Highcharts.chart('main-chart', {main_chart_config});

        // Volume chart - top right
        Highcharts.chart('volume-chart', {volume_chart_config});

        // Scatter chart - bottom right
        Highcharts.chart('scatter-chart', {scatter_chart_config});
    </script>
</body>
</html>"""

# Write temp HTML and take screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Also save as plot.html for interactive version
with open("plot.html", "w", encoding="utf-8") as f:
    # For the standalone HTML, include CDN link instead of inline script
    html_standalone = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <style>
        body {{
            margin: 0;
            padding: 40px;
            background: #ffffff;
            font-family: Arial, sans-serif;
        }}
        .dashboard-title {{
            text-align: center;
            font-size: 48px;
            font-weight: bold;
            color: #333;
            margin-bottom: 30px;
            padding: 20px 0;
        }}
        .grid-container {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            grid-template-rows: 1fr 1fr;
            gap: 30px;
            width: 100%;
            max-width: 1800px;
            height: 900px;
            margin: 0 auto;
        }}
        .chart-cell {{
            background: #ffffff;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
        }}
        .main-chart {{
            grid-column: 1;
            grid-row: 1 / 3;
        }}
        .top-right {{
            grid-column: 2;
            grid-row: 1;
        }}
        .bottom-right-left {{
            grid-column: 2;
            grid-row: 2;
        }}
    </style>
</head>
<body>
    <div class="dashboard-title">{main_title}</div>
    <div class="grid-container">
        <div id="main-chart" class="chart-cell main-chart"></div>
        <div id="volume-chart" class="chart-cell top-right"></div>
        <div id="scatter-chart" class="chart-cell bottom-right-left"></div>
    </div>
    <script>
        Highcharts.chart('main-chart', {main_chart_config});
        Highcharts.chart('volume-chart', {volume_chart_config});
        Highcharts.chart('scatter-chart', {scatter_chart_config});
    </script>
</body>
</html>"""
    f.write(html_standalone)

# Screenshot with Selenium
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
