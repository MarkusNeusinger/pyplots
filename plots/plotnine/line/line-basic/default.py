"""
line-basic: Basic Line Plot
Implementation for: plotnine
Variant: default
Python: 3.10+
"""

from typing import TYPE_CHECKING, Optional

import numpy as np
import pandas as pd
from plotnine import aes, element_line, element_text, geom_line, geom_point, ggplot, labs, theme, theme_minimal


if TYPE_CHECKING:
    from plotnine import ggplot as GGPlot


def create_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    color: str = "steelblue",
    line_width: float = 1.2,
    show_points: bool = False,
    point_size: float = 3.0,
    point_alpha: float = 0.8,
    width: int = 16,
    height: int = 9,
    **kwargs,
) -> "GGPlot":
    """
    Create a basic line plot connecting data points in order using plotnine (ggplot2 syntax).

    A simple line plot that visualizes a sequence of values, typically used for
    showing trends or changes over an ordered dimension such as time.

    Args:
        data: Input DataFrame with required columns
        x: Column name for x-axis values (typically numeric or ordered)
        y: Column name for y-axis values (numeric)
        title: Plot title (optional)
        xlabel: Custom x-axis label (optional, defaults to x column name)
        ylabel: Custom y-axis label (optional, defaults to y column name)
        color: Line color (default: 'steelblue')
        line_width: Width of the line (default: 1.2)
        show_points: Whether to show points at data locations (default: False)
        point_size: Size of points if shown (default: 3.0)
        point_alpha: Transparency of points if shown (default: 0.8)
        width: Figure width in inches (default: 16)
        height: Figure height in inches (default: 9)
        **kwargs: Additional parameters for geom_line

    Returns:
        plotnine ggplot object

    Raises:
        ValueError: If data is empty
        KeyError: If required columns not found

    Example:
        >>> data = pd.DataFrame({
        ...     'x': [1, 2, 3, 4, 5],
        ...     'y': [2, 4, 3, 5, 6]
        ... })
        >>> plot = create_plot(data, x='x', y='y')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    # Check required columns
    for col in [x, y]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available columns: {available}")

    # Sort data by x to ensure proper line connection
    plot_data = data.sort_values(by=x).copy()

    # Create the ggplot object
    plot = (
        ggplot(plot_data, aes(x=x, y=y))
        + geom_line(color=color, size=line_width, **kwargs)
        + labs(title=title or "Line Plot", x=xlabel or x, y=ylabel or y)
        + theme_minimal()
        + theme(
            figure_size=(width, height),
            plot_title=element_text(size=14, weight="bold", ha="center"),
            axis_title=element_text(size=11),
            axis_text=element_text(size=10),
            panel_grid_major=element_line(alpha=0.3, linetype="dashed"),
            panel_grid_minor=element_line(alpha=0.15, linetype="dotted"),
        )
    )

    # Optionally add points at data locations
    if show_points:
        plot = plot + geom_point(color=color, size=point_size, alpha=point_alpha)

    return plot


if __name__ == "__main__":
    # Sample data for testing - simulating a simple trend
    np.random.seed(42)  # For reproducibility

    # Generate 25 data points with a trend and some noise
    n_points = 25
    x_values = np.arange(1, n_points + 1)
    # Linear trend with noise
    y_values = 10 + 2 * x_values + np.random.normal(0, 3, n_points)

    data = pd.DataFrame({"Time": x_values, "Value": y_values})

    # Create plot with points shown
    plot = create_plot(
        data,
        x="Time",
        y="Value",
        title="Basic Line Plot Example",
        xlabel="Time (units)",
        ylabel="Measured Value",
        show_points=True,
        color="steelblue",
    )

    # Save for inspection
    plot.save("plot.png", dpi=300, verbose=False)
    print("Plot saved to plot.png")
