"""
line-basic: Basic Line Chart
Implementation for: highcharts
Variant: default
Python: 3.10+

Note: Highcharts requires a license for commercial use.
"""

from typing import Optional

import numpy as np
import pandas as pd
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.area import LineSeries


def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    color: str = "#4A90D9",
    linewidth: float = 2.0,
    marker: Optional[str] = None,
    marker_size: float = 6,
    alpha: float = 1.0,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    width: int = 1600,
    height: int = 900,
    **kwargs,
) -> Chart:
    """
    Create a basic line chart connecting data points in order using Highcharts.

    Args:
        data: Input DataFrame with required columns
        x: Column name for x-axis values (numeric or categorical)
        y: Column name for y-axis values (numeric)
        color: Line color (default: "#4A90D9" - a pleasant blue)
        linewidth: Line thickness in pixels (default: 2.0)
        marker: Marker style at data points, e.g., 'circle', 'square' (default: None)
        marker_size: Size of markers if shown (default: 6)
        alpha: Line transparency 0.0-1.0 (default: 1.0)
        title: Plot title (optional)
        xlabel: Custom x-axis label (optional, defaults to x column name)
        ylabel: Custom y-axis label (optional, defaults to y column name)
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
        ...     'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
        ...     'Sales': [100, 120, 115, 140, 160]
        ... })
        >>> chart = create_plot(data, x='Month', y='Sales')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    # Check required columns
    for col in [x, y]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available columns: {available}")

    # Prepare data
    x_values = data[x].tolist()
    y_values = data[y].tolist()

    # Determine if x-axis is categorical or numeric
    x_is_categorical = not pd.api.types.is_numeric_dtype(data[x])

    # Create chart
    chart = Chart()

    # Configure chart options
    chart.options = HighchartsOptions()

    # Title
    chart.options.title = {"text": title if title else None, "style": {"fontSize": "16px", "fontWeight": "bold"}}

    # X-axis configuration
    if x_is_categorical:
        chart.options.x_axis = {
            "categories": x_values,
            "title": {"text": xlabel or x, "style": {"fontSize": "12px"}},
            "labels": {"style": {"fontSize": "11px"}},
            "gridLineWidth": 1,
            "gridLineDashStyle": "Dot",
            "gridLineColor": "rgba(0, 0, 0, 0.1)",
        }
    else:
        chart.options.x_axis = {
            "title": {"text": xlabel or x, "style": {"fontSize": "12px"}},
            "labels": {"style": {"fontSize": "11px"}},
            "gridLineWidth": 1,
            "gridLineDashStyle": "Dot",
            "gridLineColor": "rgba(0, 0, 0, 0.1)",
        }

    # Y-axis configuration
    chart.options.y_axis = {
        "title": {"text": ylabel or y, "style": {"fontSize": "12px"}},
        "labels": {"style": {"fontSize": "11px"}},
        "gridLineWidth": 1,
        "gridLineDashStyle": "Dot",
        "gridLineColor": "rgba(0, 0, 0, 0.3)",
    }

    # Chart dimensions and background
    chart.options.chart = {"type": "line", "width": width, "height": height, "backgroundColor": "white"}

    # Plot options for line series
    plot_options: dict = {"line": {"lineWidth": linewidth, "connectNulls": False, "animation": False}}

    # Handle marker configuration
    if marker:
        marker_config: dict = {"enabled": True, "radius": marker_size, "symbol": marker}
        plot_options["line"]["marker"] = marker_config
    else:
        plot_options["line"]["marker"] = {"enabled": False}

    chart.options.plot_options = plot_options

    # Tooltip configuration
    chart.options.tooltip = {
        "shared": False,
        "useHTML": True,
        "headerFormat": "<b>{point.key}</b><br/>",
        "pointFormat": f"{ylabel or y}: <b>{{point.y:.2f}}</b>",
    }

    # Create line series
    line_series = LineSeries()

    # Set data based on x-axis type
    if x_is_categorical:
        line_series.data = y_values
    else:
        line_series.data = list(zip(x_values, y_values, strict=False))

    line_series.name = ylabel or y

    # Apply color with alpha
    if alpha < 1.0:
        # Convert hex color to rgba
        if color.startswith("#"):
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            line_series.color = f"rgba({r}, {g}, {b}, {alpha})"
        else:
            line_series.color = color
    else:
        line_series.color = color

    chart.add_series(line_series)

    # Legend (hide for single series)
    chart.options.legend = {"enabled": False}

    # Disable credits
    chart.options.credits = {"enabled": False}

    return chart


if __name__ == "__main__":
    # Sample data for testing - simulating monthly sales data
    np.random.seed(42)

    # Create sample data with 12 months
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    # Generate realistic sales trend with some variation
    base_sales = 100
    trend = np.linspace(0, 50, 12)  # Upward trend
    seasonal = 15 * np.sin(np.linspace(0, 2 * np.pi, 12))  # Seasonal variation
    noise = np.random.normal(0, 5, 12)  # Random noise
    sales = base_sales + trend + seasonal + noise

    data = pd.DataFrame({"Month": months, "Sales": sales.round(1)})

    # Create plot
    chart = create_plot(
        data,
        x="Month",
        y="Sales",
        title="Monthly Sales Performance",
        xlabel="Month",
        ylabel="Sales ($K)",
        color="#4A90D9",
        linewidth=2.5,
    )

    # Export to PNG via Selenium screenshot
    import tempfile
    import time
    from pathlib import Path

    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

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
