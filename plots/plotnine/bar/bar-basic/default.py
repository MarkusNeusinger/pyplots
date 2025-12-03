"""
bar-basic: Basic Bar Chart
Library: plotnine

A fundamental vertical bar chart that visualizes categorical data with numeric values.
"""

import pandas as pd
from plotnine import aes, geom_bar, ggplot, labs, scale_y_continuous, theme, theme_minimal
from plotnine.ggplot import ggplot as ggplot_type
from plotnine.themes.elements import element_blank, element_line, element_text


def create_plot(
    data: pd.DataFrame,
    category: str,
    value: str,
    figsize: tuple[float, float] = (10, 6),
    color: str = "steelblue",
    edgecolor: str = "black",
    alpha: float = 0.8,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    rotation: int = 0,
    **kwargs,
) -> ggplot_type:
    """
    Create a basic vertical bar chart.

    Args:
        data: Input DataFrame containing the data to plot
        category: Column name for category labels (x-axis)
        value: Column name for numeric values (bar heights)
        figsize: Figure size as (width, height)
        color: Bar fill color
        edgecolor: Bar edge color
        alpha: Transparency level for bars (0-1)
        title: Plot title (optional)
        xlabel: X-axis label (defaults to column name if None)
        ylabel: Y-axis label (defaults to column name if None)
        rotation: Rotation angle for x-axis labels
        **kwargs: Additional parameters passed to geom_bar

    Returns:
        plotnine ggplot object

    Raises:
        ValueError: If data is empty
        KeyError: If required columns are not found in data

    Example:
        >>> data = pd.DataFrame({
        ...     'category': ['A', 'B', 'C'],
        ...     'value': [10, 20, 15]
        ... })
        >>> fig = create_plot(data, 'category', 'value', title='Sample Chart')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    for col in [category, value]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available: {available}")

    # Set default labels to column names if not provided
    x_label = xlabel if xlabel is not None else category
    y_label = ylabel if ylabel is not None else value

    # Create the plot
    plot = (
        ggplot(data, aes(x=category, y=value))
        + geom_bar(stat="identity", fill=color, color=edgecolor, alpha=alpha, **kwargs)
        + labs(x=x_label, y=y_label, title=title)
        + scale_y_continuous(expand=(0, 0, 0.05, 0))  # Start y-axis at zero
        + theme_minimal()
        + theme(
            figure_size=figsize,
            axis_text_x=element_text(rotation=rotation, ha="right" if rotation else "center"),
            panel_grid_major_x=element_blank(),  # Remove vertical grid lines
            panel_grid_minor=element_blank(),  # Remove minor grid lines
            panel_grid_major_y=element_line(alpha=0.3),  # Subtle horizontal grid
        )
    )

    return plot


if __name__ == "__main__":
    # Sample data for testing
    sample_data = pd.DataFrame(
        {"category": ["Product A", "Product B", "Product C", "Product D", "Product E"], "value": [45, 78, 52, 91, 63]}
    )

    # Create plot
    fig = create_plot(sample_data, "category", "value", title="Sales by Product")

    # Save
    fig.save("plot.png", dpi=300)
    print("Plot saved to plot.png")
