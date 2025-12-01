"""
area-basic: Basic Area Chart
Implementation for: plotnine
Variant: default
Python: 3.10+
"""

from typing import TYPE_CHECKING, Optional

import numpy as np
import pandas as pd
from plotnine import aes, element_line, element_text, geom_area, geom_line, ggplot, labs, theme, theme_minimal


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
    alpha: float = 0.6,
    line_color: Optional[str] = None,
    line_width: float = 1.5,
    width: int = 16,
    height: int = 9,
    **kwargs,
) -> "GGPlot":
    """
    Create a basic area chart showing values over a continuous axis using plotnine (ggplot2 syntax).

    Args:
        data: Input DataFrame with required columns
        x: Column name for x-axis values (numeric or datetime)
        y: Column name for y-axis values (numeric)
        title: Plot title (optional)
        xlabel: Custom x-axis label (optional, defaults to x column name)
        ylabel: Custom y-axis label (optional, defaults to y column name)
        color: Fill color for the area (default: 'steelblue')
        alpha: Fill transparency level (default: 0.6)
        line_color: Color of the top line (default: same as color)
        line_width: Width of the top line (default: 1.5)
        width: Figure width in inches (default: 16)
        height: Figure height in inches (default: 9)
        **kwargs: Additional parameters for geom_area

    Returns:
        plotnine ggplot object

    Raises:
        ValueError: If data is empty
        KeyError: If required columns not found

    Example:
        >>> data = pd.DataFrame({
        ...     'time': [1, 2, 3, 4, 5],
        ...     'value': [10, 25, 15, 30, 20]
        ... })
        >>> plot = create_plot(data, x='time', y='value')
    """
    # Input validation
    if data.empty:
        raise ValueError("Data cannot be empty")

    # Check required columns
    for col in [x, y]:
        if col not in data.columns:
            available = ", ".join(data.columns)
            raise KeyError(f"Column '{col}' not found. Available columns: {available}")

    # Use the same color for line if not specified
    if line_color is None:
        line_color = color

    # Sort data by x to ensure proper area rendering
    data_sorted = data.sort_values(by=x).copy()

    # Create the ggplot object with area and line
    plot = (
        ggplot(data_sorted, aes(x=x, y=y))
        + geom_area(fill=color, alpha=alpha, **kwargs)
        + geom_line(color=line_color, size=line_width)
        + labs(title=title or "Area Chart", x=xlabel or x, y=ylabel or y)
        + theme_minimal()
        + theme(
            figure_size=(width, height),
            plot_title=element_text(size=14, weight="bold", ha="center"),
            axis_title=element_text(size=11),
            axis_text=element_text(size=10),
            panel_grid_major=element_line(alpha=0.3, linetype="dashed"),
            panel_grid_minor=element_line(alpha=0),
        )
    )

    return plot


if __name__ == "__main__":
    # Sample data for testing - simulating time series data
    np.random.seed(42)  # For reproducibility

    # Generate sample time series data (e.g., monthly website visitors)
    months = pd.date_range(start="2024-01-01", periods=12, freq="MS")

    # Create realistic-looking growth pattern with some variation
    base_values = np.linspace(1000, 2500, 12)
    noise = np.random.normal(0, 150, 12)
    values = base_values + noise

    # Ensure no negative values
    values = np.maximum(values, 100)

    data = pd.DataFrame(
        {
            "Month": range(1, 13),  # Use numeric for simpler plotting
            "Visitors": values,
        }
    )

    # Create plot
    plot = create_plot(
        data,
        x="Month",
        y="Visitors",
        title="Monthly Website Visitors (2024)",
        xlabel="Month",
        ylabel="Number of Visitors",
        color="#3498db",
        alpha=0.5,
        line_color="#2980b9",
        line_width=2,
    )

    # Save for inspection
    plot.save("plot.png", dpi=300, verbose=False)
    print("Plot saved to plot.png")
