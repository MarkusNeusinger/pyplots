"""
line-basic: Basic Line Plot
Library: plotnine

A fundamental line plot for visualizing trends and continuous data over an ordered sequence.
"""

import pandas as pd
from plotnine import aes, geom_line, geom_point, ggplot, labs, theme, theme_minimal
from plotnine.ggplot import ggplot as ggplot_type
from plotnine.themes.elements import element_line, element_text


def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    figsize: tuple[float, float] = (10, 6),
    linewidth: float = 2.0,
    color: str = "steelblue",
    alpha: float = 1.0,
    marker: str | None = None,
    markersize: float = 6.0,
    title: str = "Line Plot",
    xlabel: str | None = None,
    ylabel: str | None = None,
    linestyle: str = "-",
    grid: bool = True,
    **kwargs,
) -> ggplot_type:
    """
    Create a basic line plot connecting data points in order.

    Args:
        data: Input DataFrame containing the data to plot
        x: Column name for x-axis values (typically numeric or ordered)
        y: Column name for y-axis values (numeric)
        figsize: Figure size as (width, height) in inches
        linewidth: Width of the line in points
        color: Line color
        alpha: Line transparency (0.0 to 1.0)
        marker: Marker style for data points (e.g., 'o', 's', '^')
        markersize: Size of markers if enabled
        title: Plot title
        xlabel: X-axis label (defaults to column name if None)
        ylabel: Y-axis label (defaults to column name if None)
        linestyle: Line style ('-', '--', '-.', ':')
        grid: Whether to show grid lines
        **kwargs: Additional parameters passed to geom_line

    Returns:
        plotnine ggplot object

    Raises:
        ValueError: If data is empty
        KeyError: If required columns are not found in data

    Example:
        >>> data = pd.DataFrame({
        ...     'x': [1, 2, 3, 4, 5],
        ...     'y': [2, 4, 3, 5, 6]
        ... })
        >>> fig = create_plot(data, 'x', 'y')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    for col in [x, y]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available: {available}")

    # Set default labels to column names if not provided
    x_label = xlabel if xlabel is not None else x
    y_label = ylabel if ylabel is not None else y

    # Sort data by x to ensure proper line connection
    plot_data = data.sort_values(by=x).copy()

    # Map linestyle to plotnine format
    linetype_map = {"-": "solid", "--": "dashed", "-.": "dashdot", ":": "dotted"}
    linetype = linetype_map.get(linestyle, "solid")

    # Create the plot
    plot = (
        ggplot(plot_data, aes(x=x, y=y))
        + geom_line(color=color, size=linewidth, alpha=alpha, linetype=linetype, **kwargs)
        + labs(x=x_label, y=y_label, title=title)
        + theme_minimal()
        + theme(
            figure_size=figsize,
            plot_title=element_text(size=14, weight="bold", ha="center"),
            axis_title=element_text(size=11),
            axis_text=element_text(size=10),
            panel_grid_major=element_line(alpha=0.3) if grid else element_line(alpha=0),
            panel_grid_minor=element_line(alpha=0.15) if grid else element_line(alpha=0),
        )
    )

    # Add markers if specified
    if marker is not None:
        # Map common marker styles
        marker_map = {"o": "o", "s": "s", "^": "^", "v": "v", "D": "D", "*": "*"}
        shape = marker_map.get(marker, "o")
        plot = plot + geom_point(color=color, size=markersize, alpha=alpha, shape=shape)

    return plot


if __name__ == "__main__":
    # Sample data for testing
    sample_data = pd.DataFrame(
        {"x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "y": [2.3, 3.1, 4.5, 4.2, 5.8, 6.1, 5.9, 7.2, 8.1, 7.8]}
    )

    # Create plot with markers
    fig = create_plot(
        sample_data, "x", "y", title="Basic Line Plot Example", xlabel="Time (units)", ylabel="Value", marker="o"
    )

    # Save
    fig.save("plot.png", dpi=300)
    print("Plot saved to plot.png")
