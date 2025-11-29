# highcharts

**Note**: Highcharts requires a license for commercial use.

## Import

```python
# IMPORTANT: Correct import path
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.bar import BarSeries
from highcharts_core.options.series.scatter import ScatterSeries
```

## Create Chart

```python
chart = Chart()
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
from highcharts_core.options.series.bar import BarSeries
from highcharts_core.options.series.line import LineSeries
from highcharts_core.options.series.scatter import ScatterSeries
from highcharts_core.options.series.area import AreaSeries
from highcharts_core.options.series.pie import PieSeries
from highcharts_core.options.series.boxplot import BoxPlotSeries
```

## HTML Export

```python
# As HTML string
html = chart.to_js_literal()

# As HTML file
with open('plot.html', 'w') as f:
    f.write(f'''
    <html>
    <head>
        <script src="https://code.highcharts.com/highcharts.js"></script>
    </head>
    <body>
        <div id="container"></div>
        <script>
            Highcharts.chart('container', {html});
        </script>
    </body>
    </html>
    ''')
```

## PNG Export (via Selenium)

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def export_to_png(chart, filename='plot.png'):
    # Generate HTML
    html_content = f'''...'''  # as above

    # Selenium screenshot
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    driver.get(f'data:text/html,{html_content}')
    driver.set_window_size(1600, 900)

    element = driver.find_element('id', 'container')
    element.screenshot(filename)

    driver.quit()
```

## Chart Size

```python
chart.options.chart = {
    'width': 1600,
    'height': 900
}
```

## Folder-Name

`plots/highcharts/{series_type}/`

| Series | Folder |
|--------|--------|
| `ScatterSeries` | `scatter/` |
| `LineSeries` | `line/` |
| `BarSeries` | `bar/` |
| `BoxPlotSeries` | `boxplot/` |

## Return Type

```python
def create_plot(...) -> Chart:
```
