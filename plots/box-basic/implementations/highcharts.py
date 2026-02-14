"""pyplots.ai
box-basic: Basic Box Plot
Library: highcharts 1.10.3 | Python 3.14
Quality: 79/100 | Created: 2025-12-23
"""

import json
import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - employee performance scores across 5 departments
np.random.seed(42)
departments = ["Engineering", "Marketing", "Sales", "Design", "Finance"]
colors = ["#306998", "#FFD43B", "#9467BD", "#17BECF", "#8C564B"]
colors_fill = [
    "rgba(48, 105, 152, 0.72)",
    "rgba(255, 212, 59, 0.72)",
    "rgba(148, 103, 189, 0.72)",
    "rgba(23, 190, 207, 0.72)",
    "rgba(140, 86, 75, 0.72)",
]

scores = [
    np.random.normal(78, 8, 80),  # Engineering: high, tight
    np.random.normal(72, 14, 60),  # Marketing: moderate, wide spread
    np.random.normal(68, 9, 90),  # Sales: lower mean, moderate
    np.random.normal(82, 7, 50),  # Design: highest, tight
    np.random.normal(75, 18, 70),  # Finance: moderate, widest spread
]

# Calculate box plot statistics
box_stats = []
outlier_data = []

for i, data in enumerate(scores):
    data = np.clip(data, 0, 100)
    q1 = float(np.percentile(data, 25))
    median = float(np.percentile(data, 50))
    q3 = float(np.percentile(data, 75))
    iqr = q3 - q1
    whisker_low = float(max(data[data >= q1 - 1.5 * iqr].min(), data.min()))
    whisker_high = float(min(data[data <= q3 + 1.5 * iqr].max(), data.max()))

    box_stats.append(
        {
            "low": round(whisker_low, 1),
            "q1": round(q1, 1),
            "median": round(median, 1),
            "q3": round(q3, 1),
            "high": round(whisker_high, 1),
        }
    )

    outliers = data[(data < q1 - 1.5 * iqr) | (data > q3 + 1.5 * iqr)]
    for val in outliers:
        outlier_data.append([i, round(float(val), 1)])

# Identify key insights for annotations
medians = [s["median"] for s in box_stats]
spreads = [s["q3"] - s["q1"] for s in box_stats]
best_dept_idx = int(np.argmax(medians))
widest_dept_idx = int(np.argmax(spreads))

# Build box data with per-point color using Highcharts point objects
box_data_points = []
for i in range(len(departments)):
    box_data_points.append(
        {
            "low": box_stats[i]["low"],
            "q1": box_stats[i]["q1"],
            "median": box_stats[i]["median"],
            "q3": box_stats[i]["q3"],
            "high": box_stats[i]["high"],
            "color": colors[i],
            "fillColor": colors_fill[i],
        }
    )

box_data_json = json.dumps(box_data_points)
outlier_json = json.dumps(outlier_data)

# Build full Highcharts config as native JS (avoids Python API limitations with fillColor)
chart_js = f"""
Highcharts.chart('container', {{
    chart: {{
        type: 'boxplot',
        width: 4800,
        height: 2700,
        backgroundColor: '#fafafa',
        marginBottom: 260,
        marginLeft: 300,
        marginRight: 280,
        spacingTop: 40,
        style: {{ fontFamily: "'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif" }},
        animation: false
    }},
    title: {{
        text: 'box-basic \\u00b7 highcharts \\u00b7 pyplots.ai',
        style: {{ fontSize: '64px', fontWeight: '700', color: '#1a1a2e', letterSpacing: '0.5px' }},
        margin: 50
    }},
    subtitle: {{
        text: 'Annual Performance Review Scores by Department',
        style: {{ fontSize: '42px', color: '#636e72', fontWeight: '300' }}
    }},
    xAxis: {{
        categories: {json.dumps(departments)},
        title: {{
            text: 'Department',
            style: {{ fontSize: '44px', color: '#2d3436', fontWeight: '600' }},
            margin: 24
        }},
        labels: {{ style: {{ fontSize: '38px', color: '#2d3436', fontWeight: '500' }} }},
        lineWidth: 0,
        tickWidth: 0,
        gridLineWidth: 0
    }},
    yAxis: {{
        title: {{
            text: 'Score (out of 100)',
            style: {{ fontSize: '44px', color: '#2d3436', fontWeight: '600' }},
            margin: 20
        }},
        labels: {{ style: {{ fontSize: '34px', color: '#636e72' }} }},
        gridLineWidth: 1,
        gridLineColor: 'rgba(0, 0, 0, 0.06)',
        gridLineDashStyle: 'Dot',
        tickInterval: 5,
        lineWidth: 0
    }},
    legend: {{ enabled: false }},
    credits: {{ enabled: false }},
    tooltip: {{ enabled: false }},
    plotOptions: {{
        boxplot: {{
            pointWidth: 440,
            lineWidth: 3,
            medianWidth: 6,
            medianColor: '#1a1a2e',
            stemColor: '#555555',
            stemWidth: 3,
            stemDashStyle: 'Solid',
            whiskerWidth: 4,
            whiskerLength: '50%',
            whiskerColor: '#555555'
        }},
        series: {{ animation: false }}
    }},
    series: [{{
        name: 'Department Scores',
        type: 'boxplot',
        data: {box_data_json}
    }}, {{
        name: 'Outliers',
        type: 'scatter',
        data: {outlier_json},
        marker: {{
            fillColor: 'rgba(231, 76, 60, 0.75)',
            lineWidth: 2,
            lineColor: '#c0392b',
            radius: 14,
            symbol: 'circle'
        }},
        zIndex: 10,
        showInLegend: false
    }}]
}});
"""

# Download Highcharts JS files (required for headless Chrome)
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

highcharts_more_url = "https://code.highcharts.com/highcharts-more.js"
with urllib.request.urlopen(highcharts_more_url, timeout=30) as response:
    highcharts_more_js = response.read().decode("utf-8")

# Annotation JS for data storytelling — highlights key findings using chart.renderer
best_dept = departments[best_dept_idx]
best_median = medians[best_dept_idx]
widest_dept = departments[widest_dept_idx]
widest_iqr = spreads[widest_dept_idx]
n_outliers = len(outlier_data)
outlier_s = "s" if n_outliers != 1 else ""

annotation_js = f"""
setTimeout(function() {{
    var chart = Highcharts.charts[0];
    if (!chart) return;
    var pts = chart.series[0].points;

    // Annotation: Best performing department (positioned near its box)
    var bestPt = pts[{best_dept_idx}];
    var bestX = chart.plotLeft + bestPt.plotX - 50;
    chart.renderer.label(
        '<span style="font-size:30px;color:#1a6b3c;font-weight:700;">\\u25B2 Top Performer</span>' +
        '<br><span style="font-size:26px;color:#555;">{best_dept} \\u2014 Median: {best_median:.0f}</span>' +
        '<br><span style="font-size:24px;color:#777;">Highest scores, consistent results</span>',
        bestX,
        chart.plotTop + 15
    )
    .attr({{
        fill: 'rgba(255,255,255,0.95)',
        stroke: '#27ae60',
        'stroke-width': 2.5,
        r: 12,
        padding: 18,
        zIndex: 20
    }})
    .css({{ lineHeight: '38px' }})
    .add();

    // Annotation: Widest spread department (positioned between Design and Finance)
    var widePt = pts[{widest_dept_idx}];
    var prevPt = pts[{widest_dept_idx - 1 if widest_dept_idx > 0 else 0}];
    var wideX = chart.plotLeft + (prevPt.plotX + widePt.plotX) / 2 - 80;
    chart.renderer.label(
        '<span style="font-size:30px;color:#b45309;font-weight:700;">\\u25CF Widest Spread</span>' +
        '<br><span style="font-size:26px;color:#555;">{widest_dept} \\u2014 IQR: {widest_iqr:.0f} pts</span>' +
        '<br><span style="font-size:24px;color:#777;">Highly variable performance</span>',
        wideX,
        chart.plotTop + 140
    )
    .attr({{
        fill: 'rgba(255,255,255,0.95)',
        stroke: '#e67e22',
        'stroke-width': 2.5,
        r: 12,
        padding: 18,
        zIndex: 20
    }})
    .css({{ lineHeight: '38px' }})
    .add();

    // Annotation: Outlier count (bottom-left)
    chart.renderer.label(
        '<span style="font-size:28px;color:#c0392b;font-weight:600;">\\u25CF {n_outliers} outlier{outlier_s} detected</span>' +
        '<br><span style="font-size:24px;color:#777;">Scores beyond 1.5\\u00d7IQR from quartiles</span>',
        chart.plotLeft + 10,
        chart.plotTop + chart.plotHeight - 120
    )
    .attr({{
        fill: 'rgba(255,255,255,0.95)',
        stroke: '#e74c3c',
        'stroke-width': 2,
        r: 12,
        padding: 16,
        zIndex: 20
    }})
    .css({{ lineHeight: '36px' }})
    .add();
}}, 500);
"""

# Generate HTML with inline scripts
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{highcharts_more_js}</script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>{chart_js}</script>
    <script>{annotation_js}</script>
</body>
</html>"""

# Write temp HTML file
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

# Take screenshot with Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=5000,3000")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(6)

container = driver.find_element("id", "container")
container.screenshot("plot.png")
driver.quit()

# Clean up
Path(temp_path).unlink()
