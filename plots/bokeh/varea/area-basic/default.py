"""
area-basic: Basic Area Chart
Implementation for: bokeh
Variant: default
Python: 3.10+
"""

from typing import TYPE_CHECKING, Optional

import pandas as pd
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure


if TYPE_CHECKING:
    from bokeh.plotting import Figure


def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    fill_alpha: float = 0.5,
    line_color: Optional[str] = None,
    title: Optional[str] = None,
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
    width: int = 1600,
    height: int = 900,
    **kwargs,
) -> "Figure":
    """
    Create a basic filled area chart using bokeh.

    A simple filled area chart showing a single data series over time or
    sequential x-values. The area between the data line and the baseline
    (zero) is filled with a semi-transparent color.

    Args:
        data: Input DataFrame with x and y columns
        x: Column name for x-axis values
        y: Column name for y-axis values
        fill_alpha: Transparency of the filled area (default: 0.5)
        line_color: Color of the line and fill (default: bokeh blue)
        title: Chart title (optional)
        x_label: Label for x-axis (optional, defaults to column name)
        y_label: Label for y-axis (optional, defaults to column name)
        width: Figure width in pixels (default: 1600)
        height: Figure height in pixels (default: 900)
        **kwargs: Additional parameters passed to figure

    Returns:
        Bokeh Figure object

    Raises:
        ValueError: If data is empty or fill_alpha is out of range
        KeyError: If required columns not found

    Example:
        >>> data = pd.DataFrame({
        ...     'Month': [1, 2, 3, 4, 5, 6],
        ...     'Sales': [100, 120, 90, 140, 160, 130]
        ... })
        >>> fig = create_plot(data, x='Month', y='Sales', title='Monthly Sales')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    for col in [x, y]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available columns: {available}")

    if not 0 <= fill_alpha <= 1:
        raise ValueError(f"fill_alpha must be between 0 and 1, got {fill_alpha}")

    # Set default color (bokeh blue)
    color = line_color or "#1f77b4"

    # Sort data by x to ensure proper area rendering
    plot_data = data[[x, y]].dropna().sort_values(by=x).reset_index(drop=True)

    # Create ColumnDataSource
    source = ColumnDataSource(data={"x": plot_data[x], "y": plot_data[y], "y0": [0] * len(plot_data)})

    # Create figure
    p = figure(
        width=width,
        height=height,
        title=title or "Area Chart",
        x_axis_label=x_label or x,
        y_axis_label=y_label or y,
        toolbar_location="above",
        tools="pan,wheel_zoom,box_zoom,reset,save",
        **kwargs,
    )

    # Draw the filled area from baseline (0) to y values
    p.varea(x="x", y1="y0", y2="y", source=source, fill_color=color, fill_alpha=fill_alpha)

    # Draw line on top for better visibility
    p.line(x="x", y="y", source=source, line_color=color, line_width=2)

    # Styling
    p.title.text_font_size = "14pt"
    p.title.align = "center"

    # Grid styling - subtle
    p.xgrid.grid_line_alpha = 0.3
    p.ygrid.grid_line_alpha = 0.3
    p.xgrid.grid_line_dash = [6, 4]
    p.ygrid.grid_line_dash = [6, 4]

    # Axis styling
    p.xaxis.axis_label_text_font_size = "12pt"
    p.yaxis.axis_label_text_font_size = "12pt"
    p.xaxis.major_label_text_font_size = "10pt"
    p.yaxis.major_label_text_font_size = "10pt"

    return p


if __name__ == "__main__":
    import numpy as np

    # Sample data: Monthly website traffic over a year
    np.random.seed(42)
    months = list(range(1, 13))
    base_traffic = [1000, 1100, 1050, 1200, 1400, 1600, 1500, 1550, 1700, 1650, 1800, 2000]
    noise = np.random.normal(0, 50, 12)
    traffic = [max(0, int(b + n)) for b, n in zip(base_traffic, noise, strict=False)]

    data = pd.DataFrame({"Month": months, "Visitors": traffic})

    # Create plot
    fig = create_plot(
        data,
        x="Month",
        y="Visitors",
        title="Monthly Website Traffic",
        x_label="Month",
        y_label="Visitors (thousands)",
        fill_alpha=0.5,
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
