"""pyplots.ai
subplot-grid-custom: Custom Subplot Grid Layout
Library: highcharts unknown | Python 3.13.11
Quality: 82/100 | Created: 2025-12-30
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

# Main time series (stock price - spans 2x2 cells)
days = 90
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

# Moving average data (line chart - 1 cell)
ma_20 = np.convolve(price, np.ones(20) / 20, mode="valid")
ma_data = [[i, float(ma_20[i])] for i in range(len(ma_20))]

# Build custom HTML with multiple Highcharts in a grid layout
# Use CSS grid to create the custom subplot layout
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# Colors - colorblind-safe palette
python_blue = "#306998"
python_yellow = "#FFD43B"
purple = "#9467BD"
cyan = "#17BECF"
brown = "#8C564B"

# Chart configurations as JS objects
# Main chart - large, spans 2x2
main_chart_config = f"""
{{
    chart: {{
        type: 'line',
        backgroundColor: '#ffffff'
    }},
    title: {{
        text: 'Stock Price (90 Days)',
        style: {{ fontSize: '44px', fontWeight: 'bold' }}
    }},
    xAxis: {{
        title: {{ text: 'Trading Day', style: {{ fontSize: '32px' }} }},
        labels: {{ style: {{ fontSize: '24px' }}, step: 15 }}
    }},
    yAxis: {{
        title: {{ text: 'Price ($)', style: {{ fontSize: '32px' }} }},
        labels: {{ style: {{ fontSize: '24px' }} }},
        gridLineColor: 'rgba(0,0,0,0.1)'
    }},
    legend: {{ enabled: true, itemStyle: {{ fontSize: '24px' }} }},
    credits: {{ enabled: false }},
    plotOptions: {{
        line: {{ lineWidth: 5, marker: {{ radius: 8 }} }}
    }},
    series: [{{
        name: 'Daily Price',
        data: {price_data},
        color: '{python_blue}'
    }}]
}}
"""

# Volume chart - detail view
volume_chart_config = f"""
{{
    chart: {{
        type: 'column',
        backgroundColor: '#ffffff'
    }},
    title: {{
        text: 'Trading Volume',
        style: {{ fontSize: '40px', fontWeight: 'bold' }}
    }},
    xAxis: {{
        title: {{ text: 'Day', style: {{ fontSize: '26px' }} }},
        labels: {{ style: {{ fontSize: '20px' }}, step: 20 }}
    }},
    yAxis: {{
        title: {{ text: 'Volume (M)', style: {{ fontSize: '26px' }} }},
        labels: {{ style: {{ fontSize: '20px' }} }},
        gridLineColor: 'rgba(0,0,0,0.1)'
    }},
    legend: {{ enabled: true, itemStyle: {{ fontSize: '20px' }} }},
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

# Histogram chart - detail view (returns distribution)
histogram_chart_config = f"""
{{
    chart: {{
        type: 'column',
        backgroundColor: '#ffffff'
    }},
    title: {{
        text: 'Returns Distribution',
        style: {{ fontSize: '40px', fontWeight: 'bold' }}
    }},
    xAxis: {{
        title: {{ text: 'Daily Return (%)', style: {{ fontSize: '26px' }} }},
        labels: {{ style: {{ fontSize: '20px' }} }}
    }},
    yAxis: {{
        title: {{ text: 'Frequency', style: {{ fontSize: '26px' }} }},
        labels: {{ style: {{ fontSize: '20px' }} }},
        gridLineColor: 'rgba(0,0,0,0.1)'
    }},
    legend: {{ enabled: true, itemStyle: {{ fontSize: '20px' }} }},
    credits: {{ enabled: false }},
    plotOptions: {{
        column: {{ borderWidth: 0, pointPadding: 0, groupPadding: 0.1 }}
    }},
    series: [{{
        name: 'Frequency',
        data: {histogram_data},
        color: '{purple}'
    }}]
}}
"""

# Scatter chart - detail view (risk vs return)
scatter_chart_config = f"""
{{
    chart: {{
        type: 'scatter',
        backgroundColor: '#ffffff'
    }},
    title: {{
        text: 'Risk vs Return by Sector',
        style: {{ fontSize: '40px', fontWeight: 'bold' }}
    }},
    xAxis: {{
        title: {{ text: 'Volatility (%)', style: {{ fontSize: '26px' }} }},
        labels: {{ style: {{ fontSize: '20px' }} }},
        gridLineWidth: 1,
        gridLineColor: 'rgba(0,0,0,0.1)'
    }},
    yAxis: {{
        title: {{ text: 'Return (%)', style: {{ fontSize: '26px' }} }},
        labels: {{ style: {{ fontSize: '20px' }} }},
        gridLineColor: 'rgba(0,0,0,0.1)'
    }},
    legend: {{ enabled: true, itemStyle: {{ fontSize: '20px' }} }},
    credits: {{ enabled: false }},
    tooltip: {{
        formatter: function() {{
            return '<b>' + this.point.name + '</b><br/>Volatility: ' + this.x.toFixed(1) + '%<br/>Return: ' + this.y.toFixed(1) + '%';
        }}
    }},
    plotOptions: {{
        scatter: {{
            marker: {{
                radius: 18,
                symbol: 'circle'
            }},
            dataLabels: {{
                enabled: true,
                format: '{{point.name}}',
                style: {{ fontSize: '20px', fontWeight: 'normal' }},
                y: -25
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

# Moving average chart - detail view
ma_chart_config = f"""
{{
    chart: {{
        type: 'line',
        backgroundColor: '#ffffff'
    }},
    title: {{
        text: '20-Day Moving Average',
        style: {{ fontSize: '40px', fontWeight: 'bold' }}
    }},
    xAxis: {{
        title: {{ text: 'Day', style: {{ fontSize: '26px' }} }},
        labels: {{ style: {{ fontSize: '20px' }}, step: 15 }}
    }},
    yAxis: {{
        title: {{ text: 'MA Price ($)', style: {{ fontSize: '26px' }} }},
        labels: {{ style: {{ fontSize: '20px' }} }},
        gridLineColor: 'rgba(0,0,0,0.1)'
    }},
    legend: {{ enabled: true, itemStyle: {{ fontSize: '20px' }} }},
    credits: {{ enabled: false }},
    plotOptions: {{
        line: {{ lineWidth: 4, marker: {{ enabled: false }} }}
    }},
    series: [{{
        name: '20-Day MA',
        data: {ma_data},
        color: '{brown}'
    }}]
}}
"""

# Main title for the dashboard
main_title = "subplot-grid-custom · highcharts · pyplots.ai"

# 5-cell layout: main chart spans 2x2, plus 4 detail views
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <style>
        body {{
            margin: 0;
            padding: 30px;
            background: #ffffff;
            font-family: Arial, sans-serif;
        }}
        .dashboard-title {{
            text-align: center;
            font-size: 56px;
            font-weight: bold;
            color: #333;
            margin-bottom: 25px;
            padding: 15px 0;
        }}
        .grid-container {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr 1fr;
            grid-template-rows: 1fr 1fr;
            gap: 20px;
            width: 4740px;
            height: 2400px;
        }}
        .chart-cell {{
            background: #ffffff;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            overflow: hidden;
        }}
        .main-chart {{
            grid-column: 1 / 3;
            grid-row: 1 / 3;
        }}
        .cell-1 {{
            grid-column: 3;
            grid-row: 1;
        }}
        .cell-2 {{
            grid-column: 4;
            grid-row: 1;
        }}
        .cell-3 {{
            grid-column: 3;
            grid-row: 2;
        }}
        .cell-4 {{
            grid-column: 4;
            grid-row: 2;
        }}
    </style>
</head>
<body>
    <div class="dashboard-title">{main_title}</div>
    <div class="grid-container">
        <div id="main-chart" class="chart-cell main-chart"></div>
        <div id="volume-chart" class="chart-cell cell-1"></div>
        <div id="histogram-chart" class="chart-cell cell-2"></div>
        <div id="scatter-chart" class="chart-cell cell-3"></div>
        <div id="ma-chart" class="chart-cell cell-4"></div>
    </div>
    <script>
        // Main chart - spans 2x2 cells (rowspan + colspan demo)
        Highcharts.chart('main-chart', {main_chart_config});

        // Volume chart - top right 1
        Highcharts.chart('volume-chart', {volume_chart_config});

        // Histogram chart - top right 2
        Highcharts.chart('histogram-chart', {histogram_chart_config});

        // Scatter chart - bottom right 1
        Highcharts.chart('scatter-chart', {scatter_chart_config});

        // Moving average chart - bottom right 2
        Highcharts.chart('ma-chart', {ma_chart_config});
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
            padding: 30px;
            background: #ffffff;
            font-family: Arial, sans-serif;
        }}
        .dashboard-title {{
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #333;
            margin-bottom: 20px;
            padding: 10px 0;
        }}
        .grid-container {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr 1fr;
            grid-template-rows: 1fr 1fr;
            gap: 15px;
            width: 100%;
            max-width: 1600px;
            height: 800px;
            margin: 0 auto;
        }}
        .chart-cell {{
            background: #ffffff;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            overflow: hidden;
        }}
        .main-chart {{
            grid-column: 1 / 3;
            grid-row: 1 / 3;
        }}
        .cell-1 {{
            grid-column: 3;
            grid-row: 1;
        }}
        .cell-2 {{
            grid-column: 4;
            grid-row: 1;
        }}
        .cell-3 {{
            grid-column: 3;
            grid-row: 2;
        }}
        .cell-4 {{
            grid-column: 4;
            grid-row: 2;
        }}
    </style>
</head>
<body>
    <div class="dashboard-title">{main_title}</div>
    <div class="grid-container">
        <div id="main-chart" class="chart-cell main-chart"></div>
        <div id="volume-chart" class="chart-cell cell-1"></div>
        <div id="histogram-chart" class="chart-cell cell-2"></div>
        <div id="scatter-chart" class="chart-cell cell-3"></div>
        <div id="ma-chart" class="chart-cell cell-4"></div>
    </div>
    <script>
        Highcharts.chart('main-chart', {main_chart_config});
        Highcharts.chart('volume-chart', {volume_chart_config});
        Highcharts.chart('histogram-chart', {histogram_chart_config});
        Highcharts.chart('scatter-chart', {scatter_chart_config});
        Highcharts.chart('ma-chart', {ma_chart_config});
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
