"""
area-basic: Basic Area Chart
Implementation for: pygal
Variant: default
Python: 3.10+
"""

from typing import TYPE_CHECKING, Optional

import pandas as pd
import pygal
from pygal.style import Style


if TYPE_CHECKING:
    from pygal import Line


def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    fill_alpha: float = 0.5,
    color: Optional[str] = None,
    show_line: bool = True,
    width: int = 1600,
    height: int = 900,
    **kwargs,
) -> "Line":
    """
    Create a basic area chart showing a filled area under a line using pygal.

    An area chart displays a single data series as a filled region beneath
    a line, ideal for showing trends while emphasizing magnitude.

    Args:
        data: Input DataFrame with required columns
        x: Column name for x-axis values (categories/labels)
        y: Column name for y-axis numeric values
        title: Chart title (optional)
        xlabel: Custom x-axis label (optional, defaults to column name)
        ylabel: Custom y-axis label (optional, defaults to column name)
        fill_alpha: Transparency of the filled area (default: 0.5)
        color: Color for the line and fill (optional)
        show_line: Whether to show the line on top of fill (default: True)
        width: Figure width in pixels (default: 1600)
        height: Figure height in pixels (default: 900)
        **kwargs: Additional parameters for pygal configuration

    Returns:
        pygal Line chart object configured as an area chart

    Raises:
        ValueError: If data is empty
        KeyError: If required columns not found

    Example:
        >>> data = pd.DataFrame({
        ...     'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
        ...     'Sales': [100, 150, 130, 180, 200]
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

    # Define colors - use provided color or default
    primary_color = color or "#3498db"

    # Create custom style with appropriate opacity for fill
    custom_style = Style(
        background="white",
        plot_background="white",
        foreground="#333",
        foreground_strong="#333",
        foreground_subtle="#555",
        opacity=fill_alpha,
        opacity_hover=min(fill_alpha + 0.2, 1.0),
        colors=(primary_color,),
        font_family="Arial, sans-serif",
        major_guide_stroke_dasharray="3,3",
        guide_stroke_dasharray="1,1",
    )

    # Create line chart with fill enabled (makes it an area chart)
    chart = pygal.Line(
        title=title or "Area Chart",
        x_title=xlabel or x,
        y_title=ylabel or y,
        width=width,
        height=height,
        fill=True,  # This enables the area fill
        show_legend=True,
        style=custom_style,
        show_x_guides=True,
        show_y_guides=True,
        dots_size=3 if show_line else 0,
        stroke_style={"width": 2} if show_line else {"width": 0},
        **kwargs,
    )

    # Set x-axis labels
    x_values = data[x].tolist()
    chart.x_labels = [str(val) for val in x_values]

    # Add the data series
    y_values = data[y].tolist()
    series_label = ylabel or y
    chart.add(series_label, y_values)

    return chart


if __name__ == "__main__":
    # Sample data for testing - monthly website traffic
    data = pd.DataFrame(
        {
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            "Visitors": [12000, 15000, 18000, 22000, 25000, 28000, 30000, 32000, 29000, 26000, 23000, 20000],
        }
    )

    # Create plot
    chart = create_plot(
        data,
        x="Month",
        y="Visitors",
        title="Monthly Website Traffic",
        xlabel="Month",
        ylabel="Number of Visitors",
        fill_alpha=0.5,
        color="#2ecc71",
    )

    # Save as PNG
    chart.render_to_png("plot.png")
    print("Plot saved to plot.png")
