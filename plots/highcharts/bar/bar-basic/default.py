"""
bar-basic: Basic Bar Chart
Library: highcharts

A fundamental vertical bar chart that visualizes categorical data with numeric values.

Note: Highcharts requires a license for commercial use.
"""

from typing import Optional

import pandas as pd
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.bar import ColumnSeries


def create_plot(
    data: pd.DataFrame,
    category: str,
    value: str,
    figsize: tuple[int, int] = (10, 6),
    color: str = "steelblue",
    edgecolor: str = "black",
    alpha: float = 0.8,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    rotation: int = 0,
    width: int = 1600,
    height: int = 900,
    **kwargs,
) -> Chart:
    """
    Create a basic bar chart from DataFrame.

    Args:
        data: Input DataFrame with categorical and numeric data
        category: Column name for category labels (x-axis)
        value: Column name for numeric values (bar heights)
        figsize: Figure size as (width, height) in inches (legacy, use width/height instead)
        color: Bar fill color
        edgecolor: Bar edge color
        alpha: Transparency level for bars (0.0 to 1.0)
        title: Plot title
        xlabel: X-axis label (defaults to column name if None)
        ylabel: Y-axis label (defaults to column name if None)
        rotation: Rotation angle for x-axis labels
        width: Figure width in pixels (default: 1600)
        height: Figure height in pixels (default: 900)
        **kwargs: Additional parameters passed to chart options

    Returns:
        Highcharts Chart object

    Raises:
        ValueError: If data is empty
        KeyError: If required columns are not found in data

    Example:
        >>> data = pd.DataFrame({
        ...     'category': ['A', 'B', 'C'],
        ...     'value': [10, 20, 30]
        ... })
        >>> chart = create_plot(data, 'category', 'value', title='My Chart')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    for col in [category, value]:
        if col not in data.columns:
            available = ", ".join(data.columns.tolist())
            raise KeyError(f"Column '{col}' not found. Available: {available}")

    # Create chart with container ID for rendering
    chart = Chart(container="container")
    chart.options = HighchartsOptions()

    # Chart configuration
    chart.options.chart = {"type": "column", "width": width, "height": height, "backgroundColor": "#ffffff"}

    # Title
    if title:
        chart.options.title = {"text": title, "style": {"fontSize": "16px", "fontWeight": "bold"}}
    else:
        chart.options.title = {"text": None}

    # X-axis configuration
    categories = data[category].tolist()
    x_label = xlabel if xlabel is not None else category
    chart.options.x_axis = {
        "categories": categories,
        "title": {"text": x_label, "style": {"fontSize": "12px"}},
        "labels": {"rotation": -rotation if rotation else 0, "style": {"fontSize": "10px"}},
    }

    # Y-axis configuration with subtle grid (y-axis only per spec)
    y_label = ylabel if ylabel is not None else value
    chart.options.y_axis = {
        "title": {"text": y_label, "style": {"fontSize": "12px"}},
        "min": 0,
        "gridLineWidth": 1,
        "gridLineDashStyle": "Dot",
        "gridLineColor": "rgba(0, 0, 0, 0.15)",
        "labels": {"style": {"fontSize": "10px"}},
    }

    # Create series with column type (vertical bars in Highcharts)
    series = ColumnSeries()
    series.data = data[value].tolist()
    series.name = y_label
    series.color = color
    series.border_color = edgecolor
    series.border_width = 1

    # Set opacity via plot options
    chart.options.plot_options = {
        "column": {"opacity": alpha, "pointPadding": 0.1, "groupPadding": 0.1, "borderWidth": 1, "colorByPoint": False}
    }

    chart.add_series(series)

    # Legend (single series, so hide legend)
    chart.options.legend = {"enabled": False}

    # Credits
    chart.options.credits = {"enabled": False}

    return chart


if __name__ == "__main__":
    import tempfile
    import time
    import urllib.request
    from pathlib import Path

    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    # Sample data for testing
    sample_data = pd.DataFrame(
        {"category": ["Product A", "Product B", "Product C", "Product D", "Product E"], "value": [45, 78, 52, 91, 63]}
    )

    # Create plot
    chart = create_plot(
        sample_data, "category", "value", title="Sales by Product", xlabel="Product Category", ylabel="Sales ($)"
    )

    # Download Highcharts JS (required for headless Chrome which can't load CDN)
    highcharts_url = "https://code.highcharts.com/highcharts.js"
    with urllib.request.urlopen(highcharts_url, timeout=30) as response:
        highcharts_js = response.read().decode("utf-8")

    # Export to PNG via Selenium screenshot
    # Note: to_js_literal() includes DOMContentLoaded wrapper and Highcharts.chart() call
    html_str = chart.to_js_literal()
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 1600px; height: 900px;"></div>
    <script>{html_str}</script>
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
    chrome_options.add_argument("--window-size=1600,900")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f"file:///{temp_path}")
    time.sleep(5)  # Wait for chart to render
    driver.save_screenshot("plot.png")
    driver.quit()

    Path(temp_path).unlink()  # Clean up temp file
    print("Plot saved to plot.png")
