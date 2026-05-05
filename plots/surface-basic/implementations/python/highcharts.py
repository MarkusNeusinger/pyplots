"""anyplot.ai
surface-basic: Basic 3D Surface Plot
Library: highcharts | Python 3.13
Quality: pending | Created: 2025-12-23
"""

import json
import os
import tempfile
import time
import urllib.request
from pathlib import Path
from urllib.error import HTTPError, URLError

import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


THEME = os.getenv("ANYPLOT_THEME", "light")
PAGE_BG = "#FAF8F1" if THEME == "light" else "#1A1A17"
ELEVATED_BG = "#FFFDF6" if THEME == "light" else "#242420"
INK = "#1A1A17" if THEME == "light" else "#F0EFE8"
INK_SOFT = "#4A4A44" if THEME == "light" else "#B8B7B0"
INK_MUTED = "#6B6A63" if THEME == "light" else "#A8A79F"
GRID = "rgba(26,26,23,0.10)" if THEME == "light" else "rgba(240,239,232,0.10)"

# Viridis colormap for continuous data - sequential
VIRIDIS_COLORS = [
    (68, 1, 84),  # Dark purple
    (59, 82, 139),  # Blue-purple
    (33, 145, 140),  # Teal
    (94, 201, 98),  # Green
    (253, 231, 37),  # Yellow
]

# Data - Gaussian surface with peaks and valleys
np.random.seed(42)
n_points = 40
x = np.linspace(-3, 3, n_points)
y = np.linspace(-3, 3, n_points)
X, Y = np.meshgrid(x, y)

# Interesting surface: combination of Gaussian peaks
Z = (
    np.exp(-((X - 1) ** 2 + (Y - 1) ** 2))
    + 0.8 * np.exp(-((X + 1) ** 2 + (Y + 1) ** 2))
    - 0.5 * np.exp(-((X) ** 2 + (Y) ** 2) / 0.5)
)

# Normalize Z values for color mapping
z_min, z_max = Z.min(), Z.max()
z_normalized = (Z - z_min) / (z_max - z_min)


def get_viridis_color(val):
    """Map normalized value (0-1) to viridis RGB color."""
    n_colors = len(VIRIDIS_COLORS) - 1
    idx = min(int(val * n_colors), n_colors - 1)
    t = (val * n_colors) - idx
    r = int(VIRIDIS_COLORS[idx][0] + t * (VIRIDIS_COLORS[idx + 1][0] - VIRIDIS_COLORS[idx][0]))
    g = int(VIRIDIS_COLORS[idx][1] + t * (VIRIDIS_COLORS[idx + 1][1] - VIRIDIS_COLORS[idx][1]))
    b = int(VIRIDIS_COLORS[idx][2] + t * (VIRIDIS_COLORS[idx + 1][2] - VIRIDIS_COLORS[idx][2]))
    return f"rgb({r},{g},{b})"


# Create surface data
surface_data = []
for i in range(n_points):
    for j in range(n_points):
        val = z_normalized[i, j]
        surface_data.append(
            {"x": float(X[i, j]), "y": float(Z[i, j]), "z": float(Y[i, j]), "color": get_viridis_color(val)}
        )

# Create connecting lines for X direction (reduced density)
x_line_series = []
for i in range(0, n_points, 2):
    line_data = []
    for j in range(n_points):
        val = z_normalized[i, j]
        line_data.append(
            {"x": float(X[i, j]), "y": float(Z[i, j]), "z": float(Y[i, j]), "color": get_viridis_color(val)}
        )

    mid_val = z_normalized[i, n_points // 2]
    x_line_series.append(
        {
            "type": "scatter3d",
            "data": line_data,
            "lineWidth": 3,
            "showInLegend": False,
            "marker": {"enabled": False},
            "color": get_viridis_color(mid_val),
        }
    )

# Create connecting lines for Y direction (reduced density)
y_line_series = []
for j in range(0, n_points, 2):
    line_data = []
    for i in range(n_points):
        val = z_normalized[i, j]
        line_data.append(
            {"x": float(X[i, j]), "y": float(Z[i, j]), "z": float(Y[i, j]), "color": get_viridis_color(val)}
        )

    mid_val = z_normalized[n_points // 2, j]
    y_line_series.append(
        {
            "type": "scatter3d",
            "data": line_data,
            "lineWidth": 3,
            "showInLegend": False,
            "marker": {"enabled": False},
            "color": get_viridis_color(mid_val),
        }
    )

# Surface points
surface_series = {
    "type": "scatter3d",
    "data": surface_data,
    "showInLegend": False,
    "marker": {"enabled": True, "radius": 8, "symbol": "circle"},
    "colorKey": "color",
}

all_series = [surface_series] + x_line_series + y_line_series
series_json = json.dumps(all_series)


# Download Highcharts modules with fallback CDNs
def download_js(urls):
    """Download JS with fallback to multiple CDNs."""
    for url in urls:
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
            )
            with urllib.request.urlopen(req, timeout=60) as response:
                return response.read().decode("utf-8")
        except (HTTPError, URLError):
            continue
    raise RuntimeError("Failed to download Highcharts from all CDN sources")


highcharts_urls = [
    "https://code.highcharts.com/highcharts.js",
    "https://cdn.jsdelivr.net/npm/highcharts/dist/highcharts.js",
]

highcharts_3d_urls = [
    "https://code.highcharts.com/highcharts-3d.js",
    "https://cdn.jsdelivr.net/npm/highcharts/dist/highcharts-3d.js",
]

highcharts_js = download_js(highcharts_urls)
highcharts_3d_js = download_js(highcharts_3d_urls)

# Highcharts chart configuration with theme-adaptive colors
chart_config = f"""
Highcharts.chart('container', {{
    chart: {{
        renderTo: 'container',
        type: 'scatter3d',
        width: 4800,
        height: 2700,
        backgroundColor: '{PAGE_BG}',
        options3d: {{
            enabled: true,
            alpha: 15,
            beta: 30,
            depth: 550,
            viewDistance: 3,
            fitToPlot: false,
            frame: {{
                bottom: {{ size: 1, color: 'rgba(26,26,23,0.08)' }},
                back: {{ size: 1, color: 'rgba(26,26,23,0.05)' }},
                side: {{ size: 1, color: 'rgba(26,26,23,0.05)' }}
            }}
        }},
        marginTop: 220,
        marginBottom: 250,
        marginLeft: 200,
        marginRight: 550
    }},
    title: {{
        text: 'surface-basic · highcharts · anyplot.ai',
        style: {{ fontSize: '28px', fontWeight: '500', color: '{INK}' }}
    }},
    subtitle: {{
        text: 'Gaussian Surface with Peaks and Valley',
        style: {{ fontSize: '20px', color: '{INK_SOFT}' }}
    }},
    xAxis: {{
        min: -3.5,
        max: 3.5,
        tickInterval: 1,
        title: {{
            text: 'X Position (units)',
            style: {{ fontSize: '22px', color: '{INK}', fontWeight: '500' }},
            margin: 80
        }},
        labels: {{
            style: {{ fontSize: '18px', color: '{INK_SOFT}' }},
            format: '{{value}}',
            y: 30
        }},
        gridLineWidth: 1,
        gridLineColor: '{GRID}',
        lineColor: '{INK_SOFT}',
        tickColor: '{INK_SOFT}'
    }},
    yAxis: {{
        min: -0.6,
        max: 1.2,
        tickInterval: 0.3,
        title: {{
            text: 'Z Height (amplitude)',
            style: {{ fontSize: '22px', color: '{INK}', fontWeight: '500' }},
            margin: 60
        }},
        labels: {{
            style: {{ fontSize: '18px', color: '{INK_SOFT}' }},
            format: '{{value:.1f}}',
            x: -20
        }},
        gridLineWidth: 1,
        gridLineColor: '{GRID}',
        lineColor: '{INK_SOFT}',
        tickColor: '{INK_SOFT}'
    }},
    zAxis: {{
        min: -3.5,
        max: 3.5,
        tickInterval: 1,
        title: {{
            text: 'Y Position (units)',
            style: {{ fontSize: '22px', color: '{INK}', fontWeight: '500' }},
            margin: 80
        }},
        labels: {{
            style: {{ fontSize: '18px', color: '{INK_SOFT}' }}
        }},
        gridLineWidth: 1,
        gridLineColor: '{GRID}',
        lineColor: '{INK_SOFT}',
        tickColor: '{INK_SOFT}'
    }},
    legend: {{
        enabled: false
    }},
    credits: {{
        enabled: false
    }},
    tooltip: {{
        enabled: false
    }},
    plotOptions: {{
        scatter3d: {{
            lineWidth: 3,
            states: {{
                hover: {{ enabled: false }},
                inactive: {{ opacity: 1 }}
            }}
        }}
    }},
    series: {series_json}
}});

// Draw colorbar manually
var chart = Highcharts.charts[0];
var renderer = chart.renderer;

var colorbarX = 4300;
var colorbarY = 550;
var colorbarWidth = 70;
var colorbarHeight = 1300;

var numSteps = 50;
var stepHeight = colorbarHeight / numSteps;
var colors = [
    [68, 1, 84],
    [59, 82, 139],
    [33, 145, 140],
    [94, 201, 98],
    [253, 231, 37]
];

for (var i = 0; i < numSteps; i++) {{
    var val = i / (numSteps - 1);
    var nColors = colors.length - 1;
    var idx = Math.min(Math.floor(val * nColors), nColors - 1);
    var t = (val * nColors) - idx;
    var r = Math.round(colors[idx][0] + t * (colors[idx + 1][0] - colors[idx][0]));
    var g = Math.round(colors[idx][1] + t * (colors[idx + 1][1] - colors[idx][1]));
    var b = Math.round(colors[idx][2] + t * (colors[idx + 1][2] - colors[idx][2]));

    renderer.rect(colorbarX, colorbarY + colorbarHeight - (i + 1) * stepHeight, colorbarWidth, stepHeight + 1)
        .attr({{
            fill: 'rgb(' + r + ',' + g + ',' + b + ')',
            'stroke-width': 0
        }})
        .add();
}}

// Colorbar border
renderer.rect(colorbarX, colorbarY, colorbarWidth, colorbarHeight)
    .attr({{
        'stroke': '{INK_SOFT}',
        'stroke-width': 3,
        fill: 'none'
    }})
    .add();

// Colorbar labels
var zMin = {z_min:.2f};
var zMax = {z_max:.2f};
var labelValues = [zMin, zMin + (zMax - zMin) * 0.25, (zMin + zMax) / 2, zMin + (zMax - zMin) * 0.75, zMax];
var labelPositions = [
    colorbarY + colorbarHeight,
    colorbarY + colorbarHeight * 0.75,
    colorbarY + colorbarHeight / 2,
    colorbarY + colorbarHeight * 0.25,
    colorbarY
];

for (var j = 0; j < 5; j++) {{
    renderer.text(labelValues[j].toFixed(2), colorbarX + colorbarWidth + 25, labelPositions[j] + 15)
        .css({{
            fontSize: '18px',
            fontWeight: '500',
            color: '{INK_SOFT}'
        }})
        .add();
}}

// Colorbar title
renderer.text('Z Height (amplitude)', colorbarX + colorbarWidth / 2, colorbarY - 50)
    .attr({{
        align: 'center'
    }})
    .css({{
        fontSize: '20px',
        fontWeight: '500',
        color: '{INK}'
    }})
    .add();
"""

# Generate HTML with inline scripts
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{highcharts_3d_js}</script>
</head>
<body style="margin:0; background:{PAGE_BG};">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>{chart_config}</script>
</body>
</html>"""

# Save HTML artifact
with open(f"plot-{THEME}.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Write temp HTML and take screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4800,2700")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(10)
driver.save_screenshot(f"plot-{THEME}.png")
driver.quit()

Path(temp_path).unlink()
