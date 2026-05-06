""" anyplot.ai
heatmap-annotated: Annotated Heatmap
Library: highcharts unknown | Python 3.13.13
Quality: 83/100 | Updated: 2026-05-06
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


THEME = os.getenv("ANYPLOT_THEME", "light")
PAGE_BG = "#FAF8F1" if THEME == "light" else "#1A1A17"
ELEVATED_BG = "#FFFDF6" if THEME == "light" else "#242420"
INK = "#1A1A17" if THEME == "light" else "#F0EFE8"
INK_SOFT = "#4A4A44" if THEME == "light" else "#B8B7B0"
GRID = "rgba(26,26,23,0.10)" if THEME == "light" else "rgba(240,239,232,0.10)"

# BrBG diverging colormap — fixed neutral midpoint (#F5F5F5, never PAGE_BG)
BRBG_STOPS = [
    (0.000, (0x54, 0x30, 0x05)),
    (0.125, (0x8C, 0x51, 0x0A)),
    (0.250, (0xBF, 0x81, 0x2D)),
    (0.375, (0xDF, 0xC2, 0x7D)),
    (0.500, (0xF5, 0xF5, 0xF5)),
    (0.625, (0x80, 0xCD, 0xC1)),
    (0.750, (0x35, 0x97, 0x8F)),
    (0.875, (0x01, 0x66, 0x5E)),
    (1.000, (0x00, 0x3C, 0x30)),
]


def interpolate_brbg(t):
    """Interpolate BrBG colormap at normalized position t in [0, 1]."""
    t = max(0.0, min(1.0, t))
    for i in range(len(BRBG_STOPS) - 1):
        t0, c0 = BRBG_STOPS[i]
        t1, c1 = BRBG_STOPS[i + 1]
        if t <= t1:
            a = (t - t0) / (t1 - t0)
            r = int(c0[0] + a * (c1[0] - c0[0]))
            g = int(c0[1] + a * (c1[1] - c0[1]))
            b = int(c0[2] + a * (c1[2] - c0[2]))
            return r, g, b
    return BRBG_STOPS[-1][1]


def cell_text_color(value):
    """Return dark or light text based on perceived brightness of the cell background."""
    t = (value + 1.0) / 2.0
    r, g, b = interpolate_brbg(t)
    lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
    return INK if lum > 0.45 else "#F0EFE8"


# Data: Correlation matrix for financial indicators
np.random.seed(42)
variables = ["Revenue", "Profit", "Growth", "ROI", "Debt", "Assets", "Employees"]
n = len(variables)

# Generate realistic correlation matrix (symmetric, diagonal = 1)
raw = np.random.randn(n, n) * 0.5
corr_matrix = (raw + raw.T) / 2
np.fill_diagonal(corr_matrix, 1.0)
corr_matrix = np.clip(corr_matrix, -1, 1)

# Per-point data with auto-contrasting labels; emphasize strong correlations
data = []
for i in range(n):
    for j in range(n):
        val = round(corr_matrix[i, j], 2)
        point = {
            "x": j,
            "y": i,
            "value": val,
            "dataLabels": {
                "style": {
                    "color": cell_text_color(val),
                    "fontSize": "20px",
                    "fontWeight": "bold",
                    "textOutline": "none",
                }
            },
        }
        # Highlight strong off-diagonal correlations (|r| > 0.6) with a border
        if i != j and abs(val) > 0.6:
            point["borderColor"] = INK_SOFT
            point["borderWidth"] = 5
        data.append(point)

# Build colorAxis stops list for Highcharts
brbg_coloraxis_stops = [[t, f"#{r:02X}{g:02X}{b:02X}"] for t, (r, g, b) in BRBG_STOPS]

# Build chart options
chart_options = {
    "chart": {
        "type": "heatmap",
        "width": 3600,
        "height": 3600,
        "backgroundColor": PAGE_BG,
        "marginTop": 200,
        "marginBottom": 400,
        "marginLeft": 250,
        "marginRight": 200,
    },
    "title": {
        "text": "heatmap-annotated · highcharts · anyplot.ai",
        "style": {"fontSize": "28px", "fontWeight": "bold", "color": INK},
    },
    "subtitle": {
        "text": "Financial indicator correlations — strong relationships (|r| > 0.6) outlined",
        "style": {"fontSize": "18px", "color": INK_SOFT},
    },
    "xAxis": {
        "categories": variables,
        "title": {"text": "Variables", "style": {"fontSize": "22px", "color": INK}},
        "labels": {"style": {"fontSize": "18px", "color": INK_SOFT}},
        "lineColor": INK_SOFT,
        "tickColor": INK_SOFT,
        "gridLineColor": GRID,
    },
    "yAxis": {
        "categories": variables,
        "title": {"text": "Variables", "style": {"fontSize": "22px", "color": INK}},
        "labels": {"style": {"fontSize": "18px", "color": INK_SOFT}},
        "lineColor": INK_SOFT,
        "tickColor": INK_SOFT,
        "gridLineColor": GRID,
        "reversed": True,
    },
    "colorAxis": {
        "min": -1,
        "max": 1,
        "stops": brbg_coloraxis_stops,
        "labels": {"style": {"fontSize": "18px", "color": INK_SOFT}},
    },
    "legend": {
        "align": "right",
        "layout": "vertical",
        "verticalAlign": "middle",
        "symbolHeight": 600,
        "itemStyle": {"fontSize": "18px", "color": INK_SOFT},
        "backgroundColor": ELEVATED_BG,
        "borderColor": INK_SOFT,
        "borderWidth": 1,
    },
    "credits": {"enabled": False},
    "series": [
        {
            "type": "heatmap",
            "name": "Correlation",
            "data": data,
            "borderWidth": 2,
            "borderColor": PAGE_BG,
            "dataLabels": {"enabled": True, "format": "{point.value:.2f}"},
        }
    ],
}

# Download Highcharts JS and heatmap module (primary CDN with jsdelivr fallback)
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def fetch_js(primary_url, fallback_url):
    for url in [primary_url, fallback_url]:
        try:
            resp = requests.get(url, headers=headers, timeout=30)
            if resp.status_code == 200 and resp.text.strip().startswith(("/", "!", "(")):
                return resp.text
        except Exception:
            continue
    raise RuntimeError(f"Failed to download JS from {primary_url} and {fallback_url}")


highcharts_js = fetch_js(
    "https://code.highcharts.com/highcharts.js", "https://cdn.jsdelivr.net/npm/highcharts/highcharts.js"
)
heatmap_js = fetch_js(
    "https://code.highcharts.com/modules/heatmap.js", "https://cdn.jsdelivr.net/npm/highcharts/modules/heatmap.js"
)

# Convert options to JSON
options_json = json.dumps(chart_options)

# Generate HTML with inline scripts
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{heatmap_js}</script>
</head>
<body style="margin:0; background:{PAGE_BG};">
    <div id="container" style="width: 3600px; height: 3600px;"></div>
    <script>
        Highcharts.chart('container', {options_json});
    </script>
</body>
</html>"""

# Save HTML for interactive version
with open(f"plot-{THEME}.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Take screenshot using headless Chrome
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=3600,3600")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)
driver.save_screenshot(f"plot-{THEME}.png")
driver.quit()

Path(temp_path).unlink()
