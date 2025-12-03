"""
bar-basic: Basic Bar Chart
Library: bokeh
"""

from typing import TYPE_CHECKING

import pandas as pd
from bokeh.io import export_png
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure


if TYPE_CHECKING:
    from bokeh.plotting import figure as Figure


def create_plot(
    data: pd.DataFrame,
    category: str,
    value: str,
    figsize: tuple[int, int] = (1600, 900),
    color: str = "steelblue",
    edgecolor: str = "black",
    alpha: float = 0.8,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    rotation: int = 0,
    **kwargs,
) -> "Figure":
    """
    Create a basic vertical bar chart.

    A fundamental bar chart that visualizes categorical data with numeric values,
    ideal for comparing quantities across discrete categories.

    Args:
        data: Input DataFrame with categorical and numeric columns
        category: Column name for category labels (x-axis)
        value: Column name for numeric values (bar heights)
        figsize: Figure size as (width, height) in pixels. Defaults to (1600, 900).
        color: Bar fill color. Defaults to "steelblue".
        edgecolor: Bar edge color. Defaults to "black".
        alpha: Transparency level for bars (0-1). Defaults to 0.8.
        title: Plot title. Defaults to None.
        xlabel: X-axis label. Defaults to category column name.
        ylabel: Y-axis label. Defaults to value column name.
        rotation: Rotation angle for x-axis labels in degrees. Defaults to 0.
        **kwargs: Additional parameters passed to figure.

    Returns:
        Bokeh figure object with the bar chart.

    Raises:
        ValueError: If data is empty.
        KeyError: If required columns are not found in data.

    Example:
        >>> data = pd.DataFrame({
        ...     'category': ['A', 'B', 'C', 'D'],
        ...     'value': [10, 25, 15, 30]
        ... })
        >>> fig = create_plot(data, 'category', 'value', title='Sample Bar Chart')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    for col in [category, value]:
        if col not in data.columns:
            available = ", ".join(data.columns.tolist())
            raise KeyError(f"Column '{col}' not found. Available: {available}")

    # Prepare data - drop NaN values
    plot_data = data[[category, value]].dropna()

    # Get categories as list for x_range
    categories = plot_data[category].astype(str).tolist()

    # Create ColumnDataSource
    source = ColumnDataSource(data={"categories": categories, "values": plot_data[value].tolist()})

    # Set labels
    x_label = xlabel if xlabel is not None else category
    y_label = ylabel if ylabel is not None else value

    # Create figure with categorical x-axis
    p = figure(
        width=figsize[0],
        height=figsize[1],
        x_range=categories,
        title=title,
        x_axis_label=x_label,
        y_axis_label=y_label,
        **kwargs,
    )

    # Calculate bar width (0.8 of available space)
    bar_width = 0.8

    # Add bars
    p.vbar(
        x="categories",
        top="values",
        width=bar_width,
        source=source,
        fill_color=color,
        fill_alpha=alpha,
        line_color=edgecolor,
        line_width=1,
    )

    # Ensure y-axis starts at zero
    p.y_range.start = 0

    # Style grid - subtle y-grid only
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_alpha = 0.3

    # Apply x-axis label rotation if specified
    if rotation != 0:
        from math import pi

        p.xaxis.major_label_orientation = rotation * pi / 180

    # Style axis labels
    p.xaxis.axis_label_text_font_size = "12pt"
    p.yaxis.axis_label_text_font_size = "12pt"
    p.xaxis.major_label_text_font_size = "10pt"
    p.yaxis.major_label_text_font_size = "10pt"

    # Style title if present
    if title:
        p.title.text_font_size = "14pt"
        p.title.align = "center"

    return p


if __name__ == "__main__":
    # Sample data for testing
    sample_data = pd.DataFrame(
        {"category": ["Product A", "Product B", "Product C", "Product D", "Product E"], "value": [45, 78, 52, 91, 63]}
    )

    # Create plot
    fig = create_plot(sample_data, "category", "value", title="Sales by Product", xlabel="Product", ylabel="Sales ($)")

    # Save
    export_png(fig, filename="plot.png")
    print("Plot saved to plot.png")
