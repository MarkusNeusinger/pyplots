""" pyplots.ai
line-range-buttons: Line Chart with Range Selector Buttons
Library: highcharts unknown | Python 3.13.11
Quality: 91/100 | Created: 2026-01-20
"""

import json
import tempfile
import time
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Generate 3 years of daily data
np.random.seed(42)
start_date = datetime(2023, 1, 1)
n_days = 365 * 3  # 3 years of data

dates = []
current_date = start_date
for _ in range(n_days):
    dates.append(current_date)
    current_date += timedelta(days=1)

# Convert dates to JavaScript timestamps (milliseconds since epoch)
timestamps = [int(d.timestamp() * 1000) for d in dates]

# Generate realistic time series with trend and seasonality
trend = np.linspace(100, 180, n_days)
seasonality = 15 * np.sin(np.arange(n_days) * 2 * np.pi / 365)
noise = np.cumsum(np.random.randn(n_days) * 0.5)
values = trend + seasonality + noise
values = np.maximum(values, 50)  # Ensure positive values

# Prepare data for Highcharts
chart_data = [[ts, round(float(v), 2)] for ts, v in zip(timestamps, values, strict=True)]
data_json = json.dumps(chart_data)

# Chart configuration using Highstock with range selector buttons
chart_js = """
Highcharts.stockChart('container', {
    chart: {
        width: 4800,
        height: 2700,
        backgroundColor: '#ffffff',
        spacingTop: 60,
        spacingBottom: 80,
        style: {
            fontFamily: 'Arial, sans-serif'
        }
    },

    title: {
        text: 'line-range-buttons \\u00b7 highcharts \\u00b7 pyplots.ai',
        style: {
            fontSize: '48px',
            fontWeight: 'bold'
        },
        margin: 40
    },

    rangeSelector: {
        enabled: true,
        selected: 4,
        buttons: [{
            type: 'month',
            count: 1,
            text: '1M'
        }, {
            type: 'month',
            count: 3,
            text: '3M'
        }, {
            type: 'month',
            count: 6,
            text: '6M'
        }, {
            type: 'ytd',
            text: 'YTD'
        }, {
            type: 'year',
            count: 1,
            text: '1Y'
        }, {
            type: 'all',
            text: 'All'
        }],
        buttonTheme: {
            fill: '#f0f0f0',
            stroke: '#306998',
            'stroke-width': 2,
            style: {
                color: '#306998',
                fontSize: '24px',
                fontWeight: 'bold'
            },
            states: {
                hover: {
                    fill: '#306998',
                    style: {
                        color: '#ffffff'
                    }
                },
                select: {
                    fill: '#306998',
                    stroke: '#306998',
                    style: {
                        color: '#ffffff'
                    }
                }
            },
            width: 80,
            height: 50,
            padding: 12
        },
        buttonSpacing: 15,
        inputEnabled: true,
        inputStyle: {
            fontSize: '22px',
            color: '#306998'
        },
        inputBoxBorderColor: '#306998',
        inputBoxWidth: 180,
        inputBoxHeight: 45,
        inputDateFormat: '%b %e, %Y',
        inputEditDateFormat: '%Y-%m-%d',
        labelStyle: {
            fontSize: '22px',
            color: '#333333',
            fontWeight: 'bold'
        }
    },

    navigator: {
        enabled: true,
        height: 100,
        margin: 30,
        series: {
            color: '#306998',
            lineWidth: 2
        },
        xAxis: {
            labels: {
                style: {
                    fontSize: '18px'
                }
            }
        }
    },

    scrollbar: {
        enabled: true,
        height: 25,
        barBackgroundColor: '#306998',
        trackBackgroundColor: '#e0e0e0'
    },

    xAxis: {
        type: 'datetime',
        labels: {
            style: {
                fontSize: '24px',
                color: '#333333'
            },
            y: 35
        },
        lineColor: '#333333',
        lineWidth: 2,
        tickColor: '#333333',
        gridLineWidth: 1,
        gridLineColor: '#e0e0e0'
    },

    yAxis: {
        title: {
            text: 'Value',
            style: {
                fontSize: '28px',
                color: '#333333'
            }
        },
        labels: {
            style: {
                fontSize: '24px',
                color: '#333333'
            },
            format: '{value:.0f}'
        },
        gridLineColor: '#e0e0e0',
        gridLineWidth: 1,
        lineWidth: 2,
        lineColor: '#333333'
    },

    tooltip: {
        style: {
            fontSize: '22px'
        },
        dateTimeLabelFormats: {
            day: '%A, %B %e, %Y'
        },
        valueDecimals: 2
    },

    legend: {
        enabled: false
    },

    credits: {
        enabled: false
    },

    plotOptions: {
        series: {
            animation: {
                duration: 1000
            }
        },
        line: {
            lineWidth: 4,
            marker: {
                enabled: false
            }
        }
    },

    series: [{
        type: 'line',
        name: 'Daily Value',
        data: DATA_PLACEHOLDER,
        color: '#306998'
    }]
});
"""

# Replace data placeholder
chart_js = chart_js.replace("DATA_PLACEHOLDER", data_json)

# Download Highstock JS
highcharts_url = "https://code.highcharts.com/stock/highstock.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# Generate HTML with inline scripts
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
</head>
<body style="margin:0; padding:0; background-color:#ffffff;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>
    {chart_js}
    </script>
</body>
</html>"""

# Save HTML for interactive version
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Write temp HTML file for screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Take screenshot using Selenium
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

# Clean up temp file
Path(temp_path).unlink()
