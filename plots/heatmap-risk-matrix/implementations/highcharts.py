""" pyplots.ai
heatmap-risk-matrix: Risk Assessment Matrix (Probability vs Impact)
Library: highcharts unknown | Python 3.14.3
Quality: 83/100 | Created: 2026-03-17
"""

import json
import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Risk items with likelihood and impact ratings
np.random.seed(42)

risks = [
    {"name": "Server Outage", "likelihood": 3, "impact": 5, "category": "Technical"},
    {"name": "Data Breach", "likelihood": 2, "impact": 5, "category": "Technical"},
    {"name": "Budget Overrun", "likelihood": 4, "impact": 4, "category": "Financial"},
    {"name": "Key Staff Loss", "likelihood": 3, "impact": 4, "category": "Operational"},
    {"name": "Vendor Delay", "likelihood": 4, "impact": 3, "category": "Operational"},
    {"name": "Scope Creep", "likelihood": 5, "impact": 3, "category": "Operational"},
    {"name": "Currency Risk", "likelihood": 3, "impact": 3, "category": "Financial"},
    {"name": "Reg. Change", "likelihood": 2, "impact": 4, "category": "Financial"},
    {"name": "Tech Debt", "likelihood": 4, "impact": 2, "category": "Technical"},
    {"name": "Minor Bug", "likelihood": 5, "impact": 1, "category": "Technical"},
    {"name": "Supply Issue", "likelihood": 2, "impact": 3, "category": "Operational"},
    {"name": "IP Dispute", "likelihood": 1, "impact": 5, "category": "Financial"},
    {"name": "Power Failure", "likelihood": 1, "impact": 3, "category": "Technical"},
    {"name": "PR Crisis", "likelihood": 2, "impact": 4, "category": "Operational"},
]

likelihood_labels = ["Rare", "Unlikely", "Possible", "Likely", "Almost Certain"]
impact_labels = ["Negligible", "Minor", "Moderate", "Major", "Catastrophic"]

# Build background heatmap data (risk score = likelihood × impact)
heatmap_data = []
for li in range(5):
    for im in range(5):
        score = (li + 1) * (im + 1)
        heatmap_data.append([im, li, score])

# Colorblind-friendly gradient: blue → yellow → orange → dark red
color_stops = [
    [0, "#4575b4"],  # Low (blue)
    [0.16, "#91bfdb"],  # Low-medium (light blue)
    [0.36, "#fee090"],  # Medium (yellow)
    [0.56, "#fc8d59"],  # High (orange)
    [0.76, "#d73027"],  # Critical (red)
    [1.0, "#a50026"],  # Critical (dark red)
]

# Category colors for risk markers
category_colors = {"Technical": "#306998", "Financial": "#8e44ad", "Operational": "#16a085"}

# Build scatter series for each category with jitter
scatter_series = []
for category in ["Technical", "Financial", "Operational"]:
    cat_risks = [r for r in risks if r["category"] == category]
    data_points = []
    for risk in cat_risks:
        jitter_x = np.random.uniform(-0.25, 0.25)
        jitter_y = np.random.uniform(-0.25, 0.25)
        data_points.append(
            {
                "x": risk["impact"] - 1 + jitter_x,
                "y": risk["likelihood"] - 1 + jitter_y,
                "name": risk["name"],
                "score": risk["likelihood"] * risk["impact"],
            }
        )
    scatter_series.append(
        {
            "type": "scatter",
            "name": category,
            "data": data_points,
            "color": category_colors[category],
            "marker": {"radius": 20, "symbol": "circle", "lineWidth": 3, "lineColor": "#ffffff"},
            "dataLabels": {
                "enabled": True,
                "format": "{point.name}",
                "style": {"fontSize": "26px", "fontWeight": "600", "color": "#2c3e50", "textOutline": "3px #ffffff"},
                "y": -34,
                "allowOverlap": True,
            },
            "tooltip": {"pointFormat": "<b>{point.name}</b><br>Risk Score: <b>{point.score}</b>"},
            "zIndex": 5,
            "colorAxis": False,
            "showInLegend": True,
        }
    )

# Zone definitions for risk level annotations
# Low (1-4), Medium (5-9), High (10-16), Critical (20-25)
zone_annotations = [
    {"label": "LOW", "x": 0, "y": 0, "color": "#4575b4"},
    {"label": "MEDIUM", "x": 2, "y": 1, "color": "#fee090"},
    {"label": "HIGH", "x": 3, "y": 2, "color": "#fc8d59"},
    {"label": "CRITICAL", "x": 4, "y": 4, "color": "#a50026"},
]

# Chart configuration
chart_options = {
    "chart": {
        "type": "heatmap",
        "width": 4800,
        "height": 2700,
        "backgroundColor": "#fafafa",
        "marginTop": 200,
        "marginBottom": 200,
        "marginRight": 300,
        "marginLeft": 360,
        "style": {"fontFamily": "'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"},
    },
    "title": {
        "text": "heatmap-risk-matrix \u00b7 highcharts \u00b7 pyplots.ai",
        "style": {"fontSize": "52px", "fontWeight": "600", "color": "#2c3e50"},
        "y": 40,
    },
    "subtitle": {
        "text": "Risk score = Likelihood \u00d7 Impact \u2014 zones: Low (1\u20134) \u00b7 Medium (5\u20139) \u00b7 High (10\u201316) \u00b7 Critical (20\u201325)",
        "style": {"fontSize": "30px", "fontWeight": "normal", "color": "#7f8c8d"},
        "y": 90,
    },
    "xAxis": {
        "categories": impact_labels,
        "title": {
            "text": "Impact",
            "style": {"fontSize": "36px", "fontWeight": "600", "color": "#2c3e50"},
            "margin": 24,
        },
        "labels": {"style": {"fontSize": "30px", "color": "#34495e"}, "y": 40},
        "lineWidth": 0,
        "tickLength": 0,
        "opposite": False,
        "min": 0,
        "max": 4,
    },
    "yAxis": {
        "categories": likelihood_labels,
        "title": {
            "text": "Likelihood",
            "style": {"fontSize": "36px", "fontWeight": "600", "color": "#2c3e50"},
            "margin": 24,
        },
        "labels": {"style": {"fontSize": "30px", "color": "#34495e"}},
        "reversed": False,
        "lineWidth": 0,
        "gridLineWidth": 0,
        "min": 0,
        "max": 4,
    },
    "colorAxis": {
        "min": 1,
        "max": 25,
        "stops": color_stops,
        "labels": {"style": {"fontSize": "24px", "color": "#34495e"}},
        "showInLegend": False,
    },
    "legend": {
        "align": "right",
        "layout": "vertical",
        "verticalAlign": "middle",
        "itemStyle": {"fontSize": "28px", "color": "#34495e"},
        "itemMarginBottom": 16,
        "x": -40,
        "y": 0,
        "symbolRadius": 12,
        "symbolHeight": 24,
        "symbolWidth": 24,
    },
    "tooltip": {"style": {"fontSize": "28px"}},
    "credits": {"enabled": False},
    "plotOptions": {"heatmap": {"colsize": 1, "rowsize": 1}},
    "series": [
        {
            "type": "heatmap",
            "name": "Risk Score",
            "data": heatmap_data,
            "borderWidth": 4,
            "borderColor": "#fafafa",
            "dataLabels": {"enabled": True, "style": {"fontSize": "34px", "fontWeight": "bold", "textOutline": "none"}},
            "tooltip": {
                "headerFormat": "",
                "pointFormat": (
                    "Impact: <b>{series.xAxis.categories.(point.x)}</b><br>"
                    "Likelihood: <b>{series.yAxis.categories.(point.y)}</b><br>"
                    "Risk Score: <b>{point.value}</b>"
                ),
            },
            "showInLegend": False,
        },
        *scatter_series,
    ],
}

# Download Highcharts JS, heatmap module, and annotations module
js_urls = [
    ("https://code.highcharts.com/highcharts.js", "https://cdn.jsdelivr.net/npm/highcharts@11/highcharts.js"),
    ("https://code.highcharts.com/modules/heatmap.js", "https://cdn.jsdelivr.net/npm/highcharts@11/modules/heatmap.js"),
    (
        "https://code.highcharts.com/modules/annotations.js",
        "https://cdn.jsdelivr.net/npm/highcharts@11/modules/annotations.js",
    ),
]
js_parts = []
for primary, fallback in js_urls:
    for url in (primary, fallback):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as response:
                js_parts.append(response.read().decode("utf-8"))
            break
        except Exception:
            continue
all_js = "\n".join(js_parts)

# Convert options to JSON
options_json = json.dumps(chart_options)
zone_json = json.dumps(zone_annotations)

# Generate HTML with inline scripts, adaptive label colors, and zone annotations
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{all_js}</script>
</head>
<body style="margin:0; padding:0; overflow:hidden; background:#fafafa;">
    <div id="container" style="width:4800px; height:2700px;"></div>
    <script>
        var opts = {options_json};
        var zones = {zone_json};

        // Adaptive text color for heatmap cell scores
        opts.series[0].dataLabels.formatter = function() {{
            var v = this.point.value;
            var color = v >= 15 ? '#ffffff' : '#333333';
            return '<span style="color:' + color + ';font-size:34px;font-weight:bold">' + v + '</span>';
        }};
        opts.series[0].dataLabels.useHTML = true;

        // Add zone label annotations using Highcharts annotations API
        opts.annotations = [{{
            draggable: '',
            labelOptions: {{
                backgroundColor: 'rgba(255,255,255,0.75)',
                borderWidth: 2,
                borderRadius: 8,
                style: {{
                    fontSize: '28px',
                    fontWeight: '700'
                }},
                verticalAlign: 'middle',
                padding: 12
            }},
            labels: zones.map(function(z) {{
                return {{
                    point: {{ x: z.x, y: z.y, xAxis: 0, yAxis: 0 }},
                    text: z.label,
                    style: {{ color: z.color === '#fee090' ? '#856404' : (z.color === '#fc8d59' ? '#7c3a00' : z.color) }},
                    borderColor: z.color === '#fee090' ? '#856404' : z.color,
                    y: 60
                }};
            }})
        }}];

        Highcharts.chart('container', opts);
    </script>
</body>
</html>"""

# Save HTML for interactive version
with open("plot.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Take screenshot using headless Chrome
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4800,2840")
chrome_options.add_argument("--force-device-scale-factor=1")
chrome_options.add_argument("--hide-scrollbars")

driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(4800, 2840)
driver.get(f"file://{temp_path}")
time.sleep(5)
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()
