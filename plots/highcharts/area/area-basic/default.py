"""
area-basic: Basic Area Chart
Implementation for: highcharts
Variant: default
Python: 3.10+

Note: Highcharts requires a license for commercial use.
"""

from typing import Optional

import pandas as pd
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.area import AreaSeries


def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    color: str = "#4682B4",
    fill_opacity: float = 0.5,
    line_width: int = 2,
    width: int = 1600,
    height: int = 900,
    **kwargs,
) -> Chart:
    """
    Create a basic area chart showing magnitude and trends using Highcharts.

    Args:
        data: Input DataFrame with required columns
        x: Column name for x-axis values
        y: Column name for y-axis values (numeric)
        title: Plot title (optional)
        xlabel: Custom x-axis label (optional, defaults to x column name)
        ylabel: Custom y-axis label (optional, defaults to y column name)
        color: Fill and line color (default: "#4682B4" steelblue)
        fill_opacity: Transparency level for the fill area (default: 0.5)
        line_width: Width of the line on top of the area (default: 2)
        width: Figure width in pixels (default: 1600)
        height: Figure height in pixels (default: 900)
        **kwargs: Additional parameters for Highcharts configuration

    Returns:
        Highcharts Chart object

    Raises:
        ValueError: If data is empty
        KeyError: If required columns not found

    Example:
        >>> data = pd.DataFrame({
        ...     'month': [1, 2, 3, 4, 5, 6],
        ...     'sales': [100, 150, 130, 180, 200, 220]
        ... })
        >>> chart = create_plot(data, x='month', y='sales')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    # Check required columns
    for col in [x, y]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available columns: {available}")

    # Prepare data - sort by x values for proper area rendering
    sorted_data = data[[x, y]].dropna().sort_values(by=x)
    x_values = sorted_data[x].tolist()
    y_values = sorted_data[y].tolist()

    # Determine if x-axis should be categorical or numeric
    x_is_numeric = pd.api.types.is_numeric_dtype(data[x])

    # Create chart
    chart = Chart()

    # Configure chart options
    chart.options = HighchartsOptions()

    # Title
    chart.options.title = {
        "text": title or "Area Chart",
        "style": {"fontSize": "16px", "fontWeight": "bold"},
    }

    # X-axis configuration
    if x_is_numeric:
        chart.options.x_axis = {
            "title": {"text": xlabel or x},
            "gridLineWidth": 1,
            "gridLineDashStyle": "Dot",
            "gridLineColor": "rgba(0, 0, 0, 0.1)",
        }
    else:
        # Categorical x-axis
        chart.options.x_axis = {
            "categories": x_values,
            "title": {"text": xlabel or x},
            "gridLineWidth": 1,
            "gridLineDashStyle": "Dot",
            "gridLineColor": "rgba(0, 0, 0, 0.1)",
        }

    # Y-axis
    chart.options.y_axis = {
        "title": {"text": ylabel or y},
        "gridLineWidth": 1,
        "gridLineDashStyle": "Dot",
        "gridLineColor": "rgba(0, 0, 0, 0.1)",
        "min": 0,  # Area charts typically start from 0
    }

    # Plot options for area series
    chart.options.plot_options = {
        "area": {
            "fillOpacity": fill_opacity,
            "lineWidth": line_width,
            "marker": {
                "enabled": True,
                "radius": 4,
                "fillColor": color,
                "lineWidth": 1,
                "lineColor": "#ffffff",
            },
        }
    }

    # Tooltip
    chart.options.tooltip = {
        "shared": False,
        "useHTML": True,
        "headerFormat": "<b>{point.key}</b><br/>",
        "pointFormat": f"<span>{ylabel or y}: {{point.y}}</span>",
    }

    # Chart dimensions and type
    chart.options.chart = {
        "type": "area",
        "width": width,
        "height": height,
        "backgroundColor": "white",
    }

    # Create area series
    area_series = AreaSeries()
    area_series.name = ylabel or y
    area_series.color = color

    # Set data based on x-axis type
    if x_is_numeric:
        # For numeric x-axis, use [x, y] pairs
        area_series.data = list(zip(x_values, y_values, strict=True))
    else:
        # For categorical x-axis, use y values only (categories are set on x-axis)
        area_series.data = y_values

    chart.add_series(area_series)

    # Legend
    chart.options.legend = {
        "enabled": False,  # Single series, no legend needed
    }

    # Credits
    chart.options.credits = {"enabled": False}

    return chart


if __name__ == "__main__":
    import tempfile
    import time
    from pathlib import Path

    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    # Sample data for testing - monthly sales data
    sample_data = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "Sales": [120, 150, 170, 160, 180, 220, 250, 240, 210, 190, 230, 280],
    })

    # Create plot with categorical x-axis
    chart = create_plot(
        sample_data,
        x="Month",
        y="Sales",
        title="Monthly Sales Performance",
        ylabel="Sales ($K)",
        xlabel="Month",
        color="#4682B4",
        fill_opacity=0.4,
    )

    # Generate HTML content
    html_str = chart.to_js_literal()
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://code.highcharts.com/highcharts.js"></script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 1600px; height: 900px;"></div>
    <script>{html_str}</script>
</body>
</html>"""

    # Write temp HTML and take screenshot
    with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
        f.write(html_content)
        temp_path = f.name

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1600,900")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f"file://{temp_path}")
    time.sleep(1)  # Wait for chart to render
    driver.save_screenshot("plot.png")
    driver.quit()

    Path(temp_path).unlink()  # Clean up temp file
    print("Plot saved to plot.png")
