"""
box-basic: Basic Box Plot
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
from highcharts_core.options.series.boxplot import BoxPlotSeries


def create_plot(
    data: pd.DataFrame,
    values: str,
    groups: str,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    colors: Optional[list] = None,
    width: int = 1600,
    height: int = 900,
    **kwargs,
) -> Chart:
    """
    Create a basic box plot showing statistical distribution of multiple groups using Highcharts.

    Args:
        data: Input DataFrame with required columns
        values: Column name containing numeric values
        groups: Column name containing group categories
        title: Plot title (optional)
        xlabel: Custom x-axis label (optional, defaults to groups column name)
        ylabel: Custom y-axis label (optional, defaults to values column name)
        colors: List of colors for each box (optional)
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
        ...     'Group': ['A', 'A', 'B', 'B', 'C', 'C'],
        ...     'Value': [1, 2, 2, 3, 3, 4]
        ... })
        >>> chart = create_plot(data, values='Value', groups='Group')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    # Check required columns
    for col in [values, groups]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available columns: {available}")

    # Prepare box plot data
    group_names = sorted(data[groups].unique())
    box_data = []
    outliers_data = []

    for i, group in enumerate(group_names):
        group_data = data[data[groups] == group][values].dropna()

        # Calculate statistics
        q1 = float(group_data.quantile(0.25))
        median = float(group_data.quantile(0.5))
        q3 = float(group_data.quantile(0.75))
        iqr = q3 - q1
        lower_whisker = max(float(group_data.min()), q1 - 1.5 * iqr)
        upper_whisker = min(float(group_data.max()), q3 + 1.5 * iqr)

        # Box plot data: [low, q1, median, q3, high]
        box_data.append([lower_whisker, q1, median, q3, upper_whisker])

        # Find outliers
        outliers = group_data[(group_data < lower_whisker) | (group_data > upper_whisker)]
        for outlier in outliers:
            outliers_data.append([i, float(outlier)])

    # Create chart with container ID for rendering
    chart = Chart(container="container")

    # Configure chart options
    chart.options = HighchartsOptions()

    # Title
    chart.options.title = {
        "text": title or "Box Plot Distribution",
        "style": {"fontSize": "16px", "fontWeight": "bold"},
    }

    # X-axis
    chart.options.x_axis = {"categories": list(group_names), "title": {"text": xlabel or groups}}

    # Y-axis
    chart.options.y_axis = {
        "title": {"text": ylabel or values},
        "gridLineWidth": 1,
        "gridLineDashStyle": "Dot",
        "gridLineColor": "#e0e0e0",
    }

    # Colors
    if colors:
        chart.options.colors = colors
    else:
        chart.options.colors = ["#66c2a5", "#fc8d62", "#8da0cb", "#e78ac3", "#a6d854"]

    # Plot options
    chart.options.plot_options = {
        "boxplot": {
            "fillColor": None,
            "lineWidth": 2,
            "medianWidth": 3,
            "medianColor": "#FF0000",
            "stemWidth": 1,
            "whiskerWidth": 2,
            "whiskerLength": "50%",
        }
    }

    # Tooltip
    chart.options.tooltip = {
        "shared": False,
        "useHTML": True,
        "headerFormat": "<em>{point.key}</em><br/>",
        "pointFormat": (
            "<span>Max: {point.high}</span><br/>"
            "<span>Q3: {point.q3}</span><br/>"
            '<span style="color: red">Median: {point.median}</span><br/>'
            "<span>Q1: {point.q1}</span><br/>"
            "<span>Min: {point.low}</span><br/>"
        ),
    }

    # Chart dimensions
    chart.options.chart = {"type": "boxplot", "width": width, "height": height, "backgroundColor": "white"}

    # Add box plot series
    box_series = BoxPlotSeries()
    box_series.data = box_data
    box_series.name = "Distribution"
    box_series.color_by_point = True
    chart.add_series(box_series)

    # Add outliers as scatter series if any exist
    if outliers_data:
        from highcharts_core.options.series.scatter import ScatterSeries

        scatter_series = ScatterSeries()
        scatter_series.data = outliers_data
        scatter_series.name = "Outliers"
        scatter_series.color = "rgba(255, 0, 0, 0.5)"
        scatter_series.marker = {
            "fillColor": "rgba(255, 0, 0, 0.5)",
            "lineWidth": 1,
            "lineColor": "#000000",
            "radius": 4,
        }
        scatter_series.tooltip = {"pointFormat": "Outlier: <b>{point.y}</b>"}
        chart.add_series(scatter_series)

    # Legend
    chart.options.legend = {
        "enabled": False  # Hide legend for cleaner look
    }

    # Credits
    chart.options.credits = {"enabled": False}

    return chart


if __name__ == "__main__":
    # Sample data for testing with different distributions per group
    np.random.seed(42)  # For reproducibility

    # Generate sample data with 4 groups
    data_dict = {"Group": [], "Value": []}

    # Group A: Normal distribution, mean=50, std=10
    group_a_data = np.random.normal(50, 10, 40)
    # Add some outliers
    group_a_data = np.append(group_a_data, [80, 85, 15])

    # Group B: Normal distribution, mean=60, std=15
    group_b_data = np.random.normal(60, 15, 35)
    # Add outliers
    group_b_data = np.append(group_b_data, [100, 10])

    # Group C: Normal distribution, mean=45, std=8
    group_c_data = np.random.normal(45, 8, 45)

    # Group D: Skewed distribution
    group_d_data = np.random.gamma(2, 2, 30) + 40
    # Add outliers
    group_d_data = np.append(group_d_data, [75, 78, 20])

    # Combine all data
    for group, values in zip(
        ["Group A", "Group B", "Group C", "Group D"],
        [group_a_data, group_b_data, group_c_data, group_d_data],
        strict=False,
    ):
        data_dict["Group"].extend([group] * len(values))
        data_dict["Value"].extend(values)

    data = pd.DataFrame(data_dict)

    # Create plot
    chart = create_plot(
        data,
        values="Value",
        groups="Group",
        title="Statistical Distribution Comparison Across Groups",
        ylabel="Measurement Value",
        xlabel="Categories",
    )

    # Export to PNG via Selenium screenshot
    import tempfile
    import time
    import urllib.request
    from pathlib import Path

    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    # Download Highcharts JS (required for headless Chrome which can't load CDN)
    highcharts_url = "https://code.highcharts.com/highcharts.js"
    highcharts_more_url = "https://code.highcharts.com/highcharts-more.js"

    with urllib.request.urlopen(highcharts_url, timeout=30) as response:
        highcharts_js = response.read().decode("utf-8")
    with urllib.request.urlopen(highcharts_more_url, timeout=30) as response:
        highcharts_more_js = response.read().decode("utf-8")

    # Generate HTML content with inline scripts
    html_str = chart.to_js_literal()
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script>{highcharts_js}</script>
    <script>{highcharts_more_js}</script>
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
