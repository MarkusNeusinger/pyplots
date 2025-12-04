"""
line-basic: Basic Line Plot
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
    color: str = "#3498db",
    linewidth: int = 3,
    show_dots: bool = True,
    dot_size: int = 4,
    width: int = 1600,
    height: int = 900,
    fill: bool = False,
    **kwargs,
) -> "Line":
    """
    Create a basic line plot showing trends over a continuous variable using pygal.

    Args:
        data: Input DataFrame with required columns
        x: Column name for x-axis values
        y: Column name for y-axis values (numeric)
        title: Plot title (optional)
        xlabel: Custom x-axis label (optional, defaults to x column name)
        ylabel: Custom y-axis label (optional, defaults to y column name)
        color: Line color (default: "#3498db" - blue)
        linewidth: Width of the line in pixels (default: 3)
        show_dots: Whether to show data point markers (default: True)
        dot_size: Size of data point markers (default: 4)
        width: Figure width in pixels (default: 1600)
        height: Figure height in pixels (default: 900)
        fill: Whether to fill area under the line (default: False)
        **kwargs: Additional parameters for pygal configuration

    Returns:
        pygal Line chart object

    Raises:
        ValueError: If data is empty
        KeyError: If required columns not found

    Example:
        >>> data = pd.DataFrame({
        ...     'month': [1, 2, 3, 4, 5, 6],
        ...     'sales': [100, 120, 115, 140, 160, 155]
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

    # Sort data by x-axis for proper line rendering
    sorted_data = data.sort_values(by=x).copy()

    # Create custom style with subtle grid
    custom_style = Style(
        background="white",
        plot_background="white",
        foreground="#333",
        foreground_strong="#333",
        foreground_subtle="#666",
        opacity=0.8,
        opacity_hover=1.0,
        colors=(color,),
        font_family="Arial, sans-serif",
        guide_stroke_dasharray="3,3",
        major_guide_stroke_dasharray="5,5",
    )

    # Create line chart
    line_chart = pygal.Line(
        title=title,
        x_title=xlabel or x,
        y_title=ylabel or y,
        width=width,
        height=height,
        style=custom_style,
        show_dots=show_dots,
        dots_size=dot_size,
        stroke_style={"width": linewidth},
        fill=fill,
        show_legend=True,
        legend_at_bottom=False,
        show_x_guides=True,
        show_y_guides=True,
        print_values=False,
        **kwargs,
    )

    # Set x-axis labels from data
    x_values = sorted_data[x].tolist()
    # Convert to string labels for pygal
    line_chart.x_labels = [str(val) for val in x_values]

    # Add data series
    y_values = sorted_data[y].tolist()
    series_label = ylabel if ylabel else y
    line_chart.add(series_label, y_values)

    return line_chart


if __name__ == "__main__":
    # Sample data for testing - Monthly sales data
    data = pd.DataFrame(
        {
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            "Sales": [120, 135, 148, 162, 175, 168, 182, 195, 178, 165, 188, 210],
        }
    )

    # Create plot with custom styling
    chart = create_plot(
        data,
        x="Month",
        y="Sales",
        title="Monthly Sales Performance (2024)",
        xlabel="Month",
        ylabel="Sales (Units)",
        color="#2ecc71",
        linewidth=3,
        show_dots=True,
        dot_size=5,
    )

    # Save as PNG
    chart.render_to_png("plot.png")
    print("Plot saved to plot.png")
