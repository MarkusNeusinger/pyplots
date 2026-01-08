""" pyplots.ai
kagi-basic: Basic Kagi Chart
Library: highcharts unknown | Python 3.13.11
Quality: 85/100 | Created: 2026-01-08
"""

import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Generate realistic stock price data
np.random.seed(42)

# Simulate 200 days of stock price data with trends and reversals
n_days = 200
base_price = 100
returns = np.random.normal(0.001, 0.02, n_days)  # Daily returns with slight upward drift

# Add some trend patterns to make the Kagi chart interesting
trend_changes = [0, 40, 80, 120, 160, 200]
for i in range(len(trend_changes) - 1):
    start, end = trend_changes[i], trend_changes[i + 1]
    if i % 2 == 0:
        returns[start:end] += 0.003  # Uptrend
    else:
        returns[start:end] -= 0.002  # Downtrend

prices = base_price * np.cumprod(1 + returns)

# Calculate Kagi chart data with 4% reversal threshold
reversal_pct = 0.04
kagi_data = []
direction = 1  # 1 for up (yang), -1 for down (yin)
current_price = prices[0]
high_point = prices[0]
low_point = prices[0]
kagi_x = 0

# Initialize first point
kagi_data.append({"x": kagi_x, "y": round(current_price, 2), "direction": direction})

for price in prices[1:]:
    if direction == 1:  # Currently in uptrend
        if price > high_point:
            high_point = price
            # Update the last point
            kagi_data[-1]["y"] = round(high_point, 2)
        elif price <= high_point * (1 - reversal_pct):
            # Reversal to downtrend
            kagi_x += 1
            direction = -1
            low_point = price
            kagi_data.append({"x": kagi_x, "y": round(price, 2), "direction": direction})
    else:  # Currently in downtrend
        if price < low_point:
            low_point = price
            # Update the last point
            kagi_data[-1]["y"] = round(low_point, 2)
        elif price >= low_point * (1 + reversal_pct):
            # Reversal to uptrend
            kagi_x += 1
            direction = 1
            high_point = price
            kagi_data.append({"x": kagi_x, "y": round(price, 2), "direction": direction})

# Create line segments with proper yang/yin coloring
# Build series data for Highcharts with segment colors
yang_segments = []  # Thick green lines (bullish)
yin_segments = []  # Thin red lines (bearish)

for i in range(len(kagi_data) - 1):
    p1 = kagi_data[i]
    p2 = kagi_data[i + 1]

    # Vertical segment
    if p2["direction"] == 1:  # Yang (up)
        yang_segments.extend(
            [{"x": p1["x"], "y": p1["y"]}, {"x": p1["x"], "y": p2["y"]}, None]  # Horizontal  # Vertical  # Break
        )
    else:  # Yin (down)
        yin_segments.extend([{"x": p1["x"], "y": p1["y"]}, {"x": p1["x"], "y": p2["y"]}, None])

    # Horizontal segment (shoulder or waist)
    if i < len(kagi_data) - 2:
        if p2["direction"] == 1:
            yang_segments.extend([{"x": p1["x"], "y": p2["y"]}, {"x": p2["x"], "y": p2["y"]}, None])
        else:
            yin_segments.extend([{"x": p1["x"], "y": p2["y"]}, {"x": p2["x"], "y": p2["y"]}, None])

# Format data for JavaScript
yang_js = [f"[{p['x']}, {p['y']}]" if p else "null" for p in yang_segments]
yin_js = [f"[{p['x']}, {p['y']}]" if p else "null" for p in yin_segments]

yang_data_str = "[" + ", ".join(yang_js) + "]"
yin_data_str = "[" + ", ".join(yin_js) + "]"

# Download Highcharts JS
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# Create the chart configuration in pure JavaScript
# Using line series with different lineWidths to simulate yang/yin
chart_js = f"""
Highcharts.chart('container', {{
    chart: {{
        type: 'line',
        width: 4800,
        height: 2700,
        backgroundColor: '#ffffff',
        spacingBottom: 100,
        spacingTop: 80
    }},
    title: {{
        text: 'kagi-basic · highcharts · pyplots.ai',
        style: {{
            fontSize: '48px',
            fontWeight: 'bold'
        }},
        margin: 40
    }},
    subtitle: {{
        text: 'Stock Price Analysis with 4% Reversal Threshold',
        style: {{
            fontSize: '28px'
        }}
    }},
    xAxis: {{
        title: {{
            text: 'Kagi Line Index',
            style: {{
                fontSize: '32px'
            }},
            margin: 20
        }},
        labels: {{
            style: {{
                fontSize: '24px'
            }}
        }},
        gridLineWidth: 1,
        gridLineColor: 'rgba(0, 0, 0, 0.1)'
    }},
    yAxis: {{
        title: {{
            text: 'Price ($)',
            style: {{
                fontSize: '32px'
            }},
            margin: 20
        }},
        labels: {{
            style: {{
                fontSize: '24px'
            }},
            format: '${{value}}'
        }},
        gridLineWidth: 1,
        gridLineColor: 'rgba(0, 0, 0, 0.1)'
    }},
    legend: {{
        enabled: true,
        align: 'center',
        verticalAlign: 'bottom',
        layout: 'horizontal',
        itemStyle: {{
            fontSize: '28px'
        }},
        symbolWidth: 50,
        itemDistance: 60,
        margin: 30
    }},
    plotOptions: {{
        line: {{
            marker: {{
                enabled: false
            }},
            connectNulls: false
        }}
    }},
    series: [{{
        name: 'Yang (Bullish)',
        data: {yang_data_str},
        color: '#228B22',
        lineWidth: 8,
        zIndex: 2
    }}, {{
        name: 'Yin (Bearish)',
        data: {yin_data_str},
        color: '#DC143C',
        lineWidth: 4,
        zIndex: 1
    }}],
    credits: {{
        enabled: false
    }}
}});
"""

# Generate HTML with inline script
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
</head>
<body style="margin:0; padding:0; overflow:hidden;">
    <div id="container" style="width: 4800px; height: 2700px; margin:0; padding:0;"></div>
    <script>{chart_js}</script>
</body>
</html>"""

# Write temp HTML and take screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Also save HTML for interactive viewing
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4900,2800")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)  # Wait for chart to render

driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()  # Clean up temp file
