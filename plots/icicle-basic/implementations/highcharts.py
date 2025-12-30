""" pyplots.ai
icicle-basic: Basic Icicle Chart
Library: highcharts unknown | Python 3.13.11
Quality: 78/100 | Created: 2025-12-30
"""

import json
import tempfile
import time
import urllib.request
from pathlib import Path

from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Data - File system hierarchy with folders and files
# Hierarchical structure showing directories and file sizes (KB)
# Color-coded by top-level directory with colorblind-safe palette
data = [
    # Root - explicitly visible at top (gray background)
    {"id": "root", "name": "Project Files", "color": "#5A5A5A", "value": 2000},
    # Level 1 - Main directories (each with distinct color)
    {"id": "src", "name": "src", "parent": "root", "color": "#306998"},
    {"id": "docs", "name": "docs", "parent": "root", "color": "#FFD43B"},
    {"id": "tests", "name": "tests", "parent": "root", "color": "#9467BD"},
    {"id": "assets", "name": "assets", "parent": "root", "color": "#17BECF"},
    # Level 2 - src subdirectories (inherit src color)
    {"id": "components", "name": "components", "parent": "src", "color": "#306998"},
    {"id": "utils", "name": "utils", "parent": "src", "color": "#306998"},
    {"id": "api", "name": "api", "parent": "src", "color": "#306998"},
    # Level 2 - docs files (inherit docs color, leaf nodes with values)
    {"name": "README.md", "parent": "docs", "value": 45, "color": "#FFD43B"},
    {"name": "guide.md", "parent": "docs", "value": 120, "color": "#FFD43B"},
    {"name": "api.md", "parent": "docs", "value": 85, "color": "#FFD43B"},
    # Level 2 - tests files (inherit tests color)
    {"name": "test_main.py", "parent": "tests", "value": 65, "color": "#9467BD"},
    {"name": "test_utils.py", "parent": "tests", "value": 48, "color": "#9467BD"},
    {"name": "test_api.py", "parent": "tests", "value": 72, "color": "#9467BD"},
    # Level 2 - assets subdirectories (inherit assets color)
    {"id": "images", "name": "images", "parent": "assets", "color": "#17BECF"},
    {"id": "styles", "name": "styles", "parent": "assets", "color": "#17BECF"},
    # Level 3 - components files (lighter shade of src blue)
    {"name": "Header.tsx", "parent": "components", "value": 95, "color": "#4A7FB0"},
    {"name": "Footer.tsx", "parent": "components", "value": 55, "color": "#4A7FB0"},
    {"name": "Sidebar.tsx", "parent": "components", "value": 110, "color": "#4A7FB0"},
    {"name": "Modal.tsx", "parent": "components", "value": 78, "color": "#4A7FB0"},
    # Level 3 - utils files
    {"name": "helpers.ts", "parent": "utils", "value": 42, "color": "#4A7FB0"},
    {"name": "constants.ts", "parent": "utils", "value": 28, "color": "#4A7FB0"},
    {"name": "validators.ts", "parent": "utils", "value": 65, "color": "#4A7FB0"},
    # Level 3 - api files
    {"name": "client.ts", "parent": "api", "value": 88, "color": "#4A7FB0"},
    {"name": "endpoints.ts", "parent": "api", "value": 56, "color": "#4A7FB0"},
    {"name": "types.ts", "parent": "api", "value": 34, "color": "#4A7FB0"},
    # Level 3 - images files (lighter shade of assets cyan)
    {"name": "logo.png", "parent": "images", "value": 125, "color": "#4DCCE5"},
    {"name": "banner.jpg", "parent": "images", "value": 280, "color": "#4DCCE5"},
    {"name": "icons.svg", "parent": "images", "value": 45, "color": "#4DCCE5"},
    # Level 3 - styles files
    {"name": "main.css", "parent": "styles", "value": 92, "color": "#4DCCE5"},
    {"name": "theme.css", "parent": "styles", "value": 68, "color": "#4DCCE5"},
]

data_json = json.dumps(data)

# Highcharts configuration for icicle chart using treemap with sliceAndDice layout
# sliceAndDice creates adjacent rectangles that show parent-child relationships
# through spatial adjacency - the defining characteristic of icicle charts
chart_config = f"""
Highcharts.chart('container', {{
    chart: {{
        width: 4800,
        height: 2700,
        backgroundColor: '#ffffff',
        marginTop: 180,
        marginBottom: 250,
        marginLeft: 80,
        marginRight: 80
    }},
    title: {{
        text: 'icicle-basic · highcharts · pyplots.ai',
        style: {{
            fontSize: '56px',
            fontWeight: 'bold'
        }}
    }},
    subtitle: {{
        text: 'File System Structure - Directory hierarchy showing file sizes (KB)',
        style: {{
            fontSize: '36px'
        }}
    }},
    legend: {{
        enabled: true,
        align: 'center',
        verticalAlign: 'bottom',
        layout: 'horizontal',
        itemStyle: {{
            fontSize: '32px',
            fontWeight: 'normal'
        }},
        symbolHeight: 28,
        symbolWidth: 28,
        symbolRadius: 4,
        itemMarginBottom: 10,
        itemMarginTop: 20,
        y: 30
    }},
    tooltip: {{
        style: {{
            fontSize: '32px'
        }},
        formatter: function() {{
            if (this.point.value) {{
                return '<b>' + this.point.name + '</b><br/>Size: ' + this.point.value + ' KB';
            }}
            return '<b>' + this.point.name + '</b>';
        }}
    }},
    series: [{{
        type: 'treemap',
        name: 'File Size',
        layoutAlgorithm: 'sliceAndDice',
        layoutStartingDirection: 'horizontal',
        alternateStartingDirection: false,
        allowTraversingTree: true,
        animationLimit: 1000,
        borderWidth: 4,
        borderColor: '#ffffff',
        dataLabels: {{
            enabled: true,
            style: {{
                fontSize: '26px',
                fontWeight: 'normal',
                textOutline: '3px white'
            }},
            formatter: function() {{
                // Hide labels for very small rectangles
                if (this.point.shapeArgs && this.point.shapeArgs.width < 80) {{
                    return '';
                }}
                return this.point.name;
            }}
        }},
        levels: [{{
            level: 1,
            dataLabels: {{
                enabled: true,
                align: 'center',
                verticalAlign: 'middle',
                style: {{
                    fontSize: '52px',
                    fontWeight: 'bold',
                    textOutline: '4px white'
                }}
            }},
            borderWidth: 6,
            borderColor: '#ffffff'
        }}, {{
            level: 2,
            dataLabels: {{
                enabled: true,
                style: {{
                    fontSize: '40px',
                    fontWeight: 'bold',
                    textOutline: '3px white'
                }}
            }},
            borderWidth: 5,
            borderColor: '#ffffff'
        }}, {{
            level: 3,
            dataLabels: {{
                enabled: true,
                style: {{
                    fontSize: '32px',
                    fontWeight: 'normal',
                    textOutline: '3px white'
                }}
            }},
            borderWidth: 4,
            borderColor: '#ffffff'
        }}, {{
            level: 4,
            dataLabels: {{
                enabled: true,
                style: {{
                    fontSize: '26px',
                    fontWeight: 'normal',
                    textOutline: '2px white'
                }}
            }},
            borderWidth: 3,
            borderColor: '#ffffff'
        }}],
        data: {data_json}
    }}, {{
        // Empty series for legend entries
        type: 'line',
        name: 'src',
        color: '#306998',
        showInLegend: true,
        data: [],
        marker: {{ enabled: true, symbol: 'square', radius: 14 }},
        lineWidth: 0
    }}, {{
        type: 'line',
        name: 'docs',
        color: '#FFD43B',
        showInLegend: true,
        data: [],
        marker: {{ enabled: true, symbol: 'square', radius: 14 }},
        lineWidth: 0
    }}, {{
        type: 'line',
        name: 'tests',
        color: '#9467BD',
        showInLegend: true,
        data: [],
        marker: {{ enabled: true, symbol: 'square', radius: 14 }},
        lineWidth: 0
    }}, {{
        type: 'line',
        name: 'assets',
        color: '#17BECF',
        showInLegend: true,
        data: [],
        marker: {{ enabled: true, symbol: 'square', radius: 14 }},
        lineWidth: 0
    }}]
}});
"""

# Download Highcharts JS and treemap module
highcharts_url = "https://code.highcharts.com/highcharts.js"
treemap_url = "https://code.highcharts.com/modules/treemap.js"

with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

with urllib.request.urlopen(treemap_url, timeout=30) as response:
    treemap_js = response.read().decode("utf-8")

# Generate HTML with inline scripts
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{treemap_js}</script>
</head>
<body style="margin:0; padding:0; background:#ffffff;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>{chart_config}</script>
</body>
</html>"""

# Save HTML for interactive version
with open("plot.html", "w", encoding="utf-8") as f:
    standalone_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>icicle-basic · highcharts · pyplots.ai</title>
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/modules/treemap.js"></script>
    <style>
        body {{ margin: 0; padding: 20px; font-family: sans-serif; background: #ffffff; }}
        #container {{ width: 100%; height: 90vh; min-height: 600px; }}
    </style>
</head>
<body>
    <div id="container"></div>
    <script>{chart_config}</script>
</body>
</html>"""
    f.write(standalone_html)

# Write temp HTML and take screenshot
with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(html_content)
    temp_path = f.name

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=4800,2900")

driver = webdriver.Chrome(options=chrome_options)
driver.get(f"file://{temp_path}")
time.sleep(5)  # Wait for chart to render
driver.save_screenshot("plot_raw.png")
driver.quit()

# Crop to exact 4800x2700 dimensions
img = Image.open("plot_raw.png")
img_cropped = img.crop((0, 0, 4800, 2700))
img_cropped.save("plot.png")
Path("plot_raw.png").unlink()

Path(temp_path).unlink()  # Clean up temp file
