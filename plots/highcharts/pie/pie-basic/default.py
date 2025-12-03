"""
pie-basic: Basic Pie Chart
Library: highcharts

A fundamental pie chart that visualizes proportions and percentages of categorical data
as slices of a circular chart. Each slice represents a category's share of the whole.

Note: Highcharts requires a license for commercial use.
"""

from typing import Optional

import pandas as pd
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.pie import PieSeries


# Style guide colors
PYPLOTS_COLORS = [
    "#306998",  # Python Blue (Primary)
    "#FFD43B",  # Python Yellow
    "#DC2626",  # Signal Red
    "#059669",  # Teal Green
    "#8B5CF6",  # Violet
    "#F97316",  # Orange
]


def create_plot(
    data: pd.DataFrame,
    category: str,
    value: str,
    figsize: tuple[int, int] = (10, 8),
    title: Optional[str] = None,
    colors: Optional[list[str]] = None,
    startangle: float = 90,
    autopct: str = "%1.1f%%",
    explode: Optional[list[float]] = None,
    shadow: bool = False,
    labels: Optional[list[str]] = None,
    legend: bool = True,
    legend_loc: str = "best",
    width: int = 1600,
    height: int = 900,
    **kwargs,
) -> Chart:
    """
    Create a basic pie chart from DataFrame.

    Args:
        data: Input DataFrame with categorical and numeric data
        category: Column name for category names (slice labels)
        value: Column name for numeric values (slice proportions)
        figsize: Figure size as (width, height) in inches (legacy, use width/height instead)
        title: Plot title
        colors: Custom color palette for slices (defaults to PyPlots style guide colors)
        startangle: Starting angle for first slice in degrees (from positive x-axis)
        autopct: Format string for percentage labels
        explode: Offset distances for each slice (0-0.1 typical)
        shadow: Add shadow effect for 3D appearance
        labels: Custom labels (defaults to category names)
        legend: Whether to display legend
        legend_loc: Legend location (e.g., 'best', 'right', 'left')
        width: Figure width in pixels (default: 1600)
        height: Figure height in pixels (default: 900)
        **kwargs: Additional parameters passed to chart options

    Returns:
        Highcharts Chart object

    Raises:
        ValueError: If data is empty or contains negative values
        KeyError: If required columns are not found in data

    Example:
        >>> data = pd.DataFrame({
        ...     'category': ['Product A', 'Product B', 'Product C'],
        ...     'value': [35, 25, 40]
        ... })
        >>> chart = create_plot(data, 'category', 'value', title='Market Share')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    for col in [category, value]:
        if col not in data.columns:
            available = ", ".join(data.columns.tolist())
            raise KeyError(f"Column '{col}' not found. Available: {available}")

    # Validate non-negative values
    if (data[value] < 0).any():
        raise ValueError("Pie chart values must be non-negative")

    # Check if all values sum to zero
    if data[value].sum() == 0:
        raise ValueError("Sum of values cannot be zero")

    # Get colors (use provided or default to PyPlots style guide)
    slice_colors = colors if colors is not None else PYPLOTS_COLORS

    # Get labels (use provided or default to category names)
    slice_labels = labels if labels is not None else data[category].tolist()

    # Create chart with container ID for rendering
    chart = Chart(container="container")
    chart.options = HighchartsOptions()

    # Chart configuration
    chart.options.chart = {"type": "pie", "width": width, "height": height, "backgroundColor": "#ffffff"}

    # Title with style guide typography
    if title:
        chart.options.title = {
            "text": title,
            "style": {
                "fontSize": "20px",
                "fontWeight": "600",
                "fontFamily": "Inter, DejaVu Sans, Arial, Helvetica, sans-serif",
            },
        }
    else:
        chart.options.title = {"text": None}

    # Build data points for pie series
    pie_data = []
    for i, (cat, val) in enumerate(zip(data[category].tolist(), data[value].tolist(), strict=True)):
        point = {
            "name": slice_labels[i] if i < len(slice_labels) else cat,
            "y": val,
            "color": slice_colors[i % len(slice_colors)],
        }

        # Apply explode if provided
        if explode is not None and i < len(explode) and explode[i] > 0:
            point["sliced"] = True
            point["selected"] = True

        pie_data.append(point)

    # Create pie series
    series = PieSeries()
    series.data = pie_data
    series.name = value

    # Configure data labels to show percentages
    # Parse autopct format for decimal places (e.g., '%1.1f%%' -> 1 decimal)
    decimal_places = 1
    if autopct and "." in autopct:
        try:
            decimal_places = int(autopct.split(".")[1][0])
        except (IndexError, ValueError):
            decimal_places = 1

    # Pie series options
    series.show_in_legend = legend
    series.start_angle = startangle
    series.shadow = shadow

    # Data labels configuration
    series.data_labels = {
        "enabled": True,
        "format": f"{{point.percentage:.{decimal_places}f}}%",
        "distance": 20,
        "style": {
            "fontSize": "14px",
            "fontWeight": "normal",
            "fontFamily": "Inter, DejaVu Sans, Arial, Helvetica, sans-serif",
            "textOutline": "2px white",
        },
    }

    chart.add_series(series)

    # Plot options for pie
    chart.options.plot_options = {
        "pie": {
            "allowPointSelect": True,
            "cursor": "pointer",
            "showInLegend": legend,
            "startAngle": startangle,
            "shadow": shadow,
            "center": ["50%", "50%"],
            "size": "75%",
        }
    }

    # Legend configuration
    if legend:
        # Map legend_loc to Highcharts position
        legend_config = {
            "enabled": True,
            "align": "right",
            "verticalAlign": "middle",
            "layout": "vertical",
            "itemStyle": {"fontSize": "16px", "fontFamily": "Inter, DejaVu Sans, Arial, Helvetica, sans-serif"},
            "backgroundColor": "#ffffff",
            "borderWidth": 1,
            "borderRadius": 5,
        }

        if legend_loc in ["left"]:
            legend_config["align"] = "left"
        elif legend_loc in ["right"]:
            legend_config["align"] = "right"
        elif legend_loc in ["top", "upper center"]:
            legend_config["align"] = "center"
            legend_config["verticalAlign"] = "top"
            legend_config["layout"] = "horizontal"
        elif legend_loc in ["bottom", "lower center"]:
            legend_config["align"] = "center"
            legend_config["verticalAlign"] = "bottom"
            legend_config["layout"] = "horizontal"

        chart.options.legend = legend_config
    else:
        chart.options.legend = {"enabled": False}

    # Tooltip configuration
    chart.options.tooltip = {
        "pointFormat": "<b>{point.percentage:.1f}%</b><br/>Value: {point.y}",
        "style": {"fontSize": "14px", "fontFamily": "Inter, DejaVu Sans, Arial, Helvetica, sans-serif"},
    }

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

    # Sample data for testing (from spec)
    sample_data = pd.DataFrame(
        {"category": ["Product A", "Product B", "Product C", "Product D", "Other"], "value": [35, 25, 20, 15, 5]}
    )

    # Create plot
    chart = create_plot(sample_data, "category", "value", title="Market Share Distribution")

    # Download Highcharts JS (required for headless Chrome which can't load CDN)
    highcharts_url = "https://code.highcharts.com/highcharts.js"
    with urllib.request.urlopen(highcharts_url, timeout=30) as response:
        highcharts_js = response.read().decode("utf-8")

    # Export to PNG via Selenium screenshot
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
    with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
        f.write(html_content)
        temp_path = f.name

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1600,900")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f"file://{temp_path}")
    time.sleep(5)  # Wait for chart to render
    driver.save_screenshot("plot.png")
    driver.quit()

    Path(temp_path).unlink()  # Clean up temp file
    print("Plot saved to plot.png")
