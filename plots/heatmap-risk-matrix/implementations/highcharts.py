"""pyplots.ai
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
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
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

# Green-yellow-orange-red gradient per spec requirement
color_stops = [
    [0, "#2b8c3e"],
    [0.12, "#5aad5e"],
    [0.28, "#b5cc3e"],
    [0.40, "#fee090"],
    [0.56, "#fc8d59"],
    [0.76, "#d73027"],
    [1.0, "#a50026"],
]

# Category colors for risk markers
category_colors = {"Technical": "#306998", "Financial": "#8e44ad", "Operational": "#16a085"}

# Per-point label offsets to prevent overlaps (alternate above/below)
label_y_offsets = {
    "Server Outage": -38,
    "Data Breach": -38,
    "Budget Overrun": -38,
    "Key Staff Loss": 52,
    "Vendor Delay": -38,
    "Scope Creep": 52,
    "Currency Risk": 52,
    "Reg. Change": 52,
    "Tech Debt": 52,
    "Minor Bug": -38,
    "Supply Issue": -38,
    "IP Dispute": -38,
    "Power Failure": -38,
    "PR Crisis": -38,
}

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
                "dataLabels": {"y": label_y_offsets.get(risk["name"], -38)},
            }
        )
    scatter_series.append(
        {
            "type": "scatter",
            "name": category,
            "data": data_points,
            "color": category_colors[category],
            "marker": {"radius": 22, "symbol": "circle", "lineWidth": 3, "lineColor": "#ffffff"},
            "dataLabels": {
                "enabled": True,
                "format": "{point.name}",
                "style": {"fontSize": "28px", "fontWeight": "600", "color": "#2c3e50", "textOutline": "3px #ffffff"},
                "y": -38,
                "allowOverlap": True,
                "crop": False,
                "overflow": "allow",
            },
            "tooltip": {"pointFormat": "<b>{point.name}</b><br>Risk Score: <b>{point.score}</b>"},
            "zIndex": 5,
            "colorAxis": False,
            "showInLegend": True,
        }
    )

# Zone annotation labels
zone_annotations = [
    {"label": "LOW", "x": 0, "y": 0, "color": "#1a6b2d"},
    {"label": "MEDIUM", "x": 1, "y": 1, "color": "#8a7d00"},
    {"label": "HIGH", "x": 3, "y": 3, "color": "#c44600"},
    {"label": "CRITICAL", "x": 4, "y": 4, "color": "#a50026"},
]

# Build chart options using highcharts-core Python API
chart = Chart(container="container")
chart.options = HighchartsOptions()

chart.options.chart = {
    "type": "heatmap",
    "width": 4800,
    "height": 2700,
    "backgroundColor": "#fafafa",
    "marginTop": 200,
    "marginBottom": 200,
    "marginRight": 300,
    "marginLeft": 360,
    "style": {"fontFamily": "'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"},
}

chart.options.title = {
    "text": "heatmap-risk-matrix \u00b7 highcharts \u00b7 pyplots.ai",
    "style": {"fontSize": "52px", "fontWeight": "600", "color": "#2c3e50"},
    "y": 40,
}

chart.options.subtitle = {
    "text": "Risk score = Likelihood \u00d7 Impact \u2014 zones: Low (1\u20134) \u00b7 Medium (5\u20139) \u00b7 High (10\u201316) \u00b7 Critical (20\u201325)",
    "style": {"fontSize": "30px", "fontWeight": "normal", "color": "#7f8c8d"},
    "y": 90,
}

chart.options.x_axis = {
    "categories": impact_labels,
    "title": {"text": "Impact", "style": {"fontSize": "36px", "fontWeight": "600", "color": "#2c3e50"}, "margin": 24},
    "labels": {"style": {"fontSize": "30px", "color": "#34495e"}, "y": 40},
    "lineWidth": 0,
    "tickLength": 0,
    "opposite": False,
    "min": 0,
    "max": 4,
}

chart.options.y_axis = {
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
}

chart.options.color_axis = {
    "min": 1,
    "max": 25,
    "stops": color_stops,
    "labels": {"style": {"fontSize": "24px", "color": "#34495e"}},
    "showInLegend": False,
}

chart.options.legend = {
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
}

chart.options.tooltip = {"style": {"fontSize": "28px"}}
chart.options.credits = {"enabled": False}
chart.options.plot_options = {"heatmap": {"colsize": 1, "rowsize": 1}}

# Build series
heatmap_series_config = {
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
}

chart.options.series = [heatmap_series_config, *scatter_series]

# Export options as JSON dict via highcharts-core serialization
options_dict = chart.options.to_dict()
options_json = json.dumps(options_dict)

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

zone_json = json.dumps(zone_annotations)

# HTML template with highcharts-core options, adaptive colors, and zone annotations
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

        // Add zone annotations via Highcharts annotations API
        opts.annotations = [{{
            draggable: '',
            labelOptions: {{
                backgroundColor: 'rgba(255,255,255,0.82)',
                borderWidth: 3,
                borderRadius: 10,
                style: {{
                    fontSize: '30px',
                    fontWeight: '700'
                }},
                verticalAlign: 'middle',
                padding: 14
            }},
            labels: zones.map(function(z) {{
                return {{
                    point: {{ x: z.x, y: z.y, xAxis: 0, yAxis: 0 }},
                    text: z.label,
                    style: {{ color: z.color }},
                    borderColor: z.color,
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
