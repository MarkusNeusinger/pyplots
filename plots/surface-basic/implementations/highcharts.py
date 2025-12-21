""" pyplots.ai
surface-basic: Basic 3D Surface Plot
Library: highcharts 1.10.3 | Python 3.13.11
Quality: 92/100 | Created: 2025-12-17
"""

import json
import tempfile
import time
import urllib.request
from pathlib import Path

import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - Gaussian surface with peaks and valleys
np.random.seed(42)
n_points = 40  # Grid size for smooth surface
x = np.linspace(-3, 3, n_points)
y = np.linspace(-3, 3, n_points)
X, Y = np.meshgrid(x, y)

# Create an interesting surface: combination of Gaussian peaks
Z = (
    np.exp(-((X - 1) ** 2 + (Y - 1) ** 2))  # Peak at (1, 1)
    + 0.8 * np.exp(-((X + 1) ** 2 + (Y + 1) ** 2))  # Peak at (-1, -1)
    - 0.5 * np.exp(-((X) ** 2 + (Y) ** 2) / 0.5)  # Valley at center
)

# Normalize Z values for color mapping
z_min, z_max = Z.min(), Z.max()
z_normalized = (Z - z_min) / (z_max - z_min)

# Download required Highcharts modules
highcharts_url = "https://code.highcharts.com/highcharts.js"
highcharts_3d_url = "https://code.highcharts.com/highcharts-3d.js"

with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

with urllib.request.urlopen(highcharts_3d_url, timeout=30) as response:
    highcharts_3d_js = response.read().decode("utf-8")


# Color interpolation function for viridis-like colormap
def get_color(value):
    """Get viridis-like color for value in [0, 1]"""
    # Viridis-inspired colors: dark blue -> teal -> green -> yellow
    colors = [
        (68, 1, 84),  # Dark purple
        (59, 82, 139),  # Blue-purple
        (33, 145, 140),  # Teal
        (94, 201, 98),  # Green
        (253, 231, 37),  # Yellow
    ]
    # Interpolate between colors
    n_colors = len(colors) - 1
    idx = min(int(value * n_colors), n_colors - 1)
    t = (value * n_colors) - idx
    r = int(colors[idx][0] + t * (colors[idx + 1][0] - colors[idx][0]))
    g = int(colors[idx][1] + t * (colors[idx + 1][1] - colors[idx][1]))
    b = int(colors[idx][2] + t * (colors[idx + 1][2] - colors[idx][2]))
    return f"rgb({r},{g},{b})"


# Create surface data as scatter3d points with colors
surface_data = []
for i in range(n_points):
    for j in range(n_points):
        surface_data.append(
            {
                "x": float(X[i, j]),
                "y": float(Z[i, j]),  # Height is Z value
                "z": float(Y[i, j]),  # Depth is Y grid position
                "color": get_color(z_normalized[i, j]),
            }
        )

# Create connecting lines for X direction to show surface structure
x_line_series = []
for i in range(n_points):
    line_data = []
    for j in range(n_points):
        color_val = z_normalized[i, j]
        line_data.append({"x": float(X[i, j]), "y": float(Z[i, j]), "z": float(Y[i, j]), "color": get_color(color_val)})
    x_line_series.append(
        {
            "type": "scatter3d",
            "data": line_data,
            "lineWidth": 3,
            "showInLegend": False,
            "marker": {"enabled": False},
            "color": get_color(z_normalized[i, n_points // 2]),
        }
    )

# Create connecting lines for Y direction
y_line_series = []
for j in range(n_points):
    line_data = []
    for i in range(n_points):
        color_val = z_normalized[i, j]
        line_data.append({"x": float(X[i, j]), "y": float(Z[i, j]), "z": float(Y[i, j]), "color": get_color(color_val)})
    y_line_series.append(
        {
            "type": "scatter3d",
            "data": line_data,
            "lineWidth": 3,
            "showInLegend": False,
            "marker": {"enabled": False},
            "color": get_color(z_normalized[n_points // 2, j]),
        }
    )

# Surface points with large markers to create filled appearance
surface_series = {
    "type": "scatter3d",
    "data": surface_data,
    "showInLegend": False,
    "marker": {"enabled": True, "radius": 6, "symbol": "circle"},
    "colorKey": "color",
}

all_series = [surface_series] + x_line_series + y_line_series
series_json = json.dumps(all_series)

# Highcharts chart configuration
chart_config = f"""
Highcharts.chart('container', {{
    chart: {{
        renderTo: 'container',
        type: 'scatter3d',
        width: 4800,
        height: 2700,
        backgroundColor: '#ffffff',
        options3d: {{
            enabled: true,
            alpha: 15,
            beta: 30,
            depth: 400,
            viewDistance: 5,
            fitToPlot: true,
            frame: {{
                bottom: {{ size: 1, color: 'rgba(0,0,0,0.05)' }},
                back: {{ size: 1, color: 'rgba(0,0,0,0.03)' }},
                side: {{ size: 1, color: 'rgba(0,0,0,0.03)' }}
            }}
        }},
        marginTop: 180,
        marginBottom: 200,
        marginLeft: 180,
        marginRight: 180
    }},
    title: {{
        text: 'surface-basic · highcharts · pyplots.ai',
        style: {{ fontSize: '72px', fontWeight: 'bold' }}
    }},
    subtitle: {{
        text: 'Gaussian Surface with Peaks and Valley',
        style: {{ fontSize: '48px', color: '#666666' }}
    }},
    xAxis: {{
        min: -3.5,
        max: 3.5,
        tickInterval: 1,
        title: {{
            text: 'X',
            style: {{ fontSize: '48px', color: '#306998', fontWeight: 'bold' }},
            margin: 40
        }},
        labels: {{
            style: {{ fontSize: '32px' }},
            format: '{{value}}'
        }},
        gridLineWidth: 1,
        gridLineColor: 'rgba(0, 0, 0, 0.1)'
    }},
    yAxis: {{
        min: -0.6,
        max: 1.2,
        tickInterval: 0.3,
        title: {{
            text: 'Z (Height)',
            style: {{ fontSize: '48px', color: '#306998', fontWeight: 'bold' }},
            margin: 30
        }},
        labels: {{
            style: {{ fontSize: '32px' }},
            format: '{{value:.1f}}'
        }},
        gridLineWidth: 1,
        gridLineColor: 'rgba(0, 0, 0, 0.1)'
    }},
    zAxis: {{
        min: -3.5,
        max: 3.5,
        tickInterval: 1,
        title: {{
            text: 'Y',
            style: {{ fontSize: '48px', color: '#306998', fontWeight: 'bold' }}
        }},
        labels: {{
            style: {{ fontSize: '32px' }}
        }},
        gridLineWidth: 1,
        gridLineColor: 'rgba(0, 0, 0, 0.1)'
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
                hover: {{
                    enabled: false
                }},
                inactive: {{
                    opacity: 1
                }}
            }}
        }}
    }},
    series: {series_json}
}});
"""

# Generate HTML with inline scripts
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{highcharts_3d_js}</script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>{chart_config}</script>
</body>
</html>"""

# Write temp HTML and take screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4800,2800")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(8)  # Extra time for 3D rendering with many series

# Take screenshot of just the chart container element
container = driver.find_element("id", "container")
container.screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()

# Also save HTML for interactive version
with open("plot.html", "w", encoding="utf-8") as f:
    interactive_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/highcharts-3d.js"></script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 100%; height: 100vh;"></div>
    <script>{chart_config}</script>
</body>
</html>"""
    f.write(interactive_html)
