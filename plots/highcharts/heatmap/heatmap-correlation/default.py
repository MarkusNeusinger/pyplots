"""
heatmap-correlation: Correlation Matrix Heatmap
Library: highcharts
"""

from typing import Optional

import numpy as np
import pandas as pd
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.heatmap import HeatmapSeries


def create_plot(
    data: pd.DataFrame,
    cmap: str = "coolwarm",
    annotate: bool = True,
    fmt: str = ".2f",
    vmin: float = -1.0,
    vmax: float = 1.0,
    center: float = 0.0,
    square: bool = True,
    cbar_label: str = "Correlation",
    figsize: tuple = (10, 8),
    font_size: int = 10,
    **kwargs
) -> Chart:
    """
    Display a correlation matrix as a heatmap showing pairwise correlations between numeric variables.

    Args:
        data: Input DataFrame with numeric columns to correlate
        cmap: Diverging colormap (default: 'coolwarm')
        annotate: Show correlation values in cells (default: True)
        fmt: Format for annotations (default: '.2f')
        vmin: Minimum value for color scale (default: -1.0)
        vmax: Maximum value for color scale (default: 1.0)
        center: Center point for diverging colormap (default: 0.0)
        square: Make cells square-shaped (default: True)
        cbar_label: Label for color bar (default: 'Correlation')
        figsize: Figure size in inches (default: (10, 8))
        font_size: Font size for annotations (default: 10)
        **kwargs: Additional parameters for Highcharts configuration

    Returns:
        Highcharts Chart object

    Raises:
        ValueError: If data is empty or has no numeric columns
        KeyError: If required columns not found

    Example:
        >>> data = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]})
        >>> chart = create_plot(data)
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    # Select only numeric columns
    numeric_data = data.select_dtypes(include=[np.number])

    if numeric_data.empty:
        raise ValueError("No numeric columns found in the data")

    # Calculate correlation matrix
    corr_matrix = numeric_data.corr()

    # Prepare data for heatmap
    heatmap_data = []
    categories = list(corr_matrix.columns)

    for i, row_name in enumerate(categories):
        for j, col_name in enumerate(categories):
            value = float(corr_matrix.iloc[i, j])
            # Highcharts heatmap format: [x, y, value]
            heatmap_data.append([j, len(categories) - 1 - i, value])

    # Create chart
    chart = Chart()
    chart.options = HighchartsOptions()

    # Convert figsize from inches to pixels (approximately)
    width = int(figsize[0] * 160)
    height = int(figsize[1] * 160)

    # Chart configuration
    chart.options.chart = {
        'type': 'heatmap',
        'width': width,
        'height': height,
        'backgroundColor': 'white'
    }

    # Title
    chart.options.title = {
        'text': 'Correlation Matrix',
        'style': {'fontSize': '16px', 'fontWeight': 'bold'}
    }

    # X-axis (bottom)
    chart.options.x_axis = {
        'categories': categories,
        'title': None,
        'labels': {
            'rotation': 315,  # Use 315 instead of -45 for highcharts
            'style': {'fontSize': f'{font_size}px'}
        }
    }

    # Y-axis (left)
    chart.options.y_axis = {
        'categories': list(reversed(categories)),
        'title': None,
        'labels': {
            'style': {'fontSize': f'{font_size}px'}
        }
    }

    # Color axis (color bar)
    chart.options.color_axis = {
        'min': vmin,
        'max': vmax,
        'stops': [
            [0, '#3060cf'],      # Blue for -1
            [0.5, '#ffffff'],    # White for 0
            [1, '#c4463a']       # Red for +1
        ],
        'labels': {
            'format': '{value}'
        }
    }

    # Legend (color bar)
    chart.options.legend = {
        'align': 'right',
        'layout': 'vertical',
        'margin': 0,
        'verticalAlign': 'middle',
        'symbolHeight': height - 100,
        'title': {
            'text': cbar_label,
            'style': {'fontSize': f'{font_size}px'}
        }
    }

    # Tooltip
    chart.options.tooltip = {
        'shared': False,
        'useHTML': True,
        'headerFormat': '<em>{point.key}</em><br/>',
        'pointFormat': 'Correlation: <b>{point.value:.2f}</b>'
    }

    # Create heatmap series
    heatmap_series = HeatmapSeries()
    heatmap_series.name = 'Correlation'
    heatmap_series.data = heatmap_data
    heatmap_series.border_width = 1
    heatmap_series.border_color = '#ffffff'

    # Data labels (annotations)
    if annotate:
        decimals = int(fmt[1]) if len(fmt) > 1 and fmt[1].isdigit() else 2
        heatmap_series.data_labels = {
            'enabled': True,
            'color': '#000000',
            'style': {
                'fontSize': f'{font_size}px',
                'textOutline': 'none'
            },
            'format': '{point.value:' + fmt + '}'
        }

    # Add series to chart
    chart.add_series(heatmap_series)

    # Disable credits
    chart.options.credits = {'enabled': False}

    return chart


if __name__ == '__main__':
    # Sample data with correlated variables
    np.random.seed(42)
    n = 100

    # Create correlated data
    base = np.random.normal(25, 5, n)
    data = pd.DataFrame({
        'Temperature': base + np.random.normal(0, 2, n),
        'Ice_Cream_Sales': base * 2 + np.random.normal(0, 5, n),
        'Beach_Visitors': base * 1.5 + np.random.normal(0, 8, n),
        'Sunscreen_Sales': base * 1.2 + np.random.normal(0, 4, n),
        'AC_Usage': base * 0.8 + np.random.normal(0, 3, n)
    })

    # Create plot
    chart = create_plot(data)

    # Export to PNG via Selenium screenshot
    import tempfile
    import time
    from pathlib import Path

    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    # Generate HTML content with heatmap module
    html_str = chart.to_js_literal()
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/modules/heatmap.js"></script>
    <script src="https://code.highcharts.com/modules/exporting.js"></script>
</head>
<body style="margin:0;">
    <div id="container" style="width: 1600px; height: 1280px;"></div>
    <script>{html_str}</script>
</body>
</html>"""

    # Write temp HTML and take screenshot
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        f.write(html_content)
        temp_path = f.name

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1600,1280')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f'file://{temp_path}')
    time.sleep(2)  # Wait for chart to render
    driver.save_screenshot('plot.png')
    driver.quit()

    Path(temp_path).unlink()  # Clean up temp file
    print("Plot saved to plot.png")