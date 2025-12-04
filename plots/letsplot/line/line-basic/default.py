"""
line-basic: Basic Line Chart
Library: lets-plot

A fundamental line chart that visualizes trends and patterns in data over a continuous axis.
"""

import pandas as pd
from lets_plot import (
    LetsPlot,
    aes,
    element_line,
    element_text,
    geom_line,
    geom_point,
    ggplot,
    ggsave,
    ggsize,
    labs,
    theme,
    theme_minimal,
)
from lets_plot.plot.core import PlotSpec


LetsPlot.setup_html()


def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    figsize: tuple[float, float] = (10, 6),
    linewidth: float = 2.0,
    color: str = "#306998",
    alpha: float = 1.0,
    marker: str | None = None,
    marker_size: float = 6.0,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    linestyle: str = "solid",
    grid: bool = True,
    **kwargs,
) -> PlotSpec:
    """
    Create a basic line chart connecting data points in sequence.

    Args:
        data: Input DataFrame containing the data to plot
        x: Column name for x-axis values (typically numeric or ordered)
        y: Column name for y-axis values (numeric)
        figsize: Figure size as (width, height) in inches (used for aspect ratio)
        linewidth: Width of the line in points
        color: Line color (default: Python Blue from style guide)
        alpha: Line transparency (0.0 to 1.0)
        marker: Marker style for data points (e.g., 'o', 's', '^')
        marker_size: Size of markers if enabled
        title: Plot title (optional)
        xlabel: X-axis label (defaults to column name if None)
        ylabel: Y-axis label (defaults to column name if None)
        linestyle: Line style ('solid', 'dashed', 'dotted', 'dotdash')
        grid: Whether to show grid lines
        **kwargs: Additional parameters

    Returns:
        lets-plot PlotSpec object

    Raises:
        ValueError: If data is empty
        KeyError: If required columns are not found in data

    Example:
        >>> data = pd.DataFrame({
        ...     'month': [1, 2, 3, 4, 5, 6],
        ...     'sales': [100, 150, 130, 180, 200, 190]
        ... })
        >>> fig = create_plot(data, 'month', 'sales')
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

    # Map linestyle aliases to lets-plot format
    linetype_map = {
        "-": "solid",
        "--": "dashed",
        "-.": "dotdash",
        ":": "dotted",
        "solid": "solid",
        "dashed": "dashed",
        "dotted": "dotted",
        "dotdash": "dotdash",
    }
    linetype = linetype_map.get(linestyle, "solid")

    # Create the base plot with line geometry
    plot = (
        ggplot(plot_data, aes(x=x, y=y))
        + geom_line(color=color, size=linewidth, alpha=alpha, linetype=linetype)
        + labs(x=x_label, y=y_label, title=title)
        + theme_minimal()
        + theme(
            plot_title=element_text(size=20, face="bold"),
            axis_title=element_text(size=20),
            axis_text=element_text(size=16),
            legend_text=element_text(size=16),
            panel_grid_major=element_line(color="#CCCCCC", size=0.5) if grid else element_line(color="rgba(0,0,0,0)"),
            panel_grid_minor=element_line(color="#EEEEEE", size=0.3) if grid else element_line(color="rgba(0,0,0,0)"),
        )
        + ggsize(1600, 900)  # Base size, scaled 3x on export to get 4800 x 2700
    )

    # Add markers if specified
    if marker is not None:
        # Map common marker styles to lets-plot shapes
        marker_map = {
            "o": 16,  # circle
            "s": 15,  # square
            "^": 17,  # triangle up
            "v": 25,  # triangle down
            "D": 18,  # diamond
            "*": 8,  # asterisk
        }
        shape = marker_map.get(marker, 16)
        plot = plot + geom_point(color=color, size=marker_size, alpha=alpha, shape=shape)

    return plot


if __name__ == "__main__":
    # Sample data for testing
    sample_data = pd.DataFrame(
        {
            "month": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            "sales": [120, 150, 170, 160, 190, 220, 240, 230, 210, 195, 180, 210],
        }
    )

    # Create plot with markers
    fig = create_plot(
        sample_data,
        "month",
        "sales",
        title="Monthly Sales Trend",
        xlabel="Month",
        ylabel="Sales ($K)",
        marker="o",
        linewidth=2.5,
    )

    # Save - scale 3x to get 4800 x 2700 px
    ggsave(fig, "plot.png", path=".", scale=3)
    print("Plot saved to plot.png")
