"""
line-basic: Basic Line Plot
Implementation for: bokeh
Variant: default
Python: 3.10+
"""

from typing import TYPE_CHECKING, Optional

import numpy as np
import pandas as pd
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure


if TYPE_CHECKING:
    from bokeh.plotting import Figure


def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    color: str = "steelblue",
    line_width: float = 2.0,
    marker: Optional[str] = None,
    marker_size: float = 8,
    alpha: float = 1.0,
    width: int = 1600,
    height: int = 900,
    **kwargs,
) -> "Figure":
    """
    Create a basic line plot visualizing trends over continuous or sequential data.

    Args:
        data: Input DataFrame with required columns
        x: Column name for x-axis values (numeric or datetime)
        y: Column name for y-axis values (numeric)
        title: Plot title (optional)
        xlabel: Custom x-axis label (optional, defaults to column name)
        ylabel: Custom y-axis label (optional, defaults to column name)
        color: Line color (default: "steelblue")
        line_width: Width of the line (default: 2.0)
        marker: Marker style for data points (optional, e.g., "circle", "square")
        marker_size: Size of markers if enabled (default: 8)
        alpha: Line transparency (default: 1.0)
        width: Figure width in pixels (default: 1600)
        height: Figure height in pixels (default: 900)
        **kwargs: Additional parameters

    Returns:
        Bokeh Figure object

    Raises:
        ValueError: If data is empty
        KeyError: If required columns not found
        TypeError: If y column contains non-numeric data

    Example:
        >>> data = pd.DataFrame({'x': [1, 2, 3, 4, 5], 'y': [2, 4, 3, 5, 6]})
        >>> fig = create_plot(data, 'x', 'y')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    # Check required columns
    for col in [x, y]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available columns: {available}")

    # Check if y column is numeric
    if not pd.api.types.is_numeric_dtype(data[y]):
        raise TypeError(f"Column '{y}' must contain numeric data")

    # Sort data by x to ensure proper line connection
    plot_data = data[[x, y]].dropna().sort_values(by=x)

    # Determine x-axis type
    x_axis_type = "datetime" if pd.api.types.is_datetime64_any_dtype(plot_data[x]) else "auto"

    # Create ColumnDataSource
    source = ColumnDataSource(data={"x": plot_data[x], "y": plot_data[y]})

    # Create figure
    p = figure(
        width=width,
        height=height,
        title=title or "Line Plot",
        x_axis_type=x_axis_type,
        toolbar_location="above",
        tools="pan,wheel_zoom,box_zoom,reset,save",
    )

    # Plot line
    p.line(x="x", y="y", source=source, line_color=color, line_width=line_width, line_alpha=alpha)

    # Add markers if specified
    if marker:
        p.scatter(x="x", y="y", source=source, size=marker_size, color=color, alpha=alpha, marker=marker)

    # Labels
    p.xaxis.axis_label = xlabel or x
    p.yaxis.axis_label = ylabel or y

    # Styling
    p.title.text_font_size = "14pt"
    p.title.align = "center"
    p.xaxis.axis_label_text_font_size = "12pt"
    p.yaxis.axis_label_text_font_size = "12pt"
    p.xgrid.grid_line_alpha = 0.3
    p.ygrid.grid_line_alpha = 0.3
    p.xgrid.grid_line_dash = [6, 4]
    p.ygrid.grid_line_dash = [6, 4]

    return p


if __name__ == "__main__":
    # Sample data for testing - simulating time series data
    np.random.seed(42)
    n_points = 50

    # Create sequential x values
    x_values = np.arange(n_points)
    # Create y values with a trend and some noise
    y_values = 10 + 0.5 * x_values + np.random.randn(n_points) * 2

    data = pd.DataFrame({"Time": x_values, "Value": y_values})

    # Create plot
    fig = create_plot(
        data,
        x="Time",
        y="Value",
        title="Basic Line Plot Example",
        xlabel="Time (units)",
        ylabel="Measurement Value",
        color="steelblue",
        line_width=2.5,
        marker="circle",
        marker_size=6,
    )

    # Save as PNG using webdriver-manager for automatic chromedriver
    from bokeh.io import export_png
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    export_png(fig, filename="plot.png", webdriver=driver)
    driver.quit()
    print("Plot saved to plot.png")
