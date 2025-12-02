"""
bar-basic: Basic Bar Chart
Library: pygal
"""

import pandas as pd
import pygal
from pygal.style import Style


def create_plot(
    data: pd.DataFrame,
    category: str,
    value: str,
    figsize: tuple[int, int] = (1600, 900),
    color: str = "#3498db",
    alpha: float = 0.8,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    rotation: int = 0,
    **kwargs,
) -> pygal.Bar:
    """
    Create a basic vertical bar chart for categorical data comparison.

    Args:
        data: Input DataFrame containing the data to plot.
        category: Column name for category labels (x-axis).
        value: Column name for numeric values (bar heights).
        figsize: Figure size as (width, height) in pixels.
        color: Bar fill color.
        alpha: Transparency level for bars (0.0 to 1.0).
        title: Optional plot title.
        xlabel: X-axis label (defaults to category column name).
        ylabel: Y-axis label (defaults to value column name).
        rotation: Rotation angle for x-axis labels.
        **kwargs: Additional parameters passed to pygal.Bar.

    Returns:
        pygal.Bar chart object.

    Raises:
        ValueError: If data is empty.
        KeyError: If required columns are not found in data.

    Example:
        >>> data = pd.DataFrame({
        ...     'category': ['A', 'B', 'C'],
        ...     'value': [10, 20, 30]
        ... })
        >>> chart = create_plot(data, 'category', 'value', title='Sample Chart')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    for col in [category, value]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available: {available}")

    # Handle missing values
    clean_data = data[[category, value]].dropna()

    # Create custom style with subtle grid and proper colors
    custom_style = Style(
        background="white",
        plot_background="white",
        foreground="#333333",
        foreground_strong="#333333",
        foreground_subtle="#666666",
        opacity=str(alpha),
        opacity_hover=str(min(alpha + 0.1, 1.0)),
        colors=(color,),
        guide_stroke_color="#cccccc",
        major_guide_stroke_color="#cccccc",
    )

    # Create chart
    chart = pygal.Bar(
        width=figsize[0],
        height=figsize[1],
        title=title,
        x_title=xlabel if xlabel else category,
        y_title=ylabel if ylabel else value,
        style=custom_style,
        show_legend=False,
        show_y_guides=True,
        show_x_guides=False,
        x_label_rotation=rotation,
        print_values=False,
        range=(0, None),
        **kwargs,
    )

    # Set x-axis labels
    chart.x_labels = [str(cat) for cat in clean_data[category].tolist()]

    # Add data series
    chart.add("", clean_data[value].tolist())

    return chart


if __name__ == "__main__":
    # Sample data for testing
    sample_data = pd.DataFrame(
        {"category": ["Product A", "Product B", "Product C", "Product D", "Product E"], "value": [45, 78, 52, 91, 63]}
    )

    # Create plot
    chart = create_plot(sample_data, "category", "value", title="Sales by Product")

    # Save to PNG
    chart.render_to_png("plot.png")
    print("Plot saved to plot.png")
