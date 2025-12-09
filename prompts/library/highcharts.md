# highcharts

**Note**: Highcharts requires a license for commercial use.

## Import

```python
# IMPORTANT: Correct import path
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.bar import BarSeries, ColumnSeries
from highcharts_core.options.series.scatter import ScatterSeries
```

## Create Chart

**CRITICAL**: Always pass `container="container"` to the Chart constructor. This ensures the generated JavaScript targets the correct HTML element.

```python
# CORRECT - always specify container
chart = Chart(container="container")
chart.options = HighchartsOptions()

# Title
chart.options.title = {'text': title}

# Axes
chart.options.x_axis = {'title': {'text': x_label}}
chart.options.y_axis = {'title': {'text': y_label}}
```

## Add Series

```python
from highcharts_core.options.series.scatter import ScatterSeries

series = ScatterSeries()
series.data = list(zip(x_values, y_values))
series.name = 'Data'

chart.add_series(series)
```

## Series Types

```python
from highcharts_core.options.series.bar import BarSeries, ColumnSeries  # ColumnSeries for vertical bars
from highcharts_core.options.series.line import LineSeries
from highcharts_core.options.series.scatter import ScatterSeries
from highcharts_core.options.series.area import AreaSeries
from highcharts_core.options.series.pie import PieSeries
from highcharts_core.options.series.boxplot import BoxPlotSeries
```

## PNG Export (via Selenium)

**IMPORTANT**: Headless Chrome cannot load external CDN scripts from `file://` URLs. You MUST download Highcharts JS and embed it inline.

```python
import tempfile
import time
import urllib.request
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Download Highcharts JS (required for headless Chrome)
highcharts_url = "https://code.highcharts.com/highcharts.js"
with urllib.request.urlopen(highcharts_url, timeout=30) as response:
    highcharts_js = response.read().decode("utf-8")

# For boxplot/errorbar charts, also download highcharts-more.js:
# highcharts_more_url = "https://code.highcharts.com/highcharts-more.js"
# with urllib.request.urlopen(highcharts_more_url, timeout=30) as response:
#     highcharts_more_js = response.read().decode("utf-8")

# Generate HTML with INLINE scripts (not CDN links!)
html_str = chart.to_js_literal()
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 4800px; height: 2700px;"></div>
    <script>{html_str}</script>
</body>
</html>"""

# Write temp HTML and take screenshot
# IMPORTANT: Use encoding="utf-8" for special characters in Highcharts JS
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
time.sleep(5)  # Wait for chart to render
driver.save_screenshot("plot.png")
driver.quit()

Path(temp_path).unlink()  # Clean up temp file
```

## Chart Size

```python
# Target: 4800 × 2700 px (see default-style-guide.md)
chart.options.chart = {
    'type': 'column',  # or 'bar', 'scatter', etc.
    'width': 4800,
    'height': 2700,
    'backgroundColor': '#ffffff'
}
```

## Output File

`plots/{spec-id}/implementations/highcharts.py`

## Common Pitfalls

1. **White/blank images**: Forgetting `container="container"` in Chart() constructor
2. **CDN not loading**: Using `<script src="...">` instead of inline scripts in headless Chrome
3. **Missing modules**: BoxPlot needs `highcharts-more.js` in addition to `highcharts.js`
4. **Screenshot timing**: Use `time.sleep(5)` for reliable rendering
5. **Encoding errors**: Always use `encoding="utf-8"` in NamedTemporaryFile (Highcharts JS contains special Unicode characters)
