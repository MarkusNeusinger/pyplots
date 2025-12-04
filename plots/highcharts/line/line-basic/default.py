"""
line-basic: Basic Line Chart
Library: highcharts

Note: Highcharts requires a license for commercial use.
"""

import tempfile
import time
import urllib.request
from pathlib import Path
from typing import TYPE_CHECKING

import pandas as pd
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.area import LineSeries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


if TYPE_CHECKING:
    pass

# Style guide colors
COLORS = ["#306998", "#FFD43B", "#DC2626", "#059669", "#8B5CF6", "#F97316"]

# Default dimensions from style guide
DEFAULT_WIDTH = 4800
DEFAULT_HEIGHT = 2700


def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    color: str = "#306998",
    linewidth: float = 2.0,
    marker: str | None = None,
    marker_size: float = 6.0,
    alpha: float = 1.0,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    linestyle: str = "solid",
    **kwargs,
) -> Chart:
    """
    Create a basic line chart using Highcharts.

    Args:
        data: Input DataFrame containing the data to plot
        x: Column name for x-axis values (numeric or categorical)
        y: Column name for y-axis values (numeric)
        color: Line color (default: "#306998" - Python Blue)
        linewidth: Width of the line in pixels (default: 2.0)
        marker: Marker style for data points - circle, square, diamond, triangle (default: None)
        marker_size: Size of markers if enabled (default: 6.0)
        alpha: Transparency level for the line 0.0-1.0 (default: 1.0)
        title: Plot title (default: None)
        xlabel: X-axis label (default: uses column name)
        ylabel: Y-axis label (default: uses column name)
        linestyle: Line style - solid, dash, dot, shortdash, shortdot (default: "solid")
        **kwargs: Additional parameters

    Returns:
        Highcharts Chart object

    Raises:
        ValueError: If data is empty
        KeyError: If required columns not found in data

    Example:
        >>> data = pd.DataFrame({'month': [1, 2, 3, 4], 'sales': [100, 150, 130, 180]})
        >>> chart = create_plot(data, 'month', 'sales')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    for col in [x, y]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available: {available}")

    # Prepare data - handle NaN values
    plot_data = data[[x, y]].dropna()
    x_values = plot_data[x].tolist()
    y_values = plot_data[y].tolist()

    # Determine if x-axis is categorical or numeric
    x_is_categorical = not pd.api.types.is_numeric_dtype(data[x])

    # If numeric, sort by x values
    if not x_is_categorical:
        sorted_indices = sorted(range(len(x_values)), key=lambda i: x_values[i])
        x_values = [x_values[i] for i in sorted_indices]
        y_values = [y_values[i] for i in sorted_indices]

    # CRITICAL: Always pass container="container" to avoid blank images
    chart = Chart(container="container")
    chart.options = HighchartsOptions()

    # Chart configuration with style guide dimensions
    chart.options.chart = {
        "type": "line",
        "width": DEFAULT_WIDTH,
        "height": DEFAULT_HEIGHT,
        "backgroundColor": "#ffffff",
        "style": {"fontFamily": "Arial, sans-serif"},
        "animation": False,
    }

    # Title configuration (scaled for 4800x2700)
    if title:
        chart.options.title = {"text": title, "style": {"fontSize": "48px", "fontWeight": "bold"}}
    else:
        chart.options.title = {"text": None}

    # Axis labels - use custom or column names
    x_label = xlabel if xlabel else x
    y_label = ylabel if ylabel else y

    # X-axis configuration
    x_axis_config = {
        "title": {"text": x_label, "style": {"fontSize": "40px"}},
        "labels": {"style": {"fontSize": "32px"}},
        "gridLineWidth": 1,
        "gridLineDashStyle": "Dot",
        "gridLineColor": "rgba(0, 0, 0, 0.15)",
    }

    if x_is_categorical:
        x_axis_config["categories"] = x_values

    chart.options.x_axis = x_axis_config

    # Y-axis configuration
    chart.options.y_axis = {
        "title": {"text": y_label, "style": {"fontSize": "40px"}},
        "labels": {"style": {"fontSize": "32px"}},
        "gridLineWidth": 1,
        "gridLineDashStyle": "Dot",
        "gridLineColor": "rgba(0, 0, 0, 0.3)",
    }

    # Map linestyle to Highcharts dashStyle
    dash_style_map = {"solid": "Solid", "dash": "Dash", "dot": "Dot", "shortdash": "ShortDash", "shortdot": "ShortDot"}
    dash_style = dash_style_map.get(linestyle, "Solid")

    # Plot options for line series
    plot_options: dict = {
        "line": {"lineWidth": linewidth, "connectNulls": False, "animation": False, "dashStyle": dash_style}
    }

    # Marker configuration
    if marker:
        marker_symbol_map = {
            "o": "circle",
            "s": "square",
            "d": "diamond",
            "^": "triangle",
            "circle": "circle",
            "square": "square",
            "diamond": "diamond",
            "triangle": "triangle",
        }
        marker_symbol = marker_symbol_map.get(marker, "circle")
        plot_options["line"]["marker"] = {"enabled": True, "symbol": marker_symbol, "radius": marker_size}
    else:
        plot_options["line"]["marker"] = {"enabled": False}

    chart.options.plot_options = plot_options

    # Create line series
    line_series = LineSeries()

    # Set data based on x-axis type
    if x_is_categorical:
        line_series.data = y_values
    else:
        line_series.data = list(zip(x_values, y_values, strict=False))

    line_series.name = y_label

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

    # Tooltip configuration
    chart.options.tooltip = {
        "shared": False,
        "useHTML": True,
        "headerFormat": "<b>{point.key}</b><br/>",
        "pointFormat": f"{y_label}: <b>{{point.y:.2f}}</b>",
        "style": {"fontSize": "24px"},
    }

    # Legend (hide for single series)
    chart.options.legend = {"enabled": False}

    # Disable credits
    chart.options.credits = {"enabled": False}

    return chart


def save_chart_as_png(chart: Chart, filename: str = "plot.png") -> None:
    """
    Save a Highcharts chart as a PNG file using Selenium.

    Args:
        chart: Highcharts Chart object
        filename: Output filename (default: "plot.png")
    """
    # Download Highcharts JS (required for headless Chrome - CDN won't load from file://)
    highcharts_url = "https://code.highcharts.com/highcharts.js"
    with urllib.request.urlopen(highcharts_url, timeout=30) as response:
        highcharts_js = response.read().decode("utf-8")

    # Generate HTML with INLINE scripts (not CDN links!)
    html_str = chart.to_js_literal()
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
</head>
<body style="margin:0;">
    <div id="container" style="width: {DEFAULT_WIDTH}px; height: {DEFAULT_HEIGHT}px;"></div>
    <script>{html_str}</script>
</body>
</html>"""

    # Write temp HTML and take screenshot
    with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
        f.write(html_content)
        temp_path = f.name

    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument(f"--window-size={DEFAULT_WIDTH},{DEFAULT_HEIGHT}")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(f"file://{temp_path}")
        time.sleep(5)  # Wait for chart to render
        driver.save_screenshot(filename)
        driver.quit()
    finally:
        Path(temp_path).unlink()  # Clean up temp file


if __name__ == "__main__":
    import numpy as np

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
        color="#306998",
        linewidth=3,
        marker="circle",
        marker_size=8,
    )

    # Save as PNG
    save_chart_as_png(chart, "plot.png")
    print("Plot saved to plot.png")
